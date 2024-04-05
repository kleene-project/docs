---
title: Overview
description: Overview of options for persisting data in containers
keywords: storage, persistence, data persistence, volumes, mounts, nullfs mounts
---

Containers are often seen as ephemeral and something that is going to be
replaced often. For instance, during system and package upgrades, changes
in application configuration etc. Therefore, lasting data should be stored
outside of the container. It might also be relevante to share data across
containers.

Kleene has two options for containers to store files on the host machine, so
that the files are persisted acroos containers: _volumes_, and
_nullfs mounts_.

## Choose the right type of mount

No matter which type of mount you choose to use, the data looks the same from
within the container. It is exposed as either a directory or an individual file
in the container's filesystem.

- **Volumes** are managed by Kleene and stored in the `<kleene_root>/volumes`
  dataset. This means that they are automatically kept in a fixed location on
  the zpool, together with other Kleene data. See the section on
  [Kleene and ZFS](FIXME) to read more about how to configure Kleene's ZFS filesystem.

  If you mount an **empty volume** into a directory in the container in which files
  or directories exist, these files or directories are propagated (copied)
  into the volume. Similarly, if you start a container and specify a volume which
  does not already exist, an empty volume is created for you.
  This is a good way to pre-populate data that another container needs.

- **Nullfs mounts** are flexible and may be stored *anywhere* on the host system.
  They may even be important system files or directories. The flexibility comes
  with the risk of using/modifying files that is also used by any host processes,
  including Kleened. Nullfs mounts are not managed by Kleene except for the
  mount-operation during container creation.

  If you mount a **nullfs mount or non-empty volume** into a directory in the container
  in which some files or directories exist, these files or directories are
  hidden by the mount.
  The hidden files are not removed or altered, but are not accessible while the
  nullfs mount or volume is mounted.

See the [`container create` command](/engine/reference/commandline/container_create/#specifying-mounts)
for details on how to specify volume or nullfs mounts with Klee.

## Next steps

- Learn more about [volumes](volumes.md).
- Learn more about [nullfs mounts](nullfs-mounts.md).
