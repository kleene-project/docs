---
title: Operating Kleene
description: Kleene operation overview
keywords: Kleene, operation, maintenance
---

This section discusses a few topics related to the operation and maintenance of a
Kleene host.

## Pruning unused objects

Images, containers, networks and volumes can quickly accumulater,
when developing images and experimenting with containers. To easily remove them,
use the `klee <object> prune` family of commands. The conditions on what is
removed differs, depending on which object is being pruned.

Use `klee <object> prune --help` to see what condition holds for a particular
object. Note that using `klee <object> prune` *does not* output the help text as
it usually does with most commands, but instead execute the command. Luckily, it
does prompt the user before removing any objects.

## Containers are independent from Kleene

It is worth mentioning the decoupling of Kleene and its containers.
When Kleene starts a container it is done by starting a FreeBSD jail under the hood,
and that jail is independently managed by FreeBSD and will continue to run if
Kleened is shutdown. For instance:

```console
$ klee run FreeBSD
ab7857f95f13
created execution instance a88528cd8383
ELF ldconfig path: /lib /usr/lib /usr/lib/compat
32-bit compatibility ldconfig path: /usr/lib32
Updating motd:.
Creating and/or trimming log files.
Clearing /tmp (X related).
Updating /var/run/os-release done.
Starting syslogd.
Starting sendmail_submit.
Starting sendmail_msp_queue.
Starting cron.

Thu Mar  7 12:12:31 UTC 2024

a88528cd8383 has exited with exit-code 0

$ sudo kill 6117 # Killing Kleened

$ klee lsc
unable to connect to kleened: [Errno 61] Connection refused
$ jls
   JID  IP Address      Hostname                      Path
    19                                                /zroot/kleene/container/ab7857f95f13
$ sudo jexec 19 /bin/ls
.cshrc          bin             COPYRIGHT       etc             libexec         mnt             proc            root            sys             usr
.profile        boot            dev             lib             media           net             rescue          sbin            tmp             var
```

The jail is still running without Kleened, and if Kleened is started again, it will
immediately recognize the running container:

```console
$ sudo service kleened start
$ klee lsc
 CONTAINER ID    NAME       IMAGE            COMMAND           CREATED          STATUS    JID
──────────────────────────────────────────────────────────────────────────────────────────────
 ab7857f95f13    funny_wu   FreeBSD:latest   /bin/sh /etc/rc   18 minutes ago   running   19
```

However, from the perspective of the FreeBSD host, it is a fire-and-forget
action when Kleene starts a jail: Jails/containers will not automatically start with
FreeBSD during system boot, unless Kleened is started as well (and they are
configured to start with Kleened), even though FreeBSD has the functionality
to do so with jails.
