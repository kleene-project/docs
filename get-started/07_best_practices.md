---
title: "Containerization tips"
keywords: get started, setup, orientation, quickstart, intro, containers
description: Tips for building images and running containers
---

This sections provides attempts at a few best-practices for building
images and running containers. However, since Kleene is new this should be seen as
tentative suggestions that might change as Kleene develops and more user-experience
is gained with the software.

## Image partitioning

At the moment there is no caching when building images.
However, a common pattern in image-building is to install/build som packages with
[pkg(8)](FIXME) or [ports(7)](FIXME) and then make some configurations of the installed applications.
Usually the first part takes by far the most build time. In that case, it might make sense to
factor out the slow installation part into it's own seperate image and make a
'configuration' image based on it.

### The `MariaDB` image

For instance, consider the `Dockerfile.mariadb` file from [part 6](06_multi_container.md)

```dockerfile
FROM FreeBSD-13.2-RELEASE:latest
RUN pkg install -y mariadb106-client mariadb106-server

CMD service mysql-server onestart && \
    mysql -u root -e "CREATE DATABASE IF NOT EXISTS $DATABASE_NAME;" && \
    mysql -u root -e "CREATE USER IF NOT EXISTS 'webapp'@'%' IDENTIFIED BY '$DATABASE_PASSWORD';" && \
    mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'webapp'@'%' WITH GRANT OPTION;" && \
    mysql -u root -e "FLUSH PRIVILEGES;"
```

which can be split up into,

```dockerfile
# Dockerfile.mariadb-pkg
FROM FreeBSD-13.2-RELEASE:latest
RUN pkg install -y mariadb106-client mariadb106-server
```

built with `klee build -t MariaDB-pkg -f Dockerfile.mariadb-pkg`, and

```dockerfile
# Dockerfile.mariadb
FROM MariabDB-pkg:latest
CMD service mysql-server onestart && \
       mysql -u root -e "CREATE DATABASE IF NOT EXISTS $DATABASE_NAME;" && \
       mysql -u root -e "CREATE USER IF NOT EXISTS 'webapp'@'%' IDENTIFIED BY '$DATABASE_PASSWORD';" && \
       mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'webapp'@'%' WITH GRANT OPTION;" && \
       mysql -u root -e "FLUSH PRIVILEGES;"
```

built with `klee build -t MariaDB -f Dockerfile.mariadb`.
We can then experiment with the database configuration and initialization
using `Dockerfile.mariadb` that builds much faster.

### The `webapp` images

Similarily we have the `Dockerfile` used for the `webapp` image from [part 2](./02_our_app.md)

```dockerfile
FROM FreeBSD-13.2-RELEASE:latest
RUN pkg install -y node20 npm-node20 yarn-node20
WORKDIR /app
COPY . .
RUN yarn install --production
# Listens on port 3000
CMD cd /app && node src/index.js
```

and `Dockerfile.dev` for the `webapp-dev` image from [part 5](./05_nullfs_mounts.md)

```dockerfile
FROM webapp:latest
RUN rm -rf /app
# Listens on port 3000
CMD cd /app && yarn install && yarn run dev
```

If we factor out the time-consuming `pkg install ...` we get

Package-image:

```dockerfile
# Dockerfile.pkg
FROM FreeBSD-13.2-RELEASE:latest
RUN pkg install -y node20 npm-node20 yarn-node20
```

built with `klee build -t webapp-pkg -f Dockerfile.pkg .`.

Revised `Dockerfile` for part 2:

```dockerfile
FROM webapp-pkg:latest
WORKDIR /app
COPY . .
RUN yarn install --production
CMD cd /app && node src/index.js
```

built with `klee build -t webapp .`.

Revised `Dockerfile.dev` for part 5:

```dockerfile
FROM webapp-pkg:latest
CMD cd /app && yarn install && yarn run dev
```

built with `klee build -t webapp-dev -f Dockerfile.dev .`.

## Using image build snapshots

An alternative approach is to use 'build snapshots' which provides more flexibility
and might be an effective tool in the image development proces.

During an image build, Kleene snapshots the state of the filesystem of the container.
These snapshots can then be used to create containers from partially built images
(or new images, for that matter).
This can be useful when an image build fail, and you like to debug the image from,
e.g., the last succesful instruction of the failed build.

Let's try to build the following Dockerfile

```dockerfile
# Dockerfile.fail
FROM FreeBSD-13.2-RELEASE:latest
RUN pkg install -y node20 npm-node20 yarn-node20
# Woops, spelling error:
COPY . /apps
RUN cd app && yarn install --production
# Listens on port 3000
CMD cd /app && node src/index.js
```

but this time we also use the `--no-cleanup` flag:

```
$ klee build --no-cleanup -t WontWork -f Dockerfile.fail .
```



## Running containers as virtual machines

### 'ephemeral' vs. 'thin VM'

The images of this guide has been designed after the
["ephemeral containers"](https://docs.docker.com/develop/develop-images/guidelines/#create-ephemeral-containers)-approach, that focues on lightweight images/containers with respect to complexity and size. The container should also start and stop with the `CMD`-instruction.

However, traditionally FreeBSD jails have been used more with a "containers-as-thin-vm's"
-approach. This is exemplified with the native FreeBSD jail-configuration where you
specify your jails in [`jail.conf(5)`](https://man.freebsd.org/cgi/man.cgi?query=jail.conf) and then manage jails like they were services.
In this setup, containers are often started/stopped together with host itself,
and contain have the full FreeBSD userland available. The particular service
is then managed with [rc.conf(5)](https://man.freebsd.org/cgi/man.cgi?query=rc.conf)
within the container, or perhaps a third-party service manager such as `py-supervisord`.
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

## Next steps

That's it for the introductory guide! The next steps is to explore the in depth manuals
and reference documentation. Additionally there is the [FreeBSD docs](https://docs.freebsd.org/)
where you can find the excellent handbook and relevant man-pages,
some of which have been linked to here. Reading up up on, e.g., FreeBSD jails,
provides useful background knowledge.
