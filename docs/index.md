---
description: Home page for Kleene's documentation
title: Kleene Documentation
hide:
  - toc
  - navigation
---

# ![](assets/images/kleene-logo.svg){ .title-logo } Kleene Documentation

Kleene is a container management tool for FreeBSD, similar to Docker but using
FreeBSD jails, ZFS and PF.

*Kleene is under active development. See the [project status](project/status.md).*

## Pick your path

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } **Install Kleene**

    ---

    Install Kleened and Klee from packages, ports or source.

    [:octicons-arrow-right-24: Install Kleene](get-started/install.md)

-   :material-school:{ .lg .middle } **Get started**

    ---

    Containerize an application, persist its data, connect containers
    together — a step-by-step introduction to Kleene.

    [:octicons-arrow-right-24: Start the tutorial](get-started/tutorial/index.md)

-   :material-package-variant-closed:{ .lg .middle } **Build images**

    ---

    Write a Dockerfile, understand the build context, and keep images small.

    [:octicons-arrow-right-24: Building images](guides/build/index.md)

-   :material-play-box-outline:{ .lg .middle } **Run containers**

    ---

    Start containers in the foreground or detached, constrain their
    resources, and tune them with jail parameters.

    [:octicons-arrow-right-24: Running containers](guides/run/index.md)

-   :material-lan:{ .lg .middle } **Networking**

    ---

    `ipnet`, `vnet` and `host` networking, published ports, and the
    firewall rules Kleene manages for you.

    [:octicons-arrow-right-24: Networking](guides/network/index.md)

-   :material-book-open-variant:{ .lg .middle } **Reference**

    ---

    Every `klee` command, the Kleened REST API, and the Dockerfile syntax
    Kleene implements.

    [:octicons-arrow-right-24: Read the reference](reference/index.md)

</div>

## Kleene in 60 seconds

=== "Install"

    ```console
    # pkg install kleene-daemon kleene-cli
    # sysrc kleened_enable=yes
    # service kleened init
    # service kleened start
    ```

=== "First container"

    Download a FreeBSD base image and run a command in a container:

    ```console
    $ klee image create fetch-auto
    ...
    Succesfully extracted binaries, creating image...
    Created image from the automatically detected version: FreeBSD-15.1-RELEASE-p3 amd64.

    image created
    a1041764afd3
    $ klee run FreeBSD-15.1-RELEASE-p3:latest echo hello
    ffd0f89c3259
    created execution instance 665e02ab151a
    hello

    executable 665e02ab151a and its container exited with exit-code 0
    ```

=== "Build an image"

    Describe an image in a `Dockerfile` and build it with `klee build`:

    ```dockerfile
    FROM FreeBSD-15.1-RELEASE-p3:latest
    RUN pkg bootstrap -y && pkg install -y git
    CMD ["/bin/sh"]
    ```

    ```console
    $ klee build -t hello .
    Step 1/3 : FROM FreeBSD-15.1-RELEASE-p3:latest
    Step 2/3 : RUN pkg bootstrap -y && pkg install -y git
    ...
    --> Snapshot created: @8b08f14cffdc
    Step 3/3 : CMD ["/bin/sh"]

    image created
    71a0ef0fee7d
    ```

## Coming from Docker?

Kleene defines itself relative to Docker. Most concepts map directly, but
Kleene runs full FreeBSD userlands in jails backed by ZFS, has no image
registry, and implements a subset of the Dockerfile instructions. See
[Kleene for Docker users](get-started/docker-users.md) for the full picture.

| Docker | Kleene |
|---|---|
| `docker ps -a` | [`klee lsc -a`](reference/klee/lsc.md) |
| `docker images` | [`klee lsi`](reference/klee/lsi.md) |
| `docker run` | [`klee run`](reference/klee/run.md) |
| `docker build` | [`klee build`](reference/klee/build.md) |
| `docker exec` | [`klee exec`](reference/klee/exec.md) |
| `docker network create` | [`klee network create`](reference/klee/network_create.md) |
| `docker volume create` | [`klee volume create`](reference/klee/volume_create.md) |
| bind mount `-v /host:/ctr` | [`klee run --mount /host:/ctr`](reference/klee/container_run.md) |
| `docker compose` | no equivalent |

## Common tasks

| Task | Page |
|---|---|
| Publish a port | [Networking: publish ports](guides/network/publish-ports.md) |
| Mount a host directory | [Storage: nullfs mounts](guides/storage/nullfs-mounts.md) |
| Persist data in a volume | [Storage: volumes](guides/storage/volumes.md) |
| Start containers at boot | [Running: start automatically](guides/run/autostart.md) |
| Set jail parameters | [Running: jail parameters](guides/run/jail-parameters.md) |
| Limit CPU and memory | [Running: resource constraints](guides/run/resource-constraints.md) |
| Create a base image | [Building: base images](guides/build/base-images.md) |
| Protect the Kleened socket | [Operating: protect the Kleened socket](guides/operate/protect-access.md) |
| Customize the firewall | [Networking: firewall](guides/network/firewall.md) |
| Troubleshoot networking | [Networking: troubleshooting](guides/network/troubleshoot.md) |

## Community, FreeBSD and contributing

<div class="grid" markdown>

- **Community**

    — GitHub: <https://github.com/kleene-project>
    — IRC: **#kleene** on Libera Chat
    — Mastodon: post with the **@kleene** tag

- **Learn FreeBSD**

    — [FreeBSD Handbook](https://docs.freebsd.org/en/books/handbook/)
    — [FreeBSD man pages](https://man.freebsd.org/)
    — [Get FreeBSD](https://www.freebsd.org/where/)

- **Contribute**

    — [Contribute to Kleene's docs](project/contribute/index.md)
    — [Project status and roadmap](project/status.md)

</div>
