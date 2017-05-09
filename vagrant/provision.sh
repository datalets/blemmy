#!/bin/bash

PROJECT_NAME=$1

PROJECT_DIR=/vagrant
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME

PYTHON=$VIRTUALENV_DIR/bin/python
PIP=$VIRTUALENV_DIR/bin/pip


# Create database
su - vagrant -c "createdb $PROJECT_NAME"


# Virtualenv setup for project
su - vagrant -c "virtualenv --python=python3 $VIRTUALENV_DIR"
# Replace previous line with this if you are using Python 2
# su - vagrant -c "virtualenv --python=python2 $VIRTUALENV_DIR"

su - vagrant -c "echo $PROJECT_DIR > $VIRTUALENV_DIR/.project"


# Upgrade PIP
su - vagrant -c "$PIP install --upgrade pip"

# Install PIP requirements
su - vagrant -c "$PIP install -r $PROJECT_DIR/requirements.txt"


# Set execute permissions on manage.py as they get lost if we build from a zip file
chmod a+x $PROJECT_DIR/manage.py


# Run syncdb/migrate/update_index
su - vagrant -c "$PYTHON $PROJECT_DIR/manage.py migrate --noinput && \
                 $PYTHON $PROJECT_DIR/manage.py update_index"


# Add a couple of aliases to manage.py into .bashrc
cat << EOF >> /home/vagrant/.bashrc
export PYTHONPATH=$PROJECT_DIR
export DJANGO_SETTINGS_MODULE=$PROJECT_NAME.settings.dev


alias dj="django-admin.py"
alias djrun="dj runserver 0.0.0.0:8000"

source $VIRTUALENV_DIR/bin/activate
export PS1="[$PROJECT_NAME \W]\\$ "
cd $PROJECT_DIR

# Install Ruby SASS
apt-get update
apt-get install ruby-sass

# Install node.js
curl https://raw.githubusercontent.com/isaacs/nave/master/nave.sh > nave.sh
chmod a+x nave.sh
./nave.sh usemain stable
cp nave.sh /home/vagrant/

su - vagrant -c "/home/vagrant/nave.sh usemain stable"
su - vagrant -c "/home/vagrant/nave.sh use stable"

# Install Frontend dependencies
su - vagrant -c "npm install -g bower grunt-cli"
su - vagrant -c "npm install --no-bin-links"
su - vagrant -c "bower install"
alias bower="bower install"

EOF
