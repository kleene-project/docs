---
title: "Configure Klee"
description: "Configure Klee"
keywords: "Klee, Klee documentation, CLI, command line, klee_config.yaml, CLI configuration file"
---

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

See [klee root command](/reference/klee/klee/) documentation for details.

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

  The IMAGE syntax is: (IMAGE_ID|IMAGE_NAME[:TAG])[@SNAPSHOT]

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
