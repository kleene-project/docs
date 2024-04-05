---
title: Disable networking for a container
description: How to disable networking by using the none driver
keywords: network, none, standalone
---

If the container should not have any networking capabilities the network driver
`disabled` can be used. It basically has the same effect as using the `ipnet`
driver, except that not IP's are assigned:

```console
$ klee run -l disabled FreeBSD ifconfig
79a401f5b4a1
created execution instance 841bda6b7c21
em0: flags=8863<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> metric 0 mtu 1500
        options=481009b<RXCSUM,TXCSUM,VLAN_MTU,VLAN_HWTAGGING,VLAN_HWCSUM,VLAN_HWFILTER,NOMAP>
        ether 08:00:27:b2:00:96
        media: Ethernet autoselect (1000baseT <full-duplex>)
        status: active
em1: flags=8863<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> metric 0 mtu 1500
        options=481009b<RXCSUM,TXCSUM,VLAN_MTU,VLAN_HWTAGGING,VLAN_HWCSUM,VLAN_HWFILTER,NOMAP>
        ether 08:00:27:a3:0d:42
        media: Ethernet autoselect (1000baseT <full-duplex>)
        status: active
lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> metric 0 mtu 16384
        options=680003<RXCSUM,TXCSUM,LINKSTATE,RXCSUM_IPV6,TXCSUM_IPV6>
        groups: lo
pflog0: flags=0<> metric 0 mtu 33160
        groups: pflog

executable 841bda6b7c21 and its container exited with exit-code 0
```

and it is not possible to publish ports

```console
$ klee run -l disabled -p 8080 FreeBSD
cannot publish ports of a container using the 'disabled' network driver
could not create container: cannot publish ports of a container using the 'disabled' network driver
```
