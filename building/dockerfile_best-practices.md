---
description: Hints, tips and guidelines for writing clean, reliable Dockerfiles
keywords: parent image, images, dockerfile, best practices, hub, official image
title: Best practices for writing Dockerfiles
---

This sections discusses a few best-practices for building images.
However, since Kleene is a new tool, this should be seen as tentative suggestions
that might change as Kleene develops, and more user-experience is gained
with the software.

## Partitioning of images

When creating Dockerfiles it can be advantageous to consider
to divide an otherwise self-contained image, into a 'package installation'
and a 'configuration' image, respectively.
The former builds and installs the necessary application packages using, e.g., [pkg(7)](https://man.freebsd.org/cgi/man.cgi?query=pkg) or [ports(7)](https://man.freebsd.org/cgi/man.cgi?query=ports),
while the 'configuration' image copies configuration files and sets up the runtime environment.

Dividing images this way has several advantages:

1. It reduces build times of the 'configuration' image, which is where most of the
   debugging/development usually takes place, and avoids repeatedly fetching binaries
   and compiling software.

2. It is easy to setup the same application with different configurations.
   For instance, if a new database is needed for at new product with different configuration
   requirements than the present setup, or if there is a need for different environments such as 'development'
   and 'production'.

3. If an new application is builded from scratch, the 'package installation' image can be shared to other
   users, while having a custom 'configuration' image for specific internal deployments.

Let's make this concrete with a few examples.

### Example 1: MariaDB

Consider the `Dockerfile.mariadb` file from [part 6](/get-started/06_multi_container/):

```dockerfile
FROM FreeBSD-13.2-RELEASE:latest
RUN pkg install -y mariadb106-client mariadb106-server

CMD service mysql-server onestart && \
    mysql -u root -e "CREATE DATABASE IF NOT EXISTS $DATABASE_NAME;" && \
    mysql -u root -e "CREATE USER IF NOT EXISTS 'webapp'@'%' IDENTIFIED BY '$DATABASE_PASSWORD';" && \
    mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'webapp'@'%' WITH GRANT OPTION;" && \
    mysql -u root -e "FLUSH PRIVILEGES;"
```

This can be split up into

```dockerfile
# Dockerfile.mariadb-pkg build with tag 'MariaDB'
FROM FreeBSD-13.2-RELEASE:latest
RUN pkg install -y mariadb106-client mariadb106-server
```

and

```dockerfile
# Dockerfile.mariadb:
FROM MariabDB-pkg:latest
CMD service mysql-server onestart && \
       mysql -u root -e "CREATE DATABASE IF NOT EXISTS $DATABASE_NAME;" && \
       mysql -u root -e "CREATE USER IF NOT EXISTS 'webapp'@'%' IDENTIFIED BY '$DATABASE_PASSWORD';" && \
       mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'webapp'@'%' WITH GRANT OPTION;" && \
       mysql -u root -e "FLUSH PRIVILEGES;"
```

The latter builds much faster, and can be used to experiment with the database
configuration and initialization. The former image
from `Dockerfile.mariadb-pkg` is resuable for different projects that also
require a MariaDB database but require a different database schema.

### Example 2: A web application

Similarily, the `Dockerfile` used for the 'production' `webapp` image from [part 2](/get-started/02_our_app/)

```dockerfile
FROM FreeBSD-13.2-RELEASE:latest
RUN pkg install -y node20 npm-node20 yarn-node20
WORKDIR /app
COPY . .
RUN yarn install --production
CMD cd /app && node src/index.js
```

and `Dockerfile.dev` for the 'development' `webapp-dev` image from [part 5](/get-started/05_nullfs_mounts/)

```dockerfile
FROM webapp:latest
RUN rm -rf /app
CMD cd /app && yarn install && yarn run dev
```

can be refactored into a time-consuming `pkg install ...` 'installation' image,

```dockerfile
# Dockerfile.pkg build with tag 'webapp-pkg'
FROM FreeBSD-13.2-RELEASE:latest
RUN pkg install -y node20 npm-node20 yarn-node20
```

that can be used for the two environment-specific images:

```dockerfile
# Production image
FROM webapp-pkg:latest
WORKDIR /app
COPY . .
RUN yarn install --production
CMD cd /app && node src/index.js
```

and

```dockerfile
# Developemnt image
FROM webapp-pkg:latest
CMD cd /app && yarn install && yarn run dev
```

## 'ephemeral' vs. 'thin VM' containers

The images in the [Getting started](/get-started/) guide are designed as
["ephemeral containers"](https://docs.docker.com/develop/develop-images/guidelines/#create-ephemeral-containers),
where the containerized application is started
with the container using the `CMD`-instruction.
This is a standard way of building images in the Linux-world.

However, traditionally with FreeBSD jails there have been a "containers-as-thin-vm's"
-approach. This is exemplified by the native FreeBSD jail-configuration, where jails
are specified in [`jail.conf(5)`](https://man.freebsd.org/cgi/man.cgi?query=jail.conf) and manage jails like they were services.
In this setup, containers are often started with the system startup script
`/etc/rc`, as exemplified in the `jails` man-page, and containers have the full
FreeBSD userland available.
Applications and services in the container are then managed with [rc.conf(5)](https://man.freebsd.org/cgi/man.cgi?query=rc.conf)
(or a third-party service manager such as `py-supervisord`).
Sometimes auxillary services such as `sshd` may be running together with the
main application.

Both the 'ephemeral' and 'thin VM' approaches to container design aim for seperation
of concerns and isolation of services:
Run the database in one container and the web-application in another.
Also, it is not a 'one or the other' situation, since both approaches can be used,
and mixed, with FreeBSD jails and thus Kleene.

### Example image for 'thin-VM' containers

As a simple example, let's try to make a simple 'playground VM' image that
creates a user, grants it password-free sudo in the `sudoers` file, and lastly enables
the ssh-server at container startup:

```dockerfile
FROM FreeBSD-13.2-RELEASE:latest
ARG MY_USER=stephen
ARG MY_PASSWORD=changeme

# Install sudo package
RUN pkg install -y sudo

# Creating user:
RUN pw groupadd -q -n $MY_USER
RUN echo -n "$MY_PASSWORD" | pw useradd -n $MY_USER -u 1001 -s /bin/sh -m -G $MY_USER -h 0
RUN echo "$MY_USER ALL=(ALL) ALL" >> /usr/local/etc/sudoers

# Enable ssh-server in /etc/rc.conf
RUN sysrc sshd_enable=YES
CMD /bin/sh /etc/rc
```

The `CMD`-instruction runs FreeBSD's own startup script that initializes the
container (thereby starting `sshd`) and then exits.

Save the instructions to `Dockerfile.lite-vm` and build the image

```console
$ klee build -t MyLiteVM -f Dockerfile.lite-vm .
```

Once it has finished, you can run and instance of your new image.
It will look something like this:

```console
$ klee run MyLiteVM
dfd0bdf5c2c1
created execution instance 168285340bb0
ELF ldconfig path: /lib /usr/lib /usr/lib/compat /usr/local/lib /usr/local/lib/compat/pkg /usr/local/lib/compat/pkg
32-bit compatibility ldconfig path: /usr/lib32
Updating motd:.
Creating and/or trimming log files.
Clearing /tmp (X related).
Updating /var/run/os-release done.
Starting syslogd.
Generating RSA host key.
3072 SHA256:oQIRiWPEzHXegIQSMYZkXFLgNrYtnnuKD2DTzolTmVE root@ (RSA)
Generating ECDSA host key.
256 SHA256:ndiEbY7GMdVM2mQafDTYkUkMYtSzaELEJqSoZHzw/5Q root@ (ECDSA)
Generating ED25519 host key.
256 SHA256:dc9ELmQqWyfphUwS4+u1auMIlE6HzzcgIE1DE2xbBQM root@ (ED25519)
Performing sanity check on sshd configuration.
Starting sshd.
Starting sendmail_submit.
Starting sendmail_msp_queue.
Starting cron.

Tue Feb  6 17:14:16 UTC 2024
```

And the new playground is up and running!
Now, hurry up and ssh into the newly created 'vm-container' and change
the password and start playing around!

## General guidelines and recommendations

The following sections contain a few tips and conrete advices for image development.

### Don't install unnecessary packages

To reduce complexity, dependencies, file sizes, and build times, avoid
installing extra or unnecessary packages just because they might be "nice to
have." For example, there is no need to include a text editor in a database image.

### Decouple applications

Each container should have only one concern. Decoupling applications into
multiple containers makes it easier to scale, reuse containers and upgrade
the tech stack.
For instance, a web application stack might consist of three separate
containers, each with its own unique image, to manage the web application,
database, and an in-memory cache in a decoupled manner.

Try and keep containers as clean and modular as possible. If
containers depend on each other, use container [networks](/run/network/)
to ensure that the containers can communicate.

### Keep Dockerfile instructions simple

Try to avoid multiline-instructions, such as long `RUN`-instructions
of the form

```dockerfile
RUN /some_script.sh && \
    some_command && \
    some_other_command && \
```

use instead

```dockerfile
RUN some_script.sh
RUN some_command
RUN some_other_command
```

Each `RUN`-instruction causes Kleene to make a [zfs snapshot](https://man.freebsd.org/cgi/man.cgi?query=zfs-snapshot)
which a fast operation that takes up (practically) no
space. It also makes debugging easier, since more snapshots
increases flexibility when investigating a failed build.
See [Using build snapshots](/building/snapshots/) for details.

### Using pipes in `RUN`-instructions

Some `RUN` commands depend on the ability to pipe the output of one command into another, using the pipe character (`|`), as in the following example:

```dockerfile
RUN fetch -o - https://some.site | wc -l > /number
```

Kleene executes these commands using the `/bin/sh -c` interpreter, which only
evaluates the exit code of the last operation in the pipe to determine success.
In the example above this build step succeeds and produces a new image so long
as the `wc -l` command succeeds, even if the `fetch` command fails.

To make the command fail due to an error at any stage in the pipe,
prepend `set -o pipefail &&` to ensure that an unexpected error prevents the
build from inadvertently succeeding. For example:

```dockerfile
RUN set -o pipefail && wget -O - https://some.site | wc -l > /number
```

### `ENV`-instructions can't be unset
`ENV` lines are stored as metadata during image build, and applied at each step.
Therefore, if environment variables are unset in one step, it is
still persisted and will appear in the following instructions. Test this by
creating a Dockerfile like the following, and build it.

```dockerfile
FROM FreeBSD
ENV ADMIN_USER="mark"
RUN echo $ADMIN_USER > ./mark
RUN unset ADMIN_USER
```

Then run the following (and be careful to avoid the `ADMIN_USER` environment
variable from being evaluated by the local shell before it is sent to Kleened)

```console
$ klee run test sh -c 'echo $ADMIN_USER'
1aeff4eb2897
created execution instance 98d33442355c
mark

executable 98d33442355c and its container exited with exit-code 0
```

To prevent this, and really unset the environment variable, use a `RUN` command
with shell commands, to set, use, and unset the variable all in a single instruction.
Seperate commands with `;` or `&&`. If the second method is used,
and one of the commands fails, `klee build` also fails. This is usually a
good idea. Using `\` as a line continuation character for Dockerfiles
improves readability. Alternatively, put all of the commands into a shell script
and have the `RUN` command just run that shell script.

```dockerfile
FROM FreeBSD
RUN export ADMIN_USER="mark" \
    && echo $ADMIN_USER > ./mark \
    && unset ADMIN_USER
CMD sh
```

```console
$ klee run test sh -c 'echo $ADMIN_USER'
e8321f2dfdb5
created execution instance 340d38bfc458


executable 340d38bfc458 and its container exited with exit-code 0
```
