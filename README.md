# back-labs
fist try


Copy project from VCS
if Windows:
- open project directory in cmd
- upgrade package manager: python -m pip install --upgrade pip
- download virtualenv: pip install virtualenv
- create folder with virtual environment: python -m venv env
- download dependencies: pip install requests
- activate environment: project_folder\env\Scripts\activate.bat
- set FLASK_APP=lab
- flask run

if Linux(approximate instruction):
- same as on Windows, but activate environment: source ./env/bin/activate
- export FLASK_APP=lab
- and the same: flask run