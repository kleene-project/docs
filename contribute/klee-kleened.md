---
title: Contribute to Klee and Kleened
description: Guidelines for contributing to Klee and Kleened
keywords: contribute, klee, kleened
---

Do you want to hack on the Kleene project? Awesome!
Here are a few guidelines and useful information on how to get started.

This community is still in its infancy, so this is subject to change as
we gain experience. Also, remember that we are all busy people, so please
be patient with us

## Development guidelines

- As a rule of thumb, functional end-to-end tests are the primary way of testing in
  Kleene, and functional tests should be added to the Klee test-suite. Most of the
  functional tests in the Kleened repository are going to be migrated to Klee bit by bit.
- Unittests should be stored in their respective (Klee or Kleened) repositories.
- Make sure that tests runs fast, e.g., do not create a complicated vnet-container that starts with `/bin/sh /etc/rc`
  if it can be avoided.
- Do not make pull requests for new flags, features etc. without discussing it with
  the maintainers first.
- All code for Klee should be formatted using `black`
- All code for Klee should pass `flake8` and `pylint` linters. For `flake8`, rules E501 and E701 can be ignored.
  In the rare case that it poses a problem, an inline pylint-exception can be made, i.e., `# pylint: disable=unused-argument`.
- All code for Kleened should be formatted using `mix format`.

## Creating a development environment

To facilitate development, there exists a development repos containing a
Vagrantfile for a development environemnt and a couple of useful `Makefile`'s.
To set it up the environment, do the following:

```console
$ git clone https://github.com/kleene-project/kleene-dev
$ cd kleene-dev
$ make init
```

The last command clones the three repositories for Klee, Kleened, and this
documentation, respectively.

> **Note**
>
> The `Vagrantfile` requires a version of the FreeBSD base system (`base.txz`)
> to be available in the `kleene-dev` folder.
> Remember to fetch one and adjust the `$base_txz` parameter accordingly,
> in the `Vagrantfile`.

Assuming [Jekyll is installed](/contribute/contribute-guide/#build-and-preview-the-docs-locally)
there is a an additional make-target in the `kleene-dev` repos to build the
docs:

```console
$ make docs
```

If Vagrant is installed, the development environment can be created by runnning:

```console
$ vagrant up dev
```

Note that it will take quite some time to setup the environment, while Vagrant
takes care of

- Creating a dummy zpool.
- Installing relevant packages, such as `elixir`, `python` and `openapi-python-client`
- Installing development configuration files into `/usr/local/etc/kleened`
- Creating a utility `Makefile` in `~/`
- Creating a Poetry environment for Klee and installing it (using `pipx`) in editable-mode.
- Finally, a custom script `customize_vagrant_user.sh` is run to install any user-specific files such as,
  e.g., dotfiles. This needs to be created by the user and placed in the
  `kleene-dev` directory.

Consult `/home/vagrant/Makefile` to see useful make-targets for use during
development. For instance, `make test-shell` starts Kleened and creates a
base image image for testing.
