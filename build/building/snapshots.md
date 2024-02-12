---
title: Build Snapshots
description: How snapshots work and possible use-cases
keywords: build, best practices
---
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
```

but this time we also use the `--no-cleanup` flag:

```
$ klee build --no-cleanup -t WontWork -f Dockerfile.fail .
```
