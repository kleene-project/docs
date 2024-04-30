---
title: ZFS configuration
description: Configuring ZFS for Kleene
keywords: debugging, troubleshoot
---

One of the fundamental building blocks of Kleene is the Zettabyte File System
(ZFS), which has been a stable part of FreeBSD for many years.
Besides being used internally in Kleene for image-building and container creation,
Kleene's core ZFS datasets can be configured to suit specific needs.
In the following, the Kleene zroot dataset is assumed to be `zroot/kleene`.

Since ZFS properties in general are hereditery in nature, configuring a dataset
can affect future dataset children when they are created.
For instance,

```console
$ zfs list
NAME                                  USED  AVAIL     REFER  MOUNTPOINT
zroot                                1.01G  3.34G       24K  /zroot
zroot/kleene                         2.59M  3.34G       30K  /zroot/kleene
zroot/kleene/container                396K  3.34G       24K  /zroot/kleene/container
zroot/kleene/container/ab7857f95f13   372K  3.34G     1.01G  /zroot/kleene/container/ab7857f95f13
zroot/kleene/image                   2.15M  3.34G       25K  /zroot/kleene/image
zroot/kleene/image/7e223d81bfb4      1.03M  3.34G     1.01G  /zroot/kleene/image/7e223d81bfb4
zroot/kleene/image/d99bc7a5f62b      1.03M  3.34G     1.01G  /zroot/kleene/image/d99bc7a5f62b
zroot/kleene/image/f750ae32e804        73K  3.34G     1.01G  /zroot/kleene/image/f750ae32e804
zroot/kleene/volumes                   24K  3.34G       24K  /zroot/kleene/volumes
```

illustrates a Kleene installation with with a root dataset `zroot/kleene`, which
in turn has three dataset children for containers, images, and volumes. Thus, it
is possible to set/adjust properties of the entire Kleene installation, for all
future containers/images/volumes or a particular container/image/volume.

A few examples of this is provided below. See the complete list of
[ZFS properties](https://man.freebsd.org/cgi/man.cgi?query=zfsprops) to get an overview of possible configurations.

## Example: File system compression

To enable the compression scheme `lz4` on all images, containers and volumes:

```console
$ sudo zfs set compression=lz4 zroot/kleene
$ zfs list -o name,compression
NAME                                 COMPRESS
zroot                                off
zroot/kleene                         lz4
zroot/kleene/container               lz4
zroot/kleene/container/ab7857f95f13  lz4
zroot/kleene/image                   lz4
zroot/kleene/image/7e223d81bfb4      lz4
zroot/kleene/image/d99bc7a5f62b      lz4
zroot/kleene/image/f750ae32e804      lz4
zroot/kleene/volumes                 lz4
```

If a container requires more extensive compression, set it by

```console
$ sudo zfs set compression=gzip-9 zroot/kleene/container/ab7857f95f13
$ zfs list -o name,compression
NAME                                 COMPRESS
zroot                                off
zroot/kleene                         lz4
zroot/kleene/container               lz4
zroot/kleene/container/ab7857f95f13  gzip-9
zroot/kleene/image                   lz4
zroot/kleene/image/7e223d81bfb4      lz4
zroot/kleene/image/d99bc7a5f62b      lz4
zroot/kleene/image/f750ae32e804      lz4
zroot/kleene/volumes                 lz4
```

## Limiting storage consumption

Another useful feature of ZFS is to set a limit on how much storage a dataset
can use. This can be configured using by, e.g., setting the `quota` property:

```console
## We start be disabling compression, otherwise we can write a large file :)
$ sudo zfs set compression=off zroot/kleene/container/ab7857f95f13
$ sudo zfs set quota=1M zroot/kleene/container/ab7857f95f13
$ sudo jexec 19 /bin/dd if=/dev/zero of=too_large bs=1M count=1
dd: too_large: Disc quota exceeded
1+0 records in
0+1 records out
786432 bytes transferred in 0.054138 secs (14526313 bytes/sec)
```

Note that container's jail ID (JID) is 19 in this example.

## Enabling backup

There are many ways to backup a system, including Kleene, so this serves merely
as tentative suggestion. However, since all of Kleene i stored on ZFS it opens
up several possibilities of taking snapshots and backups of Kleene and its
objects. A few options are:

- [The `zfs-periodic` package](https://www.freshports.org/sysutils/zfs-periodic/) for periodically taking snpashots.
- [The `sanoid` package](https://www.freshports.org/sysutils/sanoid/) contains the `syncoid` CLI for backups with ZFS datasets to a remote host.
