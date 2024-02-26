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
