---
title: Container name resolution
description: Resolving container names as hostnames with Kleene's built-in DNS resolver
---

Containers on the same Kleene network can reach each other by container
name, like on Docker user-defined networks: a container named `web` can be
connected to as `web` from any other container on the same network. Kleene
provides this with a small DNS resolver that runs on each network.

## How it works

Every network with a subnet gets a resolver listening on the network's
first IP address — `10.13.37.1` for a `10.13.37.0/24` network, the same
address that the automatically configured gateway of `vnet` containers
uses. When a container is started, Kleene writes a
`nameserver <resolver-ip>` line into its `/etc/resolv.conf`, so lookups of
plain container names go to the network's resolver.

Queries for names of containers that are connected to the same network are
answered with the address the target container has on that network. Any
other query is forwarded to the upstream resolvers configured on the
Kleene host, so normal DNS keeps working:

```console
$ klee network create --subnet 10.13.37.0/24 testnet
6b933304be4a
$ klee run -d --name web -n testnet FreeBSD sleep 600
e91d64df0e02
$ klee run -n testnet FreeBSD host web
web has address 10.13.37.2
```

Each container also gets an entry for its own name and address in its
`/etc/hosts`, managed between `# kleene-managed hosts` markers, so its own
name resolves even without the resolver.

## Networks without the resolver

The resolver can be disabled per network with
`klee network create --no-dns`. On such a network no IP is reserved for
the resolver, and the containers' `/etc/resolv.conf` is left as the image
provided it. Hostname resolution then relies on whatever the image
configures.

!!! note

    The resolver holds the first usable address of the network's subnet,
    so the first container connected gets the second address (`10.13.37.2`
    in the example above), not the first.

## Limits

- Only `A` and `AAAA` queries for container names are answered locally;
  everything else is forwarded.
- A container is resolvable by name only from networks it is connected to.
- Renaming or disconnecting a container takes effect in the resolver
  immediately (answers are computed from the current state), but a running
  container's `/etc/hosts` entry is only refreshed when it is started
  again.
