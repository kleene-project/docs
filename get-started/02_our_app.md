---
title: "Containerize an application"
keywords: get started, setup, orientation, quickstart, intro, concepts, containers
description: Containerize and run a simple application to learn Kleene
---

In the following guide you will try and deploy a simple Node.js webapp, based on
[Docker's get-started guide](https://docs.docker.com/get-started/02_our_app/).
This guide does not go into details of the webapp, so no prior
knowledge of Node.js or JavaScript is required.

### Pre-requisites

- A conceptual understanding of [containers and images](/get-started/overview/#the-kleene-components).
- Kleened and Klee [installed and configured on the host](/install/) so they can communicate with each other.
- `git`

## Get the app

Before you can run the application, you need to get the application source code onto your machine.

1. Clone the [getting-started repository](https://github.com/docker/getting-started/tree/master){:target="_blank" rel="noopener" class="_"} using the following command:

   ```console
   $ git clone https://github.com/docker/getting-started.git
   ```

2. View the contents of the cloned repository. Inside the `/app` directory of the repository you should see `package.json`, two subdirectories (`src` and `spec`),
   and perhaps a few other files.

## prepare the Kleened host

When you have a fresh installation, a few preparations is needed before you can start
building images and creating containers.

You need to create a [base image](/building/base-images/) and a network to use for the images and containers that are created in this guide.

1. Create a base image. The simplest way to do this is to let Kleened find and download an approriate relase of the FreeBSD userland:

   ```console
   $ klee image create fetch-auto
   ```

2. In order for you to isolate your containers from the host networking create a dedicated network to use for our containers:

   ```console
   $ klee network create --subnet 10.13.37.0/24 testnet
   ```

   In general it is good practice to connect your containers to a network
   instead of using the fallback `host` network driver, that does not use
   networks but comes with much less networking isolation compared to containers
   using the `ipnet` or `vnet` network driver.


## Build the app's container image

In order to build the [container image](/get-started/overview/#kleene-objects){:target="_blank" rel="noopener" class="_"}, you'll need to use a `Dockerfile`.
A Dockerfile contains the instructions that Kleened uses to create the image.

1. In the `app` directory mentioned previously, create a file named `Dockerfile`.

   You can use the following commands below to create a Dockerfile, replacing `/path/to/` with the path to your `getting-started` repository.

   ```console
   $ cd /path/to/app
   $ touch Dockerfile
   ```

2. Add the following contents to the Dockerfile:

   ```dockerfile
   FROM FreeBSD-13.2-RELEASE:latest
   RUN pkg install -y node20 npm-node20 yarn-node20
   WORKDIR /app
   COPY . .
   RUN yarn install --production
   # Listens on port 3000
   CMD cd /app && node src/index.js
   ```
   > **Note**
   >
   > Select an instruction in the Dockerfile example to learn more about the instruction.

4. Build the container image using the following commands:

   Assuming you are still in the `app` directory, run

   ```console
   $ klee build -t webapp .
   ```

   to build the container image.

   The `klee build` command uses the Dockerfile to build a new container image.
   The `Dockerfile` starts with `FROM FreeBSD-13.2-RELEASE:latest` that refers to the base-image we created previously,
   so it will be used as the foundation for our new `webapp` image.

   The remaining instructions from the Dockerfile installs the application dependencies, copies application data into the image, and uses `yarn` to install the application's JavaScript dependencies.
   The `CMD` directive specifies the default command to run when starting a container from this image, which in this case is set to run the application.

   Finally, the `-t` flag tags your image. Think of this simply as a human-readable name for the final image. Since you named the image `webapp`,
   you can refer to that image when you run a container. Since we have not specified a `tag`, Kleened tags the image with `latest`.

   The `.` at the end of the `klee build` command tells Kleene that it should look for the `Dockerfile` in the current directory.

   >**Note**
   >
   > The directory `.` is converted to its absolute path by Klee and then sent to Kleened.
   > *Kleened will then interpret this as a path on the machine where it is running*.
   > If Klee and Kleened are runnning on the same host this is fine, but if Klee is running
   > on a remote machine this will probably not work. In the latter case, remember to use absolute
   > paths on the host machine where Kleened is running.

## Start an app container

Now that you have an image, you can run the application in a [container](/get-started/overview/#kleene-objects){:target="_blank" rel="noopener" class="_"}.
To do so, you will use the `klee run` command. But first, we'll set up network for our containers.

1. Start your container and specify the name of the image you just created:

   ```console
   $ klee run -n testnet -d webapp
   ```

   Using `-n testnet` connects the new container to our recently created `testnet` network, which provides connectivity for your `webapp` container.
   The new container runs in "detached" mode (in the background) when the `-d` flag is used.

2. Verify that the container is running as expected using `klee lsc`. This command also shows the id and auto-generated name of your new container.
   It is also possible to verify that the container is running using the FreeBSD native tool `jls`:
   ```
   $ jls
      JID  IP Address      Hostname                      Path
        6  10.13.37.1                                    /zroot/kleene/container/d23e37375ffd
   ```
   This also shows the ip address of the container that is needed for accessing the web application.

3. After a few seconds, open your web browser to [http://10.13.37.1:3000](http://10.13.37.1:3000){:target="_blank" rel="noopener" class="_"}.
   If you are not running the container locally you might need to access the app at another location or use a port forward etc.
   For example, using portforward with `ssh` such as `ssh -L 3000:10.13.37.1:3000 ...` you should be able to access the web application
   on [http://localhost:3000](http://localhost:3000) instead.

   ![Empty todo list](images/todo-list-empty.png){: style="width:450px;margin-top:20px;"}
   {: .text-center }

4. Go ahead and add an item or two and see that it works as you expect. You can mark items as complete and remove items.
   Your frontend is successfully storing items in the backend.

At this point, you should have a running todo list manager with a few items, all built by you.

Note that our images and containers are just zfs datasets one the host. Use `zfs list` to get an overview of how Kleene
stores its objects.

## Next steps

Next, you're going to make a modification to your app and learn how to update your running application with a new image. Along the way, you'll learn a few other useful commands.

[Update the application](03_updating_app.md){: .button .primary-btn}
