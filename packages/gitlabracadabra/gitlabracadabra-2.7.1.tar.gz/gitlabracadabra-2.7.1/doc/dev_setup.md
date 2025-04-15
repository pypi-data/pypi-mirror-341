# Development environment <!-- omit in toc -->

- [Install Docker](#install-docker)
- [Install GitLab](#install-gitlab)
- [Configure GitLab](#configure-gitlab)
- [Setup virtual environment](#setup-virtual-environment)
- [Run tests](#run-tests)

## Install Docker

See [official installation documentation](https://docs.docker.com/install/).

## Install GitLab

From gitlabracadabra directory:

```sh
export GITLAB_HOME=$PWD/../gitlab
sudo docker pull gitlab/gitlab-ee:latest
sudo docker run --detach \
  --hostname gitlab.example.com \
  --env GITLAB_OMNIBUS_CONFIG="registry_external_url 'http://gitlab-registry.example.com';" \
  --publish 443:443 --publish 80:80 --publish 22:22 \
  --name gitlab \
  --restart always \
  --volume $GITLAB_HOME/config:/etc/gitlab \
  --volume $GITLAB_HOME/logs:/var/log/gitlab \
  --volume $GITLAB_HOME/data:/var/opt/gitlab \
  --shm-size 256m \
  gitlab/gitlab-ee:latest
```

See also [official installation documentation](https://docs.gitlab.com/ee/install/docker.html#install-gitlab-using-docker-engine)
for additional instructions.

Ensure your `/etc/hosts` has the following aliases for `127.0.0.1`:

```pre
127.0.0.1       localhost       gitlab.example.com gitlab-registry.example.com
```

## Configure GitLab

Get initial root password:

```console
$ sudo docker exec -it gitlab grep 'Password:' /etc/gitlab/initial_root_password
Password: abcd
```

Visit <http://gitlab.example.com> (or <http://localhost>), go to *Edit profile*,
*[Access Tokens](http://gitlab.example.com/-/user_settings/personal_access_tokens)*, and create a
new token with the `api` scope. Paste this token in
[`tests/python-gitlab.cfg`](../src/gitlabracadabra/tests/python-gitlab.cfg), and change `url`.

Depending on your tests, you may need to create additional resources in GitLab
(groups, projects, ...).

## Setup virtual environment

```shell
rm -rf venv .venv
virtualenv .venv
. .venv/bin/activate
pip install hatch hatch-pip-compile
```

## Run tests

```shell
. .venv/bin/activate

hatch fmt && \
hatch run types:check && \
hatch test --cover -vv && \
hatch run hatch-test.py3.11:coverage html
```

When recording a new cassette, change `record_mode` in [`tests/vcrfuncs.py`](../src/gitlabracadabra/tests/vcrfuncs.py#L103).
