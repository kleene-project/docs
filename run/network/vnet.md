---
title: VNET networking
description: Introduction to VNET container networking
keywords: network, vnet, bridge, networking
---

This section describes how to setup container networking
using the `vnet` network driver.

## Creating network and containers

Let's start by creating a bridge network for our containers.
Bridge networks are the only type that works for vnet-containers.

```console
$ klee network create -t bridge --subnet 10.4.6.0/24 testvnet
2f1dc29b8f36
```

Now we can connect containers to it. Using the `klee run` command we
can connect a container on-the-fly, similar to ipnet-containers:

```console
$ klee run -l vnet -n testvnet FreeBSD ifconfig
173a1a8d848d
created execution instance 2fc5447ef1e8
add net default: gateway 10.4.6.1
lo0: flags=8008<LOOPBACK,MULTICAST> metric 0 mtu 16384
        options=680003<RXCSUM,TXCSUM,LINKSTATE,RXCSUM_IPV6,TXCSUM_IPV6>
        groups: lo
        nd6 options=21<PERFORMNUD,AUTO_LINKLOCAL>
pflog0: flags=0<> metric 0 mtu 33160
        groups: pflog
epair0b: flags=8863<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> metric 0 mtu 1500
        options=8<VLAN_MTU>
        ether 02:1e:66:05:b0:0b
        inet 10.4.6.2 netmask 0xffffff00 broadcast 10.4.6.255
        groups: epair
        media: Ethernet 10Gbase-T (10Gbase-T <full-duplex>)
        status: active
        nd6 options=29<PERFORMNUD,IFDISABLED,AUTO_LINKLOCAL>

executable 2fc5447ef1e8 and its container exited with exit-code 0
```

You can compare the output of `ifconfig` with the similar output from
the [IPNet intro](ipnet.md):

- A gateway is added before the command `ifconfig` is run. Since VNet-containers
  have their own network stack, the default gateway needs to be set manually.
  Thankfully, Kleene does this for us.

- There is no physical interface since it belongs to the hosts' network
  stack. However, the container has its own loopback interface `lo0` and
  firewall logging interface `pflog0`.

- One end of the virtual ethernet-cable ends `epair0b` is attached to the
  container with its IP as assigned to it.

Looking at the interfaces on the host:

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
kleene0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> metric 0 mtu 16384
        options=680003<RXCSUM,TXCSUM,LINKSTATE,RXCSUM_IPV6,TXCSUM_IPV6>
        inet6 fe80::1%kleene0 prefixlen 64 scopeid 0x5
        groups: lo
        nd6 options=21<PERFORMNUD,AUTO_LINKLOCAL>
kleene1: flags=8843<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> metric 0 mtu 1500
        ether 58:9c:fc:10:30:3d
        inet 10.4.6.1 netmask 0xffffff00 broadcast 10.4.6.255
        id 00:00:00:00:00:00 priority 32768 hellotime 2 fwddelay 15
        maxage 20 holdcnt 6 proto rstp maxaddr 2000 timeout 1200
        root id 00:00:00:00:00:00 priority 32768 ifcost 0 port 0
        groups: bridge
        nd6 options=9<PERFORMNUD,IFDISABLED>
```

We note that a new bridge interface `kleene0` have been created. `kleene0`
belongs to our loopback network from the [IPNet introduction](ipnet.md).
There is no `epair0a` since the epair interfaces have been destroyed, when the
container stopped (after running `ifconfig`).

## Inter-container communication on the same network

In the [IPNet introduction](ipnet.md) we saw how two containers on
the same network are able to communicate.
That also holds for bridge networks + vnet-containers in exactly
the same manner as the ipnet-containers on our loopback network.

Similarily, we can connect a ipnet and a vnet container using a bridge network:

```console
$ klee network create -t bridge --subnet 10.4.6.0/24 testnet
$ klee run -n testnet --ip 10.4.6.2 -l ipnet -J allow.raw_sockets --name webservice FreeBSD
$ klee run -n testnet --ip 10.4.6.3 -l vnet --name vpnservice FreeBSD
```

Note that we manually assign IP's this time so services running in the
containers can always be reached from the same address. Also note that
we enabled raw sockets for the ipnet-container, otherwise we could not use
`ping`. That is not necessary for the vnet container since it has its own
virtual network stack.

We verify connectivity:

```console
$ klee exec webservice ping 10.4.6.3
created execution instance 8a270fa61bcb
PING 10.4.6.3 (10.4.6.3): 56 data bytes
64 bytes from 10.4.6.3: icmp_seq=0 ttl=64 time=0.097 ms
64 bytes from 10.4.6.3: icmp_seq=1 ttl=64 time=0.505 ms
```
