call %~dp0venv\scripts\activate.bat & waitress-serve --port=80 --threads=6 --url-scheme=https _app:app
