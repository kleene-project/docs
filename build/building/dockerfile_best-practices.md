---
description: Hints, tips and guidelines for writing clean, reliable Dockerfiles
keywords: parent image, images, dockerfile, best practices, hub, official image
title: Best practices for writing Dockerfiles
---

This sections discusses a few best-practices for building images.
However, since Kleene is new this should be seen as tentative suggestions
that might change as Kleene develops and more user-experience is gained
with the software.

## Partitioning of images

When create Dockerfiles it can in many cases be advantageous to consider
splitting an otherwise self-contained image for a service, into two.

Since Kleene does not have caching, dividing an image into a 'package installation'
(using [pkg(8)](FIXME) or [ports(7)](FIXME)) part and 'configuration' part.
This reduces build times of the latter, which is where most of the debugging/development
usually takes place. This usually overlaps with other relevant considerations:

1. Being able to easily setup the same software with different configurations.
   For instance, if you need a new database for at new product with different configuration
   requirements than your present setup, or you need different environments such as 'development'
   and 'production'.

2. Your build a piece of software from scratch and would like to be able to share it to other
   users while having your own custom-configuration for your own deployment.

Let's make this concrete with a few examples.

### Example 1: MariaDB

Consider the `Dockerfile.mariadb` file from [part 6](06_multi_container.md):

```dockerfile
FROM FreeBSD-13.2-RELEASE:latest
RUN pkg install -y mariadb106-client mariadb106-server

CMD service mysql-server onestart && \
    mysql -u root -e "CREATE DATABASE IF NOT EXISTS $DATABASE_NAME;" && \
    mysql -u root -e "CREATE USER IF NOT EXISTS 'webapp'@'%' IDENTIFIED BY '$DATABASE_PASSWORD';" && \
    mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'webapp'@'%' WITH GRANT OPTION;" && \
    mysql -u root -e "FLUSH PRIVILEGES;"
```

this can be split up into,

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

We can then experiment with the database configuration and initialization
using `Dockerfile.mariadb` that builds much faster. And we can use the image
from `Dockerfile.mariadb-pkg` as the basis for different projects that also
require a MariaDB database.

### Example 2: A web application

Similarily we have the `Dockerfile` used for the 'production' `webapp` image from [part 2](./02_our_app.md):

```dockerfile
FROM FreeBSD-13.2-RELEASE:latest
RUN pkg install -y node20 npm-node20 yarn-node20
WORKDIR /app
COPY . .
RUN yarn install --production
CMD cd /app && node src/index.js
```

and `Dockerfile.dev` for the 'development' `webapp-dev` image from [part 5](./05_nullfs_mounts.md):

```dockerfile
FROM webapp:latest
RUN rm -rf /app
CMD cd /app && yarn install && yarn run dev
```

If we factor out the time-consuming `pkg install ...` we get

```dockerfile
# Dockerfile.pkg build with tag 'webapp-pkg'
FROM FreeBSD-13.2-RELEASE:latest
RUN pkg install -y node20 npm-node20 yarn-node20
```

that can be used as the basis for our two environment-specific images:

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

The images of the [Getting started](/get-started/) guide are designed by the
["ephemeral containers"](https://docs.docker.com/develop/develop-images/guidelines/#create-ephemeral-containers)-approach of Docker,
that focues on lightweight images/containers with respect to complexity and size.
The container should also start and stop with the `CMD`-instruction.

However, traditionally FreeBSD jails have been used more with a "containers-as-thin-vm's"
-approach. This is also exemplified by the native FreeBSD jail-configuration where you
specify your jails in [`jail.conf(5)`](https://man.freebsd.org/cgi/man.cgi?query=jail.conf) and then manage jails like they were services.
In this setup, containers are often started/stopped together with host itself,
and containers have the full FreeBSD userland available.
The particular service is then managed with [rc.conf(5)](https://man.freebsd.org/cgi/man.cgi?query=rc.conf)
within the container or a third-party service manager such as `py-supervisord`.
Just as if it was running directly on the host.
Sometimes auxillary services such as `sshd` may be running together with the
main application. This approach is also suitable for sandbox VM environments,
where a user can get (ssh)-access to a development-container and use it as a
playground/sandbox for trying out different software packages or play
around with data etc.

Both approaches, however, aim for seperation of concerns and isolation of services:
Run your database in one container and your web-applikation in another.
Luckliy, it is not a 'one or the other' situation since both approaches can be used,
and mixed, as see fit. FreeBSD jails and thus Kleene supports both ways.

### Example image for 'thin-VM' containers

As a simple example, let's try to make a lightweight template image that
creates a user, grants him password-free sudo in the `sudoers` file, and lastly enables
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
$ klee run -n testnet MyLiteVM
dfd0bdf5c2c1
created execution instance 168285340bb0
ELF ldconfig path: /lib /usr/lib /usr/lib/compat /usr/local/lib /usr/local/lib/compat/pkg /usr/local/lib/compat/pkg
32-bit compatibility ldconfig path: /usr/lib32
/etc/rc: WARNING: $hostname is not set -- see rc.conf(5).
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

And you new playground is up and running! You can check with `jls`.
Now, hurry up and ssh into your newly created 'vm-container' so you can change
the password and start playing around!

## General guidelines and recommendations

The following sections contain a few tips and conrete advices for image development.

### Don't install unnecessary packages

To reduce complexity, dependencies, file sizes, and build times, avoid
installing extra or unnecessary packages just because they might be "nice to
have." For example, you don’t need to include a text editor in a database image.

### Decouple applications

Each container should have only one concern. Decoupling applications into
multiple containers makes it easier to scale, reuse containers and upgrade
your tech stack.
For instance, a web application stack might consist of three separate
containers, each with its own unique image, to manage the web application,
database, and an in-memory cache in a decoupled manner.

Use your best judgment to keep containers as clean and modular as possible. If
containers depend on each other, you can use [Kleene container networks](FIXME)
to ensure that these containers can communicate.

### Keep Dockerfile instructions simple

Try to avoid multiline-instructions, such as long `RUN`-instructions
of the form

```dockerfile
RUN /some_script.sh && \
    some_command && \
    some_other_command && \
```

and use instead

```dockerfile
RUN some_script.sh && \
RUN some_command && \
RUN some_other_command && \
```

Each `RUN`-instruction causes Kleene to make a [zfs snapshot](https://man.freebsd.org/cgi/man.cgi?query=zfs-snapshot)
which a fast operation that takes up (practically) no
space. It also makes debugging easier, since more snapshots
increases flexibility when investigating a failed build.
See [Using build snapshots](/build/building/snapshots/) for details.

### Using pipes in `RUN`-instructions

Some `RUN` commands depend on the ability to pipe the output of one command into another, using the pipe character (`|`), as in the following example:

```dockerfile
RUN fetch -o - https://some.site | wc -l > /number
```

Kleene executes these commands using the `/bin/sh -c` interpreter, which only
evaluates the exit code of the last operation in the pipe to determine success.
In the example above this build step succeeds and produces a new image so long
as the `wc -l` command succeeds, even if the `fetch` command fails.

If you want the command to fail due to an error at any stage in the pipe,
prepend `set -o pipefail &&` to ensure that an unexpected error prevents the
build from inadvertently succeeding. For example:

```dockerfile
RUN set -o pipefail && wget -O - https://some.site | wc -l > /number
```

### `ENV`-instructions can't be unset
Each `ENV` lines are stored as metadata during image build, and applied at each step.
This means that even if you unset the environment variable in one step, it is
still persisted and will appear in the next instructions. You can test this by
creating a Dockerfile like the following, and then building it.

```dockerfile
FROM FreeBSD:testing
ENV ADMIN_USER="mark"
RUN echo $ADMIN_USER > ./mark
RUN unset ADMIN_USER
```

```console
$ klee run test sh -c 'echo $ADMIN_USER'
1aeff4eb2897
created execution instance 98d33442355c
mark

executable 98d33442355c and its container exited with exit-code 0
```

Be careful to avoid the `ADMIN_USER` environment variable from being evaluated
by your own shell before it is sent to Kleened.

To prevent this, and really unset the environment variable, use a `RUN` command
with shell commands, to set, use, and unset the variable all in a single instruction.
You can separate your commands with `;` or `&&`. If you use the second method,
and one of the commands fails, the `docker build` also fails. This is usually a
good idea. Using `\` as a line continuation character for Linux Dockerfiles
improves readability. You could also put all of the commands into a shell script
and have the `RUN` command just run that shell script.

```dockerfile
FROM FreeBSD:testing
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


