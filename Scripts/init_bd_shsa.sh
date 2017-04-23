#!/usr/bin/env bash


export pg_user='postgres'
export pg_password='123456'
# export pg_password='postgres'
export pg_db='shsa_db'
export pg_host='127.0.0.1'

echo "~~~~ Deleting database ~~~~"
export PGPASSWORD=$pg_password
dropdb -U$pg_user $pg_db

echo -e "\n\n~~~~ Recreate database ~~~~"
export PGPASSWORD=$pg_password
createdb -U$pg_user -E'UTF-8' $pg_db


python manage.py makemigrations
python manage.py migrate 

echo "Cargando Fixtures de Registro"
python manage.py loaddata apps/registro/fixtures/0*

echo "Cargando Fixtures de Gestion de Solicitud"
python manage.py loaddata apps/rcs/fixtures/0*


python manage.py loaddata helps/registro.json