---
title: Building your runtime environments
keywords: build, image, container, getting started, dockerfile
---

## Dockerfile

It all starts with a Dockerfile. For a thorough walk-through of what a
Dockerfile is, it is recommended to consult [Docker's documention](https://docs.docker.com/build/building/packaging/) or
Kleene's [getting started](/get-started) guide, which is an adapted version
of Docker's [guide](https://docs.docker.com/get-started/), to highlight differences.

Kleened builds images by reading the instructions from a Dockerfile,
using a subset of the instructions known from Docker.
You can find Kleene's specification reference in the [Dockerfile reference](/reference/dockerfile/).

Here are the most common and basic instructions:

| Instruction                                                | Description                                                                                                              |
|------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| [`FROM <image>`](/reference/dockerfile#from)              | Defines a base for your image. This is used to create a new designated filesystem for the image that is being built.     |
| [`RUN <command>`](/reference/dockerfile#run)           | Executes any commands within the designated filesystem. `RUN` also has a shell form for running commands.                |
| [`WORKDIR <directory>`](/reference/dockerfile#workdir) | Sets the working directory for any `RUN`, `CMD`, and `COPY` instructions that follow it in the Dockerfile.               |
| [`COPY <src> <dest>`](/reference/dockerfile#copy)      | Copies new files or directories from `<src>` and adds them to the filesystem of the container at the path `<dest>`.      |
| [`CMD <command>`](/reference/dockerfile#cmd)           | Defines the default command that runs when starting containers based on this image.                                      |

The default filename to use for a Dockerfile is `Dockerfile`, without a file
extension. Using the default name allows you to run the `klee build` command
without having to specify additional command flags.

Some projects may need distinct Dockerfiles for specific purposes. A common
convention is to name these `Dockerfile.<something>`. Such Dockerfiles can then
be used through the `--file` (or `-f` shorthand) option on the `klee build` command.
Refer to the [`klee build` section](/reference/klee/build)
in the `klee` reference documentation to learn about build configuration.

## Context

A build's context is the set of files located at a path specified
by the positional `PATH` argument to the build command, i.e.,

```console
$ klee build [OPTIONS] PATH
```

The build process can refer to any of the files or directories in the context
using the [`COPY` instruction](/reference/dockerfile#copy).

> **Note**
>
> Presently, the `PATH` argment should refer to a path
> *on the host machine* and not the client where `klee` is running.
> If you are using Klee on the same system as Kleened, those
> two are the same.

## How image building works

Kleene images are essentially created by [cloning](https://man.freebsd.org/cgi/man.cgi?query=zfs-clone)
the filesystem of another image. The cloned file system is then used
to create a container that is used to execute instructions from the Dockerfile.
When there is no more instructions, Kleene saves all relevant metadata and
converts the container's filesystem into an image-filesystem and the build
is complete.

Since the basis for an image build is a ZFS-clone, it is
duplicated with practically zero storage costs. Only the data that is written during
the build process takes up actual space on the hosts filesystem.

Note that unlike images of, e.g., Docker and Podman, Kleene has no concept of layers.
Kleene uses zfs [snapshots](https://man.freebsd.org/cgi/man.cgi?query=zfs-snapshot)
and [clones](https://man.freebsd.org/cgi/man.cgi?query=zfs-clone)
for creating images and containers.

## Example: Creating an image

Here's a simple Dockerfile example to get you started with building images.
We'll take a simple "Hello World" Python Flask application, and bundle it into
an image that can be easily deployed by Kleene.

Remember to [prepare the Kleene host](/get-started/02_our_app/#prepare-the-kleened-host)
if haven't already been done:

```console
$ klee image create -t FreeBSD fetch-auto
... a lot of output here ...
$ klee network create --subnet 10.13.37.0/24 testnet
```

Since no tag was given, kleene automatically uses `latest`, meaning that the
nametag of the image created above will be `FreeBSD:latest`.

Now, let's say we have a `hello.py` file with the following content:

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
```

If you're not familiar with Python, it's just a simple web server that
will contain a single page that says "Hello World". However, remember to
preserve indentation.

Here's the Dockerfile that will be used to create an image for our application:

```dockerfile
FROM FreeBSD:latest

# install app dependencies
RUN pkg install -y py39-flask

# install app
COPY hello.py /

# final configuration
ENV FLASK_APP=hello
CMD flask run --host 0.0.0.0 --port 8000
```

First, we define the `FROM`-instruction:

```dockerfile
FROM FreeBSD:latest
```

Here the [`FROM` instruction](/reference/dockerfile#from) sets the
parent image of our "Hello World"-app to the [base image](/building/base-images/) that we created just before.

All following instructions are executed on (a clone of) this base image.

```dockerfile
# install app dependencies
RUN pkg install -y py39-flask
```

The [`RUN` instruction](/reference/dockerfile#run) executes a shell
command that installs Flask and all it's dependencies, including Python.

In this example, our context is a full FreeBSD base system matching that of the host.

Also note the `# install app dependencies` comment line. Comments in
Dockerfiles begin with the `#` symbol. As your Dockerfile evolves, comments can
be instrumental to document how your dockerfile works for any future readers
and editors of the file.

```dockerfile
COPY hello.py /
```

Now we use the [`COPY` instruction](/reference/dockerfile#copy) to
copy our `hello.py` file from the local [build context](/glossary/#context) into the
root directory of our image. After being executed, we'll end up with a file
called `/hello.py` inside the image.

```dockerfile
ENV FLASK_APP=hello
```

The [`ENV` instruction](/reference/dockerfile#env) sets an
environment variable we'll need later. This is a flask-specific variable,
that configures the command later used to run our `hello.py` application.
Without this, flask wouldn't know where to find our application to be able to
run it.

```dockerfile
CMD flask run --host 0.0.0.0 --port 8000
```

Finally, [`CMD` instruction](/reference/dockerfile#cmd) sets the
command that is run when the user starts a container based on this image. In
this case we'll start the flask development server listening on all addresses
on port `8000`.

### Building the image and running the app

To test our Dockerfile, we'll first build it using the [`klee build` command](/reference/klee/build):

```console
$ klee build -t test:latest .
```

Here `-t test:latest` option specifies the name (required) and tag (optional)
of the image we're building. `.` specifies the [build context](/glossary/#context) as
the current directory. In this example, this is where Kleene expects to find the
Dockerfile and the local files the Dockerfile needs to access, in this case
your Python application (`hello.py`).

So, in accordance with the build command issued and how [build context](/glossary/#context)
works, your Dockerfile and python app need to be in the same directory.

Now run your newly built image:

```console
$ klee run --network testnet test:latest
```

Now the application should be running on your computer. We did not specify
an IP-address, so Kleene automatically found a unused one from the subnet
of the `testnet` network. There are several ways to identify it, however,
using `jls` or using `klee container inspect <container-id>` where
`<container-id>` is outputted by `klee run ...`.

If you run this container locally, you can open a browser and navigate to
`http://localhost:8000`. If you run the container on a remote server you
can make a SSH-tunnel `ssh -L 8000:<container IP>:8000 <your-host>`
before navigating to `http://localhost:8000`.

## Build configuration

Since the image creation uses a build container for running build commands, it
can be configured like any other container. This can be necessary when some
some build steps require non-standard privileges, as illustrated in the image
[snapshots example](/building/snapshots). Conversely, there might be a
need to restrict the build environment for security reasons.

The configuration parameters used to configure the build container with
`klee build` is almost identical to the container configuration of `klee run`.
See the [the reference documentation](/reference/klee/build)
for details.

## Image design

Since Kleene is a new tool, there is not any well-established patterns for
image design, except for what is being used by other similar tools.
However, here follows a few tentative suggestion on image design.

### How to keep your images small

In order to keep build times low and minimize storage footprint, it is a good
idea to try and keep image sizes small. Here are a few rules of thumb to try an
achieve that:

- If there are multiple images with a lot in common, consider creating a
  'core' image with the shared components, and basing the images on that instead
  of installing/configuring the shared components across all images.

- Consider using the production image as the base image for a debug image, if needed.
  Additional testing or debugging tooling can be added on top of the production image.

- When building images, always tag them with useful tags which codify version
  information, intended destination (`prod` or `test`, for instance), stability,
  or other information that is useful when deploying the application in
  different environments. Do not rely on the automatically-created `latest` tag.

### Where and how to persist application data

- Store data using [volumes](/run/storage/volumes/).

- One case where it is appropriate to use
  [nullfs mounts](/run/storage/nullfs-mounts/) is during development,
  where it is desirable to mount a source directory or newly built binaries
  into the container. For production, use a volume instead, mounting it into
  the same location as the bind mount that was used during development.

- For production, use files mounted into the container for sensitive
  application data used by services.
