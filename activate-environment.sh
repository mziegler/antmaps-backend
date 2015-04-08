#!/bin/bash

# This file starts the virtual environment, and sets environment variables with 
# configurations for the antmaps server.  Since this file is published to GitHub,

# ---->  DON'T PUT ANY PASSWORDS OR SENSITIVE INFORMATION IN THIS FILE.  <------

# This script will attempt to call a script one directory up from this script,
# called "extra-config.sh".  Any environment variables set in that script will 
# over-write the variables set in this script, and it's not in the git repository,
# so ../extra-config.sh is a good place to set environment variables with sensitive
# passwords.





echo "###IMPORTANT###  Make sure to run this script with the command \"source ./activate-environment.sh\""
echo
echo "Use the command \"deactivate\" to deactivate the environment"
echo

source ENV/bin/activate 


# set environment variables here

# IMPORTANT!  Don't set ANTMAPS_DEBUG production.  (Don't even set it to '0' or 'false'.)
export ANTMAPS_DEBUG=true


# IMPORTANT!  This file is published publically to Github, so don't put any sensitive
# passwords here.  Use this file for dummy development database only.
# (Put production settings in a different, unpublished file)
export ANTMAPS_DB_NAME="antmaps"
export ANTMAPS_DB_HOST="127.0.0.1"
export ANTMAPS_DB_PORT="5432"
export ANTMAPS_DB_USER="antmaps"
export ANTMAPS_DB_PASSWORD="password"



# Credentials for the email account that AntMaps uses to send email, for error reports.
# If these are not configured properly, you will still be able to use most of the site,
# but it will crash if you try to submit an error report.
export ANTMAPS_EMAIL_HOST="smtp.gmail.com"
export ANTMAPS_EMAIL_PORT=587
export ANTMAPS_EMAIL_HOST_USER="foo"     # username for logging into email server
export ANTMAPS_EMAIL_HOST_PASSWORD="foo" # set this in a different file so it's not published to GitHub


# Only set 1 of ANTMAPS_EMAIL_USE_TLS or ANTMAPS_EMAIL_USE_SSL (not both)
export ANTMAPS_EMAIL_USE_TLS=true
#export ANTMAPS_EMAIL_USE_SSL=true

# Email address to send data error reports to
export ANTMAPS_REPORT_TO_EMAIL_ADDRESS='foo@foo.foo'





# Run the extra config file if it exists
if [ -f ../extra-config.sh ]; then
	source ../extra-config.sh
fi
