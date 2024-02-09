---
title: "Using nullfs mounts"
keywords: >
  get started, setup
description: Using nullfs mounts in our application
---

In the previous chapter, we talked about and used a volume mount to persist the
data in our database. A volume mount is a great choice when you need somewhere
persistent to store your application data within Kleene.

A nullfs mount is another type of mount, which lets you share a directory from the
host's filesystem into the container. When working on an application, you can
use a nullfs mount to mount source code into the container. Another usecase can be
the need to make contents available from external storage such as `nfs`.

In this chapter, we'll see how we can use nullfs mounts and a tool called
[nodemon](https://npmjs.com/package/nodemon){:target="_blank" rel="noopener"
class="_"} to watch for file changes, and then restart the application
automatically. There are equivalent tools in most other languages and
frameworks.

## Quick volume type comparisons

The following table outlines the main differences between volume mounts and nullfs
mounts.

|                                    | Named volumes                                          | Nullfs mounts                                        |
| ---------------------------------- | ------------------------------------------------------ | ---------------------------------------------------- |
| Host location                      | Kleened stores it under the `<zroot>/volumes` dataset  | You decide                                           |
| Mount example (using `--mount`)    | `my-volume:/usr/local/data`                            | `/path/to/data:/usr/local/data`                      |

Under the hood, volume mounts are also nullfs mounts where Kleene manages the
underlying ZFS filesystem.

Nullfs mounts are, as the name suggests, mountpoints created using the `nullfs(5)`
file system layer of FreeBSD.

## Trying out Kleene's nullfs mounts

Before looking at how we can use nullfs mounts for developing our application,
let's run a quick experiment to get a practical understanding of how they work.

1. Open a terminal and and go to the `app` directory of the getting started repository.

2. Run the following command to start `sh` in an fresh container with a
   nullfs mount.

   ```console
   $ klee run -it --mount /vagrant/getting-started:/mnt FreeBSD-13.2-RELEASE /bin/sh
   ```

   The `--mount` option tells Kleene to create a nullfs mount, where `/vagrant/getting-started`
   is the app-repos on our app on our laptop with `/vagrant` being the NFS-mount from our laptop
   into our Vagrant virtual development machine.
   `/mnt` is where that directory should be mounted inside the container.

3. After running the command, Klee starts an interactive `sh` session in the
   root directory of the container's filesystem.
   Now, list the contents of `/mnt` within the container:

   ```console
   # ls /mnt
   ls /mnt
   .dockerignore           LICENSE                 docs
   .git                    README.md               mkdocs.yml
   .github                 app                     requirements.txt
   .gitignore              build.sh
   Dockerfile              docker-compose.yml
   ```

   This is the directory that you mounted when starting the container. Listing
   the contents of this directory displays the same files as in the
   `getting-started` directory on our laptop.

4. Create a new file named `myfile.txt`.

   ```console
   # touch /mnt/myfile.txt
   # ls /mnt
   .dockerignore           LICENSE                 docs
   .git                    README.md               mkdocs.yml
   .github                 app                     myfile.txt
   .gitignore              build.sh                requirements.txt
   Dockerfile              docker-compose.yml
   ```

5. Now if you open this directory on the host, you'll see the `myfile.txt` file
   has been created in the directory.

6. From the host, delete the `myfile.txt` file and look into the container again.
   The file has disappeared.

7. Type `exit` in the container-console to exit the container and close the session.

This demonstrated how files are shared between the host and the container, and how
changes are immediately reflected on both sides. Now let's see how we can use
nullfs mounts during application development.

## Run your app in a development container

The following steps describe how to run a development container does the following:

- Nullfs-mount our source code stored on the host in `/home/jane/getting-started/app`, into the container.
- Install all dependencies
- Start `nodemon` to watch for filesystem changes

So, let's do it!

1. Make sure to delete any `webapp` containers previously created.

2. Make a Dockerfile for a new image that *does not* contain the application
   source code. In this example, the easy way is to build on the existing image
   where `node` and `yarn` are already installed. Ideally we would split up the first
   image in two, such that we had a 'base image' containing the necessary software
   packages and another image for setting up our application.

   Save the following content in `Dockerfile.dev`

   ```
   FROM webapp:latest
   RUN rm -rf /app
   # Listens on port 3000
   CMD cd /app && yarn install && yarn run dev
   ```

   in same directory as the other Dockerfile.
   The `CMD` instruction starts a Bourne shell (`sh`) and runs `yarn install` to
   install dependency packages and then running `yarn run dev` to start
   the development server. If we look in the `package.json`, we'll see that
   the `dev` script starts `nodemon`.

4. Build the new image in a similar way as the previous image:

   ```
   $ klee build -t webapp-dev -f Dockerfile.dev .
   ```
   We explicitly tell Kleene which Dockerfile should be used for the build with `-f Dockerfile.dev`,
   thus avoiding the default `Dockerfile` we created previously.
   The above command should be executed in the `getting-started/app` directory.

5. Run the following command from the `getting-started/app` directory.

   ```console
   $ klee run -n testnet --mount /home/jane/getting-started/app:/app webapp-dev
   ```

   - The `-d` flag is omitted so the container output will be printed to the terminal.
   - The `-n testnet` connects the container to our testing network.
   - `--mount /home/jane/getting-started/app:/app` - nullfs mount our
     application source code from the host into the `/app` directory
     in the container.
   - `webapp-dev` - the image to use. This is our newly built image from above.

   You should see output similar to this:
 
   ```
   <initial output here>
   $ nodemon src/index.js
   2.0.20
   to restart at any time, enter `rs`
   watching path(s): *.*
   watching extensions: js,mjs,json
   starting `node src/index.js`
   Using sqlite database at /etc/todos/todo.db
   Listening on port 3000
   ```
   
   Now you can hit `Ctrl`+`C` to return to the terminal prompt. Don't worry,
   your container is stilling running. Use `klee lsc` to be sure.

8. Now, make a change to the app. In the `src/static/js/app.js` file, on line
   109, change the "Add Item" button to simply say "Add":

   ```diff
   - {submitting ? 'Adding...' : 'Add Item'}
   + {submitting ? 'Adding...' : 'Add'}
   ```

   Save the file.

9. Refresh the page in your web browser, and you should see the change reflected
   almost immediately. It might take a few seconds for the Node server to
   restart. If you get an error, try refreshing after a few seconds.

   ![Screenshot of updated label for Add button](images/updated-add-button.png){:
   style="width:75%;" .text-center}

Using nullfs mounts is useful for local development setups. The advantage is that
the development machine doesn't need to have all of the build tools and
environments installed. With a single `klee run` command, dependencies and
tools are ready to go.

## Next steps

In order to prepare for production, you need to migrate your database from
working in SQLite to something that can scale a little better. For simplicity,
you'll keep with a relational database and switch your application to use MySQL.
But, how should you run MySQL? How do you allow the containers to talk to each
other? You'll learn about that next!

[Multi container apps](06_multi_container.md){: .button .primary-btn}
