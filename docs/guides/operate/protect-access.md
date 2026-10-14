---
description: How to choose between SSH and TLS to protect the Kleened socket
title: Protect the Kleened socket
---

Creating containers, manipulating the firewall etc. requires root, so the
Kleene backend daemon (Kleened) runs with root privileges.
Given the capabilities of Kleened, it implies that having access to the Kleened API
is equivalent to *having full root access to the host machine*. Therefore, obviously,
**only trusted users should have access to Kleened**.
For this reason, the REST API endpoint uses a UNIX socket by default,
instead of, e.g., a TCP socket bound to 127.0.0.1 (or a similar widely accessible
TCP socket). With a UNIX socket, traditional UNIX permission checks can be used to
limit access to the API socket.

However, the REST API can be exposed over TCP if explicitly configured to do so,
but be aware of the above mentioned security implications of doing this.
Even if the host has a firewall that limits accesses to the REST API
endpoint from external networks, the endpoint can still be accessible
from containers, and it can easily result in privilege escalation.
Therefore it is *mandatory* to secure exposed API endpoints with
TLS and certificates, as described in the following.
It is also recommended to ensure that it is reachable only from a trusted
network and/or VPN.

## Choosing an approach

- [SSH access to the Kleened socket](ssh-access.md): forward the UNIX socket
  over SSH. Simple, reuses SSH authentication, but requires that the user has
  access to the root socket on the host.
- [TLS (HTTPS) for the Kleened socket](tls.md): serve the API over TCP with
  certificates, optionally requiring client certificates. Needed whenever
  Kleened must be reachable without an SSH login, e.g. by CI or other hosts.
- [Combining SSH and TLS](ssh-access.md#use-a-combination-of-ssh-and-tls):
  the most locked-down setup — SSH for access control and mutual TLS on
  127.0.0.1 to guard against unintended access from containers.
