---
description: components and formatting examples used in Kleene's docs
title: Callouts
toc_max: 3
---

We support these broad categories of callouts:

- Notes (no Liquid tag required)
- Tips, which use the `{: .tip }` tag
- Important, which use the `{: .important}` tag
- Warning , which use the `{: .warning}` tag

## Examples

> **Note**
>
> Note the way the `get_hit_count` function is written. This basic retry
> loop lets us attempt our request multiple times if the redis service is
> not available. This is useful at startup while the application comes
> online, but also makes our application more resilient if the Redis
> service needs to be restarted anytime during the app's lifetime. In a
> cluster, this also helps handling momentary connection drops between
> nodes.

> **Tip**
>
> Pin the base image to an explicit release, for example `FreeBSD-13.2-RELEASE:latest`.
{: .tip }


> **Important**
>
> Treat access tokens like your password and keep them secret. Store your
> tokens securely (for example, in a credential manager).
{: .important}


> **Warning**
>
> Removing Volumes
>
> Volumes are NOT removed when you remove the container using them. Use
> `klee volume rm` to remove a volume explicitly, or `klee volume prune` to
> remove every volume that is not in use by a container.
{: .warning}

## HTML

```html
> **Note**
>
> Note the way the `get_hit_count` function is written. This basic retry
> loop lets us attempt our request multiple times if the redis service is
> not available. This is useful at startup while the application comes
> online, but also makes our application more resilient if the Redis
> service needs to be restarted anytime during the app's lifetime. In a
> cluster, this also helps handling momentary connection drops between
> nodes.

> **Tip**
>
> Pin the base image to an explicit release, for example `FreeBSD-13.2-RELEASE:latest`.
{: .tip }

> **Important**
>
> Treat access tokens like your password and keep them secret. Store your
> tokens securely (for example, in a credential manager).
{: .important} 

> **Warning**
>
> Removing Volumes
>
> Volumes are NOT removed when you remove the container using them. Use
> `klee volume rm` to remove a volume explicitly, or `klee volume prune` to
> remove every volume that is _not_ in use by a container.
{: .warning}
```
