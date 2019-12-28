
|                                                         Travis                                                          | AppVeyor |
| :---------------------------------------------------------------------------------------------------------------------: | :------: |
| [![Build Status](https://travis-ci.org/oefsv/ulti-players.svg?branch=master)](https://travis-ci.org/oefsv/ulti-players) |    -     |



# Backend
Is a container stack defined in `docker-compose`.
it is a django application with a posgresql database backend, managed via gunicorn and served via nginx.

## Tests

## Testing Locally
You can set up your local test environment.
**DO NOT expose this environment to the internet!**

## Setup
1. clone the repository.
1. optional: place a valid`google_drive_credentials.json`in the `credentials` directory to be able to load testdata
1. `docker-compose build`
1. `docker-compose up`
2. log in: `http://localhost:8080`with user:`admin` password:`admin`
3. optional: load test data with command: 
    ```
    docker exec -it ulti-players_django_1 bash -c "python manage.py shell < ultimate_frisbee_management/utils/import_from_google_sheet.py"
    ``` 
    This takes about 10 minutes. progress (loaded objects) should be visible in the webapp
3. run automated tests: 
   ```
   docker exec -it ulti-players_django_1 bash -c "pytest"
   ```
   the results are available under on the test instance you can find test coverage reports at `localhost:8080/tests/index.html` and test report under `localhost:8080/tests/report.html`


# Frontend
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


### 1. Install configure nginx
in the first terminal:
```
sudo apt update
sudo apt install nginx -y
sudo systemctl disable nginx
sudo systemctl stop nginx
sudo nginx -c  $PWD/frontend/nginx/conf/nginx.conf
```
