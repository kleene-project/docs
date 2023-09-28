---
title: Packaging your software
keywords: build, buildx, buildkit, getting started, dockerfile
redirect_from:
- /build/hellobuild/
---

## Dockerfile

It all starts with a Dockerfile.

Docker builds images by reading the instructions from a Dockerfile. This is a
text file containing instructions that adhere to a specific format needed to
assemble your application into a container image and for which you can find
its specification reference in the [Dockerfile reference](../../engine/reference/builder.md).

Here are the most common types of instructions:

| Instruction                                                        | Description                                                                                                                                                                                              |
|--------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`FROM <image>`](../../engine/reference/builder.md#from)           | Defines a base for your image.                                                                                                                                                                           |
| [`RUN <command>`](../../engine/reference/builder.md#run)           | Executes any commands in a new layer on top of the current image and commits the result. `RUN` also has a shell form for running commands.                                                               |
| [`WORKDIR <directory>`](../../engine/reference/builder.md#workdir) | Sets the working directory for any `RUN`, `CMD`, `ENTRYPOINT`, `COPY`, and `ADD` instructions that follow it in the Dockerfile.                                                                          |
| [`COPY <src> <dest>`](../../engine/reference/builder.md#copy)      | Copies new files or directories from `<src>` and adds them to the filesystem of the container at the path `<dest>`.                                                                                      |
| [`CMD <command>`](../../engine/reference/builder.md#cmd)           | Lets you define the default program that is run once you start the container based on this image. Each Dockerfile only has one `CMD`, and only the last `CMD` instance is respected when multiple exist. |

Dockerfiles are crucial inputs for image builds and can facilitate automated,
multi-layer image builds based on your unique configurations. Dockerfiles can
start simple and grow with your needs and support images that require complex
instructions. For all the possible instructions, see the [Dockerfile reference](../../engine/reference/builder.md).

The default filename to use for a Dockerfile is `Dockerfile`, without a file
extension. Using the default name allows you to run the `docker build` command
without having to specify additional command flags.

Some projects may need distinct Dockerfiles for specific purposes. A common
convention is to name these `<something>.Dockerfile`. Such Dockerfiles can then
be used through the `--file` (or `-f` shorthand) option on the `docker build` command.
Refer to the ["Specify a Dockerfile" section](../../engine/reference/commandline/build.md#file)
in the `docker build` reference to learn about the `--file` option.

> **Note**
>
> We recommend using the default (`Dockerfile`) for your project's primary
> Dockerfile.

Docker images consist of **read-only layers**, each resulting from an
instruction in the Dockerfile. Layers are stacked sequentially and each one is
a delta representing the changes applied to the previous layer.

## Example

Here's a simple Dockerfile example to get you started with building images.
We'll take a simple "Hello World" Python Flask application, and bundle it into
a Docker image that can test locally or deploy anywhere!

Let's say we have a `hello.py` file with the following content:

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
```

Don't worry about understanding the full example if you're not familiar with
Python, it's just a simple web server that will contain a single page that
says "Hello World".

> **Note** 
>
> If you test the example, make sure to copy over the indentation as well! For
> more information about this sample Flask application, check the
> [Flask Quickstart](https://flask.palletsprojects.com/en/2.1.x/quickstart/){:target="blank" rel="noopener" class=""}
> page.

Here's the Dockerfile that will be used to create an image for our application:

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install flask==2.1.*

# install app
COPY hello.py /

# final configuration
ENV FLASK_APP=hello
EXPOSE 8000
CMD flask run --host 0.0.0.0 --port 8000
```

The first line to add to a Dockerfile is a [`# syntax` parser directive](../../engine/reference/builder.md#syntax).
While optional, this directive instructs the Docker builder what syntax to use
when parsing the Dockerfile, and allows older Docker versions with [BuildKit enabled](../buildkit/index.md#getting-started)
to use a specific [Dockerfile frontend](../buildkit/dockerfile-frontend.md)
before starting the build. [Parser directives](../../engine/reference/builder.md/#parser-directives)
must appear before any other comment, whitespace, or Dockerfile instruction in
your Dockerfile, and should be the first line in Dockerfiles.

```dockerfile
# syntax=docker/dockerfile:1
```

> **Note**
>
> We recommend using `docker/dockerfile:1`, which always points to the latest
> release of the version 1 syntax. BuildKit automatically checks for updates of
> the syntax before building, making sure you are using the most current version.

Next we define the first instruction:

```dockerfile
FROM ubuntu:22.04
```

Here the [`FROM` instruction](../../engine/reference/builder.md#from) sets our
base image to the 22.04 release of Ubuntu. All following instructions are
executed on this base image, in this case, an Ubuntu environment. The notation
`ubuntu:22.04`, follows the `name:tag` standard for naming docker images. When
you build your image you use this notation to name your images and use it to
specify any existing Docker image. There are many public images you can
leverage in your projects. Explore [Docker Hub](https://hub.docker.com/search?image_filter=official&q=&type=image){:target="blank" rel="noopener" class=""}
to find out.

```dockerfile
# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
```

This [`RUN` instruction](../../engine/reference/builder.md#run) executes a shell
command in the [build context](context.md).

In this example, our context is a full Ubuntu operating system, so we have
access to its package manager, apt. The provided commands update our package
lists and then, after that succeeds, installs `python3` and `pip`, the package
manager for Python.

Also note `# install app dependencies` line. This is a comment. Comments in
Dockerfiles begin with the `#` symbol. As your Dockerfile evolves, comments can
be instrumental to document how your dockerfile works for any future readers
and editors of the file.

> **Note**
>
> Starting your Dockerfile by a `#` like regular comments is treated as a
> directive when you are using BuildKit (default), otherwise it is ignored.

```dockerfile
RUN pip install flask==2.1.*
```

This second `RUN` instruction requires that we've installed pip in the layer
before. After applying the previous directive, we can use the pip command to
install the flask web framework. This is the framework we've used to write
our basic "Hello World" application from above, so to run it in Docker, we'll
need to make sure it's installed.

```dockerfile
COPY hello.py /
```

Now we use the [`COPY` instruction](../../engine/reference/builder.md#copy) to
copy our `hello.py` file from the local [build context](context.md) into the
root directory of our image. After being executed, we'll end up with a file
called `/hello.py` inside the image.

```dockerfile
ENV FLASK_APP=hello
```

This [`ENV` instruction](../../engine/reference/builder.md#env) sets a Linux
environment variable we'll need later. This is a flask-specific variable,
that configures the command later used to run our `hello.py` application.
Without this, flask wouldn't know where to find our application to be able to
run it.

```dockerfile
EXPOSE 8000
```

This [`EXPOSE` instruction](../../engine/reference/builder.md#expose) marks that
our final image has a service listening on port `8000`. This isn't required,
but it is a good practice, as users and tools can use this to understand what
your image does.

```dockerfile
CMD flask run --host 0.0.0.0 --port 8000
```

Finally, [`CMD` instruction](../../engine/reference/builder.md#cmd) sets the
command that is run when the user starts a container based on this image. In
this case we'll start the flask development server listening on all addresses
on port `8000`.

## Testing

To test our Dockerfile, we'll first build it using the [`docker build` command](../../engine/reference/commandline/build.md):

```console
$ docker build -t test:latest .
```

Here `-t test:latest` option specifies the name (required) and tag (optional)
of the image we're building. `.` specifies the [build context](context.md) as
the current directory. In this example, this is where build expects to find the
Dockerfile and the local files the Dockerfile needs to access, in this case
your Python application.

So, in accordance with the build command issued and how [build context](context.md)
works, your Dockerfile and python app need to be in the same directory.

Now run your newly built image:

```console
$ docker run -p 8000:8000 test:latest
```

From your computer, open a browser and navigate to `http://localhost:8000`

> **Note**
>
> You can also build and run using [Play with Docker](https://labs.play-with-docker.com){:target="blank" rel="noopener" class=""}
> that provides you with a temporary Docker instance in the cloud.

## Image design
The following development patterns have proven to be helpful for people
building applications with Docker. If you have discovered something we should
add,
[let us know]({{ site.repo }}/issues/new){: target="_blank" rel="noopener" class="_"}.

### How to keep your images small

Small images are faster to pull over the network and faster to load into
memory when starting containers or services. There are a few rules of thumb to
keep image size small:

- If you have multiple images with a lot in common, consider creating your own
  [base image](../build/building/base-images.md) with the shared
  components, and basing your unique images on that. Docker only needs to load
  the common layers once, and they are cached. This means that your
  derivative images use memory on the Docker host more efficiently and load more
  quickly.

- To keep your production image lean but allow for debugging, consider using the
  production image as the base image for the debug image. Additional testing or
  debugging tooling can be added on top of the production image.

- When building images, always tag them with useful tags which codify version
  information, intended destination (`prod` or `test`, for instance), stability,
  or other information that is useful when deploying the application in
  different environments. Do not rely on the automatically-created `latest` tag.

### Where and how to persist application data

- Store data using [volumes](../storage/volumes.md).
- One case where it is appropriate to use
  [bind mounts](../storage/bind-mounts.md) is during development,
  when you may want to mount your source directory or a binary you just built
  into your container. For production, use a volume instead, mounting it into
  the same location as you mounted a bind mount during development.
- For production, use [secrets](../engine/swarm/secrets.md) to store sensitive
  application data used by services, and use [configs](../engine/swarm/configs.md)
  for non-sensitive data such as configuration files. If you currently use
  standalone containers, consider migrating to use single-replica services, so
  that you can take advantage of these service-only features.
