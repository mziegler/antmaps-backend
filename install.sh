#!/bin/bash

echo
echo "Setting up Antmaps back-end development environment.  This script should work on Mac/Unix/Linux environments, but you can follow basically the same steps in the script to set it up in Windows."
echo

echo "Make sure you've installed Python 3.x  https://www.python.org/downloads/"
echo "And you've installed virtualenv  https://virtualenv.pypa.io/en/latest/installation.html"
echo

if [ ! -d ENV ]; then
  echo "Setting up virtual environment"
  virtualenv -p python3 ENV           # set up virtual environment with python3
else
  echo "Virtual environment ENV already exists"
fi 

source ENV/bin/activate              # activate virtual environment

echo
echo "Installing python package requirements"
echo

pip install -r antmaps_dataserver/python-package-requirements.txt

