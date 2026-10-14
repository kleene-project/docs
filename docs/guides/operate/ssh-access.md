---
description: Forward the Kleened socket over an SSH tunnel
title: SSH access to the Kleened socket
---

## Use SSH to access the Kleened daemon socket

`ssh -L /path/to/kleened.sock:/var/run/kleened.sock` can be used to get
remote access to Kleened. However, the drawback is that the user on the
host needs to have access to the root socket.

## Use a combination of SSH and TLS

Another approach is to combine the certificate protected TLS-socket,
desecribed above, with the SSH + portward method described in the beginning.

Combining these gives:

- The possibilty to leverage sophisticated authentication mechanisms of SSH
  (like 2FA) to gain host access, while

- Protecting the socket on 127.0.0.1 with mutual (client/server) TLS to add a layer
  of security against unintended access from containers or applications running on
  the host.
