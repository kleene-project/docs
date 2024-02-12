---
title: Creating base images
description: How to create base images
keywords: images, base image, examples
---

Images form a hierachy since all Dockerfiles start by cloning the parent image that
is specified in the `FROM`-instruction, which in turn can be used in other
Dockerfiles etc. However, at some point a Dockerfile refers to an image without
a parent, and that image is a base image.

## Overview

Base images are on the top of the image hierachy and they are created without
Dockerfiles using `klee image create ..` instead of `klee image build ...`.

Usually, it is recommended to use a userland of the same version as the userland
of the host. However, there can be many reasons to divert from this, and Kleene
have different methods of creating base images to support many different use-cases.

`klee image create` supports four different methods of creating base images:

- `fetch-auto`: Kleene tries to detect the userland of the host using `uname(1)`
  and then creates a base image from a pre-compiled binary of the detected version,
  fetched from the official FreeBSD repositories. If you are new to FreeBSD this is
  probably a good place to start.

- `fetch`: Create a base image from a custom tar-archive stored locally or fetched
  remotely using `fetch(1)`. For instance, a tar-archive of a pre-compiled userland
  (`base.txz`) of a different version than what is running on the host.

- `zfs-clone`: Create a base image by [zfs-cloning](https://man.freebsd.org/cgi/man.cgi?query=zfs-clone)
  an existing dataset on the Kleene host. This is ideal, for example, if you have
  builded a custom version of the userland from source or have patched an official
  release using `freebsd-update`. It can also be relevant for completely customized
  base images. Note that this method does not require additional space but
  implicitly creates a dependency on the dataset being cloned.

- `zfs-copy`: Similar to previous method but instead of cloning the dataset it is
  copied using [`zfs-send`](https://man.freebsd.org/cgi/man.cgi?query=zfs-send) and
  [`zfs-recv`](https://man.freebsd.org/cgi/man.cgi?query=zfs-recv).
  This means that additional space is required for the base image and it is slower
  than `zfs-clone` since data needs to be copied. However, the resulting base image
  is independent of the source dataset.

The following sections discusses and exemplifies different usecases using
the previously mentioned methods of creating base images.

## Examples

### Creating base images automagically

The easiest way to get a base image is to use the `fetch-auto` method

```console
$ klee image create -t FreeBSD fetch-auto
```

where Kleened tries to detect the version of the host system and then downloads
the corresponding userland (`base.txz`) from the official FreeBSD repositories.
Note that if we omit the nametag `-t FreeBSD`, Kleened will derive a name based
on the detected version and tag it with `latest`. Using `-t FreeBSD` keeps
the nametag simple.

### Creating base images of custom versions of pre-built userlands

Similarily, if you want to pick a specific version you can use the `fetch` method:

```console
$ export VERSION=13.3-BETA1
$ klee image create -t FreeBSD:$VERSION fetch https://download.freebsd.org/releases/amd64/$VERSION/base.txz
```

You do not need to use the official FreeBSD-mirror if you have a third-party
site instead. Additionally, it is also possible to use a locally stored userland

```console
$ klee image create -t FreeBSD:testing fetch file:///my/own/releases/testting/base.txz
```

which can be handy in case of a locally built
[releases](https://man.freebsd.org/cgi/man.cgi?query=release). Remember to use
absolute paths when specifying the location of your TAR-archive.

### Creating base images of locally compiled userlands

For instance, if your host system is running a custom version of FreeBSD by, .e.g,
following a STABLE-branch you can build a base image using the `zfs-clone` or
`zfs-copy` methods:

```console
$ D=/zroot/here/is/the/base_image
$ cd /usr/src # This contains the source of your STABLE-branch
$ mkdir -p $D
$ make world DESTDIR=$D
$ make distribution DESTDIR=$D
$ klee image create -t FreeBSD:13-STABLE zfs-clone zroot/here/is/the/base_image
```

This assumes that you have already compiled and installed your preferred FreeBSD
version. See the [handbook for details](https://docs.freebsd.org/en/books/handbook/cutting-edge/#makeworld).
If you want a complete copy instead of a clone, use `zfs-copy` instead.

### Creating a customized minimal base image (experimental)

If you want to run a very minimal base image you can either trim-down a full base
system like the ones used en the previous examples, or you can try to use a small
tool, like `https://github.com/Freaky/mkjail` to help (requires `ruby`).
In the following there is a small example. Note that it is assumed that `mkjail`
is in your `PATH`.

```
$ mkjail -a minimal_testjail.txz /usr/bin/env /usr/local/bin/python3.9 -c "print('lol')"
... output ...
a var
a var/run
a var/run/ld-elf.so.hints
Total bytes written: 2024168
$ klee image create -t FreeBSD:testing fetch file://$(pwd)/minimal_testjail.txz
/zroot/kleenebase.txz                           0% of 1976 kB    0  Bps
/zroot/kleenebase.txz                                 1976 kB 1344 MBps    00s

succesfully fetched base system.
Unpacking contents and creating image...
extracted 101 files...
succesfully extracted binaries - creating image

image created
a9835b86808a
$ klee run -J mount.devfs=false \
  -J exec.system_jail_user \
  -J exec.clean=false \
  FreeBSD:testing /usr/local/bin/python3.9 -c "print('minimal jail')"
157538749b34
created execution instance 81bd541b6473
minimal jail

executable 81bd541b6473 and its container exited with exit-code 0
```

Note that `klee run` is executed with a special pairs of jail-parameters since the
image does not contain basic components such as a user database, a `dev` directory
and many of directories usually present in a `PATH` variable.
