---
title: Build Snapshots
description: How to use snapshots in image development
keywords: image, build, best practices
---
## Using image build snapshots

While the image builds, Kleene takes filesystem [snapshots](https://man.freebsd.org/cgi/man.cgi?query=zfs-snapshot)
of the build container's filesystem after successfully running a `RUN` or `COPY` instruction.
Containers and images can be created from these snapshots, which can be useful
when developing images. For instance, when an image build fail and you need
to understand why it crashed, you can investigate the runtime environment as it
looked before the build failed.
 
This is illustrated with a somewhat artifical image development scenario.
Which, nevertheless, aims to give inspiration in using image snapshots for image
development, to reduce build-times between test-builds and as a
flexible debugging tool.

Start with the following draft Dockerfile

```dockerfile
FROM FreeBSD:latest
RUN pkg install -y postgresql16-server
RUN sysrc postgresql_enable=yes
RUN service postgresql initdb
RUN service postgresql start
RUN psql -c "CREATE DATABASE my_db;"
RUN service postgresql stop
```

and try to build it

```console
$ klee build -t PostgreSQL .
Started to build image with ID f472c80affa4
Step 1/7 : FROM FreeBSD:latest
Step 2/7 : RUN pkg install -y postgresql16-server
..............................
... <lots of build output> ...
..............................
--> Snapshot created: @c069e69af8cf
Step 3/7 : RUN sysrc postgresql_enable=yes
postgresql_enable:  -> yes
--> Snapshot created: @fb70baa07e6e
Step 4/7 : RUN service postgresql initdb
..............................
... <lots of build output> ...
..............................
creating directory /var/db/postgres/data16 ... ok
creating subdirectories ... ok
selecting dynamic shared memory implementation ... posix
selecting default max_connections ... 20
selecting default shared_buffers ... 400kB
selecting default time zone ... UTC
creating configuration files ... ok 
running bootstrap script ... 2024-02-20 18:09:13.060 UTC [6935] FATAL:  could not create shared memory segment: Function not implemented
2024-02-20 18:09:13.060 UTC [6935] DETAIL:  Failed system call was shmget(key=55715, size=56, 03600).
child process exited with exit code 1
initdb: removing data directory "/var/db/postgres/data16"
jail: /usr/bin/env /bin/sh -c service postgresql initdb: failed
The command '/bin/sh -c service postgresql initdb' returned a non-zero code: 1
Failed to build image f472c80affa4. Most recent snapshot is @fb70baa07e6e
```

It failed! 
The last line informs us of the most recent snapshot, i.e., the snapshot taken
after the last succesful `COPY`/`RUN` instruction.

> **Tip**
>
> Every time a snapshot is created during a build Kleene prints a message
> `--> Snapshot created: @<image-id>` exemplified by the failed build output.
> You can create new images and containers using these image-snapshots as
> parent-images.
{: .tip }

Kleene have saved the state of the failed build as an image with nametag
`<name-supplied>:failed`. In in this example:

```console
$ klee lsi
 ID             NAME         TAG      CREATED            
─────────────────────────────────────────────────────────
 f472c80affa4   PostgreSQL   failed   About a minute ago 
 b905ae354338   FreeBSD      latest   5 months ago 
```

Note that if the tag already exists, the existing image will be untagged.

After a bit of research we discovered that PostgresSQL needs a specific
kernel functionalty that is disabled for containers by default. This can be
enabled using jail-parameter `allow.sysvipc`. We rebuild using the last vaild
snapshot from our previous failed build, by modifying our draft Dockerfile:

```dockerfile
FROM PostgreSQL:failed@fb70baa07e6e
#FROM FreeBSD:latest
#RUN pkg install -y postgresql16-server
#RUN sysrc postgresql_enable=yes
RUN service postgresql initdb
RUN service postgresql start
RUN psql -c "CREATE DATABASE my_db;"
RUN service postgresql stop
``` 

Where we use the snapshot as our parent image as well as omitting the
instructions that workded in the previous build. We start the rebuild with

```console
$ klee build -J allow.sysvipc -t PostgreSQL .
......................
... <build output> ...
......................
--> Snapshot created: @0b4c07e5d8ad
Step 4/5 : RUN psql -c "CREATE DATABASE my_db;"
psql: error: connection to server on socket "/tmp/.s.PGSQL.5432" failed: FATAL:  role "root" does not exist
The command '/bin/sh -c psql -c "CREATE DATABASE my_db;"' returned a non-zero code: 2
Failed to build image 5db4e03a7a4e. Most recent snapshot is @0b4c07e5d8ad
```

The `RUN service postgresql initdb` now runs succesfully, but a new error occurs
in `RUN psql -c "CREATE DATABASE my_db;"`.
We immediately know what this error is about and we run a container to verify
our solution to the problem:

```console
$ klee run -J allow.sysvipc -it PostgreSQL:failed /bin/sh
# cat /etc/passwd 
# $FreeBSD$
# 
# Lines ommited for brevity
root:*:0:0:Charlie &:/root:/bin/csh
toor:*:0:0:Bourne-again Superuser:/root:
daemon:*:1:1:Owner of many system processes:/root:/usr/sbin/nologin
tests:*:977:977:Unprivileged user for tests:/nonexistent:/usr/sbin/nologin
nobody:*:65534:65534:Unprivileged user:/nonexistent:/usr/sbin/nologin
postgres:*:770:770:PostgreSQL Daemon:/var/db/postgres:/bin/sh
# service postgresql start
2024-02-20 21:41:19.415 UTC [10012] LOG:  ending log output to stderr
2024-02-20 21:41:19.415 UTC [10012] HINT:  Future log output will go to log destination "syslog".
# su postgres
$ psql -c "CREATE DATABASE my_db;" 
CREATE DATABASE
```

Great! We just need to switch to the `postgres` user when we are using `psql`.
We rebuild again with an updated Dockerfile

```dockerfile
FROM PostgreSQL:failed@0b4c07e5d8ad
#FROM FreeBSD:latest
#RUN pkg install -y postgresql16-server
#RUN sysrc postgresql_enable=yes
#RUN service postgresql initdb
RUN service postgresql start
USER postgres
RUN psql -c "CREATE DATABASE my_db;"
USER root
RUN service postgresql stop
```

containing our new solution, represented by a couple of `USER` instructions.
Also, we adapted the `FROM`-instruction in our Dockerfile, to the snapshot
that was taken after `RUN service postgresql initdb` finished. That means
our build will started right after the database has been initialized.

Note that even though the nametag `PostgreSQL:failed` remains the same, it
points to a different image. Now it refers to our latest failed build.
The previous image is still visible with `klee lsi` but now without any nametag.

We rebuild from the last snapshot and hopefully this should complete succesfully.

Finally, to have one complete image, we rerun with the final Dockerfile

```Dockerfile
FROM FreeBSD:latest
RUN IGNORE_OSVERSION=yes pkg install -y postgresql16-server
RUN sysrc postgresql_enable=yes
RUN service postgresql initdb
RUN service postgresql start
USER postgres
RUN psql -c "CREATE DATABASE my_db;"
USER root
RUN service postgresql stop
```

with the final build:

```console
$ klee build -J allow.sysvipc -t PostgreSQL .
......................
... <build output> ...
......................
Step 5/9 : RUN service postgresql start
2024-02-20 22:36:48.269 UTC [11277] LOG:  ending log output to stderr
2024-02-20 22:36:48.269 UTC [11277] HINT:  Future log output will go to log destination "syslog".
--> Snapshot created: @4df41bda8331
Step 6/9 : USER postgres
Step 7/9 : RUN psql -c "CREATE DATABASE my_db;"
CREATE DATABASE
--> Snapshot created: @af986b79c969
Step 8/9 : USER root
Step 9/9 : RUN service postgresql stop
--> Snapshot created: @5bb4138c513c

image created
e64cec8b977e
$
```

Voila!
