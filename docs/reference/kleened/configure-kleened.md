---
title: Kleened configuration
description: Configuring Kleene backend component
---

Kleened must be configured using the config file
`/usr/local/etc/kleened/config.yaml`.

A default configuration file is automatically installed, having the following
defaults:

```yaml
kleene_root: "zroot/kleene"
pf_config_template_path: "/usr/local/etc/kleened/pf.conf.kleene"
pf_config_path: "/etc/pf.conf"
api_listening_sockets:
    - address: "http:///var/run/kleened.sock"
enable_logging: true
log_level: "info"
```

where

- `kleene_root`: The root dataset of Kleened where all containers, volumes, images,
  and the metadata database `metadata.sqlite` file are stored.

- `pf_config_template_path`: Location of the template file used by Kleened to
  generate the firewall configuration file `pf.conf(5)`.

- `pf_config_path`: Location of the generated `pf.conf(5)` file that is loaded into
  the `pf(4)` firewall. Before Kleene overwrites a file at this location that it
  did not generate itself, the existing file is backed up next to it with a
  `.kleene.bak` suffix. See the [firewall configuration](../../guides/network/firewall.md) section
  for details.

- `api_listening_sockets`: List of listening sockets for exposing the HTTP API.
  The general format for specifying socket types and TLS-parameters is described
  below.

- `enable_logging`: Whether or not enable logging to `/var/log/kleened.log`.

- `log_level`: Logging verbosity. A message is logged if it is `log_level` or more
  severe. Values ordered by verbosity are: `debug`, `info`, `notice`, `warning`,
  `error`, `critical`, `alert`, and `emergency`.

## Additional logging configuration

Kleened's logging is built on the logger that ships with Erlang/OTP (Elixir's
`Logger` calls feed into it). `enable_logging` and `log_level` are the only
kleened-specific options; the behaviour around them is standard OTP logger
behaviour.

### Log file and rotation

With `enable_logging: true`, kleened writes to `/var/log/kleened.log`. The
location is fixed and cannot be changed from the configuration file.

Rotation is built into the logging itself, independent of newsyslog(8): the
log is rotated when it reaches 10 MB, and the five most recent rotated files
are kept. The handler also re-checks the log file every five seconds, so
rotating it with newsyslog(8) instead works as well.

### Setting the log level at boot

`log_level` is applied while the daemon reads its configuration at startup.
To control logging even earlier — for example to quiet boot-time messages
while debugging a daemon that fails before the configuration is read — set
the primary log level with the kernel's `logger_level` parameter:

```sh
ERL_AFLAGS="-kernel logger_level warning" service kleened start
```

When kleened runs from the FreeBSD port, the variable belongs in
`kleened_env` in `/etc/rc.conf`. Note that `kleened_env` replaces its default
value, so keep the `PATH` and `LANG` entries from the default when setting it.
Once the configuration file has been read, `log_level` overrides the
boot-time level.

The log format and logging handlers cannot be customized from kleened's
configuration file; see the [OTP logger
documentation](https://www.erlang.org/doc/apps/kernel/logger) for what can be
done with the underlying system.

## Specifying listening sockets

Each socket is specified by an `address` field using the format:

- `http[s]://ip4|ip6[:port]` for TCP-sockets

- `http[s]:///path/to/unix_socket` for UNIX-sockets. Existing sockets/files will
  be overwritten.

In case `https` is used, there are additional parameters for configuring TLS:

- `tlscert` (mandatory): Path to the PEM encoded certificate file. May also contain the private key.
- `tlskey` (mandatory): Path to the PEM encoded private key file, if not
  contained in `tlscert` file.

- `tlsverify`: Set to `true` to request a certificate from the client. Defaults to `false`.

- `tlscacert`: Path to file containing PEM encoded trusted CA certificates used
  to verify client certificates when `tlsverify` is set to `true`.

- `tlsdh`: Path to the PEM encoded Diffie-Hellman (DH) parameters file.

All TLS-parameters are ignored if TLS i not used.

A few examples of different listening socket configurations:

```yaml
api_listening_sockets:
    # IPv4 TCP-socket using TLS _with_ client authentication and DH-parameters
    - address: "https://127.0.0.1:8085"
      tlscert: "/usr/local/etc/kleened/certs/server-cert.pem"
      tlskey: "/usr/local/etc/kleened/certs/server-key.pem"
      tlsverify: true
      tlscacert: "/usr/local/etc/kleened/certs/ca.pem"
      tlsdh: "/usr/local/etc/kleened/certs/dhparams.pem"

    # UNIX-socket using TLS _without_ client authentication and no DH-parameters
    - address: "https:///var/run/kleened.tlssock"
      tlscert: "/usr/local/etc/kleened/certs/server-cert.pem"
      tlskey: "/usr/local/etc/kleened/certs/server-key.pem"
      tlsverify: false
      tlscacert: "/usr/local/etc/kleened/certs/ca.pem"

    # UNIX-socket without TLS without
    - address: "http:///var/run/kleened.sock"

    # TCP IPv6 socket (localhost) without TLS
    - address: "http://[::1]:8080/"
```
