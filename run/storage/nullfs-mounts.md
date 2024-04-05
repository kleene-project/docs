---
description: Using nullfs mounts
title: Nullfs mounts
keywords: storage, persistence, data persistence, mounts, nullfs mounts
---

When you use a [nullfs mount](https://man.freebsd.org/cgi/man.cgi?query=nullfs),
a file or directory on the _host machine_ is mounted into a container.
The file or directory is referenced by its absolute path on the host
machine. By contrast, when you use a volume, a new directory is created within
Kleene's storage dataset on the host machine, and Kleene manages that
directory's contents.

Nullfs mounts rely on the host machine's filesystem having a specific directory structure
available.

See the [`container create` command](/engine/reference/commandline/container_create/#specifying-mounts)
for details on how to specify nullfs mounts with Klee.

> Nullfs mounts allow access to sensitive files
>
> One side effect of using nullfs mounts, for better or for worse,
> is that you can change the **host** filesystem via processes running in a
> **container**, including creating, modifying, or deleting important system
> files or directories. This is a powerful ability which can have security
> implications, including impacting non-Kleene processes on the host system.
{: .important }

## Good use cases for nullfs mounts

In general, you should use volumes where possible. Nullfs mounts are appropriate
for the following types of use case:

- Sharing configuration files from the host machine to containers in cases where
  the should be a single point of truth, i.e., making a copy of the files is
  insuffcient.

- You have some storage that is not based on ZFS, such as NFS-mounts that needs to
  be (partly) accessible in a container.

## Start a container with a nullfs mount

Consider a case where you have a directory `source` and when you build the
source code, the artifacts are saved into another directory, `source/target/`.
You want the artifacts to be available to a container at `/app/`, and you
want the container to get access to a new build each time you build the source
on your development host. Use the following command to nullfs-mount the `target/`
directory into your container at `/app/`. Run the command from within the
`source` directory. The `$(pwd)` sub-command expands to the current working
directory.

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

Stop the container:

```console
$ klee rmc -f devtest
```

### Mount into a non-empty directory on the container

If you nullfs-mount a directory into a non-empty directory on the container, the directory's
existing contents are obscured by the nullfs mount. This can be beneficial,
such as when you want to test a new version of your application without
building a new image. However, it can also be surprising and this behavior
differs from [Kleene volumes](volumes.md).

This example is contrived to be extreme, but replacing the contents of the
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

The container is created but does not start. Remove it:

```console
$ klee rmc broken-container
```

## Use a read-only nullfs mount

For some development applications, the container needs to
write into the mount, so changes are propagated back to the
Kleene host. At other times, the container only needs read access.

This example modifies the one above but mounts the directory as a read-only
mount, by adding `:ro`, after the mount point within the container.

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

Stop the container:

```console
$ klee rmc -f devtest
```
