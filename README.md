
| Travis        | AppVeyor      |
|:-------------:|:-------------:|
| [![Build Status](https://travis-ci.org/oefsv/ulti-players.svg?branch=master)](https://travis-ci.org/oefsv/ulti-players) | - |

# Test

You need to install

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


