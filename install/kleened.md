---
title: Kleened installation
description: Describes the Kleened installation steps
keywords: kleene, kleened, installation, install
---

## Install using `pkg` or ports

Since Kleened is not part of the official ports repository yet, it has to be
downloaded manually.

The easiest way to fetch the latest version of Kleened and install it using
`pkg`:

```console
$ fetch https://FIXME/kleened-0.1.0.pkg
$ sudo pkg install ./kleened-0.1.0.pkg
```

All the versions of Kleened can be found [here](FIXME).

Alternatively, build it from source using the FreeBSD port that is shipped with
the source code:

```console
$ git clone https://github.com/kleene/kleened.git
$ cd kleened/ports/sysutils/kleened
$ sudo make install
```

### Configuration

It is recommended to take a peek at the configuration file before running
Kleened. It is located at `/usr/local/etc/kleened/config.yaml` and contains
defaults intended to work in most basic cases.

### Running Kleened and initialize the host

Once Kleened is installed, enable it:

```console
$ sudo sysrc kleened_enable=yes
```

This ensures that it will start automatically after reboots.
To make sure that all host requirements are met and the host system is properly
configured, run

```console
$ sudo service kleened init
```

It is also possible to do a dry-run instead using
`service kleened dryinit`, and see which requirements are met and what
Kleened intends to configure.

Finally, start Kleened

```console
$ sudo service kleened start
```

## Create development environement with `mix`

For developers or users that want to tinker with Klee a development environemnt
can be established with Mix:

```console
$ git clone https://github.com/kleene/kleened.git
$ cd kleened
$ sudo iex -S mix
```

The last command starts Kleened and enters a interactive shell. It also possible
to create releases, which is also for `pkg`-packages, running tests etc. See the
[mix documentation](https://hexdocs.pm/mix/1.15.7/Mix.html) for details.
Note however, that installation of `rc.d`-scripts are not installed and
configuration files needs to copied manually.
