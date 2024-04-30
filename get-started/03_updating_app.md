---
title: "Update the application"
keywords: get started, setup, orientation, quickstart, intro, concepts, containers
description: Making changes to our example learning application
---

In [part 2](./02_our_app.md), you containerized a todo application.
In this part, you will update the application image and corresponding container.

## Update the source code

In the steps below, you will change the "empty text" when you don't have any todo list items to "You have no todo items yet! Add one above!"


1. In the `src/static/js/app.js` file, update line 56 to use the new empty text.

    ```diff
    ...
    -                <p className="text-center">No items yet! Add one above!</p>
    +                <p className="text-center">You have no todo items yet! Add one above!</p>
    ...
    ```

2. Build your updated version of the image, using the `klee build` command you used in [part 2](./02_our_app.md/#build-the-apps-container-image){:target="_blank" rel="noopener" class="_"}.

   ```console
   $ klee build -t webapp .
   ```

3. Start a new container using the updated code.

    ```console
    $ klee run -n testnet -d webapp
    ```

This will run a new instance of your app on another ip. Verify with `jls`:

```console
$ jls
   JID  IP Address      Hostname                      Path
     6  10.13.37.1                                    /zroot/kleene/container/d23e37375ffd
    12  10.13.37.2                                    /zroot/kleene/container/d43830c2e296
```

You can now verify that the todo app hosted on `10.13.37.2` is the updated version.
Now, it's time to replace the old todo app with the updated one.

## Remove the old container

To remove a container, you first need to stop it.

4. Get the ID of the container by using the `klee lsc` command.

5. Use the `klee stop` command to stop the container. Replace &lt;the-container-id&gt; with the ID from `klee lsc`.

    ```console
    $ klee stop <the-container-id>
    ```

6. Once the container has stopped, you can remove it by using the `klee rmc` command.

    ```console
    $ klee rmc <the-container-id>
    ```

Repeat the last three steps to remove the updated container as well, and spin up a new container (step 3).

>**Note**
>
>You can stop and remove a container in a single command by adding the `force` flag to the `klee rmc` command. For example: `klee rmc -f <the-container-id>`

### Start the updated app container

7. Now, start your updated app using the `klee run` command from step 3 and the updated app can be accessed on the original IP `10.13.37.1`.

8. Refresh your browser window from the previous chapter and see the updated text.

![Updated application with updated empty text](images/todo-list-updated-empty-text.png){: style="width:55%" }
{: .text-center }

## Next steps

While you were able to build an update, there were two things you might have noticed:

- All of the existing items in your todo list are gone! That's not a very good app! You'll fix that
shortly.
- There were a lot of steps involved for such a small change. In the next section, you'll learn
how to see code updates without needing to rebuild and start a new container every time you make a change.

[Persist application data](04_persisting_data.md){: .button .primary-btn}
