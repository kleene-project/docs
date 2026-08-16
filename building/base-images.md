---
title: Creating base images
description: How to create base images
keywords: images, base image, examples
---

Images form a hierachy since all image builds start by cloning a parent image,
specified in the `FROM`-instruction, which in turn can be used in other
images etc. However, this hiearchy has to start with an image without
a parent, i.e., a *base image*.

## Overview

Base images are created with `klee image create ...`
instead of `klee image build ...`, and normally creates the base image from
a copy of the FreeBSD userland.

It is recommended to use a userland of the same version as the host.
However, there can be many reasons to divert from this, and Kleene
have different methods of creating base images to support many different use-cases.

`klee image create` supports four different methods of creating base images:

- `fetch-auto`: Kleene tries to detect the userland version of the host using `uname(1)`
  and then creates a base image from a pre-compiled binary, fetched from the
  official FreeBSD repositories. If you are new to FreeBSD this is
  probably a good place to start.

- `fetch`: Create a base image from a custom tar-archive, stored locally or fetched
  remotely, using `fetch(1)`. That could be a pre-compiled userland
  (`base.txz`) of a different version than what is running on the host.

- `zfs-clone`: Create a base image by [zfs-cloning](https://man.freebsd.org/cgi/man.cgi?query=zfs-clone)
  an existing dataset on the Kleene host. This is ideal, for example, if you have
  compiled a custom version of the userland from source.
  It can also be relevant for completely customized
  base images. This method does not require additional space, but
  implicitly creates a dependency on the dataset being cloned.

- `zfs-copy`: Similar to `zfs-clone`, but instead of cloning the dataset it is
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

where Kleene tries to detect the version of the host system and fetches
the corresponding userland (`base.txz`) from the official FreeBSD repositories.
If the nametag options is omitted, Kleened will derive a name based
on the detected version together with the tag `latest`. Using `-t FreeBSD` in
the previous example keeps the nametag simpler.

### Creating base images of custom versions of pre-built userlands

If a specific version is needed, use the `fetch` method:

```console
$ export VERSION=13.3-BETA1
$ klee image create -t FreeBSD:$VERSION fetch https://download.freebsd.org/releases/amd64/$VERSION/base.txz
```

It is also possible to use a third-party site a locally stored tar-archive instead.

```console
$ klee image create -t FreeBSD:testing fetch file:///my/own/releases/testting/base.txz
```

which can be handy in case of a locally built
[releases](https://man.freebsd.org/cgi/man.cgi?query=release). Remember to use
absolute *host* paths when specifying the location of your TAR-archive.

### Creating base images of locally compiled userlands

If the host system runs a locally built version of FreeBSD
(for example, a build of the STABLE-branch), a base image can be created
from the local build using the `zfs-clone`/`zfs-copy` methods:

```console
$ D=/zroot/here/is/the/base_image
$ cd /usr/src # This contains the source of your STABLE-branch
$ mkdir -p $D
$ make world DESTDIR=$D # This step is not need if the system has already been built
$ make distribution DESTDIR=$D
$ klee image create -t FreeBSD:13-STABLE zfs-clone zroot/here/is/the/base_image
```

If a complete copy of the userland is preferred over a clone, use `zfs-copy` instead.
See the [handbook for details](https://docs.freebsd.org/en/books/handbook/cutting-edge/#makeworld)
on how to locally build a custom version of FreeBSD.

### Creating a customized minimal base image

It is also possible to run a minimal base image, either by trimming-down a full base
system or by using a [tool like `mkjail`](https://github.com/Freaky/mkjail) (requires `ruby`).
The following small example uses `mkjail` and it is assumed that `mkjail`
is in `PATH`.

```console
$ mkjail -a minimal_testjail.txz /usr/bin/env /usr/local/bin/python3.9 -c "print('Hello World')"
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
  FreeBSD:testing /usr/local/bin/python3.9 -c "print('Hellooo World')"
157538749b34
created execution instance 81bd541b6473
Hellooo World

executable 81bd541b6473 and its container exited with exit-code 0
```

Note that `klee run` is executed with a special pairs of jail-parameters since the
image does not contain basic components such as a user database, a `dev` directory
and many of directories usually present in a `PATH` variable.
