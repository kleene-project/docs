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
hands-on example of the similarities and differences between Kleene and Docker.

## What is a container?

Simply put, a container is a sandboxed process on your machine that is isolated
from all other processes on the host machine.
Unlike Linux, the container concept is a first class citizen in FreeBSD with [jails](https://docs.freebsd.org/en/books/handbook/jails/),
so a FreeBSD 'jail' is *almost* equivalent to a container.

However, Kleene does alot of details that is otherwise left to the user, such as
configure networking, creating container filesystems and seperating the running
container from its container-template (i.e., its image).

To summarize, a container:

- is a runnable instance of an image. You can create, start, stop, move, or delete a container using the Kleened API or Klee CLI.
- is isolated from other containers and runs its own userland, binaries, and configurations.

## What is a container image?

When running a container, it uses an isolated filesystem. This custom filesystem is provided by a container image.
Since the image contains the container's filesystem, it must contain everything needed to run an application - all dependencies, configurations, scripts, binaries, etc.
The image also contains other configurations for the container, such as environment variables, a default command to run, and other metadata.

## Next steps

In this section, you learned about containers and images.

In the next section, you'll containerize your first application.

[Containerize an application](02_our_app.md){: .button  .primary-btn}

