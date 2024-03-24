@echo off

REM Install virtual environment package
python -m pip install --upgrade pip
python -m pip install virtualenv

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate

REM Install requirements
pip install -r requirements.txt

REM Display message
echo.
echo Virtual environment created and activated, and requirements installed.
echo.

REM Start Django development server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

REM Wait for user input before exiting
echo.
echo Press any key to exit...
pause > nul
