Public Health Schweiz
=====================

New website of the [Swiss Society for Public Health](http://public-health.ch), developed by [Datalets](http://datalets.ch) using the open source, [Django](https://www.djangoproject.com/)-based [Wagtail CMS](http://wagtail.io). The frontend has been created using [Bootstrap](https://getbootstrap.com) framework.

## Development environment

The easiest way to set up your machine would be to use [Vagrant](https://vagrantup.com), then in the project folder in the terminal type: `vagrant liverun`.

To set up a full development environment, follow all these instructions.

**Frontend setup**

You will need to have Ruby and SASS installed on your system, e.g.:

```
sudo yum install rubygem-sass
```

Make sure a recent version of node.js (we recommend using [nave.sh](https://github.com/isaacs/nave)), then:

```
npm install -g bower grunt-cli
npm install
bower install
```

The first command (`..install -g..`) may require `sudo` if you installed node.js as a system package.

If you are only working on the frontend, you can start a local webserver and work on frontend assets without the backend setup described below. Mock content is at `publichealth/static/mockup`

**Backend setup**

After installing Python 3, from the project folder, deploy system packages and create a virtual environment as detailed (for Ubuntu users) below:

```
sudo apt-get install python3-venv python3-dev libjpeg-dev

pyvenv env
. env/bin/activate

pip install -U pip
pip install -r requirements.txt

./manage.py migrate
./manage.py createsuperuser
```

You will be asked a few questions to create an administrator account.

**Starting up**

If you have one installed, also start your local redis server (`service redis start`).

Run this after completing setup:

```
./manage.py runserver &
grunt browser-sync
```

A default browser should open pointing to the default home page.

Now access the admin panel with the user account you created earlier: http://localhost:3000/admin/

## Troubleshooting

- Issues with migrating database tables in SQLite during development? Try `./manage.py migrate --fake`

## Production notes

We use [Ansible](https://www.ansible.com) and [Docker Compose](https://docs.docker.com/compose/reference/overview/) for automated deployment.

You need to obtain SSH and vault keys, and place these in a `.keys` folder - then to deploy a site:

```
ansible-playbook -s ansible/<*.yaml> -i ansible/inventories/production
```

We use a StackScript to deploy to Linode, the basic system set up is to have a user in the sudoers and docker group, and a few basic system packages ready.

For example, on Ubuntu:

```
apt-get install -q -y zip git nginx python-virtualenv python-dev
```

The order of deployment is:

- docker.yaml (base system)
- node.yaml
- site.yaml
- harden.yaml

For further deployment and system maintenance we have a `Makefile` which automates Docker Compose tasks.
