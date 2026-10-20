---
description: Describe a whole application in one deployment file and manage it with klee deploy
title: Deploying applications with deployment files
---

A deployment file describes a whole application — its images, containers,
networks and volumes — in a single declarative file, so it can be created,
inspected and removed as one unit. It is Kleene's counterpart to a
Compose file.

The file is YAML, named `deployment.yml` by default (override with `-f`):
a top-level mapping with four optional sections, `images`, `containers`,
`networks` and `volumes`. The following example defines the lot:

```yaml
---
images:
  - tag: "FreeBSD:latest"
    method: "zfs-clone"
    zfs_dataset: "zroot/kleene_basejail"

networks:
  - name: "testnet"
    type: "bridge"
    subnet: "10.13.37.0/24"

volumes:
  - name: "database-storage"

containers:
  - name: "dbcon"
    image: "FreeBSD:latest"
    endpoints:
      - network: "testnet"
    mounts:
      - type: "volume"
        source: "database-storage"
        destination: "/mnt/db"
```

- `images` are created (from a `zfs-clone`/`zfs-copy`/`fetch` method) or
  built (from a Dockerfile `context`) — see
  [klee image create](../../reference/klee/image_create.md) and
  [klee image build](../../reference/klee/image_build.md) for the per-image
  fields.
- `containers` take the same fields as
  [klee container create](../../reference/klee/container_create.md), plus an
  `endpoints` list that connects the container to one of the deployment's
  `networks`.
- `volumes` are just names; `klee deploy create` makes the ones that do
  not exist yet.

## Creating and running a deployment

`klee deploy up` creates every object in the file (networks, volumes,
images, containers — in that order) and then starts the containers:

```console
$ klee deploy up
created network 'testnet'
created volume 'database-storage'
created container 'dbcon': f5a92f2b1db6
```

`klee deploy down` stops the containers and removes the deployment's
containers and networks (add `-v` to remove the volumes as well). Between
the two, `klee deploy start`, `stop` and `restart` manage the containers
without touching anything else, and `klee deploy remove` is `down` with a
confirmation prompt.

To build images as part of bringing the deployment up, pass `--build`:
`klee deploy up --build` builds every image that has a `context` instead
of a `method` before creating the containers. Builds run in parallel,
ordered by their `FROM` parents, with the concurrency controlled by the
file's `build_workers` key.

## Inspecting a deployment: diff

`klee deploy diff` compares the deployment file with the actual state on
the Kleene host — a "terraform plan" for containers — and reports every
object that is missing on the host and every existing object whose
configuration differs from the file:

```console
$ klee deploy diff
container 'dbcon' is missing on the host
network 'testnet': property 'nat' differs: host='em0' spec=''
```

Pass `--json` for machine-readable output. Image diffs are deliberately
shallow: once an image is built, most of its build-time configuration is
baked in and no longer comparable to the file.

## Removing what the file does not define

`klee deploy prune` removes the containers, networks and volumes that
exist on the host but are *not* defined in the deployment file — handy to
clean up leftovers from an older version of a deployment. It never
touches images.
