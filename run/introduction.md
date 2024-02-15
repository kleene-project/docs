---
description: "Configure containers at runtime"
keywords: "docker, run, configure, runtime"
redirect_from:
- /reference/run/
---

<!-- This file is maintained within the docker/cli GitHub
     repository at https://github.com/docker/cli/. Make all
     pull requests against that repo. If you see this file in
     another repository, consider it read-only there, as it will
     periodically be overwritten by the definitive file. Pull
     requests which include edits to this file in other repositories
     will be rejected.
-->

# Docker run reference

Docker runs processes in isolated containers. A container is a process
which runs on a host. The host may be local or remote. When an operator
executes `docker run`, the container process that runs is isolated in
that it has its own file system, its own networking, and its own
isolated process tree separate from the host.

This page details how to use the `docker run` command to define the
container's resources at runtime.

## General form

The basic `docker run` command takes this form:

    $ docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]

The `docker run` command must specify an [*IMAGE*](https://docs.docker.com/glossary/#image)
 to derive the container from. An image developer can define image
defaults related to:

 * detached or foreground running
 * container identification
 * network settings
 * runtime constraints on CPU and memory

With the `docker run [OPTIONS]` an operator can add to or override the
image defaults set by a developer. And, additionally, operators can
override nearly all the defaults set by the Docker runtime itself. The
operator's ability to override image and Docker runtime defaults is why
[*run*](commandline/run.md) has more options than any
other `docker` command.

To learn how to interpret the types of `[OPTIONS]`, see
[*Option types*](commandline/cli.md#option-types).

> **Note**
>
> Depending on your Docker system configuration, you may be
> required to preface the `docker run` command with `sudo`. To avoid
> having to use `sudo` with the `docker` command, your system
> administrator can create a Unix group called `docker` and add users to
> it. For more information about this configuration, refer to the Docker
> installation documentation for your operating system.


## Operator exclusive options

Only the operator (the person executing `docker run`) can set the
following options.

 - [Detached vs foreground](#detached-vs-foreground)
     - [Detached (-d)](#detached--d)
     - [Foreground](#foreground)
 - [Container identification](#container-identification)
     - [Name (--name)](#name---name)
     - [PID equivalent](#pid-equivalent)
 - [IPC settings (--ipc)](#ipc-settings---ipc)
 - [Network settings](#network-settings)
 - [Restart policies (--restart)](#restart-policies---restart)
 - [Clean up (--rm)](#clean-up---rm)
 - [Runtime constraints on resources](#runtime-constraints-on-resources)
 - [Runtime privilege and Linux capabilities](#runtime-privilege-and-linux-capabilities)

## Detached vs foreground

When starting a Docker container, you must first decide if you want to
run the container in the background in a "detached" mode or in the
default foreground mode:

    -d=false: Detached mode: Run container in the background, print new container id

### Detached (-d)

To start a container in detached mode, you use `-d=true` or just `-d` option.

FIXME: Describe how jailed-processes exits vs. when the entire jail is shutting down (e.g., when /etc/rc exists the jail is still running)

To reattach to a detached container, use `docker`
[*attach*](commandline/attach.md) command.

### Foreground

In foreground mode (the default when `-d` is not specified), `docker
run` starts the process in the container and attach the console to
the process's standard output, standard error, and optionally standard input.
It can even pretend to be a TTY (this is what most command line executables expect).
This can be configured with:

    -t              : Allocate a pseudo-tty
    -i              : Redirect terminal STDIN to STDIN of the containerized process

For interactive processes (like a shell), you must use `-i -t` together in
order to allocate a tty for the container process. `-i -t` is often written `-it`
as you'll see in later examples.

> **Note**
>
> Pseudo-TTY allocation and STDIN-redirection are limited in functionality and cannot, for instance,
> proxy signals and send single keystrokes to STDIN. While the limited functionality might suffice
> in many cases it does mean that some features, such as tab-completion in a shell, does not work.
> If, e.g., a fully functional shell is needed, consider using FreeBSD's own `jexec(8)` instead.


## Container identification

### Name (--name)

The operator can identify a container in three ways:

| Identifier type       | Example value                                                      |
|:----------------------|:-------------------------------------------------------------------|
| UUID long identifier  | "f78375b1c487e03c9438c729345e54db9d20cfa2ac1fc3494b6eb60872e74778" |
| UUID short identifier | "f78375b1c487"                                                     |
| Name                  | "evil_ptolemy"                                                     |

The UUID identifiers come from the Docker daemon. If you do not assign a
container name with the `--name` option, then the daemon generates a random
string name for you. Defining a `name` can be a handy way to add meaning to a
container. If you specify a `name`, you can use it  when referencing the
container within a Docker network. This works for both background and foreground
Docker containers.

### Image identification

FIXME This notation needs to be explained.: `image_id|[image_name[:tag]][@snapshot]`


### Example: run htop inside a container

Create this Dockerfile:

```dockerfile
FROM FreeBSD:13-STABLE
RUN pkg install -y htop
CMD ["htop"]
```

Build the Dockerfile and tag the image as `myhtop`:

```console
$ docker build -t myhtop .
```

Use the following command to run `htop` inside a container:

```console
$ docker run -it --rm myhtop
```

## Network settings

    --network="bridge" : Connect a container to a network
    --ip=""            : Sets the container's Ethernet device's IPv4 address

By default, containers have no networking enabled so they can't make any
outgoing connections. If connectivity is needed, a network needs to specified
(and created beforehand).

See the [networking](/network/) section of the Kleene handbook for details on how
to create networks.

## Restart policies (--restart)

Using the `--restart` flag on Docker run you can specify a restart policy for
how a container should or should not be restarted on exit.

When a restart policy is active on a container, it will be shown as either `Up`
or `Restarting` in [`docker ps`](commandline/ps.md). It can also be
useful to use [`docker events`](commandline/events.md) to see the
restart policy in effect.

Docker supports the following restart policies:

<table>
  <thead>
    <tr>
      <th>Policy</th>
      <th>Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>no</strong></td>
      <td>
        Do not automatically restart the container when it exits. This is the
        default.
      </td>
    </tr>
    <tr>
      <td>
        <span style="white-space: nowrap">
          <strong>on-failure</strong>[:max-retries]
        </span>
      </td>
      <td>
        Restart only if the container exits with a non-zero exit status.
        Optionally, limit the number of restart retries the Docker
        daemon attempts.
      </td>
    </tr>
    <tr>
      <td><strong>always</strong></td>
      <td>
        Always restart the container regardless of the exit status.
        When you specify always, the Docker daemon will try to restart
        the container indefinitely. The container will also always start
        on daemon startup, regardless of the current state of the container.
      </td>
    </tr>
    <tr>
      <td><strong>unless-stopped</strong></td>
      <td>
        Always restart the container regardless of the exit status,
        including on daemon startup, except if the container was put
        into a stopped state before the Docker daemon was stopped.
      </td>
    </tr>
  </tbody>
</table>

An increasing delay (double the previous delay, starting at 100 milliseconds)
is added before each restart to prevent flooding the server.
This means the daemon will wait for 100 ms, then 200 ms, 400, 800, 1600,
and so on until either the `on-failure` limit, the maximum delay of 1 minute is
hit, or when you `docker stop` or `docker rm -f` the container.

If a container is successfully restarted (the container is started and runs
for at least 10 seconds), the delay is reset to its default value of 100 ms.

You can specify the maximum amount of times Docker will try to restart the
container when using the **on-failure** policy. The default is that Docker
will try forever to restart the container. The number of (attempted) restarts
for a container can be obtained via [`docker inspect`](commandline/inspect.md). For example, to get the number of restarts
for container "my-container";

```console
{% raw %}
$ docker inspect -f "{{ .RestartCount }}" my-container
# 2
{% endraw %}
```

Or, to get the last time the container was (re)started;

```console
{% raw %}
$ docker inspect -f "{{ .State.StartedAt }}" my-container
# 2015-03-04T23:47:07.691840179Z
{% endraw %}
```

Combining `--restart` (restart policy) with the `--rm` (clean up) flag results
in an error. On container restart, attached clients are disconnected. See the
examples on using the [`--rm` (clean up)](#clean-up---rm) flag later in this page.

## Runtime constraints on resources

FIXME: Describe the possible ways of constratining container resources using `rctl(8)` + `jail`-params (especiall `persist`) + `devfs.conf/devfs.rules`


## Overriding Dockerfile image defaults

When a developer builds an image from a [*Dockerfile*](builder.md)
or when she commits it, the developer can set a number of default parameters
that take effect when the image starts up as a container.

Four of the Dockerfile commands cannot be overridden at runtime: `FROM`,
`MAINTAINER`, `RUN`, and `ADD`. Everything else has a corresponding override
in `docker run`. We'll go through what the developer might have set in each
Dockerfile instruction and how the operator can override that setting.

 - [CMD (Default Command or Options)](#cmd-default-command-or-options)
 - [ENV (Environment Variables)](#env-environment-variables)
 - [VOLUME (Shared Filesystems)](#volume-shared-filesystems)
 - [USER](#user)
 - [WORKDIR](#workdir)

### CMD (default command or options)

Recall the optional `COMMAND` in the Docker
commandline:

```console
$ docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]
```

This command is optional because the person who created the `IMAGE` may
have already provided a default `COMMAND` using the Dockerfile `CMD`
instruction. As the operator (the person running a container from the
image), you can override that `CMD` instruction just by specifying a new
`COMMAND`.

If the image also specifies an `ENTRYPOINT` then the `CMD` or `COMMAND`
get appended as arguments to the `ENTRYPOINT`.

### ENV (environment variables)

Docker automatically sets some environment variables when creating a Linux
container. Docker does not set any environment variables when creating a Windows
container.

The following environment variables are set for Linux containers:

| Variable   | Value                                                                                                |
|:-----------|:-----------------------------------------------------------------------------------------------------|
| `HOME`     | Set based on the value of `USER`                                                                     |
| `HOSTNAME` | The hostname associated with the container                                                           |
| `PATH`     | Includes popular directories, such as `/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin` |
| `TERM`     | `xterm` if the container is allocated a pseudo-TTY                                                   |


Additionally, the operator can **set any environment variable** in the
container by using one or more `-e` flags, even overriding those mentioned
above, or already defined by the developer with a Dockerfile `ENV`. If the
operator names an environment variable without specifying a value, then the
current value of the named variable is propagated into the container's environment:

```console
$ export today=Wednesday
$ docker run -e "deep=purple" -e today --rm alpine env

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=d2219b854598
deep=purple
today=Wednesday
HOME=/root
```

Similarly the operator can set the **HOSTNAME** (Linux) or **COMPUTERNAME** (Windows) with `-h`.

### VOLUME (shared filesystems)

    -v, --volume=[host-src:]container-dest[:<options>]: Bind mount a volume.
    The comma-delimited `options` are [rw|ro], [z|Z],
    [[r]shared|[r]slave|[r]private], and [nocopy].
    The 'host-src' is an absolute path or a name value.

    If neither 'rw' or 'ro' is specified then the volume is mounted in
    read-write mode.

    The `nocopy` mode is used to disable automatically copying the requested volume
    path in the container to the volume storage location.
    For named volumes, `copy` is the default mode. Copy modes are not supported
    for bind-mounted volumes.

    --volumes-from="": Mount all volumes from the given container(s)

> **Note**
>
> When using systemd to manage the Docker daemon's start and stop, in the systemd
> unit file there is an option to control mount propagation for the Docker daemon
> itself, called `MountFlags`. The value of this setting may cause Docker to not
> see mount propagation changes made on the mount point. For example, if this value
> is `slave`, you may not be able to use the `shared` or `rshared` propagation on
> a volume.

The volumes commands are complex enough to have their own documentation
in section [*Use volumes*](https://docs.docker.com/storage/volumes/). A developer can define
one or more `VOLUME`'s associated with an image, but only the operator
can give access from one container to another (or from a container to a
volume mounted on the host).

The `container-dest` must always be an absolute path such as `/src/docs`.
The `host-src` can either be an absolute path or a `name` value. If you
supply an absolute path for the `host-src`, Docker bind-mounts to the path
you specify. If you supply a `name`, Docker creates a named volume by that `name`.

A `name` value must start with an alphanumeric character,
followed by `a-z0-9`, `_` (underscore), `.` (period) or `-` (hyphen).
An absolute path starts with a `/` (forward slash).

For example, you can specify either `/foo` or `foo` for a `host-src` value.
If you supply the `/foo` value, Docker creates a bind mount. If you supply
the `foo` specification, Docker creates a named volume.

### USER

`root` (id = 0) is the default user within a container. The image developer can
create additional users. Those users are accessible by name.  When passing a numeric
ID, the user does not have to exist in the container.

The developer can set a default user to run the first process with the
Dockerfile `USER` instruction. When starting a container, the operator can override
the `USER` instruction by passing the `-u` option.

    -u="", --user="": Sets the username or UID used and optionally the groupname or GID for the specified command.

    The followings examples are all valid:
    --user=[ user | user:group | uid | uid:gid | user:gid | uid:group ]

> **Note:** if you pass a numeric uid, it must be in the range of 0-2147483647.

### WORKDIR

The default working directory for running binaries within a container is the
root directory (`/`). It is possible to set a different working directory with the
Dockerfile `WORKDIR` command. The operator can override this with:

    -w="", --workdir="": Working directory inside the container
