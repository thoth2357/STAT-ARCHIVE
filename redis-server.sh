#!/bin/bash

NAME="STATARCHIVE-Redis"
DIR=/home/seyi/codes-in-production/STATARCHIVE
DJANGO_SETTINGS_MODULE=statArchive.settings.prod

cd $DIR
source /home/seyi/codes-in-production/STATARCHIVE/.venv/bin/activate  #Activate the virtual environment
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DIR:$

exec /home/seyi/codes-in-production/STATARCHIVE/.venv/bin/celery -A statArchive worker -E -l info --logfile=celery.log

