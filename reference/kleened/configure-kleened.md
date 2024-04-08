---
title: Kleened configuration
description: Configuring Kleene backend component
keywords: kleene, daemon, kleened, configuration, troubleshooting
---

Kleened must be configured using a config file at
`/usr/local/etc/kleened/config.yaml`. A default configuration file is automatically
installed if Kleened were installed using `pkg` or ports. The default `config.yaml`
file contains these default values:

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

- `kleene_root`: The root dataset where Kleened stores all containers, volumes, images,
  and the metadata database `metadata.sqlite` file.

- `pf_config_template_path`: Location of the template file used by Kleened to
  generate the firewall configuration file `pf.conf(5)`.

- `pf_config_path`: Location of the generated `pf.conf(5)` file that is loaded into
  the `pf(4)` firewall. See the [firewall configuration](/run/network/firewall) section
  for details.

- `api_listening_sockets`: List of listening sockets for exposing the HTTP API.
  The general format for specifying socket types and TLS-parameters is described
  below.

- `enable_logging`: Whether or not enable logging to `/var/log/Kleened.log`.

- `log_level`: Logging verbosity. Values ordered by vebosity are: `debug`, `info`,
  `notice`, `warning`, `error`, and `critical`. Advanced configuration options
  that comes with the Erlang/Elixir logging backend are given below.

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

## Additional logging configuration

FIXME: TBD
