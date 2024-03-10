---
title: Networking overview
description: Overview of networking concepts in Kleene
keywords: networking, overview
---

<blockquote class="blockquote mb-4">
  <p>
    <i class="fas fa-quote-left fa-lg me-2"></i>
    <i>It seems once people understand the basics of containers, networking is one of
the first aspects they begin experimenting with. And regarding networking, it takes
very little experimentation before ending up on the deep end of the pool.</i>
  – <a href="https://github.com/containers/podman/blob/e7a3236358c74c08fe33e860ec045c30468cbdcd/docs/tutorials/basic_networking.md" class="link-underline-secondary">Podman documentation</a>
  </p>
</blockquote>

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

Networks can be created as three different types and each network is represented
by an interface on the host.

- `loopback`: Kleene creates a [loopback](https://man.freebsd.org/cgi/man.cgi?query=lo)
  interface on the host for the network. This has historically been a classical
  way to provide networking for jails in FreeBSD. It is the default network type
  with Klee.

- `bridge`: Kleene creates a [bridge](https://man.freebsd.org/cgi/man.cgi?query=if_bridge) interface on the host for the network.
  The bridge network can be used to (logically) link interfaces on the host
  machine (physical or virtual). The bridge network is used for containers with
  the VNET network driver (see below).

- `custom`: The user determines which interface on the host should be used for
  the network. For instance, if the container should have an IP directly on the
  physical interface, the default loopback interface (`lo0`) or more exotic use
  cases. The user is expected to take care of creating/destroying the interface,
  if needed.

## Container network drivers

The networking capabilities of a container is determined by it's network driver.
There are four different network drivers a container can use and only one can be
selected. They are derived directly from the underlying
[jail-parameters](https://man.freebsd.org/cgi/man.cgi?query=lo).

- `host` (default driver): Inherit the network configuration from the host. The container is able
  to see all ips of all interfaces. However, the container can't manipulate the
  interfaces such as adding and remove IP-addresses with `ifconfig` etc. This network driver
  provides the least amount of isolation since the container can see (and use)
  all IP-addresses on the host, *including those used by other containers*.
  It is not possible to connect to any networks with this driver,
  and since it does not require a network it is the default driver.
  However, in production setups it is recommended to use networks and ipnet/VNET
  drivers instead since they provide much better isolation from the host and
  other containers.

- `ipnet`: Inherit the network configuration but restrict which IP-addresses of
  the host that is accesible to the container.
  All interfaces of the host are visible within the container but not the IP's.
  Only assigned IP's are visible within the container, and configuring network
  interfaces using tools such as [`ifconfig(8)`](https://man.freebsd.org/cgi/man.cgi?query=ifconfig)
  is prohibited. A few pro's and con's of ipnet-containers:

  - It is lightweight way of providing connectivity to a container while
    retaining isolation from the host and other containers.

  - Ipnet containers can connect to all network types.

  - The IP's assigned to the container is also visible from the host so
    getting an overview of IP usage of ipnet-containers is straightforward.

  - Access to localhost aka. `127.0.0.1` is prohibited by default. This might
    require additional configuration of applications that expects this IP to
    be accessable.

  - The restricted networking environment limits the possibilites of what you
    can do within the container. For instance, it is not possible to setup a
    firewall or manipulating routes, network interfaces etc. Use the `vnet`
    driver in that case.

- `vnet`: VNET-containers has their own virtual networkstack, such as
  a dedicated `loopback` interface, routing table, firwall capabilities etc.
  VNET-containers are connected through a virtual `cross-over` cable represented
  by a pair of [`epair(4)`](https://man.freebsd.org/cgi/man.cgi?query=epair)
  interfaces. One of these is designated to the container and the other resides
  on the host, where it is added to a `bridge` interface.
  A few pro's and con's of vnet-containers:

  - Because VNET-containers have their own network stack, they can create
    virtual interfaces, manipulate existing ones, and run their own firewall.
    This makes them ideal for more complicated networking requirements.

  - Slightly more host and container configuration is needed compared to
    ipnet-containers since epair interfaces has to be allocated/configured
    and gateways has to be added during container startup.

  - Since the network-stack is isolated from the host, the networking
    configuration of the container is only visible from within the container.

  - VNET-containers can only connect to bridge-networks.

- `disabled`: Networking capabilites are disabled. Containers using this driver
  can see all network interfaces of the host but none of the IP-addresses.

## Next steps

Go to on of driver-specific pages for introductory walk-throughs:

- [Host networking]()
- [IPNet networking]()
- [VNET networking]()
- [Disable networking]()

If you have experience with FreeBSD jails and know the different approaches to
networking, the walk-throughs should be very familiar and hopefully it shows how
Kleene incorporates it.
