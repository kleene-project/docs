---
title: "Multi container apps"
keywords: get started, setup, quickstart
description: Using more than one container in our application
---

Up to this point, we have been working with single container apps. Now it is time to add a more
advanced RDBMS to the application stack. Since the the application supports both SQLite and
MySQL, and MariaDB, we will use the latter for our new production-like setup.
We will run MariaDB in a seperate container. A few reasons for using a seperate container
for the database:

- There's a good chance you'd have to scale APIs and front-ends differently than databases
- Separate containers let you version and update versions in isolation
- While you may use a container for the database locally, you may want to use a managed service
  for the database in production. You don't want to ship your database engine with your app then.

So, we will update our application to work like this:

![Todo App connected to MySQL container](images/multi-app-architecture.png)
{: .text-center }

## Container networking

In [part 2](./02_our_app.md) we created a network to provide upstream/internet connectivity to our
container. To enable private inter-container connectivity between containers they
should be connected to the same network.

While you don't have to be a network engineer (hooray!). The following simple rule
(not immune to plenty of deviations) serves well for a start:

> **Note**
>
> If two containers are on the same network, they can talk to each other. If they aren't, they can't.

Generally, there are two ways to put a container on a network:
1) Assign it during creation or
2) connect an existing container to a network.
For now, we will continue to do the former, but if you need a container
to be connected to several networks og to change network configurations later,
the latter approach will come in handy.

Go [here](/run/network) if you want to know more about networking.

## Build and start a MariaDB-container

1. We start by creating a new image and container for our new RDBMS.
   From [part 4](./04_persisting_data.md) we learned how to persist data so let's
   start by creating a volume for the database in our new MariaDB-container:

   ```
   $ klee volume create myapp_db
   ```

   Next, save the following content in the file `Dockerfile.mariadb`

   ```dockerfile
   FROM FreeBSD-13.2-RELEASE:latest
   RUN pkg install -y mariadb106-client mariadb106-server

   CMD service mysql-server onestart && \
       mysql -u root -e "CREATE DATABASE IF NOT EXISTS $DATABASE_NAME;" && \
       mysql -u root -e "CREATE USER IF NOT EXISTS 'webapp'@'%' IDENTIFIED BY '$DATABASE_PASSWORD';" && \
       mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'webapp'@'%' WITH GRANT OPTION;" && \
       mysql -u root -e "FLUSH PRIVILEGES;"
   ```

   That could be stored in same directory as the previous Dockerfiles but it doesn't
   matter since no context is used for the build.

   Build the container:

   ```
   $ klee build -t MariaDB -f Dockerfile.rdbms .
   ```

   The large `CMD`-instruction ensures that the database is started and configured at container runtime,
   which can be done by starting a MariaDB-container:

   ```console
   $ klee run -n testnet --ip 10.13.37.1 -m todo-db:/var/db/mysql -e DATABASE_NAME=todos -e DATABASE_PASSWORD=secret MariaDB:latest
   ```

   The options do the following:

   1. Connect the container to our `testnet` network. This time we provide a specific IP in the subnet, so we know where to connect to.
   2. Our newly created volume is mounted to `/var/db/mysql` where MariaDB stores its data.
   3. Two environment variables is supplied which configures MariaDB at startup as per the multi-line `CMD`-instruction.


   > **Setting Connection Settings via Env Vars**
   >
   > While using env vars to set connection settings is generally ok for development, it is **HIGHLY DISCOURAGED**
   > when running applications in production. Diogo Monica, a former lead of security at Docker,
   > [wrote a fantastic blog post](https://diogomonica.com/2017/03/27/why-you-shouldnt-use-env-variables-for-secret-data/){:target="_blank" rel="noopener" class="_"}
   > explaining why.

2. To confirm we have the database up and running, connect to the database and verify it connects.

    ```console
    $ klee exec -it <mariadb-container-id> mysql
    ```

    In the MariaDB shell, list the databases and verify you see the `todos` database.

    ```console
    mysql> SHOW DATABASES;
    ```

    You should see output that looks like this:

    ```plaintext
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | mysql              |
    | performance_schema |
    | sys                |
    | todos              |
    +--------------------+
    5 rows in set (0.00 sec)
    ```
    Exit the MariaDB shell to return to the shell on our machine.

   ```console
   mysql> exit
   ```

   Hooray! We have our `todos` database and it's ready for us to use!

## Run your app with MySQL

The todo app supports the setting of a few environment variables to specify MySQL connection settings. They are:

- `MYSQL_HOST` - the hostname or IP for the running MySQL server. `10.13.37.1` in this example.
- `MYSQL_USER` - the username to use for the connection. `webapp` is used here (see where this is set in `Dockerfile.mariadb`?)
- `MYSQL_PASSWORD` - the password to use for the connection. `secret` as defined previously.
- `MYSQL_DB` - the database to use once connected. `todos`  as defined previously.

With all of that explained, let's start our dev-ready container!

1. We'll specify each of the environment variables above, as well as connect the container to our app network.

    ```console
    $ klee run -m /home/vagrant/getting-started/app:/app \
      -n testnet \
      --ip 10.13.37.2 \
      -e MYSQL_HOST=10.13.37.1 \
      -e MYSQL_USER=webapp \
      -e MYSQL_PASSWORD=secret \
      -e MYSQL_DB=todos \
      webapp-dev
    ```

3. The container shows a bunch of output to the terminal and we should see a message indicating it's
   using the mysql database:

   ```console
   $ nodemon src/index.js
   [nodemon] 2.0.20
   [nodemon] to restart at any time, enter `rs`
   [nodemon] watching path(s): *.*
   [nodemon] watching extensions: js,mjs,json
   [nodemon] starting `node src/index.js`
   Waiting for 10.13.37.1:3306.
   Connected!
   Connected to mysql db at host 10.13.37.1
   Listening on port 3000
   ```

   Pressing `Ctrl`+`C` exits terminal from the jail, but it is still running in the background.
   As previously, you can check for yourself by using `jls` or `klee lsc`.

4. Open the app in your browser and add a few items to your todo list.

5. Connect to the mysql database and prove that the items are being written to the database. Remember, the password
   is **secret**.

    ```console
    $ klee exec -it <mysql-container-id> mysql
    ```

    And in the mysql shell, run the following:

    ```console
    root@localhost [(none)]> select * from todos.todo_items;
    +--------------------------------------+--------------------+-----------+
    | id                                   | name               | completed |
    +--------------------------------------+--------------------+-----------+
    | c906ff08-60e6-44e6-8f49-ed56a0853e85 | Do amazing things! |         0 |
    | 2912a79e-8486-4bc3-a4c5-460793a575ab | Be awesome!        |         0 |
    +--------------------------------------+--------------------+-----------+
    ```

    Obviously, your table will look different because it has your items. But, you should see them stored there!

## Next steps

At this point, you have an application that now stores its data in an external database running in a separate
container.

If you want to dig deeper into Kleene, consider looking in:

1. [Building images](/building/introduction/)
2. [Running containers](http://localhost:4000/run/introduction/)
