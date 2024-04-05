---
title: "Klee, the command line tool"
description: "Klee's CLI command description and usage"
keywords: "Klee, Klee documentation, CLI, command line"
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
