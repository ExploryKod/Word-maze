
<p align="center">
  <img width="50%" src="cover.png" />
</p>

# <p align="center"> Word Maze </p>

## <p align="center">🔥🔥🔥A game to play with words 🔥🔥🔥</p>

###👋 Use as a pretext to learn:
  - 👀 Flask micro-framework
  - 👀 factory pattern with Flask 
  - 👀 Organize my code through "Blueprints"

### 🔥🔥🔥Rules of the game
You need to guess 3 words that the program choose among a list of secret words. 
You have one point by good answer.
You win only if 3 words are found.

### 🔥🔥🔥Installation :
🔥See it through your local environement:
  - Through Docker
  - Through your own tools
  
#### 👋See original game version on your commande line interface (branche: feature/original-version)
  - It is the first version we do as a student team. We had a lot of joy working together. It was one my first python project and one of my first coding project. 
  - I tried to do it alone in PHP after we have done it as a team in python. 
  
#### 👋Using Docker

   #### 🔥Discover the factory pattern approach and blueprints (branche: config/dockerize-factory-app)
   
  - Install Docker 
  - Configure docker properly (see docs)
  - Go to the application root folder and use this command: <br/>
  
    ```bash  
    docker compose up -d --build
    ```
    
  - Go to your browser and access http://localhost:4000/
  
   #### 🔥Compare with traditonnal approach using docker (branche: feature/config-docker)
  - The above steps
  - Go to your browser and access http://localhost:5000/
      
#### 👋Using the flask application (branche: feature/config-traditionnal)

  ##### install these necessary tools on your computer (or isolate them through a virtual env):
  - node.js (and npm), 
  - python3, 
  - sqlite3

  Install node.js by installing it through official website: https://nodejs.org/en/
  Install python3 by installing it through official website: https://www.python.org/downloads/
  Npm is already installed through Node.js, check if you have the last version and if not just do the second command: 
  
  ```
  npm --version 
  npm install npm -g
  ```
  Everything is normally automatically added to your path. Check it if the first commande above don't give a version but through an error.

  ###### sqlite3 have to be manually added to your path (windows):
  - Go the sqlite3 download page: https://sqlite.org/download.html
  - Download a bundler where you have a CLI 
  - Add a folder named sqlite3 to C: C:\sqlite3
  - Copy sqlite3.exe file from the downloaded folder and past it in the new folder sqlite3
  - Past the path C:\sqlite3
  - open your system properties tool > go to environnement variables > choose path among system variables > click on edit
  - add C:\sqlite3 to the system variables
  - check in cmder if you succeed in adding sqlite3, type: <code>sqlite3 --version </code>
  - You succeed if you have a version followed by oher stuffs. 
  Sqlite3 is installed

  To have a better access to sqlite tables you can install DBbrowser (It is easier to see tables through this tool).
  - Install it through their <a href='https://sqlitebrowser.org/dl/' alt='site de dbbrowser'>official website</a>
  - Access it as any Desktop app.
    ###### 🔥Avoid using DBbrowser in the same time as you test locally the app in the browser. Indeed, sqlite3 is not efficient to tackle concurrency : see more                  information  <a href='https://9to5answer.com/sqlalchemy-and-sqlite-database-is-locked' alt='web page about a bug'>on this page</a> 

  ##### Install the app and its dependencies:
  - git clone this repo
  - Create a virtual environment in project root.
  - You can use venv already in default python: <code>python3 -m venv venv</code> ou sur windows: <code>python -m venv venv </code>
  - and activate it (ex: in the root project folder type the path to the good activate file (windows) or type source + the good activate file (mac)). 
  - Be careful: don't type active with its extension
  - Install dependencies using requirement.txt : <code>pip install -r requirement.txt</code>
  - Install dependancies from package.json using : <code>npm install</code>

  ##### Start the app:
  - Using one terminal you start the flask interface : <code>python -m app.py</code> (be careful: you need to add extension or note depending your OS).
  - Using another terminal you start tailwind css : <code>npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch </code>
  => It will run in its watch mode 
  - Check that you have an instance containing a game.db file in your directories.

#### 👋Using the original versions (python or php)
You need to import it on your favorit IDE and/or play from your terminal.
This game can only be played using command line interface.<br/>
You need to install locally php or python:<br/>
PHP: https://www.php.net/downloads.php <br/>
python : https://www.python.org/downloads/ <br/>

With python you can also use Colab through jupyter Notebook : https://colab.research.google.com/.
Copy the code in a Colab notebook.

### 🔥🔥🔥My learning goals

I aim at coding with languages like python and PHP. 
This is my first project using python and among my first PHP projects. 

I want to compare both languages by coding the same game in these languages. 
As a consequence I'll have a better understanding of these languages by seeing differences.

### 🔥🔥🔥The original project has two versions:
#### 1. French version in python : a collective project.
##### Authors: 
- [Amaury Franssen](https://github.com/ExploryKod)
- [Farmata Sidibe](https://github.com/Farmata-sidibe) 
- Abdoulaye Diop.

#### 2. English version using PHP.
##### Author : Amaury Franssen. 


