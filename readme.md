# Django Environment Setup Script

This batch script automates the process of setting up a Django environment with a virtual environment and installing project dependencies.

## Prerequisites

- Python installed on your system

## Instructions

1. Open Command Prompt or Terminal and navigate to your Django project directory.

2. Run the script by typing the following command and hitting Enter:

3. The script will perform the following tasks:
- Install the virtual environment package using the command:
  ```
  python -m pip install --upgrade pip
  python -m pip install virtualenv
  ```
- Create a virtual environment named `venv` using the command:
  ```
  python -m venv venv
  ```
- Activate the virtual environment using the command:
  ```
  call venv\Scripts\activate
  ```
- Install project dependencies specified in `requirements.txt` using the command:
  ```
  pip install -r requirements.txt
  ```
- Apply database migrations using the following commands:
  ```
  python manage.py makemigrations
  python manage.py migrate
  ```
- Start the Django development server using the command:
  ```
  python manage.py runserver
  ```
  
- Start the Radar server using the command:
  ```
  python manage.py radar
  ```

5. Once the setup is complete, you can access your Django application by navigating to `http://127.0.0.1:8000/` in your web browser.

6. To stop the server and exit, press any key in the Command Prompt or Terminal window.
