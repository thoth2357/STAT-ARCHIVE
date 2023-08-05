#!/bin/bash

NAME="STATARCHIVE"
DIR=/home/seyi/codes-in-production/STATARCHIVE
USER=seyi
GROUP=seyi
WORKERS=3
SOCKFILE=unix:/home/seyi/codes-in-production/STATARCHIVE/gunicorn.sock
DJANGO_SETTINGS_MODULE=statArchive.settings.prod
DJANGO_WSGI_MODULE=statArchive.wsgi
LOG_LEVEL=debug


cd $DIR
source /home/seyi/codes-in-production/STATARCHIVE/.venv/bin/activate  #Activate the virtual environment
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DIR:$PYTHONPATH


#Command to run the progam VIA supervisor
exec /home/seyi/codes-in-production/STATARCHIVE/.venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $WORKERS \
--user=$USER \
--group=$GROUP \
--bind=$SOCKFILE \
--log-level=$LOG_LEVEL \
--log-file=-⏎                                                                                                                                                           
