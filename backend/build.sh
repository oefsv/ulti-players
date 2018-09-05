#!/usr/bin/env bash

# be shure you are runing this script from the directory it is in

environment="local"


### BEGIN virtual envs only needed for local environments ###
# maybe remove the condition later
if [  ${environment} = "local" ] || [ ${environment} = "aws" ]; then
    echo "building local environement"
    # this solution was done with gitbash on windows
    python -m venv frisbee-venv

    # activate the virtual environment
    # on linux or mac run source frisbee-venv/bin/activate
    echo "activating local environement"
    source frisbee-venv/Scripts/activate
fi
### END virtual envs only needed for local environments ###


echo "installing required packages"
pip install -r requirements.txt

echo "running database migrations"
python manage.py makemigrations
python manage.py migrate

if [ ${environment} = "local" ]; then
    python manage.py runserver
fi

if [ ${environment} = "aws" ] then

    #collect static files
    python manage.py collectstatic

    # install aws elastic benastalk cli
    pip install awsebcli --upgrade

    # not sure about how these steps work when not logged into my (fkan) account.
    eb init
    eb deploy
    eb open

fi


