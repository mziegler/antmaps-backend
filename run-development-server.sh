#!/bin/bash

echo "Starting Antmaps development server"

source ./activate-dev-environment.sh > /dev/null
python antmaps_dataserver/manage.py runserver
