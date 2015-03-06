#!/bin/bash

echo "Starting Antmaps development server"

source ./activate-environment.sh > /dev/null
python antmaps_dataserver/manage.py runserver
