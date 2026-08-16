---
description: How to start containers automatically
keywords: containers, restart, policies, automation, administration
title: Start containers automatically
---

It is possible to configure containers to start when Kleened is.
If Kleened is enabled i `rc.conf`, it will start during FreeBSD startup
and automatically start any containers configured to do so.

This can also be combined with the `--persist` option for containers,
to avoid it being accidentially removed when pruning containers.

## Use a restart policy

To configure the restart policy for a container, use the `--restart` option
when using the `klee run` or `klee create` commands.
The value of `--restart` can be any of the two following:

| Option value | Description                                               |
|--------------|-----------------------------------------------------------|
| `no`         | Do not automatically restart the container. (the default) |
| `on-startup` | Start the container when Kleened starts                   |

### Restart policy details

Keep the following in mind when using the `on-startup` restart policy:

- If you manually stop a container, its restart policy is ignored until Kleened
  restarts or the container is manually restarted.

- When Kleened starts it creates the necessary bridge and loppback network
  interfaces of the networks. Then all the containers with the `on-start` restart
  policy i started one by one. Check the logs of Kleened if there are
  containers that did not start automatically as expected.

## Use a process manager

If more sophisticated restart strategies is needed, consider:

- Creating one or more [`rc.d` scripts](https://docs.freebsd.org/en/articles/rc-scripting/) to start containers,
  or
- Use an external process manager such as [supervisor](http://supervisord.org/).

These options can be used together with Klee (or Curl to use Kleened's API directly)
to start containers.
