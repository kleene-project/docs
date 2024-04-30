---
title: "Restrict container resource consumption"
description: "Specify the runtime resource consumption limits for a container"
keywords: "kleened, jail, rctl, zfs, resource limit, configuration, runtime"
---

By default, there is no resource constraints on containers, so it is possible
to exhaust a host resource, such as memory, from within a container.
There are two ways of restricting containers that will be briefly discussed
in the following.

## ZFS

Since a container reside on a seperate ZFS dataset it is possible restrict
filesystem-related resources, such as limiting the amount of space that can be
used by a container. This and other ways of configuring the underlying dataset
of a container are discussed in the section on [ZFS configuration](/operation/zfs).

## RCTL

FreeBSD comes with the [`rctl(4)` subsystem](https://man.freebsd.org/cgi/man.cgi?query=rctl&sektion=4)
which provides a flexible mechanism for limiting resources, such as memory and CPU.
Specifically, it can be used to limit resources for jails and thus
containers. However, this subsystem have not been integrated into Kleene yet, so
it has to be configured manually. This is straightforward to do, since the jail name
that is used when specifying RCTL-rules equals the container id in Kleene.

Consult the following external resources to know more about RCTL:

- [The section on jail resource limits](https://docs.freebsd.org/en/books/handbook/jails/#jail-resource-limits)
  in the FreeBSD handbook introduces RCTL resource limiting of jails with
  links to a general introduction on resource limiting in FreeBSD.
- [The man-page of the `rctl` CLI](https://man.freebsd.org/cgi/man.cgi?query=rctl&sektion=8)
  used to manage RCTL-rules. It includes a list of resources
  that can be managed with RCTL, as well as the rule-syntax for doing so.
