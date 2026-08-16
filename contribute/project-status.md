---
title: Project status
description: Kleene project status and roadmap
keywords: kleene, project, documentation, status, roadmap
---

The Kleene project has recently been released, and while it offers a complete
set of features for managing containers on FreeBSD, it is *not* a mature piece of
software ready for production. However, it *is* ready for testing and
experimentation on non-critical infrastructure.
Testing of Kleene is now paramount in maturing the software.

Feature-wise, Kleene can be considered a minimal version of Docker, with Dockerfiles,
images containers, volumes, and networks.
Most of the present functionality should not be subject to major changes, but tweaks
and minor additions should be expected.

Major features not part of Kleene (for now) includes:

- Multi-container orchestration similar to docker-compose.
- Built-in functionality for distributing images (container registry).
- Clustering of several FreBSD Kleene hosts.

If resources permit, some of these features, especially multi-container orchestration,
will be implemented in the future, see the roadmap below.

## Versioning

The initial release of 0.1.0 marks a phase shift from pure development to testing
and maturing of the software. Kleene follows [semantic versioning](https://semver.org/)
which means that there is no stable API (Kleened) or CLI (Klee) for now.
In this initial phase, patch versions (y in 0.x.y) are intended for minor
adjustments whereas minor versions (x in 0.x.y) are reserved for larger features
or changes. Follow project progress [here](/release-notes/).

Minor versions of Klee and Kleene should be synced and released simultaneously.

## Project roadmap

The tentative highly condensed roadmap is:

1. Initial phase focusing on bugfixes and minor adjustments

2. Introduce server-side (Kleened) management of contexts

3. Introduce functionality similar to docker-compose

4. Introduce 'namespacing', similar to Ansible host-vars.

This is definitely subject to change. See the [GitHub organisation](https://github.com/kleene-project) for
details and dicussion.
