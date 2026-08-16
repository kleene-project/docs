---
title: Publishing ports
description: How to expose services to the outside world
keywords: networking, container, expose ports, publish ports
---

The previous sections covering the network drivers has shown how a
container, unless specifically configured otherwise, is reachable by the
containers that are connected to its networks.
However, sometimes it is necessary to expose services to the outside world, i.e.,
expose sockets on the external interfaces of the host.

> **Note**
>
> While there is large overlap in syntax, publishing ports in Kleene is
> completely different compared to Docker. Kleene exposes its ports by
> redirecting traffic from interfaces to the container, whereas Docker proxys traffic
> from a listening socket on the host to the container.

When a port is published, Kleene configures the host firewall to redirect and
allow traffic coming from one or more interfaces to an ip/port of the container.
When a port is published, it becomes reachable by containers on all networks.
Remember to be cautious when publishing ports as it can expose them to the
public internet (which often is the purpose, of course).

When redirecting traffic, it must be directed to a specific IP, so Kleene chooses
one from the networks that the container is connected to. Publishing
ports on containers using the `host` network-driver is not supported at the
moment.

## Syntax

When specifying ports to expose, there are two formats to use:

1. The simple syntax: `<HOST-PORT>[:CONTAINER-PORT][/<PROTOCOL>]` where
   `CONTAINER-PORT` defaults to `HOST-PORT`.
2. Full syntax: `<INTERFACE>:<HOST-PORT>:<CONTAINER-PORT>[/<PROTOCOL>]` and `INTERFACE`
   refer to a network interface on the host.

`PROTOCOL` defaults to `tcp` in both formats.
The full version requires all fields, except protocol, to be specified.

Here are some examples:

| Flag value                      | Description                                                                                                                                           |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-p 8080`                       | Redirect traffic from the gateway interface of the host, on TCP port 8080, to port 8080 in the container.                                             |
| `-p 8080:80`                    | Redirect traffic from the gateway interface of the host, on TCP port 8080, to port 80 in the container.                                               |
| `-p em1:8080:80`                | Redirect traffic from interface `em1` of the host, on TCP port 8080, to port 80 in the container.                                                     |
| `-p 8080:80/udp`                | Redirect traffic from the gateway interface of the host, on UDP port 8080, to port 80 in the container.                                               |
| `-p 8080:80/tcp -p 8080:80/udp` | Redirect traffic from the gateway interface of the host, on TCP and UDP port 8080, to port 80 in the container.                                       |
| `-p em0:8080:80 -p em1:8080:80` | Redirect traffic from interface `em0` and `em1` of the host, on TCP port 8080, to port 80 in the container.                                           |
