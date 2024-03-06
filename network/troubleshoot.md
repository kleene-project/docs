---
title: Troubleshooting
description: How to troubleshoot networking problems in Kleene
keywords: debugging, troubleshoot
---

Often it is a matter of time before issues occur when tweaking the
networking configuration. In that case, using `tcpdump` to monitor for blocked
packets can be a good place to start troubleshooting. Kleene automatically
enables the PF logging interface `pflog0` which can be used by `tcpdump`:

## Using `pflog0`

```
$ sudo tcpdump -tt -n -vv -e -i pflog0
tcpdump: listening on pflog0, link-type PFLOG (OpenBSD pflog file), capture size 262144 bytes
1709629771.126272 rule 0/0(match): block in on em0: (tos 0x0, ttl 246, id 54321, offset 0, flags [none], proto TCP (6), length 40)
    x.x.x.x.53722 > y.y.y.y.888: Flags [S], cksum 0x00da (correct), seq 1541908246, win 65535, length 0
1709629773.136602 rule 0/0(match): block in on em0: (tos 0x0, ttl 44, id 64466, offset 0, flags [none], proto UDP (17), length 73)
    z.z.z.z.5181 > y.y.y.y.53: [udp sum ok] 28826+ [1au] A? freebsd.org. ar: . OPT UDPsize=512 DO (45)
```

This can be very effective in case there is connectivity issues, i.e.,
when experiencing unexpected timeouts. From the `tcpdump`-output it is possible
to see import information such as IP-addresses (`x.x.x.x`, `y.y.y.y` etc.),
ports, traffic direction, protocols, interface receiving the traffic,
and which rule triggered the block. In the previous example it was the first
rule, which in this case could correspond to a `block all` rule in `pf.conf`.
Using `tcpdump` and comparing the results with current firewall configuration
`/etc/pf.conf` can provide useful information during troubleshooting.

Note that if some cases, such as ipnet-containers operating in restricted
networking environments, if a service tries to create an outgoing connection
that is blocked by the firewall, the connection operation will fail with a
permission error instead of timing out.

If vnet-containers is used, the container has its own network stack, including
a seperate firewall and `pflog0`.

Lastly, there can be problems with NAT'ing, in which case it can be relevant to
inspect traffic on other interfaces with `tcpdump`. In that case it might be
relevant to filter what packets should be printed by tcpdump, otherwise the
terminal might be flooded with traffic.

## Problems with routes

If there is routing problems, i.e., receiving an error `No route to host` it is
possible to inspect the routing table on the host (or within vnet-containers)
using `netstat -rn`. Consult the FreeBSD Handbooks section on
[Gateways and Routes](https://docs.freebsd.org/en/books/handbook/advanced-networking/#network-routing)
for more information.
