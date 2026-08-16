---
description: components and formatting examples used in Docker's docs
title: Accordions
toc_max: 3
---

## Example

<i class="fa fa-caret-down" aria-hidden="true"></i> (fa-caret-down) and
<i class="fa fa-caret-up" aria-hidden="true"></i> (fa-caret-up).

<div class="panel panel-default">
    <div class="panel-heading collapsed" data-toggle="collapse" data-target="#collapseSample1" style="cursor: pointer">
    Simple Klee help example
    <i class="chevron fa fa-fw"></i></div>
    <div class="collapse block" id="collapseSample1">
<pre>
<code>
$ klee --theme simple run
Usage: klee run [OPTIONS] IMAGE [COMMAND]...

  Run a command in a new container.

  The IMAGE syntax is: (**IMAGE_ID**|**IMAGE_NAME**[:**TAG**])[:**@SNAPSHOT**]

Options:
 -u, --user text       Default user used when running commands in the
                       container. This parameter will be overwritten by the
                       jail parameter `exec.jail_user` if it is set.
 -e, --env TEXT        Set environment variables (e.g. --env FIRST=SomeValue
                       --env SECOND=AnotherValue)
 -m, --mount list      Mount a volume/directory/file on the host filesystem
                       into the container. Mounts are specfied using a
                       `--mount SOURCE:DESTINATION[:rw|ro]` syntax.
 -J, --jailparam TEXT  Specify one or more jail parameters to use. If you do
                       not want `mount.devfs`, `exec.clean`, and
                       `exec.stop="/bin/sh /etc/rc.shutdown"` enabled, you
                       must actively disable them.
 -l, --driver TEXT     Network driver of the container. Possible values:
                       `ipnet`, `host`, `vnet`, and `disabled`. If no network
                       and no network driver is supplied, the network driver
                       is set to `host`. If a network is specfied but no
                       network driver, it is set to `ipnet`,
 -n, --network TEXT    Connect container to this network.
 --ip TEXT             IPv4 address used for the container. If omitted, an
                       unused ip is allocated from the IPv4 subnet of
                       `--network`.
 --ip6 TEXT            IPv6 address used for the container. If omitted, an
                       unused ip is allocated from the IPv6 subnet of
                       `--network`.
 -d, --detach          Do not output STDOUT/STDERR to the terminal. If this
                       is set, Klee will exit and return the container ID
                       when the container has been started.
 -i, --interactive     Send terminal input to container's STDIN. If set,
                       `--detach` will be ignored.
 -t, --tty             Allocate a pseudo-TTY
 --name TEXT           Assign a name to the container
 -p, --publish TEXT    Publish one or more ports using the syntax `HOST-
                       PORT[:CONTAINER-PORT][/PROTOCOL]` or
                       `INTERFACE:HOST-PORT:CONTAINER-
                       PORT[/PROTOCOL]`. `CONTAINER-PORT` defaults to
                       `HOST-PORT` and `PROTOCOL` defaults to 'tcp'.
 --help                Show this message and exit.

</code>
</pre>
</div>

<div class="panel-heading collapsed" data-toggle="collapse" data-target="#collapseSample2"  style="cursor: pointer"> Another Sample <i class="chevron fa fa-fw"></i></div>
<div class="collapse block" id="collapseSample2">
<p>
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.</p>
 </div>
</div>

## HTML

```
<div class="panel panel-default">
    <div class="panel-heading collapsed" data-toggle="collapse" data-target="#collapseSample1" style="cursor: pointer">
    Kleene hello-world example
    <i class="chevron fa fa-fw"></i></div>
    <div class="collapse block" id="collapseSample1">
<pre>
<code>
$ klee --theme simple container create
Usage: klee container create [OPTIONS] IMAGE [COMMAND]...

  Create a new container. The **IMAGE** parameter syntax is:
  `IMAGE-ID|[IMAGE-NAME[:TAG]][@SNAPSHOT]`

  See the documentation for details.

Options:
  -u, --user text       Default user used when running commands in the
                        container. This parameter will be overwritten by the
                        jail parameter `exec.jail_user` if it is set.
  -e, --env TEXT        Set environment variables (e.g. --env FIRST=SomeValue
                        --env SECOND=AnotherValue)
  -m, --mount list      Mount a volume/directory/file on the host filesystem
                        into the container. Mounts are specfied using a
                        `--mount SOURCE:DESTINATION[:rw|ro]` syntax.
  -J, --jailparam TEXT  Specify one or more jail parameters to use. If you do
                        not want `mount.devfs`, `exec.clean`, and
                        `exec.stop="/bin/sh /etc/rc.shutdown"` enabled, you
                        must actively disable them.
  -l, --driver TEXT     Network driver of the container. Possible values:
                        `ipnet`, `host`, `vnet`, and `disabled`. If no network
                        and no network driver is supplied, the network driver
                        is set to `host`. If a network is specfied but no
                        network driver, it is set to `ipnet`,
  -n, --network TEXT    Connect container to this network.
  --ip TEXT             IPv4 address used for the container. If omitted, an
                        unused ip is allocated from the IPv4 subnet of
                        `--network`.
  --ip6 TEXT            IPv6 address used for the container. If omitted, an
                        unused ip is allocated from the IPv6 subnet of
                        `--network`.
  --name TEXT           Assign a name to the container
  -p, --publish TEXT    Publish one or more ports using the syntax `HOST-
                        PORT[:CONTAINER-PORT][/PROTOCOL]` or
                        `INTERFACE:HOST-PORT:CONTAINER-
                        PORT[/PROTOCOL]`. `CONTAINER-PORT` defaults to
                        `HOST-PORT` and `PROTOCOL` defaults to 'tcp'.
  --help                Show this message and exit.
</code>
</pre>
</div>

<div class="panel-heading collapsed" data-toggle="collapse" data-target="#collapseSample2"  style="cursor: pointer"> Another Sample <i class="chevron fa fa-fw"></i></div>
<div class="collapse block" id="collapseSample2">
<p>
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.</p>
 </div>
</div>
```

This implementation makes use of the `.panel-heading` classes in
`_utilities.scss.md`,
along with [FontAwesome icons](http://fontawesome.io/cheatsheet/){: target="_blank" rel="noopener" class="_" }

> Note
>
>Make sure `data-target`'s and `id`'s match, and are unique.
>
>For each drop-down, the value for `data-target` and
`collapse` `id` must match, and id's must be unique per page. In this example,
we name these `collapseSample1` and `collapseSample2`.

Adding `block` to the `div` class `collapse` gives you some padding around the
sample content. This works nicely for standard text. If you have a code sample,
the padding renders as white space around the code block grey background.

The `style="cursor: pointer"` tag enables the expand/collapse functionality to
work on mobile. (You can use the [Xcode iPhone simulator](https://developer.apple.com/library/content/documentation/IDEs/Conceptual/iOS_Simulator_Guide/GettingStartedwithiOSSimulator/GettingStartedwithiOSSimulator.html#//apple_ref/doc/uid/TP40012848-CH5-SW4){: target="_blank" rel="noopener" class="_" } to test on mobile.)
