---
title: Customizing the firewall
description: How to add you own custom firewall rules to PF
keywords: networking, customization, expose ports, publish ports
---

Kleene manages the [PF](https://docs.freebsd.org/en/books/handbook/firewalls/#firewalls-pf)
firewall but it is also possible to add additional firewall rules together with
Kleene's. This section describes how and provides a simple example.

> **Note**
>
> Customizing the firewall can cause unpredicted networking behavior in Kleene
> as the custom configurations can interfere with Kleene's own rules.
> In case of problems, go to the
> [networking debuggingpage](/run/network/troubleshoot/).

## Configuring a Kleene-managed firewall

When networking-related change occurs, such as creating a network,
connecting a container to a network etc. Kleene updates the firewall
configuration by

- Updating its firewall rules and inserting them into the firewall
  [configuration file](https://man.freebsd.org/cgi/man.cgi?query=pf.conf)
  template.
  The default location of the template is `/usr/local/etc/kleened/pf.conf.kleene`.

- The rendered template is then written to an actual `pf.conf` file
   in `/etc/pf.conf` and then PF is updated using this new firewall
   configuration file.

The locations of the template and PF-config file can be configured
in `/usr/local/etc/kleened_config.yaml`.

Therefore, it is possible to add custom firewall rules in the template-file
as long as the Kleene tags `<%= kleene_macros %>`, `<%= kleene_translation %>`,
and `<%= kleene_filtering %>` is present in the correct order etc.
Furthermore, after a network operation such as creating a network or connecting
a container, or a restart of Kleened, the template will be rendered to `/etc/pf.conf`
which can then be inspected, to verify that the final configuration file looks
as expected. The following example shows this i practice.

## Example: Blocking incoming traffic on the Kleene host

In many cases it is desirable to block all incoming traffic on the physical
interface, if not explicitly allowed to reach a service.

This means that the baseline template config (excluding the preamble-comment)

```
### KLEENED MACROS START ###
<%= kleene_macros %>
### KLEENED MACROS END #####

### KLEENED TRANSLATION RULES START ###
<%= kleene_translation %>
### KLEENED TRANSLATION RULES END #####

### KLEENED FILTERING RULES START #####
<%= kleene_filtering %>
### KLEENED FILTERING RULES END #######
```

is expanded to include a general blocking rule:

```
set block-policy drop
ext_if="em0"

### KLEENED MACROS START ###
<%= kleene_macros %>
### KLEENED MACROS END #####

scrub in on $ext_if all fragment reassemble

### KLEENED TRANSLATION RULES START ###
<%= kleene_translation %>
### KLEENED TRANSLATION RULES END #####

# block everything
block log all
# Allow our client to SSH into the host
pass in quick on $ext_if from 10.0.2.2 to 10.0.2.15 port 22

### KLEENED FILTERING RULES START #####
<%= kleene_filtering %>
### KLEENED FILTERING RULES END #######
```

which is saved at `/usr/local/etc/pf.conf.kleene`. Note that a couple of
additional statements have been added:

- We explicitly allow the client to reach the host by SSH
- The blocking policy is explicitly set to just drop blocked packets
- The `scrub ...` statement makes the firewall sanitize incoming traffic on the
  physical interface.

See `pf.conf(5)` for details.

We restart Kleene and create a network and a bunch of containers. After the
restart, any open ssh-connections might disconnect. Also, it might be a good
idea to test the custom firewall settings in safe manner to avoid being kicked
out of the host.

```console
$ klee network create --subnet 10.23.45.0/24 testnet
3069bfded2bb
$ klee run --network testnet --name container2 -J allow.raw_sockets=true FreeBSD
...
b06f4c1f9685 has exited with exit-code 0
$ klee run --network testnet --name container2 -J allow.raw_sockets=true FreeBSD
...
9df2c3546ecb has exited with exit-code 0
$ jls
   JID  IP Address      Hostname                      Path
     1  10.23.45.1                                    /zroot/kleene/container/d824d5fb64bc
     2  10.23.45.2                                    /zroot/kleene/container/6a6b58ca41ce
$ sudo jexec 1 /sbin/ping 10.23.45.2
PING 10.23.45.2 (10.23.45.2): 56 data bytes
64 bytes from 10.23.45.2: icmp_seq=0 ttl=64 time=0.138 ms
64 bytes from 10.23.45.2: icmp_seq=1 ttl=64 time=0.699 ms
64 bytes from 10.23.45.2: icmp_seq=2 ttl=64 time=0.636 ms
^C
--- 10.23.45.2 ping statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 0.138/0.491/0.699/0.251 ms
```

Voila! The containers can reach each other. Inspecting the PF configuration file
`/etc/pf.conf`

```
$ cat /etc/pf.conf
set block-policy drop
ext_if="em0"

### KLEENED MACROS START ###
kleenet_host_gw_if="em0"
kleenet_network_interfaces="{lo0, kleene0}"
kleenet_3069bfded2bb_interface="kleene0"
kleenet_3069bfded2bb_subnet="10.23.45.0/24"
kleenet_3069bfded2bb_nat_if="em0"
kleenet_3069bfded2bb_all_interfaces="{kleene0, lo0}"
#### KLEENED MACROS END #####

scrub in on $ext_if all fragment reassemble

### KLEENED TRANSLATION RULES START ###
nat on $kleenet_3069bfded2bb_nat_if from ($kleenet_3069bfded2bb_interface:network) to any -> ($kleenet_3069bfded2bb_nat_if)
### KLEENED TRANSLATION RULES END #####

# block everything
block log all
# Allow our client to SSH into the host
pass in quick on $ext_if proto tcp from 10.0.2.2 to 10.0.2.15 port 22

### KLEENED FILTERING RULES START #####
block in log from any to $kleenet_3069bfded2bb_subnet
pass quick on $kleenet_3069bfded2bb_all_interfaces from $kleenet_3069bfded2bb_subnet to $kleenet_3069bfded2bb_subnet
### KLEENED FILTERING RULES END #######
```

it is shown how Kleene has populated the template with the rules used for
setting up the network as was configured previously.

## FreeBSD resources

A few relevant external ressources to learn more about FreeBSD firewalls and PF
in particular:

- [Firewall chapter in the FreeBSD handbook](https://docs.freebsd.org/en/books/handbook/firewalls/)
- [Man-page on the PF configuration file](https://man.freebsd.org/cgi/man.cgi?query=pf.conf)
- [Man-page on the `pfctl` PF CLI](https://man.freebsd.org/cgi/man.cgi?query=pfctl)

## Next steps

When the networking configuration does not work as expected, what to do?
This is the topic of the [next section](/run/network/troubleshoot/).

