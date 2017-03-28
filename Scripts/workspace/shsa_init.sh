#!/usr/bin/env bash


terminator -e  firefox_shsa.sh 

echo "Tesis!!"

echo "Sublime Proyecto"
sublime /home/rcerqueira/Tesis/WebProject/Shsa

echo "workon Sigt"
workon Shsa

echo "cd Shsa"
cd /home/rcerqueira/Tesis/WebProject/Shsa

echo "Haciendo update"
git pull 

echo "Correindo Servidor"
python manage.py runserver

