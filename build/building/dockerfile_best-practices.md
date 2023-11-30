---
description: Hints, tips and guidelines for writing clean, reliable Dockerfiles
keywords: parent image, images, dockerfile, best practices, hub, official image
redirect_from:
- /articles/dockerfile_best-practices/
- /engine/articles/dockerfile_best-practices/
- /docker-cloud/getting-started/intermediate/optimize-dockerfiles/
- /docker-cloud/tutorials/optimize-dockerfiles/
- /engine/userguide/eng-image/dockerfile_best-practices/
title: Best practices for writing Dockerfiles
---

This document covers recommended best practices and methods for building
efficient images.

Docker builds images automatically by reading the instructions from a
`Dockerfile` -- a text file that contains all commands, in order, needed to
build a given image. A `Dockerfile` adheres to a specific format and set of
instructions which you can find at [Dockerfile reference](../../engine/reference/builder.md).

A Docker image consists of read-only layers each of which represents a
Dockerfile  instruction. The layers are stacked and each one is a delta of the
changes from the previous layer. Consider this `Dockerfile`:

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:18.04
COPY . /app
RUN make /app
CMD python /app/app.py
```

Each instruction creates one layer:

- `FROM` creates a layer from the `ubuntu:18.04` Docker image.
- `COPY` adds files from your Docker client's current directory.
- `RUN` builds your application with `make`.
- `CMD` specifies what command to run within the container.

When you run an image and generate a container, you add a new _writable layer_
(the "container layer") on top of the underlying layers. All changes made to
the running container, such as writing new files, modifying existing files, and
deleting files, are written to this writable container layer.

For more on image layers (and how Docker builds and stores images), see
[About storage drivers](../../storage/storagedriver/index.md).

## General guidelines and recommendations

### Create ephemeral containers

The image defined by your `Dockerfile` should generate containers that are as
ephemeral as possible. By "ephemeral", we mean that the container can be stopped
and destroyed, then rebuilt and replaced with an absolute minimum set up and
configuration.

Refer to [Processes](https://12factor.net/processes) under _The Twelve-factor App_
methodology to get a feel for the motivations of running containers in such a
stateless fashion.

### Understand build context

See [Build context](../../build/building/context.md) page for more information.

### Whether to use `/etc/rc` as `CMD`
TBD:
- jail/FreeBSD-approach vs. Docker
- "Create multiple services in an image"

### Pipe Dockerfile through `stdin`

Docker has the ability to build images by piping `Dockerfile` through `stdin`
with a _local or remote build context_. Piping a `Dockerfile` through `stdin`
can be useful to perform one-off builds without writing a Dockerfile to disk,
or in situations where the `Dockerfile` is generated, and should not persist
afterwards.

> The examples in this section use [here documents](https://tldp.org/LDP/abs/html/here-docs.html)
> for convenience, but any method to provide the `Dockerfile` on `stdin` can be
> used.
>
> For example, the following commands are equivalent: 
> 
> ```bash
> echo -e 'FROM busybox\nRUN echo "hello world"' | docker build -
> ```
> 
> ```bash
> docker build -<<EOF
> FROM busybox
> RUN echo "hello world"
> EOF
> ```
> 
> You can substitute the examples with your preferred approach, or the approach
> that best fits your use-case.


#### Build an image using a Dockerfile from stdin, without sending build context

Use this syntax to build an image using a `Dockerfile` from `stdin`, without
sending additional files as build context. The hyphen (`-`) takes the position
of the `PATH`, and instructs Docker to read the build context (which only
contains a `Dockerfile`) from `stdin` instead of a directory:

```bash
docker build [OPTIONS] -
```

The following example builds an image using a `Dockerfile` that is passed through
`stdin`. No files are sent as build context to the daemon.

```bash
docker build -t myimage:latest -<<EOF
FROM busybox
RUN echo "hello world"
EOF
```

Omitting the build context can be useful in situations where your `Dockerfile`
does not require files to be copied into the image, and improves the build-speed,
as no files are sent to the daemon.

If you want to improve the build-speed by excluding _some_ files from the build-
context, refer to [exclude with .dockerignore](#exclude-with-dockerignore).

> **Note**: Attempting to build a Dockerfile that uses `COPY` or `ADD` will fail
> if this syntax is used. The following example illustrates this:
> 
> ```bash
> # create a directory to work in
> mkdir example
> cd example
> 
> # create an example file
> touch somefile.txt
> 
> docker build -t myimage:latest -<<EOF
> FROM busybox
> COPY somefile.txt ./
> RUN cat /somefile.txt
> EOF
> 
> # observe that the build fails
> ...
> Step 2/3 : COPY somefile.txt ./
> COPY failed: stat /var/lib/docker/tmp/docker-builder249218248/somefile.txt: no such file or directory
> ```

#### Build from a local build context, using a Dockerfile from stdin

Use this syntax to build an image using files on your local filesystem, but using
a `Dockerfile` from `stdin`. The syntax uses the `-f` (or `--file`) option to
specify the `Dockerfile` to use, using a hyphen (`-`) as filename to instruct
Docker to read the `Dockerfile` from `stdin`:

```bash
docker build [OPTIONS] -f- PATH
```

The example below uses the current directory (`.`) as the build context, and builds
an image using a `Dockerfile` that is passed through `stdin` using a [here
document](https://tldp.org/LDP/abs/html/here-docs.html).

```bash
# create a directory to work in
mkdir example
cd example

# create an example file
touch somefile.txt

# build an image using the current directory as context, and a Dockerfile passed through stdin
docker build -t myimage:latest -f- . <<EOF
FROM busybox
COPY somefile.txt ./
RUN cat /somefile.txt
EOF
```

#### Build from a remote build context, using a Dockerfile from stdin

Use this syntax to build an image using files from a remote `git` repository, 
using a `Dockerfile` from `stdin`. The syntax uses the `-f` (or `--file`) option to
specify the `Dockerfile` to use, using a hyphen (`-`) as filename to instruct
Docker to read the `Dockerfile` from `stdin`:

```bash
docker build [OPTIONS] -f- PATH
```

This syntax can be useful in situations where you want to build an image from a
repository that does not contain a `Dockerfile`, or if you want to build with a custom
`Dockerfile`, without maintaining your own fork of the repository.

The example below builds an image using a `Dockerfile` from `stdin`, and adds
the `hello.c` file from the ["hello-world" Git repository on GitHub](https://github.com/docker-library/hello-world).

```bash
docker build -t myimage:latest -f- https://github.com/docker-library/hello-world.git <<EOF
FROM busybox
COPY hello.c ./
EOF
```

> **Under the hood**
>
> When building an image using a remote Git repository as build context, Docker 
> performs a `git clone` of the repository on the local machine, and sends
> those files as build context to the daemon. This feature requires `git` to be
> installed on the host where you run the `docker build` command.

### Exclude with .dockerignore

To exclude files not relevant to the build (without restructuring your source
repository) use a `.dockerignore` file. This file supports exclusion patterns
similar to `.gitignore` files. For information on creating one, see the
[.dockerignore file](../../engine/reference/builder.md#dockerignore-file).

### Don't install unnecessary packages

To reduce complexity, dependencies, file sizes, and build times, avoid
installing extra or unnecessary packages just because they might be "nice to
have." For example, you don’t need to include a text editor in a database image.

### Decouple applications

Each container should have only one concern. Decoupling applications into
multiple containers makes it easier to scale horizontally and reuse containers.
For instance, a web application stack might consist of three separate
containers, each with its own unique image, to manage the web application,
database, and an in-memory cache in a decoupled manner.

Limiting each container to one process is a good rule of thumb, but it is not a
hard and fast rule. For example, not only can containers be
[spawned with an init process](../../engine/reference/run.md#specify-an-init-process),
some programs might spawn additional processes of their own accord. For
instance, [Celery](https://docs.celeryproject.org/) can spawn multiple worker
processes, and [Apache](https://httpd.apache.org/) can create one process per
request.

Use your best judgment to keep containers as clean and modular as possible. If
containers depend on each other, you can use [Docker container networks](../../network/index.md)
to ensure that these containers can communicate.

### Minimize the number of layers

In older versions of Docker, it was important that you minimized the number of
layers in your images to ensure they were performant. The following features
were added to reduce this limitation:

- Only the instructions `RUN`, `COPY`, `ADD` create layers. Other instructions
  create temporary intermediate images, and do not increase the size of the build.

- Where possible, use [multi-stage builds](../../build/building/multi-stage.md),
  and only copy the artifacts you need into the final image. This allows you to
  include tools and debug information in your intermediate build stages without
  increasing the size of the final image.

### Sort multi-line arguments

Whenever possible, ease later changes by sorting multi-line arguments
alphanumerically. This helps to avoid duplication of packages and make the
list much easier to update. This also makes PRs a lot easier to read and
review. Adding a space before a backslash (`\`) helps as well.

Here’s an example from the [`buildpack-deps` image](https://github.com/docker-library/buildpack-deps):

```dockerfile
RUN apt-get update && apt-get install -y \
  bzr \
  cvs \
  git \
  mercurial \
  subversion \
  && rm -rf /var/lib/apt/lists/*
```

### Leverage build cache

When building an image, Docker steps through the instructions in your
`Dockerfile`, executing each in the order specified. As each instruction is
examined, Docker looks for an existing image in its cache that it can reuse,
rather than creating a new (duplicate) image.

If you do not want to use the cache at all, you can use the `--no-cache=true`
option on the `docker build` command. However, if you do let Docker use its
cache, it is important to understand when it can, and cannot, find a matching
image. The basic rules that Docker follows are outlined below:

- Starting with a parent image that is already in the cache, the next
  instruction is compared against all child images derived from that base
  image to see if one of them was built using the exact same instruction. If
  not, the cache is invalidated.

- In most cases, simply comparing the instruction in the `Dockerfile` with one
  of the child images is sufficient. However, certain instructions require more
  examination and explanation.

- For the `ADD` and `COPY` instructions, the contents of the file(s)
  in the image are examined and a checksum is calculated for each file.
  The last-modified and last-accessed times of the file(s) are not considered in
  these checksums. During the cache lookup, the checksum is compared against the
  checksum in the existing images. If anything has changed in the file(s), such
  as the contents and metadata, then the cache is invalidated.

- Aside from the `ADD` and `COPY` commands, cache checking does not look at the
  files in the container to determine a cache match. For example, when processing
  a `RUN apt-get -y update` command the files updated in the container
  are not examined to determine if a cache hit exists.  In that case just
  the command string itself is used to find a match.

Once the cache is invalidated, all subsequent `Dockerfile` commands generate new
images and the cache is not used.

## Dockerfile instructions

These recommendations are designed to help you create an efficient and
maintainable `Dockerfile`.

### FROM

[Dockerfile reference for the FROM instruction](../../engine/reference/builder.md#from)

Whenever possible, use current official images as the basis for your
images. We recommend the [Alpine image](https://hub.docker.com/_/alpine/) as it
is tightly controlled and small in size (currently under 6 MB), while still
being a full Linux distribution.

### RUN

[Dockerfile reference for the RUN instruction](../../engine/reference/builder.md#run)

Split long or complex `RUN` statements on multiple lines separated with
backslashes to make your `Dockerfile` more readable, understandable, and
maintainable.

#### apt-get

Probably the most common use-case for `RUN` is an application of `apt-get`.
Because it installs packages, the `RUN apt-get` command has several gotchas to
look out for.

Always combine `RUN apt-get update` with `apt-get install` in the same `RUN`
statement. For example:

```dockerfile
RUN apt-get update && apt-get install -y \
    package-bar \
    package-baz \
    package-foo  \
    && rm -rf /var/lib/apt/lists/*
```

Using `apt-get update` alone in a `RUN` statement causes caching issues and
subsequent `apt-get install` instructions fail. For example, say you have a
Dockerfile:

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y curl
```

After building the image, all layers are in the Docker cache. Suppose you later
modify `apt-get install` by adding extra package:

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y curl nginx
```

Docker sees the initial and modified instructions as identical and reuses the
cache from previous steps. As a result the `apt-get update` is _not_ executed
because the build uses the cached version. Because the `apt-get update` is not
run, your build can potentially get an outdated version of the `curl` and
`nginx` packages.

Using `RUN apt-get update && apt-get install -y` ensures your Dockerfile
installs the latest package versions with no further coding or manual
intervention. This technique is known as "cache busting". You can also achieve
cache-busting by specifying a package version. This is known as version pinning,
for example:

```dockerfile
RUN apt-get update && apt-get install -y \
    package-bar \
    package-baz \
    package-foo=1.3.*
```

Version pinning forces the build to retrieve a particular version regardless of
what’s in the cache. This technique can also reduce failures due to unanticipated changes
in required packages.

Below is a well-formed `RUN` instruction that demonstrates all the `apt-get`
recommendations.

```dockerfile
RUN apt-get update && apt-get install -y \
    aufs-tools \
    automake \
    build-essential \
    curl \
    dpkg-sig \
    libcap-dev \
    libsqlite3-dev \
    mercurial \
    reprepro \
    ruby1.9.1 \
    ruby1.9.1-dev \
    s3cmd=1.1.* \
 && rm -rf /var/lib/apt/lists/*
```

The `s3cmd` argument specifies a version `1.1.*`. If the image previously
used an older version, specifying the new one causes a cache bust of `apt-get
update` and ensures the installation of the new version. Listing packages on
each line can also prevent mistakes in package duplication.

In addition, when you clean up the apt cache by removing `/var/lib/apt/lists` it
reduces the image size, since the apt cache is not stored in a layer. Since the
`RUN` statement starts with `apt-get update`, the package cache is always
refreshed prior to `apt-get install`.

> Official Debian and Ubuntu images [automatically run `apt-get clean`](https://github.com/moby/moby/blob/03e2923e42446dbb830c654d0eec323a0b4ef02a/contrib/mkimage/debootstrap#L82-L105),
> so explicit invocation is not required.

#### Using pipes

Some `RUN` commands depend on the ability to pipe the output of one command into another, using the pipe character (`|`), as in the following example:

```dockerfile
RUN wget -O - https://some.site | wc -l > /number
```

Docker executes these commands using the `/bin/sh -c` interpreter, which only
evaluates the exit code of the last operation in the pipe to determine success.
In the example above this build step succeeds and produces a new image so long
as the `wc -l` command succeeds, even if the `wget` command fails.

If you want the command to fail due to an error at any stage in the pipe,
prepend `set -o pipefail &&` to ensure that an unexpected error prevents the
build from inadvertently succeeding. For example:

```dockerfile
RUN set -o pipefail && wget -O - https://some.site | wc -l > /number
```

> Not all shells support the `-o pipefail` option.
>
> In cases such as the `dash` shell on
> Debian-based images, consider using the _exec_ form of `RUN` to explicitly
> choose a shell that does support the `pipefail` option. For example:
>
> ```dockerfile
> RUN ["/bin/bash", "-c", "set -o pipefail && wget -O - https://some.site | wc -l > /number"]
> ```

### CMD

[Dockerfile reference for the CMD instruction](../../engine/reference/builder.md#cmd)

The `CMD` instruction should be used to run the software contained in your
image, along with any arguments. `CMD` should almost always be used in the form
of `CMD ["executable", "param1", "param2"…]`. Thus, if the image is for a
service, such as Apache and Rails, you would run something like `CMD
["apache2","-DFOREGROUND"]`. Indeed, this form of the instruction is recommended
for any service-based image.

In most other cases, `CMD` should be given an interactive shell, such as bash,
python and perl. For example, `CMD ["perl", "-de0"]`, `CMD ["python"]`, or `CMD
["php", "-a"]`. Using this form means that when you execute something like
`docker run -it python`, you’ll get dropped into a usable shell, ready to go.
`CMD` should rarely be used in the manner of `CMD ["param", "param"]` in
conjunction with [`ENTRYPOINT`](../../engine/reference/builder.md#entrypoint), unless
you and your expected users are already quite familiar with how `ENTRYPOINT`
works.

### ENV

[Dockerfile reference for the ENV instruction](../../engine/reference/builder.md#env)

To make new software easier to run, you can use `ENV` to update the
`PATH` environment variable for the software your container installs. For
example, `ENV PATH=/usr/local/nginx/bin:$PATH` ensures that `CMD ["nginx"]`
just works.

The `ENV` instruction is also useful for providing required environment
variables specific to services you wish to containerize, such as Postgres’s
`PGDATA`.

Lastly, `ENV` can also be used to set commonly used version numbers so that
version bumps are easier to maintain, as seen in the following example:

```dockerfile
ENV PG_MAJOR=9.3
ENV PG_VERSION=9.3.4
RUN curl -SL https://example.com/postgres-$PG_VERSION.tar.xz | tar -xJC /usr/src/postgres && …
ENV PATH=/usr/local/postgres-$PG_MAJOR/bin:$PATH
```

Similar to having constant variables in a program (as opposed to hard-coding
values), this approach lets you change a single `ENV` instruction to
auto-magically bump the version of the software in your container.

Each `ENV` line creates a new intermediate layer, just like `RUN` commands. This
means that even if you unset the environment variable in a future layer, it
still persists in this layer and its value can be dumped. You can test this by
creating a Dockerfile like the following, and then building it.

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
ENV ADMIN_USER="mark"
RUN echo $ADMIN_USER > ./mark
RUN unset ADMIN_USER
```

```console
$ docker run --rm test sh -c 'echo $ADMIN_USER'

mark
```

To prevent this, and really unset the environment variable, use a `RUN` command
with shell commands, to set, use, and unset the variable all in a single layer.
You can separate your commands with `;` or `&&`. If you use the second method,
and one of the commands fails, the `docker build` also fails. This is usually a
good idea. Using `\` as a line continuation character for Linux Dockerfiles
improves readability. You could also put all of the commands into a shell script
and have the `RUN` command just run that shell script.

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN export ADMIN_USER="mark" \
    && echo $ADMIN_USER > ./mark \
    && unset ADMIN_USER
CMD sh
```

```console
$ docker run --rm test sh -c 'echo $ADMIN_USER'

```


### COPY

- [Dockerfile reference for the COPY instruction](../../engine/reference/builder.md#copy)

If you have multiple `Dockerfile` steps that use different files from your
context, `COPY` them individually, rather than all at once. This ensures that
each step's build cache is only invalidated (forcing the step to be re-run) if
the specifically required files change.

For example:

```dockerfile
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY . /tmp/
```

Results in fewer cache invalidations for the `RUN` step, than if you put the
`COPY . /tmp/` before it.

For other items (files, directories) that do not require `ADD`’s tar
auto-extraction capability, you should always use `COPY`.

### VOLUME

[Dockerfile reference for the VOLUME instruction](../../engine/reference/builder.md#volume)

The `VOLUME` instruction should be used to expose any database storage area,
configuration storage, or files/folders created by your docker container. You
are strongly encouraged to use `VOLUME` for any mutable and/or user-serviceable
parts of your image.

### USER

[Dockerfile reference for the USER instruction](../../engine/reference/builder.md#user)

If a service can run without privileges, use `USER` to change to a non-root
user. Start by creating the user and group in the `Dockerfile` with something
like:

```dockerfile
RUN groupadd -r postgres && useradd --no-log-init -r -g postgres postgres
```

> Consider an explicit UID/GID
>
> Users and groups in an image are assigned a non-deterministic UID/GID in that
> the "next" UID/GID is assigned regardless of image rebuilds. So, if it’s
> critical, you should assign an explicit UID/GID.

> Due to an [unresolved bug](https://github.com/golang/go/issues/13548) in the
> Go archive/tar package's handling of sparse files, attempting to create a user
> with a significantly large UID inside a Docker container can lead to disk
> exhaustion because `/var/log/faillog` in the container layer is filled with
> NULL (\0) characters. A workaround is to pass the `--no-log-init` flag to
> useradd. The Debian/Ubuntu `adduser` wrapper does not support this flag.

Avoid installing or using `sudo` as it has unpredictable TTY and
signal-forwarding behavior that can cause problems. If you absolutely need
functionality similar to `sudo`, such as initializing the daemon as `root` but
running it as non-`root`, consider using [“gosu”](https://github.com/tianon/gosu).

Lastly, to reduce layers and complexity, avoid switching `USER` back and forth
frequently.

### WORKDIR

[Dockerfile reference for the WORKDIR instruction](../../engine/reference/builder.md#workdir)

For clarity and reliability, you should always use absolute paths for your
`WORKDIR`. Also, you should use `WORKDIR` instead of  proliferating instructions
like `RUN cd … && do-something`, which are hard to read, troubleshoot, and
maintain.
