---
title: Dockerfile reference
description: "Dockerfiles use a simple DSL which allows you to automate the steps you would normally manually take to create an image."
keywords: build, dockerfile, reference
toc_max: 3
redirect_from:
- /reference/builder/
fetch_remote:
  line_start: 2
  line_end: -1
---
Kleene can build images by reading instructions from a
`Dockerfile`. A `Dockerfile` contains all the commands a
user would run on the command line to build an image, including a few
shortcuts to make it easier/more readable. Thus, a `Dockerfile` can be
seen as a recipe for setting up and configuring a runtime environment.
This page describes the commands you can use in a `Dockerfile` for Kleene.

## Format

In general, Kleene follows a subset of the Dockerfile syntax specified by Docker,
and used by Docker, Podman etc. for building images. Thus, with the exception
of missing features, it should be a familiar experience writing Dockerfiles for
Kleene compared to writing Dockerfiles for these tools.

However, given Kleene's approach to building images, there are
deviations in best-practices. For instance, aggregating commands
into a single large `RUN`-instruction is discouraged in Kleene.
See [Dockerfile best practices](/building/dockerfile_best-practices/)
for details.

Here is the format of the `Dockerfile` as it used in Kleene:

```dockerfile
# Comment
INSTRUCTION arguments
```

Unlike Docker, Kleene requires that instructions in Dockerfiles MUST
be uppercase to distinguish them from arguments more easily.

Kleene runs instructions in a `Dockerfile` in order. A `Dockerfile` **must
begin with a `FROM` instruction**, with the exception of [comments](#format),
and [ARGs](#arg). The `FROM` instruction specifies the [*Parent
Image*](/glossary/#parent-image) from which you are
building.

Kleene always treats a `\` as the last character of a line as an escaped
newline, so

```dockerfile
RUN /bin/bash -c 'source $HOME/.bashrc; \
echo $HOME'
```

are equivalent to this single line:

```dockerfile
RUN /bin/bash -c 'source $HOME/.bashrc; echo $HOME'
```

Kleene treats lines that *begin* with `#` as a comment. A `#` marker anywhere
else in a line is treated as part of an argument.
This allows statements like:

```dockerfile
# Comment
RUN echo 'we are running some # of cool things'
```

Comment lines are removed before the Dockerfile instructions are executed, which
means that the comment in the following example is not handled by the shell
executing the `echo` command, and both examples below are equivalent:

```dockerfile
RUN echo hello \
# comment
world
```

```dockerfile
RUN echo hello \
world
```

Line continuation characters are not supported in comments and leading
whitespaces before comments (`#`) and instructions (such as `RUN`) are
**not** allowed.

## Environment replacement

Environment variables (declared with [the `ENV` instruction](#env)) can also be
used in certain instructions other than [the `RUN` instruction](#run) as
variables to be interpreted by Kleene.
Environment replacement is done using the [Bourne shell](https://man.freebsd.org/cgi/man.cgi?query=sh)
supplied with environment variables defined by preceding
`ENV`-instructions. Thus, the rules of notation and syntax are identical
to `sh`, as discussed below.

Environment variables are notated in the `Dockerfile` either with
`$variable_name` or `${variable_name}`.

The `${variable_name}` syntax also supports the standard `sh`
modifiers, such as:

- `${variable:-word}` indicates that if `variable` is set then the result
  will be that value. If `variable` is not set then `word` will be the result.
- `${variable:+word}` indicates that if `variable` is set then `word` will be
  the result, otherwise the result is the empty string.

In all cases, `word` can be any string, including additional environment
variables.

Escaping is possible by adding a `\` before the variable: `\$foo` or `\${foo}`,
for example, will translate to `$foo` and `${foo}` literals respectively.

Example:

```dockerfile
FROM FreeBSD:latest
ENV FOO=bar
# Use the user 'bar' for subsequent RUN/CMD-instructions:
USER $FOO
# Creates /bar:
RUN mkdir /${FOO}
# Variable identifier escaping makes
COPY \$FOO /quux
# into 'COPY $FOO /quux'
```

Environment variables are supported by the following list of instructions in
the `Dockerfile`:

- `FROM`
- `RUN`
- `CMD`
- `COPY`
- `ENV`
- `USER`

Note that environment variables in `RUN` and `CMD` instructions only works when using
the *shell* form. When the *exec* form is used, the environment variables
are supplied but it is up to the executable to make use of them.

## FROM

```dockerfile
FROM <image>[:<tag>][@<snapshot>]
```

where `<image>` can be the name or ID of an existing image and the `<tag>`
value is optional. If the `<tag>` is omitted, the builder assumes a `latest`
tag by default.
The builder returns an error if it cannot find the `tag` value.
Optionally, it is possible to specify which image snapshot should be used
by providing a snapshot ID for `<snapshot>`.

The `FROM` instruction initializes a [*build container*](/glossary/#build-container)
within which subsequent instructions are executed.
The build container follows the naming scheme `build_<image ID>`.
A valid `Dockerfile` needs to begin with a `FROM` instruction,
except for the `ARG` instruction, which is the only instruction
that may precede `FROM` in the `Dockerfile`.
This means that `FROM` instructions support variables that are
declared by `ARG` instructions preceding it, e.g.,

```dockerfile
ARG  CODE_VERSION=13.0-STABLE
FROM FreeBSD:${CODE_VERSION}
CMD  /code/run-app
```

## RUN

RUN has 2 forms:

- `RUN <command>` *shell* form, the command is run in a Bourne shell
  `/bin/sh -c <command>`.
- `RUN ["executable", "param1", "param2"]` *exec* form.

After a `RUN` instruction have been succesfully executed in the build-container,
a ZFS snapshot is created. Snapshotting instructions in this way makes it possible
to create containers from any point in an image's history.

The *exec* form makes it possible to avoid shell string munging, and to use `RUN`
commands with a base image that does not contain the shell executable.

Using a different shell, other than '/bin/sh', is also possible with the *exec*
form. For example:

```dockerfile
RUN ["/bin/bash", "-c", "echo hello"]
```

Since the *exec* form does not invoke a command shell, normal shell processing
does not happen. For example,
`RUN [ "echo", "$HOME" ]` will not do variable substitution on `$HOME`.
If you want shell processing then either use the *shell* form or execute
a shell directly, for example: `RUN [ "sh", "-c", "echo $HOME" ]`.
When using the exec form to execute a shell directly, it is the shell
that is doing the environment variable expansion, not Kleened.

> **Note**
>
> The *exec* form is parsed as a JSON array, which means that
> you must use double-quotes (") around words not single-quotes (').
> Also, in the *JSON* form, it is necessary to escape backslashes.

## CMD

The `CMD` instruction has two forms:

- `CMD ["executable","param1","param2"]` (*exec* form, this is the preferred form)
- `CMD command param1 param2` (*shell* form)

There can only be one `CMD` instruction in a `Dockerfile`. If you list more than
one `CMD` then only the last `CMD` will take effect.

**The main purpose of a `CMD` is to provide defaults for an executing
container, i.e., `CMD` does nothing during the image build and is only used by
containers.**

Since the *exec* form does not invoke a command shell, normal shell processing
does not happen. For example,
`CMD [ "echo", "$HOME" ]` will not do variable substitution on `$HOME`.
If you want shell processing then either use the *shell* form or execute
a shell directly, for example: `CMD [ "sh", "-c", "echo $HOME" ]`.
When using the exec form to execute a shell directly, it is the shell
that is doing the environment variable expansion, not Kleened.

> **Note**
>
> The *exec* form is parsed as a JSON array, which means that
> you must use double-quotes (") around words not single-quotes (').
> Also, in the *JSON* form, it is necessary to escape backslashes.

When used in the shell or exec formats, the `CMD` instruction sets the
default command to be executed when running containers based on the image.

When using the *shell* form of `CMD`, the `<command>` will execute in
`/bin/sh -c`:

```dockerfile
FROM FreeBSD
CMD echo "This is a test." | wc -
```

If `<command>` needs to be run without a shell, use the *exec* form and express
the command as a JSON array, giving the full path to the executable.
Any additional parameters must be individually expressed as strings in the array:

```dockerfile
FROM FreeBSD
CMD ["/usr/bin/wc","--help"]
```

If the user specifies a command to `klee run` it will override the
default specified by `CMD`.

## ENV

```dockerfile
ENV <key>=<value> ...
```

The `ENV` instruction sets the environment variable `<key>` to the value
`<value>`. This value will be in the environment for all subsequent instructions
and can be [substitued inline](#environment-replacement) in many instructions as well.
Outer quote characters will be removed if they are not escaped.
Like command line parsing, quotes and backslashes can be used to include spaces
within values.

Example:

```dockerfile
ENV MY_NAME="John Doe"
ENV MY_DOG=Rex\ The\ Dog
ENV MY_CAT=fluffy
```

The `ENV` instruction does *not* allow for multiple `<key>=<value> ...` variables to be set
at one time.

The environment variables set using `ENV` will persist when a container is run
from the resulting image. You can view the values using `klee inspect`, and
change them at container creation using, e.g., `klee run --env <key>=<value>`.

Environment variable persistence can cause unexpected side effects. For example,
setting `ENV DISTDIR=newdistfiles/` changes the behavior of `make` when building ports,
and may confuse users of your image.

If an environment variable is only needed during build, and not in the final
image, consider setting a value for a single command instead:

```dockerfile
RUN cd /usr/ports/www/nginx && BATCH=on DISTDIR=newdistfiles/ make install
```

Or using [`ARG`](#arg), which is not persisted in the final image:

```dockerfile
ARG BATCH=on
RUN cd /usr/ports/www/nginx && make install
```

## COPY

COPY has two forms:

```dockerfile
COPY <src>... <dest>
COPY ["<src>",... "<dest>"]
```

This latter form is required for paths containing whitespaces.

The `COPY` instruction copies content from the context given by `<src>`
into the container at `<dest>`.

Multiple `<src>` resources may be specified and the paths of files and
directories will be interpreted as relative to the source of the build
context.

Each `<src>` will be expanded using Erlangs's
[filelib.wildcard/1](https://www.erldocs.com/current/stdlib/filelib.html?#wildcard/1)
rules and then copied with the [`cp -R` command](https://man.freebsd.org/cgi/man.cgi?query=cp).
These external external resources, describes the mechanics of the
`COPY` instrcution. For instance, adding all files starting with "hom":

```dockerfile
COPY hom* /mydir/
```

In the next example, `?` is replaced with any single character, e.g., "home.txt".

```dockerfile
COPY hom?.txt /mydir/
```

`<dest>` is an absolute path, or a path relative to `WORKDIR`, into which
the source will be copied inside the destination container.

The example below uses a relative path, and adds "test.txt" to `<WORKDIR>/relativeDir/`:

```dockerfile
COPY test.txt relativeDir/
```

Another example adds "test.txt" to an absolute path `/absoluteDir/`:

```dockerfile
COPY test.txt /absoluteDir/
```

When copying files or directories that contain special characters (such as `[`
and `]`), you need to escape those paths following the
[`filelib.wildcard/1` rules](https://www.erldocs.com/current/stdlib/filelib.html?#wildcard/1)
to prevent them from being treated as a matching pattern.
For example, to copy a file named `arr[0].txt`, use the following;

```dockerfile
COPY arr\\[0\\].txt /mydir/
```

This is described in more detail in the documentation of
[filelib.wildcard/1](https://www.erldocs.com/current/stdlib/filelib.html?#wildcard/1).

All new files and directories are created with the `root` user.
Use `chown(8)` in a `RUN`-instruction if ownership of the copied files and
directories needs to be changed.

`COPY` obeys the following rules:

- The `<src>` path must be inside the *context* of the build, i.e.,
  `COPY ../something /something` is not possible.

- If `<src>` is a directory, the entire contents of the directory are copied,
  including filesystem metadata.

- If `<src>` is any other kind of file, it is copied individually along with
  its metadata. In this case, if `<dest>` ends with a trailing slash `/`, it
  will be considered a directory and the contents of `<src>` will be written
  *into* `<dest>`.

- If multiple `<src>` resources are specified, either directly or due to the
  use of a wildcard, then `<dest>` must be a directory, and it must end with
  a slash `/`.

- If `<dest>` does not end with a trailing slash, it will be considered a
  regular file and the contents of `<src>` will be written at `<dest>`.

- If `<dest>` doesn't exist, it is created along with all missing directories
  in its path.

## USER

```dockerfile
USER <user>[:<group>]
```

or

```dockerfile
USER <UID>[:<GID>]
```

The `USER` instruction sets the user name (or UID) and optionally the user
group (or GID) to use as the default user and group for the remainder of the
build. The specified user is used for `RUN` instructions, and runs the `CMD` command
in containers.

```dockerfile
FROM FreeBSD

# Create group and user in the container
RUN pw groupadd -q -n patrick
RUN pw useradd -n patrick -s /bin/sh -m -d /usr/home/patrick -G patrick -h -

# Set it for subsequent commands
USER patrick
```

> **Security considerations**
>
> When creating users in Dockerfiles, as shown in the example above, it might be worth to
> consider the following:
> 1. Is it necessary to use a password for the user? If no, then use `-h -` as above.
> 2. If the user requires a password, an option could be to use the `-H` flag to supply
>    the *hashed* password instead of clear-text. A hashed password can be generated using
>    `openssl` with `openssl passwd -6 <yourpass>` and supplied with a buildarg, e.g., like:
>    ```dockerfile
>    # The actual contents of the variable can be supplied by the CLI using the --build-arg flag
>    ARG HASHED_PASSWORD
>    RUN pw groupadd -q -n patrick
>    RUN echo -n "$HASHED_PASSWORD" $ |\
>        pw useradd -n patrick -s /bin/sh -m -d /usr/home/patrick -G patrick -H 0
>    ```
> See `pw(8)` and `openssl(1)` for details.
> 3. In general, passing secrets using CLI-parameters such as `--build-arg` can be
>    [problematic](https://blog.diogomonica.com//2017/03/27/why-you-shouldnt-use-env-variables-for-secret-data/)
>    since it can end up in, e.g., shell-history logs or elsewhere.
>    Instead, consider providing secrets as (encrypted) files mounted into the container.
{:.warning}

## WORKDIR

```dockerfile
WORKDIR /path/to/workdir
```

The `WORKDIR` instruction sets the working directory of any subsequent `RUN`, `CMD`,
and `COPY` instructions in the `Dockerfile`.
If the path specified in `WORKDIR` doesn't exist, it will be created even if it's
not used in any subsequent instructions.

> **Note**
>
> `WORKDIR` only works for `RUN` and `CMD` instructions in the *shell form*,
> and if `CMD` is replaced, the new command won't automatically be
> executed in `WORKDIR`.

The `WORKDIR` instruction can be used multiple times in a `Dockerfile`. If a
relative path is provided, it will be relative to the path of the previous
`WORKDIR` instruction. For example, in

```dockerfile
WORKDIR /a
WORKDIR b
WORKDIR c
RUN pwd
```

the output of the `pwd` command is `/a/b/c`.

The `WORKDIR` instruction can resolve environment variables previously set using
`ENV`. You can only use environment variables explicitly set in the `Dockerfile`.
For example, in

```dockerfile
ENV DIRPATH=/path
WORKDIR $DIRPATH/$DIRNAME
RUN pwd
```

the output of the `pwd` command is `/path/$DIRNAME`.

The default working directory is `/` and working directories
previously set in parent images will not be inherited.

## ARG

```dockerfile
ARG <name>[=<default value>]
```

The `ARG` instruction defines a variable that users can pass at build-time to
the builder with the `klee build` command using the `--build-arg <varname>=<value>`
flag.

A Dockerfile may include one or more `ARG` instructions. For example,
the following is a valid Dockerfile:

```dockerfile
FROM FreeBSD
ARG user1
ARG buildno
# ...
```

### Default values

An `ARG` instruction can optionally include a default value:

```dockerfile
FROM FreeBSD
ARG user1=someuser
ARG buildno=1
# ...
```

If an `ARG` instruction has a default value and if there is no value passed
at build-time, the builder uses the default. If no default value is specified
the empty string is used instead.

### Scope

An `ARG` variable definition comes into effect from the line on which it is
defined in the `Dockerfile`, and not from the argument's use on the command-line or
elsewhere. For example, consider this Dockerfile:

```dockerfile
FROM FreeBSD
USER ${username:-some_user}
ARG username
USER $username
# ...
```

A user builds this file by calling:

```console
$ klee build --build-arg username=what_user .
```

The `USER` at line 2 evaluates to `some_user` since the `username` variable is defined on
line 3. The `USER` at line 4 evaluates to `what_user`, as the `username` argument is
defined and the `what_user` value was passed on the command line. Prior to its definition by an
`ARG` instruction, any use of a variable results in an empty string.

### Using ARG variables

You can use an `ARG` or an `ENV` instruction to specify variables that are
available to the `RUN` instruction. Environment variables defined using the
`ENV` instruction always override an `ARG` instruction of the same name. Consider
this Dockerfile with an `ENV` and `ARG` instruction.

```dockerfile
FROM FreeBSD
ARG CONT_IMG_VER
ENV CONT_IMG_VER=v1.0.0
RUN echo $CONT_IMG_VER
```

Then, assume this image is built with this command:

```console
$ klee build --build-arg CONT_IMG_VER=v2.0.1 .
```

In this case, the `RUN` instruction uses `v1.0.0` instead of the `ARG` value
`v2.0.1` passed by the user. This behavior is similar to a shell
script where a locally scoped variable overrides the variables passed as
arguments or are inherited from environment, from its point of definition.

Using the example above but a different `ENV` specification you can create more
useful interactions between `ARG` and `ENV` instructions:

```dockerfile
FROM FreeBSD
ARG CONT_IMG_VER
ENV CONT_IMG_VER=${CONT_IMG_VER:-v1.0.0}
RUN echo $CONT_IMG_VER
```

Unlike an `ARG` instruction, `ENV` values are always persisted in the built
image. Consider a build without the `--build-arg` option:

```console
$ klee build .
```

In the previous example, `CONT_IMG_VER` is still persisted in the image but
its value would be `v1.0.0` as it is the default value set by the `ENV` instruction.

The variable expansion technique in this example allows you to pass arguments
from the command line and persist them in the final image by leveraging the
`ENV` instruction. Variable expansion is only supported for [a limited set of
Dockerfile instructions.](#environment-replacement)
