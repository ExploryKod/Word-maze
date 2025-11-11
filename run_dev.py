#!/usr/bin/env python3
"""
Development server runner with proper reloading for Docker volumes
Uses watchdog to detect file changes and trigger Flask reloads
Based on: https://medium.com/hootsuite-engineering/hot-reloading-on-a-dockerized-flask-app-4e87b88ea303
"""
import os
import sys
import time
import threading
from pathlib import Path
from werkzeug.serving import run_simple
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add the app directory to the path
sys.path.insert(0, '/python-docker')

# Import the app factory
from app import create_app

# Python file to modify for triggering reloads (similar to uwsgi-reload in the article)
RELOAD_TRIGGER_MODULE = '/python-docker/app/_reload_trigger.py'

class ReloadHandler(FileSystemEventHandler):
    """Handler that touches the reload trigger file when changes are detected"""
    def __init__(self):
        self.last_reload = 0
        self.debounce_seconds = 1  # Wait 1 second of no changes before reloading
    
    def on_any_event(self, event):
        """Handle any file system event"""
        if event.is_directory:
            return
        
        # Only watch Python and template files
        if not (event.src_path.endswith('.py') or event.src_path.endswith('.html') or 
                event.src_path.endswith('.css') or event.src_path.endswith('.js')):
            return
        
        # Only react to modification and creation events
        if event.event_type not in ('modified', 'created', 'moved'):
            return
        
        current_time = time.time()
        # Debounce: only reload if enough time has passed since last reload
        if current_time - self.last_reload < self.debounce_seconds:
            return
        
        self.last_reload = current_time
        # Modify the Python trigger file to signal Flask to reload
        try:
            trigger_path = Path(RELOAD_TRIGGER_MODULE)
            # Update the timestamp in the file to trigger reload
            with open(trigger_path, 'w') as f:
                f.write(f"# This file is automatically modified by the hot reload watcher\n")
                f.write(f"# DO NOT EDIT MANUALLY\n")
                f.write(f"_reload_timestamp = {int(current_time)}\n")
            print(f"\n[Hot Reload] File changed: {event.src_path} (event: {event.event_type})")
            print("[Hot Reload] Triggering Flask reload...")
        except Exception as e:
            print(f"[Hot Reload] Error updating trigger file: {e}")

def start_file_watcher():
    """Start watching for file changes"""
    event_handler = ReloadHandler()
    # Use PollingObserver for Docker volume compatibility (works better than inotify)
    from watchdog.observers.polling import PollingObserver
    observer = PollingObserver(timeout=1)  # Poll every 1 second
    
    # Watch the app directory
    watch_paths = [
        '/python-docker/app',
        '/python-docker/config.py'
    ]
    
    for path in watch_paths:
        if os.path.exists(path):
            observer.schedule(event_handler, path, recursive=True)
            print(f"[Hot Reload] Watching: {path} (polling mode)")
    
    observer.start()
    return observer

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    
    # Ensure the reload trigger module exists
    trigger_path = Path(RELOAD_TRIGGER_MODULE)
    if not trigger_path.exists():
        trigger_path.parent.mkdir(parents=True, exist_ok=True)
        with open(trigger_path, 'w') as f:
            f.write("# This file is automatically modified by the hot reload watcher\n")
            f.write("# DO NOT EDIT MANUALLY\n")
            f.write("_reload_timestamp = 0\n")
    
    # Start file watcher in background thread
    print("Starting file watcher for hot reloading...")
    observer = start_file_watcher()
    
    # Collect files to watch (including the trigger module)
    extra_files = [str(RELOAD_TRIGGER_MODULE)]
    
    # Add Python and template files
    app_dir = Path('/python-docker/app')
    if app_dir.exists():
        extra_files.extend(list(app_dir.rglob('*.py')))
        extra_files.extend(list(app_dir.rglob('*.html')))
    
    config_file = Path('/python-docker/config.py')
    if config_file.exists():
        extra_files.append(str(config_file))
    
    print(f"Starting Flask development server on port {port}...")
    print(f"Hot reloading enabled - watching {len(extra_files)} files")
    print("File changes will trigger automatic reload (1 second debounce)")
    
    try:
        run_simple(
            hostname='0.0.0.0',
            port=port,
            application=app,
            use_reloader=True,
            use_debugger=True,
            reloader_type='stat',
            extra_files=extra_files,
            threaded=True,
            reloader_interval=0.5  # Check every 0.5 seconds
        )
    finally:
        observer.stop()
        observer.join()
