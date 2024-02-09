---
description: Review of the Docker Daemon attack surface
keywords: FreeBSD, jail, security
title: FreeBSD jail security
---

There are four major areas to consider when reviewing Docker security:

 - the intrinsic security of the FreeBSD kernel and jailed processes;
 - the attack surface of the Docker daemon itself;
 - loopholes in the container configuration profile, either by default,
   or when customized by users.

## Kernel namespaces

Docker containers are very similar to LXC containers, and they have
similar security features. When you start a container with
`docker run`, behind the scenes Docker creates a set of namespaces and control
groups for the container.

**Namespaces provide the first and most straightforward form of
isolation**: processes running within a container cannot see, and even
less affect, processes running in another container, or in the host
system.

**Each container also gets its own network stack**, meaning that a
container doesn't get privileged access to the sockets or interfaces
of another container. Of course, if the host system is setup
accordingly, containers can interact with each other through their
respective network interfaces — just like they can interact with
external hosts. When you specify public ports for your containers or use
[*links*](../../network/links.md)
then IP traffic is allowed between containers. They can ping each other,
send/receive UDP packets, and establish TCP connections, but that can be
restricted if necessary. From a network architecture point of view, all
containers on a given Docker host are sitting on bridge interfaces. This
means that they are just like physical machines connected through a
common Ethernet switch; no more, no less.

## FreeBSD jail capabilities

By default, Docker starts containers with a restricted set of
capabilities. What does that mean?

Capabilities turn the binary "root/non-root" dichotomy into a
fine-grained access control system. Processes (like web servers) that
just need to bind on a port below 1024 do not need to run as root: they
can just be granted the `net_bind_service` capability instead. And there
are many other capabilities, for almost all the specific areas where root
privileges are usually needed.

This means a lot for container security; let's see why!

#FIXME:
- process restrictions
- network restrictions
- device-restrictions
- filesystem restrictions

This means that even if an intruder manages to escalate to root within a
container, it is much harder to do serious damage, or to escalate
to the host.

One primary risk with running Docker containers is that the default set
of capabilities and mounts given to a container may provide incomplete
isolation, either independently, or when used in combination with
kernel vulnerabilities.
