---
title: Networking overview
description: Overview of networking concepts in Kleene
keywords: networking, overview
---

*It seems once people understand the basics of containers, networking is one of*
*the first aspects they begin experimenting with. And regarding networking, it takes*
*very little experimentation before ending up on the deep end of the pool.*
– [Podman documentation](https://github.com/containers/podman/blob/e7a3236358c74c08fe33e860ec045c30468cbdcd/docs/tutorials/basic_networking.md)

This section deals with one of the more comprehensive topics when dealing with
containers: Networking. For any readers having experience with networking in
Docker, they should expect a substantially different approach to the subject.

This page gives a brief introduction to the overall concepts related to
networking and the remaning parts of this section covers them in more detail.

Most of these concepts fall into two categories: Networks and network drivers.
The former are independent objects in Kleene and the latter are a property of
containers. Networks are used to provide different kinds of connectivity to
containers, and the capabilities of using networks, and networking in general,
is determined by which kind of network driver it has.

## Network types

Networks fall into three types and are represented by a network interface on
the host.

- `loopback`: Kleene creates a [loopback](https://man.freebsd.org/cgi/man.cgi?query=lo) interface on the host for the network.
  This has historically been a classical way to provide networking for jails
  in FreeBSD. It is the default network type with Klee.

- `bridge`: Kleene creates a [bridge](https://man.freebsd.org/cgi/man.cgi?query=if_bridge) interface on the host for the network.
  The bridge network can be used to (logically) link interfaces on the host
  machine (physical or virtual). The bridge network is used for containers with
  the VNET network driver (see below).

- `custom`: The user determines which interface on the host should be used for
  the network. For instance, if the container should have an IP directly on the
  physical interface, the default loopback interface (`lo0`) or more exotic use
  cases. The user is expected to take care of creating/destroying the interface,
  if needed.

## Network drivers
FIXME: HERTIL

- `ipnet`:

- `vnet`:

- `host`: For standalone containers, remove network isolation between the
  container and the Docker host, and use the host's networking directly. See
  [use the host network](host.md).

- `disabled`: For this container, disable all networking. Usually used in
  conjunction with a custom network driver. `none` is not available for swarm
  services. See
  [disable container networking](none.md).

- [Network plugins](/engine/extend/plugins_services/): You can install and use
  third-party network plugins with Docker. These plugins are available from
  [Docker Hub](https://hub.docker.com/search?category=network&q=&type=plugin)
  or from third-party vendors. See the vendor's documentation for installing and
  using a given network plugin.

## Simple example
### Create your own loopback network

### Add containers to a network

To build web applications that act in concert but do so securely, create a
network. Networks, by definition, provide complete isolation for containers. You
can add containers to a network when you first run a container.

Launch a container running a PostgreSQL database and pass it the `--net=my_bridge` flag to connect it to your new network:

    $ docker run -d --net=my_bridge --name db training/postgres

If you inspect your `my_bridge` you can see it has a container attached.
You can also inspect your container to see where it is connected:
