---
description: Using nullfs mounts
title: Nullfs mounts
keywords: storage, persistence, data persistence, mounts, nullfs mounts
---

When using a [nullfs mount](https://man.freebsd.org/cgi/man.cgi?query=nullfs),
a file or directory on the _host machine_ is mounted into a container.
By contrast, when using a volume, a new directory is created within
Kleene's root dataset on the host, and Kleene manages that directory's contents.

See the [`container create` command](/reference/klee/container_create/#specifying-mounts)
for details on how to specify nullfs mounts with Klee.

> Nullfs mounts allow access to sensitive files
>
> One side effect of using nullfs mounts, for better or for worse,
> is that the host filesystem can be changed via processes running in a
> container, including creating, modifying, or deleting important system
> files or directories. This is a powerful ability which can have security
> implications, and potentially impacting non-Kleene processes on the host system.
{: .important }

## Good use cases for nullfs mounts

In general, you should use volumes where possible. Nullfs mounts are appropriate
for the following types of use case:

- Sharing content used in development within a container.
  See the [Get started](/get-started/05_nullfs_mounts/) guide for an example of this.

- Having storage that is not based on ZFS, such as NFS-mounts, that needs to
  be accessible in a container.

## Start a container with a nullfs mount

Consider a case with a directory `source` that contains source code,
which, when compiled, produce artifacts saved into the subdirectory
`source/target/`. The artifacts should be available within a container at `/app/`,
and always be up to date with the newest build, everytime it is produced on the
host. Use the following command to nullfs-mount the `source/target/`
directory into a container at `/app/` (run the command from within the
`source` directory).
The `$(pwd)` sub-command expands to the current working directory, i.e.,
`source`.

```console
$ klee run --name devtest --mount "$(pwd)"/target:/app nginx:latest
```

Use `klee container inspect devtest` to verify that the nullfs mount was created
correctly. Look for the `container_mountpoints` section:

```json
  "container_mountpoints": [
    {
      "container_id": "952441c02655",
      "destination": "/app",
      "read_only": false,
      "source": "/tmp/source/target",
      "type": "nullfs"
    }
  ]
```

This shows that the mount is of type `nullfs`, and it shows the correct source and
destination.

Stop and remove the container:

```console
$ klee rmc -f devtest
```

### Mount into a non-empty directory on the container

If a directory is nullfs-mounted into a non-empty directory on the container,
the directory's existing contents are hidden by the nullfs mount.
This can be beneficial when testing a new version of an application without
building a new image, as illustrated in the [Get started](/get-started/05_nullfs_mounts/)
guide. However, it can also be confusing to keep track of the state of files within
the target directory.

This example is contrived to the extreme, but replacing the contents of the
container's `/etc/` directory with the `/tmp/` directory on the host machine
will, in most cases, result in a non-functioning container.

```console
$ klee run --name broken-container --mount /tmp:/etc nginx:latest
217b19d8b21e
created execution instance 27b977efaa46
jail: getpwnam root: No such file or directory
jail: /usr/bin/env IGNORE_OSVERSION=yes /bin/sh /etc/rc: failed

executable 27b977efaa46 and its container exited with exit-code 1
```

The container is created but did not start. Remove it afterwards:

```console
$ klee rmc broken-container
```

## Use a read-only nullfs mount

For some development applications, the container only needs read access.

By modifying the previous example, the source directory is mounted as a read-only
by adding `:ro` after the mount point.

```console
$ klee run --name devtest --mount $(pwd)/target:/app:ro nginx:latest
```

Use `klee container inspect devtest` to verify that the nullfs mount was created
correctly. Look for the `container_mountpoints` section:

```json
"container_mountpoints": [
  {
    "container_id": "1459b8c75028",
    "destination": "/app",
    "read_only": true,
    "source": "/tmp/source/target",
    "type": "nullfs"
  }
]
```

Stop and remove the container:

```console
$ klee rmc -f devtest
```
