---
title: "Klee, the command line tool"
description: "Klee's CLI command description and usage"
keywords: "Klee, Klee documentation, CLI, command line, klee_config.yaml, CLI configuration file"
---

# Overview

To show the main help page and list available commands, run `klee` with no parameters:

```console
$ klee
sage: klee [OPTIONS] COMMAND [ARGS]...

  CLI to interact with Kleened.

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│    --version    Show the version and exit.                                                                        │
│    --config     Location of Klee config file.                                                                     │
│    --theme      Theme used for Klee's output. Possible values: 'fancy' or 'simple'. Default is 'fancy'.           │
│    --host       Host address and protocol to use. See the docs for details.                                       │
│    --tlsverify  Verify the server cert. Uses the CA bundle provided by Certifi unless the '--cacert' is set.      │
│    --tlscert    Path to TLS certificate file used for client authentication (PEM encoded)                         │
│    --tlskey     Path to TLS key file used for the '--tlscert' certificate (PEM encoded)                           │
│    --tlscacert  Trust certs signed only by this CA (PEM encoded). Implies '--tlsverify'.                          │
│    --help       Show this message and exit.                                                                       │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│  container  Manage containers                                                                                     │
│  image      Manage images                                                                                         │
│  network    Manage networks                                                                                       │
│  volume     Manage volumes                                                                                        │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Shortcuts ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│  build    Build a new image                                                                                       │
│  create   Create a new container.                                                                                 │
│  exec     Run a command in a container                                                                            │
│  lsc      List containers                                                                                         │
│  lsi      List images                                                                                             │
│  restart  Restart one or more containers                                                                          │
│  rmc      Remove one or more containers                                                                           │
│  rmi      Remove one or more images                                                                               │
│  run      Run a command in a new container.                                                                       │
│  start    Start one or more stopped containers.                                                                   │
│  stop     Stop one or more running containers                                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

The `Commands` panel list the available commands having each their on set of subcommands.
The following `Shortcuts` panel list convenient shortcuts to certain subcommands, e.g.,
`klee build` is a shortcut for `klee image build` and so on.

Printing the help pages of specific subcommands can be done by running the command without any parameters or
by passing the `--help` flag.

> **Note**
>
> The subcommands `klee <command> ls` and `klee <command> prune` only support the `--help` method
> since they are valid commands without parameters.

Depending on your Klee system configuration, you may be required to prefix
each `klee` command with `sudo`. To avoid having to use `sudo` with the
`klee` command, you have several possibilities. The simple one is to make an
alias `alias klee='sudo klee'`, however, that might come with some disadvantages.

For more information about approaches to avoid using `sudo`, refer to
the [Kleened post-installation](/install/kleened/#post-installation) instructions.

## Configuring Klee
Klee can be configured in several ways:

- Using the `klee` root command parameters, e.g., `$ klee --host /path/to/kleened.socket klee image ls -a`
- Using environment variables `$ KLEE_HOST="/path/to/kleened.socket" klee image ls`
- Using configuration files supplied through command line arguments, environment variables or at a default location.

Configuration parameters have the following priority:

1. Command line parameters for the root `klee` command.
2. Environment variables.
3. The configuration file.

Thus, command line parameters override environment variables and environment
variables override properties specified in the `klee_config.yaml` file.
If no configuration is set using any of these methods, Klee will rely on its defaults.

For example

```console
$ KLEE_HOST="http:///var/run/kleened.sock" klee --host "http://127.0.0.1" image ls
```

makes Klee connect to `http://127.0.0.1`.


### Configure with `klee` parameters
The root command parameters can be used to configure Klee and
will override any parameters previously set in configuration files etc.

See [klee root command](/engine/reference/commandline/klee/) documentation for details.

### Configure using the `klee_config.yaml` file

A Klee configuration file (if any) is found by following these steps and stopping when a file is found:

1. Use the file specified by the CLI flag `--config`, if it is set.
2. Use the file specified by the environment variable `KLEE_CONFIG`, if it is set.
3. Searching for a file the following order (and stopping the search if a file is found):
    1. `klee_config.yaml` in the current directory
    2. `~/.klee/klee_config.yaml`, i.e., a directory called `.klee` within in the home directory.
    3. If on Linux, also look at `/etc/klee/klee_config.yaml`. If on a *BSD system, look at `/usr/local/etc/klee/klee_config.yaml`.

### Configure using environment variables
You can modify the `klee` command behavior using environment variables.
The following list shows the environment variables that are supported by Klee:

| Variable          | CLI flag      | Description                                                                                                                             |
| ----------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `KLEE_CONFIG`     | `--config`    | Alternative location of the client configuration file.                                                                                  |
| `KLEE_THEME`      | `--theme`     | Visual theme used for outputting results of commands, etc.                                                                              |
| `KLEE_HOST`       | `--host`      | `kleened` socket to connect to. Klee uses `http:///var/run/kleened.sock` as default.                                                    |
| `KLEE_TLS_VERIFY` | `--tlsverify` | When set, Klee uses TLS and verifies the remote. Uses the CA bundle provided by `Certifi` Python package, unless the `--cacert` is set. |
| `KLEE_TLS_CACERT` | `--tlscacert` | Trust certs signed only by this CA (PEM encoded). Implies `--tlsverify`.                                                                |
| `KLEE_TLS_CERT`   | `--tlscert`   | Path to TLS certificate file used for client authentication (PEM encoded)                                                               |
| `KLEE_TLS_KEY`    | `--tlskey`    | Path to TLS key file used for the `--tlscert` certificate (PEM encoded)                                                                 |

### Configuring visual appearance
Klee comes with to different visual themes for outputting results:

- The `fancy` theme is primarily based on Python's `rich` package and uses special unicode characters and colors when formatting output.
- The `simple` theme uses Python's `click` package for printting the help-text, and uses only ASCII-characters and little/no colors when formatting output.

The `fancy` theme is used by default.

## Examples
### Display help text

To list the help on any command just execute the command, followed by the
`--help` option.

```console
$ klee run --help
Usage: klee run [OPTIONS] IMAGE [COMMAND]...
                                                                                                                       
  Run a command in a new container.                                                                                    
                                                                                                                       
  The IMAGE syntax is: (IMAGE_ID|IMAGE_NAME[:TAG])[:@SNAPSHOT]                                                         
                                                                                                                       
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│      --name         Assign a name to the container                                                                  │
│  -u  --user         Alternate user that should be used for starting the container. This parameter will be           │
│                     overwritten by the jail parameter exec.jail_user if it is set.                                  │
│  -n  --network      Connect a container to a network                                                                │
│      --ip           IPv4 address (e.g., 172.30.100.104). If the '--network' parameter is not set '--ip' is          │
│                     ignored.                                                                                        │
│  -m  --mount list   Mount a volume/directory/file on the host filesystem into the container. Mounts are specfied    │
│                     using a --mount <source>:<destination>[:rw|ro] syntax.                                          │
│  -e  --env          Set environment variables (e.g. --env FIRST=env --env SECOND=env)                               │
│  -J  --jailparam    Specify one or more jail parameters to use. See the jail(8) man-page for details. If you do     │
│                     not want exec.clean and mount.devfs enabled, you must actively disable them.  [default:         │
│                     mount.devfs]                                                                                    │
│  -d  --detach flag  Whether or not to attach to STDOUT/STDERR. If this is set, Klee will exit and return the        │
│                     container ID when the container has been started.                                               │
│  -i  --interactive  Send terminal input to container's STDIN. If set, --detach will be ignored.                     │
│  -t  --tty          Allocate a pseudo-TTY                                                                           │
│      --help         Show this message and exit.                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Option types

Single character command line options can be combined, so rather than
typing `klee run -i -t --name test FreeBSD-13.1-RELEASE /bin/sh`,
you can write `klee run -it --name test FreeBSD-13.1-RELEASE /bin/sh`.

#### Flags

Flag parameters take the form `-d`, `--detach`, `--tty`. Setting a flag
will enable some functionality that would be otherwise unset.
The help text describes what will happen if the flag i used.

```console
$ klee build --quiet .
```

#### Lists

You can specify `list` options like `--env <some value>` multiple times in a single command line,
for example in these commands:

```console
$ klee run --env SOME_VAR=value1 --env SOME_OTHER_VAR=value2 FreeBSD-13.1-RELEASE /bin/bash
```

#### Strings and Integers

Options like `--name "a_string"` expect a string, and they
can only be specified once. If the string does not contain special characters it
does not require quoting, i.e, `--name a_string`.

Options like `-c=0` expect an integer, and they can only be specified once.
