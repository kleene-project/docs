---
title: Kleene for Docker users
description: How Kleene differs from Docker and how the concepts map
---

If you have used Docker before, Kleene will feel familiar: the same objects
(containers, images, networks, volumes), a Dockerfile-based build process,
and a CLI with the same overall structure. This page sums up where Kleene is
the same as Docker, where it deliberately differs, and what is left out.

## Concept mapping

| Docker | Kleene |
|---|---|
| container | container (a FreeBSD jail with a ZFS-backed filesystem) |
| image | image (a ZFS snapshot of a filesystem, no layers) |
| Dockerfile | `Dockerfile` (a subset of the Dockerfile instructions) |
| network (bridge) | network (`ipnet` or `vnet`) |
| volume | volume (a ZFS dataset mounted with nullfs) |
| bind mount | nullfs mount (`klee run --mount /host:/ctr`) |
| registry / pull / push | build your own images from a FreeBSD base image |
| compose | no equivalent |

## Main differences

### Containers are "thin VMs"

A Docker container typically runs a single process. A Kleene container runs
a full FreeBSD userland, started by default through `/etc/rc`, closer to a
"thin VM" than a single-process container. This means a container has
services, a system logger, and can be entered with `klee exec` to run
arbitrary commands, much like a small FreeBSD host.

### Networking

Docker containers are usually connected through a bridge with NAT. Kleene
offers the `ipnet`, `vnet` and `host` network drivers instead, built
directly on FreeBSD's jail networking: `ipnet` shares the host's stack
with restricted addresses, `vnet` gives each container its own network
stack, and `host` shares the host's networking completely. Port
publishing is done by redirecting traffic with the FreeBSD packet filter,
PF, rather than proxying sockets. See the
[networking guide](../guides/network/index.md) for details.

### Images are built, not pulled

There is no image registry, and no `klee pull` or `klee push`. Images are
created from a FreeBSD base image — downloaded from the FreeBSD mirrors,
cloned or copied from an existing ZFS dataset — and built from a
`Dockerfile` with `klee build`. Since images are plain ZFS datasets,
Kleene has no layer concept: build snapshots serve the same purpose.
See [building images](../guides/build/index.md).

### Dockerfile subset

Kleene implements a subset of the Dockerfile instructions. The supported
instructions and their differences are documented in the
[Dockerfile reference](../reference/dockerfile.md) — each instruction
that deviates from the Docker behavior notes it explicitly.

### ZFS-backed objects

Images, containers and volumes are all ZFS datasets: images are snapshots
of a filesystem, containers are clones of their image, and volumes are
datasets mounted into containers with nullfs. This makes creation cheap
(instant clones) and gives Kleene build snapshots for free. See
[ZFS configuration](../guides/operate/zfs.md).

## Command mapping

| Docker | Kleene |
|---|---|
| `docker ps -a` | [`klee lsc -a`](../reference/klee/lsc.md) |
| `docker images` | [`klee lsi`](../reference/klee/lsi.md) |
| `docker run` | [`klee run`](../reference/klee/run.md) |
| `docker build` | [`klee build`](../reference/klee/build.md) |
| `docker exec` | [`klee exec`](../reference/klee/exec.md) |
| `docker network create` | [`klee network create`](../reference/klee/network_create.md) |
| `docker volume create` | [`klee volume create`](../reference/klee/volume_create.md) |
| bind mount `-v /host:/ctr` | [`klee run --mount /host:/ctr`](../reference/klee/container_run.md) |
| `docker compose` | no equivalent |

All the `klee` shortcut commands are listed in the
[klee shortcut commands](../reference/klee/cheat-sheet.md) overview.
