---
description: How to setup and run Kleene with SSH or HTTPS
keywords: kleene, kleened, daemon, security, ssh, tls, ca,  certificate
title: Protect the Kleened socket
---

## Kleened attack surface

Since the creation of containers, firewall manipulation etc. requires root, the
Kleene backend daemon (Kleened) runs with `root` privileges.
Given the capabilities of the Kleened API implies that having access to Kleened is
equivalent to *having full root access to the host machine*. Therefore, obviously,
**only trusted users should have access to Kleened**.

For this reason, the REST API endpoint uses a UNIX socket by default,
instead of, e.g., a TCP socket bound on 127.0.0.1 (or similar widely accessable
TCP socket). You can then use traditional UNIX permission checks to limit
access to the control socket.

You can expose the REST API over TCP if you explicitly decide to do so.
However, if you do that, be aware of the above mentioned security
implications.
Note that even if you have a firewall to limit accesses to the REST API
endpoint from other hosts in the network, the endpoint can still be accessible
from containers, and it can easily result in the privilege escalation.
Therefore it is *mandatory* to secure exposed API endpoints with
TLS and certificates, as described in the following.
It is also recommended to ensure that it is reachable only from a trusted
network and/or VPN.

## Use SSH to access the Kleened daemon socket

You can use `ssh -L /path/to/kleened.sock:/var/run/kleened.sock`
if you need remote access to Kleened. However, the drawback is
that the user on the host needs to have direct access to the root socket.

## Use TLS (HTTPS) to protect the Kleened socket

If you need Kleened to be reachable through TCP in a safe manner,
you can configure TLS (HTTPS) for both Klee and Kleened.

There are essentially the following scenarios:

- Establish connections using a self-signed certificate. Neither Klee nor
  Kleened check certificate is correct and thus do not know if they are talking
  to the correct party. **Not very secure!**

- Establish connections using certificates signed by a CA in two different
  scenarios:
    1. Klee verifies if Kleened's sever certificate is from a trusted CA.
    2. In addition the above, Kleened also requests a valid client certificate from Klee.

  The latter is by far the most secure since it ensures that both client and
  server knows that they are talking to the right party. Unless explicitly
  specified, Klee relies on the [CA bundle from `py-certifi`](https://pypi.org/project/certifi/).
  For Kleened, a specific CA-cert needs to be specified. If a common bundle is needed,
  consider using the [`ca_root_nss` package](https://www.freshports.org/security/ca_root_nss/)
  (similar to `py-certifi`).

In the following, the latter scenario is chosen where both Klee and Kleened uses
a certificate signed by a CA.

> Advanced topic
>
> Using TLS and managing a CA is an advanced topic. Please familiarize yourself
> with OpenSSL, x509, and TLS before using it in production.
{:.important}

### Create a CA, server and client keys with OpenSSL

> **Note**: Replace all instances of `$HOST` in the following example with the
> DNS name of your Kleened daemon's host.

First, on the **Kleened host machine**, generate CA private and public keys:

```console
$ openssl genrsa -aes256 -out ca-key.pem 4096
Generating RSA private key, 4096 bit long modulus
..............................................................................++
........++
e is 65537 (0x10001)
Enter pass phrase for ca-key.pem:
Verifying - Enter pass phrase for ca-key.pem:

$ openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem
Enter pass phrase for ca-key.pem:
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:
Locality Name (eg, city) []:
Organization Name (eg, company) [Internet Widgits Pty Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:$HOST
Email Address []:John@example.com
```

Now that a CA has been created, create the server key and certificate
signing request (CSR). Make sure that "Common Name" matches the hostname used
to connect to Kleened:

> **Note**: Replace all instances of `$HOST` in the following example with the
> DNS name of the Kleened host.

```console
$ openssl genrsa -out server-key.pem 4096
Generating RSA private key, 4096 bit long modulus
.....................................................................++
.................................................................................................++
e is 65537 (0x10001)

$ openssl req -subj "/CN=$HOST" -sha256 -new -key server-key.pem -out server.csr
```

Next, sign the public key with the CA:

Since TLS connections can be made through IP address as well as DNS name, the IP addresses
need to be specified when creating the certificate. For example, to allow connections
using `10.10.10.20` and `127.0.0.1`:

```console
$ echo subjectAltName = DNS:$HOST,IP:10.10.10.20,IP:127.0.0.1 >> extfile.cnf
```

Set Kleened key's extended usage attributes to be used only for
server authentication:

    $ echo extendedKeyUsage = serverAuth >> extfile.cnf

Now, generate the signed certificate:

```console
$ openssl x509 -req -days 365 -sha256 -in server.csr -CA ca.pem -CAkey ca-key.pem \
  -CAcreateserial -out server-cert.pem -extfile extfile.cnf
Signature ok
subject=/CN=your.host.com
Getting CA Private Key
Enter pass phrase for ca-key.pem:
```

For Klee client authentication, create a client key and certificate signing
request:

> **Note**: For simplicity of the next couple of steps, perform this
> step on the Kleend host machine as well.

```console
$ openssl genrsa -out key.pem 4096
Generating RSA private key, 4096 bit long modulus
.........................................................++
................++
e is 65537 (0x10001)

$ openssl req -subj '/CN=client' -new -key key.pem -out client.csr
```

To make the key suitable for client authentication, create a new extensions
config file:

    $ echo extendedKeyUsage = clientAuth > extfile-client.cnf

Now, generate the signed certificate:

```console
$ openssl x509 -req -days 365 -sha256 -in client.csr -CA ca.pem -CAkey ca-key.pem \
  -CAcreateserial -out cert.pem -extfile extfile-client.cnf
Signature ok
subject=/CN=client
Getting CA Private Key
Enter pass phrase for ca-key.pem:
```

After generating `cert.pem` and `server-cert.pem` the two certificate signing requests
and extensions config files can be removed:

```console
$ rm -v client.csr server.csr extfile.cnf extfile-client.cnf
```

With a default `umask` of 022, the secret keys are *world-readable* and
writable for the present user and it's group.

To protect the keys from accidental damage, remove their
write permissions. To make them only readable by the present user, change file modes as follows:

```console
$ chmod -v 0400 ca-key.pem key.pem server-key.pem
```

Certificates can be world-readable, but you might want to remove write access to
prevent accidental damage:

```console
$ chmod -v 0444 ca.pem server-cert.pem cert.pem
```

Now, configure Kleened to only accept connections from clients that
presents a certificate trusted by the CA, replacing the previous socket
configuration with this:

```yaml
# '/path/to/' could be '/usr/local/etc/kleened/certs/'
api_listening_sockets:
    - address: "https://127.0.0.1:8085"
      tlsverify: true
      tlscacert: "/path/to/ca.pem"
      tlscert: "/path/to/server-cert.pem"
      tlskey: "/path/to/server-key.pem"
```

in `/usr/local/etc/kleened/kleened_config.yaml`.

To connect to Kleened and validate its certificate and present it's client
certifcate:

```console
$ klee --tlsverify \
    --tlscacert=/path/to/ca.pem \
    --tlscert=/path/to/cert.pem \
    --tlskey=/path/to/key.pem \
    -H=$HOST:8085 version
```

This step should be run on your Klee client machine. As such, you
need to copy your CA certificate and the client cert + key to that machine.

> **Warning**:
> Note that you don't need to run `klee` with `sudo` when you use certificate
> authentication. That means anyone with the keys have root access to the
> Kleened host. Guard these keys accordingly!
{:.warning}

#### Connecting to the secure Kleened port using `curl`

To use `curl` to make test API requests, you need to use three extra command line
flags:

```console
$ curl https://$HOST:2376/images/list \
  --cert /path/to/cert.pem \
  --key /path/to/key.pem \
  --cacert /path/to/ca.pem
```

## Use a combination of SSH and TLS

Yet another approach is to combine the certificate approach, desecribed below,
to expose Kleened through a TLS-socket on, e.g., 127.0.0.1, and then
make a SSH portward from the client. You thus gain:

- The possibilty to leverage sophisticated authentication mechanisms of SSH
  (like 2FA) to gain host access, while

- Protecting the socket on 127.0.0.1 with mutual (client/server) TLS to add a layer
  of security against unintended access from containers or applications running on
  the host.
