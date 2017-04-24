docker-compose
===============

[![Build Status](https://travis-ci.org/suzuki-shunsuke/ansible-docker-compose.svg?branch=master)](https://travis-ci.org/suzuki-shunsuke/ansible-docker-compose)

Install Docker Compose.

https://galaxy.ansible.com/suzuki-shunsuke/docker-compose/

Requirements
------------

* Docker Engine

Role Variables
--------------

* docker_compose_path: the path where docker-compose is installed. The default is /usr/local/bin
* docker_compose_mode: the permission of the docker-compose. The default is 0755
* docker_compose_version: docker-compose version. The default is `1.11.2`

Dependencies
------------

Nothing.

Example Playbook
----------------

```yaml
- hosts: servers
  roles:
  - role: suzuki-shunsuke.docker-compose
```

License
-------

MIT
