(function () {
  'use strict';

  /**
   * Writes measured header/footer heights onto document.body (--header-h, --footer-h).
   * layouts/default.html: body is the grid root; --shell-main-min uses those vars.
   */
  function syncPageShellMetrics() {
    var header = document.getElementById('shell-header');
    var footer = document.getElementById('shell-footer');
    var bodyEl = document.body;
    if (!bodyEl || !header || !footer) return;

    var hh = Math.round(header.getBoundingClientRect().height);
    var fh = Math.round(footer.getBoundingClientRect().height);

    bodyEl.style.setProperty('--header-h', hh + 'px');
    bodyEl.style.setProperty('--footer-h', fh + 'px');
  }

  function initPageShellObservers() {
    var bodyEl = document.body;
    var header = document.getElementById('shell-header');
    var footer = document.getElementById('shell-footer');
    if (!bodyEl || !header || !footer) return;

    if (typeof ResizeObserver !== 'undefined') {
      var ro = new ResizeObserver(syncPageShellMetrics);
      ro.observe(header);
      ro.observe(footer);
    }

    window.addEventListener('resize', syncPageShellMetrics);
    window.addEventListener('orientationchange', function () {
      requestAnimationFrame(syncPageShellMetrics);
    });

    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(syncPageShellMetrics).catch(syncPageShellMetrics);
    }

    syncPageShellMetrics();
    requestAnimationFrame(syncPageShellMetrics);

    document.addEventListener(
      'click',
      function (e) {
        var toggle = e.target && e.target.closest('[data-collapse-toggle]');
        if (!toggle || toggle.getAttribute('data-collapse-toggle') !== 'navbar-cta')
          return;
        requestAnimationFrame(function () {
          requestAnimationFrame(syncPageShellMetrics);
        });
      },
      false
    );
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPageShellObservers);
  } else {
    initPageShellObservers();
  }
})();
