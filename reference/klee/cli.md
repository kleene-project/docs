---
title: "Klee, the command line tool"
description: "Klee's CLI command description and usage"
keywords: "Klee, Klee documentation, CLI, command line"
---

## Overview

To show the main help page and list available commands, run `klee` with no parameters:

```console
$ klee
Usage: klee [OPTIONS] COMMAND [ARGS]...

  CLI to interact with Kleened.

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────╮
│    --version         Show the version and exit.                                                          │
│    --config          Location of Klee config file.                                                       │
│    --theme           Theme used for Klee's output. Possible values: 'fancy' or 'simple'. Default is      │
│                      'fancy'.                                                                            │
│    --host            Host address and protocol to use. See the docs for details. If no host is defined   │
│                      anywhere, Klee uses http:///var/run/kleened.sock.                                   │
│    --tlsverify bool  Verify the server cert. Uses the CA bundle provided by Certifi unless the '--cacert'│
│                      is set.                                                                             │
│    --tlscert         Path to TLS certificate file used for client authentication (PEM encoded)           │
│    --tlskey          Path to TLS key file used for the '--tlscert' certificate (PEM encoded)             │
│    --tlscacert       Trust certs signed only by this CA (PEM encoded). Implies '--tlsverify'.            │
│    --help            Show this message and exit.                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────╮
│  container  Manage containers                                                                            │
│  image      Manage images                                                                                │
│  network    Manage networks                                                                              │
│  volume     Manage volumes                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Shortcuts ──────────────────────────────────────────────────────────────────────────────────────────────╮
│  build    Build a new image                                                                              │
│  create   Create a new container.                                                                        │
│  exec     Run a command in a container                                                                   │
│  start    Start one or more stopped containers.                                                          │
│  stop     Stop one or more running containers                                                            │
│  restart  Restart one or more containers                                                                 │
│  lsc      List containers                                                                                │
│  lsi      List images                                                                                    │
│  lsn      List networks                                                                                  │
│  lsv      List volumes                                                                                   │
│  rmc      Remove one or more containers                                                                  │
│  rmi      Remove one or more images                                                                      │
│  run      Run a command in a new container.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

The `Commands` panel list the available commands, each having their own set of subcommands.
The `Shortcuts` panel list convenient shortcuts to subcommands, e.g.,
`klee build` is a shortcut for `klee image build` and so on.

> **Note**
>
> Depending on your Klee system configuration, you may be required to prefix
> the `klee` command with `sudo`. The simples way to avoid using `sudo` with the
> `klee` command, is to make an alias `alias klee='sudo klee'`. However,
> `sudo` is still required even though it does not need to be typed explictly.
> Alternatively, expose Kleened through a TCP-socket which requires some additional
> security-considerations. Read more about this [here](/operation/protect-access/).

## Using Klee's help functionality

Printing the help page of a command is generally done by running the command without any
parameters *or* by passing the `--help` flag.

However, the subcommands `klee <command> ls` and `klee <command> prune` only support the `--help`
method since they are valid command invocations without any parameters specified.

### Example

```console
$ klee run --help
Usage: klee run [OPTIONS] IMAGE [COMMAND]...

  Run a command in a new container.

  The IMAGE syntax is: (IMAGE_ID|IMAGE_NAME[:TAG])[:@SNAPSHOT]

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────╮
│  -u  --user text    Default user used when running commands in the container. This parameter will be     │
│                     overwritten by the jail parameter exec.jail_user if it is set.                       │
│  -e  --env          Set environment variables (e.g. --env FIRST=SomeValue --env SECOND=AnotherValue)     │
│  -m  --mount list   Mount a volume/directory/file on the host filesystem into the container. Mounts are  │
│                     specfied using a --mount SOURCE:DESTINATION[:rw|ro] syntax.                          │
│  -J  --jailparam    Specify one or more jail parameters to use. If you do not want mount.devfs,          │
│                     exec.clean, and exec.stop="/bin/sh /etc/rc.shutdown" enabled, you must actively      │
│                     disable them                                                                         │
│  -P  --persist      Do not remove this container when pruning                                            │
│      --restart      Restarting policy of the container. Set to no for no automatic restart of the        │
│                     container. Set to on-startup to start the container each time Kleened is  [default:  │
│                     no]                                                                                  │
│  -l  --driver       Network driver of the container. Possible values: ipnet, host, vnet, and disabled.   │
│                     If no network and no network driver is supplied, the network driver is set to host.  │
│                     If a network is specfied but no network driver, it is set to ipnet,                  │
│  -n  --network      Connect container to this network.                                                   │
│      --ip           IPv4 address used for the container. If omitted, an unused ip is allocated from the  │
│                     IPv4 subnet of --network.                                                            │
│      --ip6          IPv6 address used for the container. If omitted, an unused ip is allocated from the  │
│                     IPv6 subnet of --network.                                                            │
│  -d  --detach       Do not output STDOUT/STDERR to the terminal. If this is set, Klee will exit and      │
│                     return the container ID when the container has been started.                         │
│  -i  --interactive  Send terminal input to container's STDIN. If set, --detach will be ignored.          │
│  -t  --tty          Allocate a pseudo-TTY                                                                │
│      --name         Assign a name to the container                                                       │
│  -p  --publish      Publish one or more ports using the syntax                                           │
│                     <HOST-PORT>[:CONTAINER-PORT][/<PROTOCOL>] or                                         │
│                     <INTERFACE>:<HOST-PORT>:<CONTAINER-PORT>[/<PROTOCOL>]. CONTAINER-PORT defaults to    │
│                     HOST-PORT and PROTOCOL defaults to 'tcp'.                                            │
│      --help         Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Using Klee options

Single character command line options can be combined, so rather than
typing `klee run -i -t --name test FreeBSD:latest /bin/sh`,
you can write `klee run -it --name test FreeBSD:latest /bin/sh`.

### Option types

Many optinons in Klee have been annotated with a *type*.
A typed option provides a convention for how it can be used,
which is described in the following.

#### Flags

Flag options take the form `-d`, `--detach`, `--tty`. Setting a flag
will enable some functionality that would be otherwise unset.
The help text describes what will happen if the flag i used.

```console
$ klee build --quiet .
```

#### Bools

Bool options are similar to flags, with the following exceptions:

- Bools can be both enabled or disabled, unlike flags that can only be enabled.
- Bools can be enabled by default.

Bool options can be disabled by using `no-` in front of the option name.
For example, if `--dns` is the enabled form, `--no-dns` means it is disabled.

#### Lists

You can specify `list` options like `--env <some value>` multiple times in a single command line,
for example in this command:

```console
$ klee run --env SOME_VAR=value1 --env SOME_OTHER_VAR=value2 FreeBSD:latest /bin/bash
```

#### Strings and Integers

Options like `--name "a_string"` expect a string, and they
can only be specified once. If the string does not contain special characters it
does not require quoting, i.e, `--name a_string`. Usually, an untyped option is
a string.

Options like `-c=0` expect an integer, and they can only be specified once.
