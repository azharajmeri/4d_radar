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

REM Check if superuser already exists
python manage.py shell -c "from django.contrib.auth.models import User; exists = User.objects.filter(username='admin').exists(); print(exists)"

REM Create superuser if not already present
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@metro.com', 'metro@123') if not User.objects.filter(username='admin').exists() else None"

python manage.py radar

REM Wait for user input before exiting
echo.
echo Press any key to exit...
pause > nul
