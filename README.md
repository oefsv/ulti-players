
| Travis        | AppVeyor      |
|:-------------:|:-------------:|
| [![Build Status](https://travis-ci.org/oefsv/ulti-players.svg?branch=master)](https://travis-ci.org/oefsv/ulti-players) | - |


# Develop

For local development you need to install

+ python
+ npm
+ nginx


To start the dev server for the UI, use:

```
> gradlew :frontend:startUi
```

In order to initialize the backend server, use

```
> gradlew :backend:initDev
```

The first time, you might need to create the admin user

```
> cd backend
> frisbee-venv\Scripts\python.exe manage.py createsuperuser
```

Start the backend server using

```
> frisbee-venv\Scripts\python.exe manage.py runserver
```

Run the combined web-server (for CORS)

```
> gradlew startDevServer
```

### UI

UI development is done using Angular + Npm

```
> cd frontend
> npm install
> ng serve
```

# Production

Setup a production like local environment with docker. 
## Requirements
- docker
- docker-compose

## Architecture

The ui will be hosted via nginx, the backend via apache httpd and the database via postgress
the enduser entrypoint is the nginx server serving the angular application.
this server can reach out to the api server via hostname "django" (example: http://django/api/pm)
the django server can reach the database server via hostname "db" (example: jdbc:postgresql://db)

## Setup
1. Make sure you are in the projects root directory `ulti-players` 
2. `docker-compose build`
3. `docker-compose up`

## Usage
the ui server is reachable via http://localhost
the rest server is reachable via http://localhost:8000 (note: the ui server reaches him also via http:/django)
the db server is reachable via jdbc:postgresql://localhost:5432

