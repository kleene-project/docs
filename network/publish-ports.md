---
title: Publishing ports
description: How to expose services to the outside world
keywords: networking, container, standalone
---

FIXME: From Docker:
By default, when you create or run a container using `docker create` or `docker run`,
the container doesn't expose any of it's ports to the outside world.
To make a port available to services outside of Docker,
or to Docker containers running on a different network,
use the `--publish` or `-p` flag.
This creates a firewall rule in the container,
mapping a container port to a port on the Docker host to the outside world.
Here are some examples:

| Flag value                      | Description                                                                                                                                           |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-p 8080:80`                    | Map TCP port 80 in the container to port `8080` on the Docker host.                                                                                   |
| `-p 192.168.1.100:8080:80`      | Map TCP port 80 in the container to port `8080` on the Docker host for connections to host IP `192.168.1.100`.                                        |
| `-p 8080:80/udp`                | Map UDP port 80 in the container to port `8080` on the Docker host.                                                                                   |
| `-p 8080:80/tcp -p 8080:80/udp` | Map TCP port 80 in the container to TCP port `8080` on the Docker host, and map UDP port `80` in the container to UDP port `8080` on the Docker host. |


