# ulti-players
Is a container stack defined in `docker-compose`.
it is a django application with a postgresql database backend, managed via gunicorn and served via nginx.


# Setup (localy)
**DO NOT expose the development environment to the internet! it uses default keys and passwords.**
1. clone the repository.
1. (deprecated) place a valid`google_drive_credentials.json`in the `credentials` directory to be able to load testdata from a google sheet
1. `docker-compose build`
1. `docker-compose up`
1. log in: `http://localhost:8080`with user:`admin` password:`admin`
1. (deprecated) load test data
    2.  optional place a valid`google_drive_credentials.json`in the `credentials` directory to be able to load testdata from a google sheet
    3.  run: 
    ```
    docker exec -it ulti-players_django_1 bash -c "python manage.py shell < ultimate_frisbee_management/utils/import_from_google_sheet.py"
    ``` 
    This takes about 10 minutes. progress (loaded objects) should be visible in the webapp.
3. run automated tests: 
   ```
   docker exec -it ulti-players_django_1 bash -c "pytest"
   ```
   the results are available on the test instance. you can find test coverage reports at `localhost:8080/tests/index.html` and test report under `localhost:8080/tests/report.html`

# Testing
## clone production database
`backend\ultimate_frisbee_management\scripts\clone_production_to_local_db.sh` backs up the production environment, copies it to the local filesystem, loads it into the local database and deletes all the backup files. with this you can create a copy of the production environment within minutes. Requires ssh access to the production host. ;D


# OEFSV specific troubleshooting
The Mail account to send send mail verifications etc runs on the organisations gsuite account.
this needs to allow less secure apps tu use the mail service. set it on https://myaccount.google.com/security for the db-ultimate account
