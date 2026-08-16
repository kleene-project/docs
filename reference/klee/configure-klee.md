---
title: "Configure Klee"
description: "Configure Klee"
keywords: "Klee, Klee documentation, CLI, command line, klee_config.yaml, CLI configuration file"
---

Klee can be configured in several ways:

- Using the `klee` root command parameters, e.g., `$ klee --host /path/to/kleened.socket image ls -a`
- Using environment variables `$ KLEE_HOST="/path/to/kleened.socket" klee image ls`
- Using a configuration file that can be supplied using command line arguments, environment variables or at a default location.

Configuration parameters are selected using the following priority:

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


### Configure Klee with CLI parameters

The root command parameters can be used to configure Klee and
will override any parameters previously set in configuration files etc.

See [klee root command](/reference/klee/klee/) documentation for details.

### Configure Klee with environment variables

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

### Configure Klee with a configuration file

A Klee configuration file (if any) is found by following these steps:

1. Use the file specified by the CLI flag `--config`, if it is set.
2. Use the file specified by the environment variable `KLEE_CONFIG`, if it is set.
3. Searching for a file in the following order (and stopping the search if a file is found):
    1. `./klee_config.yaml`
    2. `~/.klee/klee_config.yaml`
    3. If on Linux, look at `/etc/klee/klee_config.yaml`. If on a *BSD system, look at `/usr/local/etc/klee/klee_config.yaml`

### Configuring visual appearance
Klee comes with to different visual themes for outputting results:

- The `fancy` theme is primarily based on Python's `rich` package and uses special unicode characters and colors when formatting output.
- The `simple` theme uses Python's `click` package for printting the help-text, and uses only ASCII-characters and little/no colors when formatting output.

The `fancy` theme is used by default.
