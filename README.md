
| Travis        | AppVeyor      |
|:-------------:|:-------------:|
| [![Build Status](https://travis-ci.org/oefsv/ulti-players.svg?branch=master)](https://travis-ci.org/oefsv/ulti-players) | - |

# Test
Setup a production like local environment with docker. 
## requirements
- docker
- docker-compose

## arichtecture

The ui will be hosted via nginx, the backend via apache httpd and the database via postgress
the enduser entrypoint is the nginx server serving the angular application.
this server can reach out to the api server via hostname "django" (example: http://django/api/pm)
the django server can reach the database server via hostname "db" (example: jdbc:postgresql://db)

## setup
1. Make sure you are in the projects root directory `ulti-players` 
2. `docker-compose build`
3. `docker-compose up`

##usage
the ui server is reachable via http://localhost
the rest server is reachable via http://localhost:8000 (note: the ui server reaches him also via http:/django)
the db server is reachable via jdbc:postgresql://localhost:5432

# Develop

## UI

UI development is done using Angular + Npm

```
> cd frontend
> npm install
> npm run start
```

## Backend

In one shell execute

```
> gradlew startDevServer
```

and in the next one

```
> cd backend
> frisbee-venv\Scripts\python.exe manage.py runserver
```

# Build
Create the ZIP

```
> gradlew createZip
```


