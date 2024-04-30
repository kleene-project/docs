---
title: Configure containers using jail parameters
description: Tuning container environments with jail parameters
keywords: kleene, run, configure, runtime, jail, container, jail parameter
---

Creating containerized environments in Kleene is done using
FreeBSD's [system
jails](https://man.freebsd.org/cgi/man.cgi?query=jail&sektion=2),
and the primary way to configure the behavior of system jails is by using
[jail parameters](https://man.freebsd.org/cgi/man.cgi?query=jail).
Kleene uses some of these parameters under the hood to configure basic behavior, such as:

- What network driver is used to provide connectivity to the container.
- What user is running the initial process in the container
- Which host ressources are available to the container

Jail parameters offers flexible and powerful configuration options when creating
containers. For instance, the `exec.[pre|post]start` and `exec.[pre|post]stop`
jail parameters enable custom commands to be run during container creation and
removal, and are also used by Kleene in some cases.

Jail parameters also provides many ways of expanding the allowed capabilites in a
container, and there are many different use cases that is out of scope
here, where containers are allowed to create virtual machines, manage ZFS
datasets, creating jails within jails and more.

See the 'Jail parameters' section of the
[`jail` man page](https://man.freebsd.org/cgi/man.cgi?query=jail) for a complete
list of all possbile parameters and a description of each. It might also come in
handy in the following, where some of the parameters are introduced.

## How jail parameters are handled in Kleene

Kleene automatically sets a few default jail parameters, if they are not
explicitly set. For instance, running

```console
$ klee run FreeBSD echo "Hello World"
```

will (roughly) make Kleene start a jail/container on the host with:

```console
# /usr/sbin/jail -c path=<kleene-root-mountpoint>/container/9b4fd69fb5f2 \
  name=9b4fd69fb5f2 \
  host.hostname=9b4fd69fb5f2 \
  ip4=inherit ip6=inherit \
  exec.jail_user=root \
  exec.clean=true \
  mount.devfs \
  exec.stop="/bin/sh /etc/rc.shutdown" \
  command=echo Hello World
```

The `ip4` and `ip6` jail parameter values are derived
from the default `host` network driver.

The jail parameters where Kleene provide defaults are as follows:

| Parameter        | Default                                | Overwrite manually                                                                 |
|------------------|----------------------------------------|------------------------------------------------------------------------------------|
| `host.hostname`  | `host.hostname=<container ID>`         | `-J host.hostname=myhostname`                                                      |
|------------------|----------------------------------------|------------------------------------------------------------------------------------|
| `mount.devfs`    | `mount.devfs=true`                     | `-J mount.devfs=false` or `-J mount.nodevfs`                                       |
|------------------|----------------------------------------|------------------------------------------------------------------------------------|
| `exec.jail_user` | Inherited from the image               | Using `-u <user>` or `-J exec.jail_user=<user>` where the latter takes precedence. |
|------------------|----------------------------------------|------------------------------------------------------------------------------------|
| `exec.clean`     | `exec.clean=true`                      | `-J exec.clean=false` or `-J exec.noclean`                                         |
|------------------|----------------------------------------|------------------------------------------------------------------------------------|
| `exec.stop`      | `exec.stop="/bin/sh /etc/rc.shutdown"` | `-J exec.nostop` or `-J exec.stop=""`                                              |


## Examples

There are a few examples throught this documentation. For instance, in the last
chapter of the [guide on how to use image snapshots](/building/snapshots/)
`-J allow.sysvipc=true` is required for the PostgreSQL database to work.

Another small example frequently used, is to allow raw sockets in the jail,
since it is required by the `ping` tool:

```console
$ klee run -J allow.raw_sockets FreeBSD ping freebsd.org
2cb6500c39df
created execution instance 4c54ea1a047c
PING freebsd.org (96.47.72.84): 56 data bytes
64 bytes from 96.47.72.84: icmp_seq=0 ttl=63 time=153.314 ms
64 bytes from 96.47.72.84: icmp_seq=1 ttl=63 time=161.068 ms
64 bytes from 96.47.72.84: icmp_seq=2 ttl=63 time=169.807 ms
^C
Aborted!
```

Allowing raw sockets is also actively used in the
[networking section](/run/network/ipnet/#inter-container-communication-on-the-same-network).
