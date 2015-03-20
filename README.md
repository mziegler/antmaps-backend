Antmaps backend
========================
Django project


Installation
------------

To install the Antmaps backend locally on your own machine for development, first you need to install the following:

* Python 3.x  https://www.python.org/downloads/   (Developed using Python 3.4)
* Virtualenv for Python https://virtualenv.pypa.io/en/latest/installation.html
* psycopg2 (for python3)  http://initd.org/psycopg/docs/install.html#installation

Then, clone this git repository with "git clone --recursive", and in a shell run **./install.sh** to set up virtualenv and install Python packages.

If you get an error saying something like install.sh isn't executable, run " chmod +x activate-environment.sh run-development-server.sh install.sh " in a terminal.

**Note about psycopg2:** I (Matt) had some trouble getting psycopg2 running on my Ubuntu machine.  The python3-psycopg2 apt package didn't work for unknown reason.  I ended up installing it through Pypi, and it requires the 'python3-dev' and 'libpq-dev' apt packages, as well as a C compiler as it's a C program that needs to be built from source when installing from Pypi.  The /install.sh will attempt to install psycopg2 from Pypi, if you've already installed psycopg2 from other means ignore the error messages that it produces.


Note about git submodules
-------------------------
This git repository has a pointer to the antmaps frontend repository (antmaps-app), as the folder called "antmaps_frontend."  When you do a "git clone", use the "--recursive" option to automatically clone the submodules.  **When you do a "git pull", always also do a "git submodule update"** to update the front-end submodule.

See http://git-scm.com/docs/git-submodule

To set up the graphical Github interface to work with submodules, see http://stackoverflow.com/questions/12899163/where-is-git-submodule-update-in-sourcetree


Database connection configuration
---------------------------------
The AntMaps backend loads database connection parameters from environment variables, which are set in "activate-environment.sh"

Don't put sensitive passwords in activate-environment.sh, because it will be comitted to the git repository and published on GitHub (yikes!)

The "activate-environment.sh" script will also try to run a script called "../extra-config.sh" (where ../ is the parent directory of the git repsitory.)  If you want to change the database connection parameters (eg. to connect straight to the GABI server with your own account,) the best way to do it is by creating ../extra-config.sh and exporting the environment variables in activate-environment.sh in ../extra-config.sh.  This will keep your sensitive passwords from being committed to the git repository and published on the internet.


Setting up database connection
------------------------------
The Antmaps backend needs to connect to a Postgres database.  Connection parameters are stored in /activate-environment.sh.


Running development server
--------------------------
You can run the Antmaps-backend locally for development in a simple HTTP server by running **./run-development-server.sh**


Django management tasks
-----------------------
For Django management tasks, you first need to activate the development environment (start virtualenv and set environment variables) by running **./activate-environment.sh**

Django has a management utility found at: /antmaps_dataserver/manage.py .
See https://docs.djangoproject.com/en/1.7/ref/django-admin/
