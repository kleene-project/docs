---
title: Building images
description: How Kleened builds images from a Dockerfile and a build context
---

## Dockerfile

It all starts with a Dockerfile. For a thorough walk-through of what a
Dockerfile is, it is recommended to consult [Docker's documention](https://docs.docker.com/build/building/packaging/) or
Kleene's [getting started](../../get-started/tutorial/index.md) guide, which is an adapted version
of Docker's [guide](https://docs.docker.com/get-started/), to highlight differences.

Kleened builds images by reading the instructions from a Dockerfile,
using a subset of the instructions known from Docker.
You can find Kleene's specification reference in the [Dockerfile reference](../../reference/dockerfile.md).

Here are the most common and basic instructions:

| Instruction                                                | Description                                                                                                              |
|------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| [`FROM <image>`](../../reference/dockerfile.md#from)              | Defines a base for your image. This is used to create a new designated filesystem for the image that is being built.     |
| [`RUN <command>`](../../reference/dockerfile.md#run)           | Executes any commands within the designated filesystem. `RUN` also has a shell form for running commands.                |
| [`WORKDIR <directory>`](../../reference/dockerfile.md#workdir) | Sets the working directory for any `RUN`, `CMD`, and `COPY` instructions that follow it in the Dockerfile.               |
| [`COPY <src> <dest>`](../../reference/dockerfile.md#copy)      | Copies new files or directories from `<src>` and adds them to the filesystem of the container at the path `<dest>`.      |
| [`CMD <command>`](../../reference/dockerfile.md#cmd)           | Defines the default command that runs when starting containers based on this image.                                      |

The default filename to use for a Dockerfile is `Dockerfile`, without a file
extension. Using the default name allows you to run the `klee build` command
without having to specify additional command flags.

Some projects may need distinct Dockerfiles for specific purposes. A common
convention is to name these `Dockerfile.<something>`. Such Dockerfiles can then
be used through the `--file` (or `-f` shorthand) option on the `klee build` command.
Refer to the [`klee build` section](../../reference/klee/build.md)
in the `klee` reference documentation to learn about build configuration.

