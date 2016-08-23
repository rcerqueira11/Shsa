#!/usr/bin/env bash

###########################################################
#SCRIPT PARA LIMPIAR LA BASE DE DATOS EN DESARROLLO(LOCAL)#
###########################################################

export pg_user='postgres'
export pg_password='postgres'
export pg_db='shsa_db'
export pg_host='127.0.0.1'

echo "~~~~ Deleting database ~~~~"
export PGPASSWORD=$pg_password
dropdb -U$pg_user $pg_db

echo -e "\n\n~~~~ Recreate database ~~~~"
export PGPASSWORD=$pg_password
createdb -U$pg_user -E'UTF-8' $pg_db