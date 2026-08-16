---
description: Kleene explained in general terms
keywords: kleene, introduction, documentation, about, technology, understanding
title: Kleene overview
---

Kleene is a container management platform based on the concepts and abstractions
known from Docker, but adapted to a FreeBSD context.
Kleene aims to extend FreeBSD's 'Power to Serve', by making it easier to develop,
maintain, upgrade, and retire applications running on a FreeBSD system.

Kleene builds on the experiences from Docker and the Linux world to provide
tooling that lets you focus on how to build, run, deploy, and maintain your applications,
and spend less time on nitty gritty system configuration.

This is done by introducing highlevel concepts of containers, images, and
networks, encapsulating OS-specfic primitives and taking care of the underlying
configration, such as:

- Setting up [jailed](https://man.freebsd.org/cgi/man.cgi?query=jail&sektion=8) applications
  in lightweight environments using [zfs(8)](https://man.freebsd.org/cgi/man.cgi?query=zfs&sektion=8).
- Configuring host networking and creating necessary network devices.
- Setting up connectivity using the [packet filter](https://man.freebsd.org/cgi/man.cgi?query=pf&sektion=4) firewall.

At the same time, Kleene aims to be transparent in its interaction
with the FreeBSD host system, such that the user
can make special customizations tailored to special needs.

If you are new to containers it is recommended to consult
[Docker's high-level overview](https://docs.docker.com/get-started/overview/)
for an introduction to containerisation. However, while Kleene is heavily
inspired by Docker and the Linux container community, there are also some
substantial differences.
See [the introduction](/get-started/) of the 'getting started' guide
to get a quick intro to containers and images in Kleene.

## Kleene's approach to container management

If you already have experience using Docker or Podman then Kleene will
seem very familiar.
The `klee` command line tool follows (almost) the same structure as `docker` and
the basic concepts (container, image, network, volume) are the same.
Kleene also implements (a subset of) Dockers `Dockerfile` specification, with minor
differences.

A few differences worth highlighting, however, are the following:

- Networking and the network object is different compared to Docker and Linux containers,
  as well as system-specific configuration options for containers,
  since they are based on different OS primitives than what exists on Linux.
  More specifically, the [jail](https://man.freebsd.org/cgi/man.cgi?query=jail&sektion=8)-mechanism
  of process isolation differs from the Linux-world.

- Kleene tries to make its use of the host system as transparant as possible
  for the user and to make it easy to use FreeBSD's built-in tooling.
  FreeBSD already contain a few helpful tools that can be used in conjunction
  with Kleene, such as `jls(8)`, `jexec(8)`, `zfs(8)` etc.
  These and similar tools provide ways of further customizing your FreeBSD
  host environment and its containers besides what is offered by Kleene.
  See the [external resources](/external-resources)
  for a list of CLI tools and their documentation.

- Build your own images and share code, not binaries. Reproducibility starts with
  a Dockerfile and a context, and images should be re-build every time FreeBSD is
  upgraded or when new versions of software  packages become available.
  This is the philosophy behind further development of
  Kleene and this implies that distributing pre-compiled images have not been
  prioritised for now.

- Containers as thin virtual machines. While it is possible to use
  containers "the Docker way" by starting the main application with the `CMD`-instruction,
  it is a common pattern in FreeBSD to start containers (jails) using the system
  startup script `/etc/rc`.
  This affects the way images are designed and containers are managed.

These differences will explained throughout the Kleene handbook.
It is also worth reading some of the chapters in the FreeBSD handbook
[about jails](https://docs.freebsd.org/en/books/handbook/jails/).
In general, the FreeBSD handbook is a great resource on the operating system.

## The Kleene components

Kleene uses a client-server design. Klee (the client) tells Kleened (the server)
what to do, and the latter does all the work with building and running your containers.
Klee and Kleened can run on the same system, or you can connect Klee to a remote
Kleened host. They communicate using a REST API, over UNIX sockets or a network interface.

### Kleened, the backend daemon

Kleened listens for API requests and manages objects such as images, containers,
networks, and volumes. It is Kleened that does all the heavy lifting like manipulating
the ZFS filesystem, creating jailed processes, configuring the network and so on.

### Klee, the command line tool

The Klee command line tool (`klee`) is the primary way to interact
with Kleened. When you use commands such as `klee run`, Klee makes the needed
API requests to Kleened and renders the result to the user.

## Kleene conceptual architecture

![Kleene Architecture diagram](/assets/images/kleene_conceptual_architecture.png)

### Kleene objects

When you use Kleene, you are creating and using images, containers, networks,
volumes, and other objects. This section is a brief overview of some
of those objects.

#### Images

An _image_ is a zfs dataset containing a configured runtime used for creating containers.
Images usually includes an entire FreeBSD userland with additional application-specific
configurations. Often, an image is based on another image, adding additional
configurations. For example, you may build an image based on a parent-image of
FreeBSD 13.2-RELEASE, that installs the Nginx web server and your application,
as well as the configuration details needed to make your application run.

To build your own image, you create a _Dockerfile_
with a simple syntax for defining the commands needed to create the image and run
it.

#### Containers

A container is a writable copy of an image to run in a OS-level virtual environment
(a FreeBSD jail). You can create, start, stop, or delete a container using
the Kleened API or Klee, Kleene's native CLI.
You can connect a container to one or more networks, attach storage volumes to it
and so on.

By default, a container is mostly isolated from other containers and
its host machine. You can control how isolated a container's network, storage,
or other underlying subsystems are from other containers or from the host
system.

A container is defined by its image as well as any configuration options you
provide to it when you create or start it. When a container is removed,
any changes to its state that are not stored in persistent storage volumes disappear.

#### Networks

In order for containers to be able to communicate with the surroundings,
they need to be attache to a network. A network connects one or more containers
to eachother and to other networks. There exists a couple of different network-types,
based on how the contaner-connectivity is configured in FreeBSD.

#### Volumes

Volumes are used to provide persistent storage for the ephemeral containers.
Basically, volumes are zfs datasets that are mounted into one or more containers.

## The underlying technology

Kleene's backend, Kleened, is mostly written in the [Elixir programming language](https://elixir-lang.org/)
using the underlying OTP-framework and the BEAM VM of [Erlang](https://www.erlang.org/).
This technology stack is chosen for it's high focus on concurrency and fault-tolerance.
Kleened's objects (images, containers, networks etc.) are implemented by orchestrating
FreeBSD's core technologies such as jails, pf, and zfs. These objects can be manipulated
using Kleened's HTTP-based API which consist of a REST API and some websocket
endpoints for streaming/interactive communication.

Kleene's frontend CLI, Klee, is written in [Python](https://www.python.org/)
using the `click` and `rich` packages.
Klee communicates with Kleened through it's API and can thus run on a
seperate machine from Kleened. However, for now it is recommended to use Klee
directly on the same machine as Kleened.

## Project status

See the [Project status](/contribute/project-status/) page.
