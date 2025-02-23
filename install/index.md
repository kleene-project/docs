---
description: Installation overview
keywords: kleene, klee, kleened, installation, install, overview, download
toc_min: 1
---

# Basic installation

>**Kleene requires the ZFS filesystem and PF firewall to run**
>
> Both should be included in the official releases but remember
> to install FreeBSD using ZFS or manually create a zpool.

The most straightforward way to install Kleene is using `pkg(7)`.

First, install `kleened` the backend daemon

```console
# pkg install kleene-daemon
```

and `klee` the CLI tool

```console
# pkg install kleene-cli
```

### Configuration

It is recommended to take a peek at the configuration file before running
Kleened. It is located at `/usr/local/etc/kleened/config.yaml` and contains
defaults intended to work in most basic cases.

Once Kleened is installed, enable it:

```console
# sysrc kleened_enable=yes
```

This ensures that it will start when the system is restarted.

To initialize the host and make sure all host requirements are met, run

```console
# service kleened init
```

It is also possible to do a dry-run initialization using
`service kleened dryinit` to see if requirements are met and what
should be configured.

Finally, start Kleened

```console
# service kleened start
```

Now Kleene should be up and running!
Start [creating images and containers with `klee`](/reference/klee/cli/).


# Alternative installation methods
### Build from source using FreeBSD ports

Alternatively, build `kleened` and `klee` from source
using the FreeBSD ports collection:

```console
# git clone --depth 1 https://git.FreeBSD.org/ports.git /usr/ports
# cd /ports/sysutils/kleene-daemon
# make install
# cd /ports/sysutils/kleene-cli
# make install
```

See the FreeBSD handbook for [further details](https://docs.freebsd.org/en/books/handbook/ports/#ports-using).

### Install `klee` using `pip` or `pipx`

There are several ways of installing Klee depending on tooling and platform.
The following provides a couple of examples using `pipx`.
Alternatively, `pip` can be used in a similar way.

`pipx` works on many differen platforms and can be used to install python packages
in isolated environments to avoid dependency conflicts with other python applications.
`pipx` can be installed on most operating systems.

For instance, on FreeBSD:

```console
$ sudo pkg install py311-pipx
```

On a Debian-based Linux distribution

```console
$ sudo apt install pipx
```

Once `pipx` is install, `klee` can be installed by

```console
$ pipx install kleene-cli
```

using the latest version from [PyPI](https://pypi.org/).

### Install development version of `klee`

The latest version of `klee` can be installed directly from source using `pipx`

```console
$ git clone https://github.com/kleene-project/klee
$ pipx install ./klee
```

If `pipx install -e ./klee` is used instead, it will be installed in 'editable'
mode, meaning that any changes made to the source will take effect the next time `klee`
is invoked.
