---
description: Using volumes
title: Volumes
keywords: storage, persistence, data persistence, volumes
---

Volumes are the preferred mechanism for persisting data used
by containers. While [nullfs mounts](nullfs-mounts.md) are dependent on the
directory structure of the host machine, volumes are managed by
Kleene. Advantages of using volumes over nullfs mounts:

- Volumes are easy to back up or migrate.
- Volumes are stored within the Kleene root and can thus be managed together
  with the Kleene installation.
- You can manage volumes using Klee.
- New volumes can have their content pre-populated by a container.

Volumes are based on nullfs-mounts and can be seen as managed, but less flexible,
version of nullfs mounts.

See the [`container create` command](/reference/klee/container_create/#specifying-mounts)
for details on how to mount volumes with Klee.

When a volume is mounted into a container, a nullfs mount is created
from the volume's dataset into the target directory within the container.

## Create and manage volumes

Unlike a nullfs mount, volumes can be created and managed by Kleene.

**Create a volume**:

```console
$ klee volume create my-vol
my-vol
```

**List volumes**:

```console
$ klee lsv
 VOLUME NAME   CREATED
─────────────────────────────
 my-vol        6 minutes ago
```

**Inspect a volume**:

```console
$ klee volume inspect my-vol
{
  "mountpoints": [],
  "volume": {
    "created": "2024-02-29T14:54:05.317207Z",
    "dataset": "zroot/kleene/volumes/my-vol",
    "mountpoint": "/zroot/kleene/volumes/my-vol",
    "name": "my-vol"
  }
}
```

Note that the list of mountpoints is empty since the volume is not mounted
it into any containers yet.

**Remove a volume**:

```console
$ klee volume rm my-vol
my-vol
```

**Prune volumes:**

```console
$ klee volume prune
WARNING! This will remove all unused volumes.
Are you sure you want to continue? [y/N]: y

```

## Start a container with a volume

Starting a container with a volume that doesn't yet exist, makes Klee create
it automatically. The following example mounts the volume `myvol2` into
`/app/` in the container.

```console
$ klee run -d --name devtest --mount myvol2:/app FreBSD:latest
```

Use `klee volume inspect myvol2` to verify that the volume was created and mounted
correctly:

```json
{
  "mountpoints": [
    {
      "container_id": "cc1ea0ff3f5a",
      "destination": "/app",
      "read_only": false,
      "source": "myvol2",
      "type": "volume"
    }
  ],
  "volume": {
    "created": "2024-02-29T15:07:02.291441Z",
    "dataset": "zroot/kleene/volumes/myvol2",
    "mountpoint": "/zroot/kleene/volumes/myvol2",
    "name": "myvol2"
  }
}
```

This shows the correct source and destination, and that the mount is read-write.

Stop the container and remove the volume.

```console
$ klee container stop devtest
cc1ea0ff3f5a
$ klee container rm devtest
cc1ea0ff3f5a
$ klee volume rm myvol2
myvol2
```

### Populate a volume using a container

If a container is created with a new or empty volume, and
the target directory within the container such as `/app/` is non-empty,
the directory's contents are copied into the volume (using `cp -a`) by Kleene.
The container then mounts and uses the volume, and other containers which use
the volume also have access to the pre-populated content.

To illustrate this, the following example starts an `nginx` container and
populates the new volume `nginx-vol` with the contents of the container's
`/usr/local/www/nginx` directory. This is where Nginx stores its default HTML
content.

The `nginx` image can be built like this:

```console
$ cat Dockerfile
FROM FreeBSD:latest
RUN pkg install -y nginx
$ klee build -t nginx:latest .
```

Then run the  `nginx` container using:

```console
$ klee run --name nginxtest --mount nginx-vol:/usr/local/www/nginx nginx ls /usr/local/www/nginx
835b746a9e0d
created execution instance bd16b0b23a25
50x.html
EXAMPLE_DIRECTORY-DONT_ADD_OR_TOUCH_ANYTHING
index.html

executable bd16b0b23a25 and its container exited with exit-code 0
```

and verify that the files have appeared on the volume

```console
$ ls /zroot/kleene/volumes/nginx-vol/
50x.html                                     EXAMPLE_DIRECTORY-DONT_ADD_OR_TOUCH_ANYTHING index.html
```

Then run the following commands to clean up both volume and container.

```console
$ klee container rm nginxtest
835b746a9e0d
$ klee volume rm nginx-vol
nginx-vol
```

## Use a read-only volume

For some development applications, the container only needs read access to the data.
Multiple containers can mount the same volume, and it is possible to simultaneously
mount a single volume as `read-write` for some containers and `read-only`
for others.

The following example modifies the volume created above, but mounts the directory
as a read-only volume, by adding `:ro` after the mount point.

```console
$ klee run --name=nginxtest --mount nginx-vol:/usr/local/www/nginx:ro nginx:latest
```

Use `klee container inspect nginxtest` to verify that the read-only mount was created
correctly. Look for the `container_mountpoints` section:

```json
  "container_mountpoints": [
    {
      "container_id": "c0c874965b50",
      "destination": "/usr/local/www/nginx",
      "read_only": true,
      "source": "nginx-vol",
      "type": "volume"
    }
  ]
```

Stop and remove both container volume.

```console
$ klee container stop nginxtest
$ klee container rm nginxtest
$ klee volume rm nginx-vol
```
