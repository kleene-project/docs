---
title: IPNet networking
description: Introduction to IPNet container networking
keywords: network, ipnet, loopback, networking
---

This section describes how to setup container networking
using the `ipnet` network driver.

## Creating network and containers

Let's start by creating a loopback network for the test-containers:

```console
$ klee network create --subnet 10.2.3.0/24 testnet
6b933304be4a
```

That's it! Now we can connect containers to it. Using the `klee run` command we
can connect a container on-the-fly. For instance, to create a container with the
ipnet network-driver, connecting it to the new network, and runing `ifconfig` within the
container do as follows:

```console
$ klee run -l ipnet -n testnet FreeBSD ifconfig
d763328950a2
created execution instance ec74e2e87920
em0: flags=8863<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> metric 0 mtu 1500
        options=481009b<RXCSUM,TXCSUM,VLAN_MTU,VLAN_HWTAGGING,VLAN_HWCSUM,VLAN_HWFILTER,NOMAP>
        ether 08:00:27:b2:00:96
        media: Ethernet autoselect (1000baseT <full-duplex>)
        status: active
lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> metric 0 mtu 16384
        options=680003<RXCSUM,TXCSUM,LINKSTATE,RXCSUM_IPV6,TXCSUM_IPV6>
        groups: lo
pflog0: flags=0<> metric 0 mtu 33160
        groups: pflog
kleene0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> metric 0 mtu 16384
        options=680003<RXCSUM,TXCSUM,LINKSTATE,RXCSUM_IPV6,TXCSUM_IPV6>
        inet 10.2.3.1 netmask 0xffffffff
        groups: lo

executable ec74e2e87920 and its container exited with exit-code 0
```

In the output of `ifconfig`, the only visible IP is `10.2.3.1`, within
the `testnet` subnet. It is on the loopback interface `kleene0` that Kleene created
for the network.

To verify connectivity, spin up a second container and try to reach our
DNS-server:

```console
klee run -l ipnet -n testnet FreeBSD host freebsd.org
f455de07ac84
created execution instance c64cb51be183
freebsd.org has address 96.47.72.84
freebsd.org has IPv6 address 2610:1c1:1:606c::50:15
freebsd.org mail is handled by 10 mx1.freebsd.org.
freebsd.org mail is handled by 30 mx66.freebsd.org.

executable c64cb51be183 and its container exited with exit-code 0
```

Inspecting the last container

```console
$ klee container inspect f455de07ac84
```

gets the following output:

```json
{
  "container": {
    "cmd": [
      "host",
      "freebsd.org"
    ],
    "created": "2024-02-26T08:52:13.530611Z",
    "dataset": "zroot/kleene/container/f455de07ac84",
    "env": [],
    "id": "f455de07ac84",
    "image_id": "11370bfb4a88",
    "jail_param": [
      "mount.devfs",
      "exec.stop=\"/bin/sh /etc/rc.shutdown jail\""
    ],
    "name": "hungry_knuth",
    "network_driver": "ipnet",
    "public_ports": [],
    "running": false,
    "user": "root"
  },
  "container_endpoints": [
    {
      "container_id": "f455de07ac84",
      "epair": null,
      "id": "89ef2673d9e5",
      "ip_address": "10.2.3.2",
      "ip_address6": "",
      "network_id": "testnet"
    }
  ],
  "container_mountpoints": []
}
```

In the `container_endpoints` section there is an endpoint for the `testnet`
network having ip `10.2.3.2`. As expected there is no `epair` allocated since
this is used for VNET-containers.

Inspecting the network with `klee network inspect testnet` produces:

```json
{
  "network": {
    "gateway": "<auto>",
    "gateway6": "<auto>",
    "icc": true,
    "id": "6b933304be4a",
    "interface": "kleene0",
    "internal": false,
    "name": "testnet",
    "nat": "em0",
    "subnet": "10.2.3.0/24",
    "subnet6": "",
    "type": "loopback"
  },
  "network_endpoints": [
    {
      "container_id": "d763328950a2",
      "epair": null,
      "id": "264f73bc570a",
      "ip_address": "10.2.3.1",
      "ip_address6": "",
      "network_id": "testnet"
    },
    {
      "container_id": "f455de07ac84",
      "epair": null,
      "id": "89ef2673d9e5",
      "ip_address": "10.2.3.2",
      "ip_address6": "",
      "network_id": "testnet"
    }
  ]
}
```

Here both endpoints are shown, one from each container connected to
the network. We can also see the properties that has been assigned to the
network (the default values), such as NAT'in, subnets etc.
The `gateway`/`gateway6` properties is not relevant here,
as they are only used for VNET-containers and they can't connect to loopback
networks.

## Inter-container communication on the same network

By default, containers connected to the same network can communicate with
each other. Now, let's try and see if the two containers

```console
$ klee lsc -a
CONTAINER ID    NAME            IMAGE            COMMAND            CREATED       STATUS    JID
─────────────────────────────────────────────────────────────────────────────────────────────────
 f455de07ac84    hungry_knuth    FreeBSD:latest   host freebsd.org   2 hours ago   stopped
 d763328950a2    strange_moser   FreeBSD:latest   ifconfig           2 hours ago   stopped
```

can communicate with each other. Since this is just for illlustration purposes, the two
containers are reused and initiated as thin VM's:

```console
$ klee exec hungry_knuth /bin/sh /etc/rc
created execution instance 4c71eea4de73
   <-- initialization output -->
4c71eea4de73 has exited with exit-code 0
$ klee exec strange_moser /bin/sh /etc/rc
created execution instance 28e2471f17ed
   <-- initialization output -->
28e2471f17ed has exited with exit-code 0
```

and, to verify that they are running as expected:

```console
$ klee lsc -a
CONTAINER ID    NAME            IMAGE            COMMAND            CREATED       STATUS    JID
─────────────────────────────────────────────────────────────────────────────────────────────────
 f455de07ac84    hungry_knuth    FreeBSD:latest   host freebsd.org   2 hours ago   running   3
 d763328950a2    strange_moser   FreeBSD:latest   ifconfig           2 hours ago   running   4
```

Perfect! Let's try to see if they can reach one another:

```console
$ klee exec hungry_knuth ping 10.2.3.1
created execution instance 2845c545dfc0
ping: ssend socket: Operation not permitted

2845c545dfc0 has exited with exit-code 71
```

By default, raw sockets, which is used by `ping`, are not allowed in ipnet
containers. It can be allowed by adding the `allow.raw_sockets` jail parameter
to the containers or instead use TCP-connections to verify inter-container connectivity.
TCP will be used here, and a simple TCP-server is started in one container:

```console
## Terminal 1:
$ klee exec strange_moser nc -l 4000
klee exec strange_moser nc -l 4000
created execution instance e32b997f34f3
```

Then try to connect the second container to it in another terminal:

```console
## Terminal 2:
$ klee exec hungry_knuth /bin/sh -c "echo testing | nc -vv 10.2.3.1 4000"
created execution instance 6bf64c969523
Connection to 10.2.3.1 4000 port [tcp/*] succeeded!
```

which should be immediately visible in the first container:

```console
## Terminal 1:
$ klee exec strange_moser nc -l 4000
klee exec strange_moser nc -l 4000
created execution instance e32b997f34f3
testing
```
