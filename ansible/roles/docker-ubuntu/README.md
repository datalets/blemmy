docker-ubuntu
===============

[![Build Status](https://travis-ci.org/suzuki-shunsuke/ansible-docker-ubuntu.svg?branch=master)](https://travis-ci.org/suzuki-shunsuke/ansible-docker-ubuntu)

Install docker on Ubuntu.

(With modifications by @loleg)

https://galaxy.ansible.com/suzuki-shunsuke/docker-ubuntu/

Requirements
------------

Nothing.

Role Variables
--------------

* docker_nonroot: Whether the remote_user is root or not. This variable is set automatically, and is used to execute tasks with the become option.
* docker_users: Users who are added the docker group. The default value is an empty array.

Dependencies
------------

Nothing.

Example Playbook
----------------

```yaml
- hosts: servers
  roles:
  - role: suzuki-shunsuke.docker-ubuntu
    docker_users:
    - ubuntu
```

License
-------

MIT
