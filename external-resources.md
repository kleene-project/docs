---
description: External resources
keywords: documentation, freebsd, docker, external resources
title: External resources
---

Learning more about underlying technologies makes it easier to
understand how Kleene works, how to use it efficiently, and how to tweak
the environment to specific needs. Therefore, a list of valuable external
ressources is compiled for the interested reader that wants to know more.

## Resources on containers in general

It is assumed that the reader has some familarity with traditional containers.
If that is not the case, Docker's excellent [documentation website](https://docs.docker.com/)
is a great resource to learn more.

## Resources on FreeBSD

- [FreeBSD's main website](https://freebsd.org) for downloading FreeBSD
  and getting the latest new on the operating system.

- [FreeBSD documentation portal](https://docs.freebsd.org/en/)
  is the main entrypoint of FreeBSD's documentation.
  
- [FreeBSD's handbook](https://docs.freebsd.org/en/books/handbook/) provides a
  wealth of guides and gives thorough introductions to the capabilities of
  FreeBSD. Specifically, the following chapters is of interest in relation to
  Kleene:
  
  - [Chapter 17. Jails and Containers](https://docs.freebsd.org/en/books/handbook/jails/)
    since this is the main technology used in Kleene.
    
  - [Chapter 22. The Z File System (ZFS)](https://docs.freebsd.org/en/books/handbook/zfs/)
    another essential component in Kleene.
  
  - [Chapter 33. Firewalls](https://docs.freebsd.org/en/books/handbook/firewalls/)
    and especially the section on PF that is used by Kleened. In many cases it
    can be necessary to do some additional PF-configuration to tailor the
    host environment to a specific environment and infrastructure.
    
  - [Chapter 34. Advanced Networking](https://docs.freebsd.org/en/books/handbook/advanced-networking/)
    covers many interesting topics that can be useful and which should work
    together with Kleene.

- [FreeBSD manual pages](https://man.freebsd.org/cgi/man.cgi)
  provides a nice webinterface for the man-pages that is essential for some of
  the relevant tools and subsystems. A few examples:
  
  - `jail(8)`: CLI tool for starting, stopping and modifying jails/containers. Also
    covers jail parameters, and provides examples etc.
  - `jexec(8)`: CLI tool for running additional processes in a running jail/container.
  - `jls(8)`: CLI tool for listing running jails/containers.
  - `zfs(8)`: Main entry to the ZFS CLI that also includes an introduction to
    ZFS.
  - `pf.conf(5)`: Description of PF's firwall rule syntax.
  - `pfctl(8)`: CLI tool for interacting with the PF firewall.
  - `rctl(8)`: CLI tool displaying and updating resource limits, including
    jails/conitainers. Also covers the syntax used.

- [Jail vnet by Examples](https://freebsdfoundation.org/wp-content/uploads/2020/03/Jail-vnet-by-Examples.pdf)
  is a great article publish in the FreeBSD journal, that show by examples how
  VNet-jails work. There is a lot of spin-off knowledge on FreeBSD jails and
  networking as well.
