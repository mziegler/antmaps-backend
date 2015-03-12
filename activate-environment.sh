#!/bin/bash

echo "###IMPORTANT###  Make sure to run this script with the command \"source ./activate-environment.sh\""
echo
echo "Use the command \"deactivate\" to deactivate the environment"
echo

source ENV/bin/activate 


# set environment variables here

# IMPORTANT!  Set ANTMAPS_DEBUG to false (or don't set at all) in production.
export ANTMAPS_DEBUG=true


# IMPORTANT!  This file is published publically to Github, so don't put any sensitive
# passwords here.  Use this file for dummy development database only.
# (Put production settings in a different, unpublished file)
export ANTMAPS_DB_NAME="antmaps"
export ANTMAPS_DB_HOST="127.0.0.1"
export ANTMAPS_DB_PORT="5432"
export ANTMAPS_DB_USER="antmaps"
export ANTMAPS_DB_PASSWORD="password"


# Run the extra config file if it exists
if [ -f ../extra-config.sh ]; then
	source ../extra-config.sh
fi
