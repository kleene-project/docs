---
description: Installation overview
keywords: kleene, klee, kleened, installation, install, overview, download
toc_min: 1
---

<div class="component-container">
  <!--start row-->
  <div class="row">
     <div class="col-xs-12 col-sm-12 col-md-12 col-lg-6 block">
        <div class="component">
             <div class="component-icon">
                 <a href="/install/#kleened-installation"><img src="/assets/images/kleened-server.svg" alt="kleened" width="70" height="70"></a>
             </div>
             <p class="h2"><a href="/install/#kleened-installation">&nbsp;&nbsp;Kleened</a></p>
             <p>Install Kleene backend on a FreeBSD host</p>
        </div>
     </div>
     <div class="col-xs-12 col-sm-12 col-md-12 col-lg-6 block">
        <div class="component">
            <div class="component-icon">
                 <a href="/install/#klee-installation"><img src="/assets/images/klee-reference.svg" alt="klee" width="70" height="70"></a>
            </div>
            <p class="h2"><a href="/install/#klee-installation">&nbsp;Klee</a></p>
            <p>Install Kleene client on any machine</p>
        </div>
     </div>
  </div>
</div>

# Kleened installation

## Requirements

- Recent versions of FreeBSD on amd64: 13.x or 14.x.
  - In principle it should work on other archtectures, provided they have the necessary kernel modules.
- The ZFS kernel module. Included in the official releases.
- The PF firewall kernel module. Included in the official releases.

## Install using pkg

Since Kleened is not part of the official ports repository yet, it has to be
downloaded manually.

The easiest way to get the latest version of Kleened and install it using
`pkg`.

On FreeBSD14.x:

```console
$ fetch https://github.com/kleene-project/kleened/releases/download/v0.1.0-rc.1/kleened-0.1.0-rc1_FreeBSD14-amd64.pkg
$ sudo pkg install kleened-0.1.0-rc1_FreeBSD14-amd64.pkg
```

On FreeBSD13.x:

```console
$ fetch https://github.com/kleene-project/kleened/releases/download/v0.1.0-rc.1/kleened-0.1.0-rc1_FreeBSD13-amd64.pkg
$ sudo pkg install kleened-0.1.0-rc1_FreeBSD13-amd64.pkg
```

## Install using ports

Alternatively, build it from source using the FreeBSD port that is shipped with
the source code:

```console
$ git clone https://github.com/kleene-project/kleene-ports.git
$ cd kleene-ports/sysutils/kleened
$ sudo make install
```

## Configuration

It is recommended to take a peek at the configuration file before running
Kleened. It is located at `/usr/local/etc/kleened/config.yaml` and contains
defaults intended to work in most basic cases.

Once Kleened is installed, enable it:

```console
$ sudo sysrc kleened_enable=yes
```

This ensures that it will start when the system is restarted.

### Initialize the host

To make sure that all host requirements are met and the host system is properly
configured, run

```console
$ sudo service kleened init
```

It is also possible to do a dry-run instead using
`service kleened dryinit` to see which requirements are met and what
Kleened intends to configure.

Finally, start Kleened

```console
$ sudo service kleened start
```

# Klee installation

There are several ways of installing Klee depending on tooling and platform.
The following provides a couple of examples.

## Install using pipx

`pipx` works on many differen platforms and can be used to install python packages
in isolated environments to avoid dependency conflicts from other python applications.
`pipx` can be installed on most operating systems.

For instance, on FreeBSD:

```console
$ sudo pkg install py39-pipx
```

On a Debian-based Linux distribution

```console
$ sudo apt install pipx
```

Then install Klee by

```console
$ pipx install kleene-cli
```

This is the most common way that uses the latest version from
[PyPI](https://pypi.org/).

### Install latest development version

Alternatively, Klee can be installed directly from source using

```console
$ git clone https://github.com/kleene-project/klee
$ pipx install ./klee
```

If `pipx install -e ./klee` is used instead, it will be installed in 'editable'
mode, meaning that any changes made to Klee will take effect the next time `klee`
is invoked.
