---
title: Contribute to Klee and Kleened
description: Guidelines for contributing to Klee and Kleened
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
- Make sure that tests runs fast, e.g., do not create a complicated `vnet` container that starts with `/bin/sh /etc/rc`
  if it can be avoided.
- Do not make pull requests for new flags, features etc. without discussing it with
  the maintainers first.
- All code for Klee should be formatted using `black`
- All code for Klee should pass `flake8` and `pylint` linters. For `flake8`, rules E501 and E701 can be ignored.
  In the rare case that it poses a problem, an inline pylint-exception can be made, i.e., `# pylint: disable=unused-argument`.
- All code for Kleened should be formatted using `mix format`.

## Creating a development environment

To facilitate development, there exists a development repo containing a
couple of useful `Makefile`'s for setting up and using a FreeBSD development
environment. To set up the environment, do the following:

```console
$ git clone https://github.com/kleene-project/kleene-dev
$ cd kleene-dev
$ make init
```

The last command clones the three repositories for Klee, Kleened, and this
documentation.

!!! note
    Kleene only runs on FreeBSD. Anything that drives jails, ZFS or a running
    Kleened must be executed on a FreeBSD host, e.g., inside a FreeBSD VM.

In the kleene-docs repository, the docs can be built and served locally.
From the repository root, run:

```console
$ make serve
```

This creates the `.venv` if needed (see the Makefile) and starts the MkDocs
dev webserver at `http://127.0.0.1:8000/`.

Consult the `README.md` and `AGENTS.md` in the `kleene-dev` repository for the
current development-environment layout, and the `Makefile.vm` inside the VM
for useful make-targets to use during development. For instance, `make
test-shell` starts Kleened and creates a base image for testing.
