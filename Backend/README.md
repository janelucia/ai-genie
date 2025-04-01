# Backend of AIGenie

## Description
TBC

## Getting started

install dependencies:
```
    create and activate virtual environment
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
