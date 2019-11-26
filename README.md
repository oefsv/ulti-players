
| Travis        | AppVeyor      |
|:-------------:|:-------------:|
| [![Build Status](https://travis-ci.org/oefsv/ulti-players.svg?branch=master)](https://travis-ci.org/oefsv/ulti-players) | - |




# Develop


## With gradle

For local development you need to install

+ python
+ npm
+ nginx

To start the dev server for the UI, use:

```
> ./gradlew :frontend:startUi
```

In order to initialize the backend server, use

```
> ./gradlew :backend:initDev
```

The first time, you might need to create the admin user

```
> cd backend
> frisbee-venv\Scripts\python.exe manage.py createsuperuser
```

```
> ./gradlew :frontend:buildUi
> ./gradlew :frontend:startUi
```



## manually with Linux

open three terminals in the project directory

### 1. Install configure nginx
in the first terminal:
```
sudo apt update
sudo apt install nginx -y
sudo systemctl disable nginx
sudo systemctl stop nginx
sudo nginx -c  $PWD/frontend/nginx/conf/nginx.conf
```

### 2. Initialize and start Backend (Django) Development server
In the second terminal:
```
python3 pip install pipenv
cd backend
pipenv shell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 3.build ui
UI development is done using Angular + Npm

```
> cd frontend
> npm install
> ng serve
```

## with Docker (recommended)
Setup a production like local environment with docker. 
### Requirements
- docker
- docker-compose

### Architecture

The ui will be hosted via nginx, the backend via apache httpd and the database via postgress
the enduser entrypoint is the nginx server serving the angular application.
this server can reach out to the api server via hostname "django" (example: http://django/api/pm)
the django server can reach the database server via hostname "db" (example: jdbc:postgresql://db)

### Setup
1. Make sure you are in the projects root directory `ulti-players` 
2. `docker-compose build`
3. `docker-compose up`

### Usage
the ui server is reachable via http://localhost
the rest server is reachable via http://localhost:8000 (note: the ui server reaches him also via http:/django)
the db server is reachable via jdbc:postgresql://localhost:5432


## Using the Developer database

###  Load Developer Data
```
cd backend
python manage.py loaddata dev_db_dump.json
```

### Dumping the database
use this if you want to share changes you made to the development database.
```
cd backend
python manage.py dumpdata --help --exclude auth.permission --exclude contenttypes > dev_db_dump.json
```

### Testdata
Init Testdata 10 per db table.(using [django-seed](https://pypi.org/project/django-seed/))

```
python manage.py seed auth ultimate_frisbee_management --number=15
```