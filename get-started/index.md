---
title: "Overview"
keywords: get started, overview, quickstart, intro, concepts, containers, images
description: Get an overview of the Get started guide and learn about containers and images.
---

This guide contains step-by-step instructions on how to get started with Kleene. Some of the things you'll learn and do in this guide are:

- Building images and the image development workflow.
- Deploy applications using containers in both single- and multi-container setups.
- Using volumes for persisting data across containers.
- Using networks for inter-container communication.

Note that this guide follows Docker's [Getting started guide](https://docs.docker.com/get-started/) closely,
so if you have previous experience with Docker, comparing the two guides gives a
hands-on example on the some of ways Kleene differs from 'classical' container management.

## What is a container?

Simply put, a container is a sandboxed process on your machine that is isolated
from all other processes on the host machine.
Unlike Linux, the idea of a isolated execution environment is a first class citizen in
FreeBSD with [jails](https://docs.freebsd.org/en/books/handbook/jails/),
since it was introduced in 1999.
A FreeBSD 'jail' is *almost* equivalent to a container, although it is more primitive
compared to modern container concepts from the Linux world, such as Docker.

Kleene is based on jails, but does a lot of details that is otherwise left to the user, such as
configure networking, creating container filesystems and seperating the running
container from its container-template (i.e., its image).

To summarize, a container:

- is a runnable instance of an image. You can create, start, stop, move, or delete a container using the Kleened API or Klee CLI.
- is isolated from other containers and runs its own userland, binaries, and configurations.

## What is a container image?

When running a container, it uses an isolated filesystem.
This custom filesystem is created from an image.
Since the container is a copy of an image, the image must contain everything needed
to run an application - all dependencies, configurations, scripts, binaries, etc.
The image also contains other configurations for the container, such as
environment variables, a default command to run, and other metadata.

## Next steps

In the next section, you'll containerize your first application.

[Containerize an application](02_our_app.md){: .button  .primary-btn}

