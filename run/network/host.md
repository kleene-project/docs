---
title: Use host networking
description: All about exposing containers on the Docker host's network
keywords: network, host, standalone
---

If you use the `host` network driver for a container, that container inherits
its interface configuration from the host. This means that all interfaces and
assigned IP-addresses of the host are available to the container.

```console
$ ifconfig
em0: flags=8863<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> metric 0 mtu 1500
        options=481009b<RXCSUM,TXCSUM,VLAN_MTU,VLAN_HWTAGGING,VLAN_HWCSUM,VLAN_HWFILTER,NOMAP>
        ether 08:00:27:b2:00:96
        inet 10.0.2.15 netmask 0xffffff00 broadcast 10.0.2.255
        media: Ethernet autoselect (1000baseT <full-duplex>)
        status: active
        nd6 options=29<PERFORMNUD,IFDISABLED,AUTO_LINKLOCAL>
lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> metric 0 mtu 16384
        options=680003<RXCSUM,TXCSUM,LINKSTATE,RXCSUM_IPV6,TXCSUM_IPV6>
        inet6 ::1 prefixlen 128
        inet6 fe80::1%lo0 prefixlen 64 scopeid 0x3
        inet 127.0.0.1 netmask 0xff000000
        groups: lo
        nd6 options=21<PERFORMNUD,AUTO_LINKLOCAL>
pflog0: flags=0<> metric 0 mtu 33160
        groups: pflog
$ klee run FreeBSD ifconfig
fa70a5f54d82
created execution instance dd260b63b55a
em0: flags=8863<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> metric 0 mtu 1500
        options=481009b<RXCSUM,TXCSUM,VLAN_MTU,VLAN_HWTAGGING,VLAN_HWCSUM,VLAN_HWFILTER,NOMAP>
        ether 08:00:27:b2:00:96
        inet 10.0.2.15 netmask 0xffffff00 broadcast 10.0.2.255
        media: Ethernet autoselect (1000baseT <full-duplex>)
        status: active
        nd6 options=29<PERFORMNUD,IFDISABLED,AUTO_LINKLOCAL>
lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> metric 0 mtu 16384
        options=680003<RXCSUM,TXCSUM,LINKSTATE,RXCSUM_IPV6,TXCSUM_IPV6>
        inet6 ::1 prefixlen 128
        inet6 fe80::1%lo0 prefixlen 64 scopeid 0x3
        inet 127.0.0.1 netmask 0xff000000
        groups: lo
        nd6 options=21<PERFORMNUD,AUTO_LINKLOCAL>
pflog0: flags=0<> metric 0 mtu 33160
        groups: pflog

executable dd260b63b55a and its container exited with exit-code 0
```

However, it is not possible to modify the interfaces:

```console
$ sudo ifconfig lo0 alias 127.0.0.2
$ klee run FreeBSD ifconfig lo0 alias 127.0.0.3
f2f15d83969a
created execution instance d3acb03e0e5f
ifconfig: ioctl (SIOCAIFADDR): permission denied
jail: /usr/bin/env ifconfig lo0 alias 127.0.0.3: failed

executable d3acb03e0e5f and its container exited with exit-code 1
```

Also note that publishing ports is not possible:

```console
$ klee run -p 8080 FreeBSD
cannot publish ports of a container using the 'host' network driver
could not create container: cannot publish ports of a container using the 'host' network driver
```
