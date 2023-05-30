#! /bin/bash

# create backups
docker -H ssh://root@db-ultimate.frisbeeverband.at exec -it ulti-players_django_1 sh -c '/usr/local/bin/python /workspace/manage.py dbbackup -o db_backup.psql && /usr/local/bin/python /workspace/manage.py mediabackup -o media_backup.tar'
# deploy backup to local server
docker -H ssh://root@db-ultimate.frisbeeverband.at cp ulti-players_django_1:/workspace/backups ~/tmp/
docker -H ssh://root@db-ultimate.frisbeeverband.at exec -it ulti-players_django_1 sh -c 'rm backups/* -rf'
docker  cp ~/tmp/backups ulti-players_django_1:/workspace/backups 
docker exec -it ulti-players_django_1 sh -c '/usr/local/bin/python /workspace/manage.py dbrestore -i db_backup.psql --noinput && /usr/local/bin/python /workspace/manage.py mediarestore -i media_backup.tar --noinput'
rm -rf ../../backups/*