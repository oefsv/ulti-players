
|                                                         Travis                                                          | AppVeyor |
| :---------------------------------------------------------------------------------------------------------------------: | :------: |
| [![Build Status](https://travis-ci.org/oefsv/ulti-players.svg?branch=master)](https://travis-ci.org/oefsv/ulti-players) |    -     |



# Backend
Is a container stack defined in `docker-compose`.
it is a django application with a postgresql database backend, managed via gunicorn and served via nginx.

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
   the results are available on the test instance. you can find test coverage reports at `localhost:8080/tests/index.html` and test report under `localhost:8080/tests/report.html`



## Development

### clone production database
`backend\ultimate_frisbee_management\scripts\clone_production_to_local_db.sh` backs up the production environment, copies it to the local filesystem, loads it into the local database and deletes all the backup files. with this you can create a copy of the production environment within minutes. Requires ssh access to the production host. ;D

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

### OEFSV specific troubleshooting
The Mail account to send send mail verifications etc runs on the organisations gsuite account.
this needs to allow less secure apps tu use the mail service. set it on https://myaccount.google.com/security for the db-ultimate account
