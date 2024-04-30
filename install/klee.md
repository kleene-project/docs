---
title: Klee installation
description: Describes the Klee installation steps
keywords: kleene, klee, installation, install
---

There are several ways of installing Klee depending on tooling and platform.
The following provides a couple of examples.

## Install using pipx

`pipx` works on many differen platforms and can be used to install python packages
in isolated environments to avoid dependency conflicts from other python applications.

`pipx` can be installed on most operating systems. For instance, on FreeBSD:

```console
$ sudo pkg install py39-pipx
```

On a Debian-based Linux distribution

```console
$ sudo apt install pipx
```

Or a third way, depending on the platform.

Then installing Klee is simply

```console
$ pipx install klee
```

This is the most common way that uses the latest version from
[PyPI](https://pypi.org/).

Alternatively, Klee can be installed directly from source using, e.g.,
git

```console
$ git clone https://github.com/kleene/klee
$ pipx install ./klee
```

If `pipx install -e ./klee` is used instead, it will be installed in 'editable'
mode, meaning that any changes made to Klee will take effect the next time `klee`
is invoked.


## Install in development environement using Poetry

For developers or users that want to tinker with Klee, Poetry might be the way
to go. See Poetry's [installation instructions](https://python-poetry.org/docs/#installation)
on how to install it. Once Poetrty is installed, get the Klee source and create the
development environment:

```console
$ git clone https://github.com/kleene/klee
$ cd klee
$ poetry install
```

Poetry uses the `poetry.lock` file to fetch the exact snapshots of the dependency packages,
including packages used for development. Poetry also automatically installs Klee in 'editable' mode.

Create a shell-session in the newly created development environment by running

```console
$ poetry shell
```

in the root of Klee's repository.

See [Poetry's documentation](https://python-poetry.org/docs/) to learn more.
