---
title: klee shortcut commands
description: One-line shortcuts for the most common klee commands
---

Many `klee` subcommands have a short form. Any command that manipulates a
specific object type (containers, images, networks, volumes) can be spelled
as `klee <shortcut>` instead of `klee <object> <verb>` — for example,
`klee lsc` instead of `klee container ls`.

| Shortcut | Long form |
|---|---|
| [`klee build`](build.md) | `klee image build` |
| [`klee create`](create.md) | `klee container create` |
| [`klee exec`](exec.md) | `klee container exec` |
| [`klee run`](run.md) | `klee container run` |
| [`klee start`](start.md) | `klee container start` |
| [`klee stop`](stop.md) | `klee container stop` |
| [`klee restart`](restart.md) | `klee container restart` |
| [`klee isc`](isc.md) | `klee container inspect` |
| [`klee lsc`](lsc.md) | `klee container ls` |
| [`klee rmc`](rmc.md) | `klee container rm` |
| [`klee isi`](isi.md) | `klee image inspect` |
| [`klee lsi`](lsi.md) | `klee image ls` |
| [`klee rmi`](rmi.md) | `klee image rm` |
| [`klee isn`](isn.md) | `klee network inspect` |
| [`klee lsn`](lsn.md) | `klee network ls` |
| [`klee rmn`](rmn.md) | `klee network rm` |
| [`klee isv`](isv.md) | `klee volume inspect` |
| [`klee lsv`](lsv.md) | `klee volume ls` |
| [`klee rmv`](rmv.md) | `klee volume rm` |

Every shortcut also has a reference page of its own (linked above), and the
[full command reference](cli.md) lists every `klee` command.
