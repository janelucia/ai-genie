# Backend of AIGenie

## Description
TBC

## Getting started

install dependencies:
```
    create and activate virtual environment
        - creation command 'python -m venv .venv'
        - activation is sytem dependent
    install requirements through 'pip install -r requirements.txt' command
```

creating a database:
```
    go to core directory ('Backend/core')
    type 'python manage.py makemigrations'
    type 'python manage.py migrate'
```

to create an admin profile:
```
    go to core directory ('Backend/core')
    type 'python manage.py createsuperuser'
    follow instructions
    admin panel is accessed at 'http://localhost:8000/admin'
```

loading a mock_db.json:
```
    go to core directory ('Backend/core')
    type 'python manage.py loaddata mock_db.json'
```

setting up vector database:
```
    On windows refer to: https://milvus.io/docs/install_standalone-windows.md
    On linux no further actions need to be taken
```

setting up ollama:
```
    You need to install Ollama and dwonload model you want to use
    After that change a AI_MODEL_NAME to the name of your chosen model in /core/setting.py
```

email setup:
```
    In order for email to work properly you have to choose you smtp service provider:
        - in case of Gmail proceed as follows:
            * create .env file in /Backend directory
            * create user name environmental variable inside of it by typing "EMAIL_HOST_USER = 'your.email@gmail.com'"
            * create user password environmental variable inside of it by typing "EMAIL_HOST_PASSWORD = 'your_password'"
        - in any other case changes need to be applied to the settings.py file (in particular email section at the end)

    for a tutorial refer to: https://www.geeksforgeeks.org/setup-sending-email-in-django-project/ 
    or to django documentation: https://docs.djangoproject.com/en/5.2/topics/email/

    In case email functionality cannot be supported email endpoint can be safely commented out without interrupting other backend functionalities
```

start dev env:
```
    go to core directory ('Backend/core')
    type 'python manage.py runserver'
```

alternative way:
1. go to the `Backend` directory
2. run the following command:
```
    python core/manage.py runserver
```

Happy Coding🌻
