---
title: Customizing the firewall
description: How to add your own custom firewall rules to PF
keywords: networking, customization, expose ports, publish ports
---

Even though Kleene manages the [PF](https://docs.freebsd.org/en/books/handbook/firewalls/#firewalls-pf)
firewall to provide container connectivity etc., it is also possible
to add additional firewall rules alongside Kleene's.
This section describes how and provides a simple example.

> **Note**
>
> Customizing the firewall can cause unpredicted networking behavior in Kleene
> if the custom configuration interferes with Kleene's firewall rules.
> In case of problems, go to the
> [networking debugging page](/run/network/troubleshoot/).
{: .important}

## Configuring a Kleene-managed firewall

When Kleene's networking configuration changes, which happens when
networks are created/removed or containers are connected/disconnected,
Kleene updates the firewall configuration. This is done by:

- Updating Kleene's firewall rules and rendering them using Kleene's PF
  configuration file *template*.
  The default location of the template is `/usr/local/etc/kleened/pf.conf.kleene`.

- The rendered template is then written to an [actual `pf.conf` file](https://man.freebsd.org/cgi/man.cgi?query=pf.conf),
  which is then used to update the firewall ruleset in PF.
  The default location of PF configuration file is `/etc/pf.conf`.

The locations of both the template and PF-config file can be configured
in `/usr/local/etc/kleened_config.yaml`. See the
[Kleened configuration](reference/kleened/configure-kleened/) page for details.

Using the template file, it is possible to add custom firewall rules
as long as Kleene's tags `<%= kleene_macros %>`, `<%= kleene_translation %>`,
and `<%= kleene_filtering %>` is present, and in the correct order etc.
Once `pf.conf` is updated, which also happens when Kleened (re)starts,
it can be inspected to verify that the overall configuration file looks
as expected. The following example shows this i practice.

## Example: Blocking incoming traffic on the Kleene host

Usually, it is desirable to block all incoming traffic on the physical
interface by default, and only allow traffic to explicitly whitelisted ports.
A common whitelist rule is to allow one or more IP's to connect to the ssh daemon
for remote access.
Finally, PF supports traffic sanitation that does IP fragment reassembly etc.

Configuring the above in PF is achieved by modifying the default template config
(excluding preamble comment)

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

into

```
ext_if="em0" # External interface of the host
set block-policy drop # Drop blocked packets

### KLEENED MACROS START ###
<%= kleene_macros %>
### KLEENED MACROS END #####

# Perform traffic sanitation on the external interface
scrub in on $ext_if all fragment reassemble

### KLEENED TRANSLATION RULES START ###
<%= kleene_translation %>
### KLEENED TRANSLATION RULES END #####

# block everything by default
block log all

# Allow the client machine to SSH into the host
pass in quick on $ext_if from 10.0.2.2 to 10.0.2.15 port 22

### KLEENED FILTERING RULES START #####
<%= kleene_filtering %>
### KLEENED FILTERING RULES END #######
```

The modfied template file is saved at `/usr/local/etc/pf.conf.kleene` and Kleened is
restarted for the changes to take effect.

See `pf.conf(5)` for details on the PF configuration file syntax.

Note that when Kleened restarts, any open ssh-connections might disconnect.
It might also be a good idea to test the custom firewall settings in safe manner
to avoid being locked out of the host.

A quick test to verify that the usual container connectivity is not affected by
the firewall configuration changes:

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

Voila! The containers can reach each other. Inspect the PF configuration file
`/etc/pf.conf` to see the custom rules together with Kleene's configuration:

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

This shows how Kleene has populated the template with the rules used for
the network just created and the containers connected to it.

## External FreeBSD resources on firewall configuration

A few relevant external ressources to learn more about FreeBSD firewalls and PF
in particular:

- [Firewall chapter in the FreeBSD handbook](https://docs.freebsd.org/en/books/handbook/firewalls/)
- [Man-page on the PF configuration file](https://man.freebsd.org/cgi/man.cgi?query=pf.conf)
- [Man-page on the `pfctl` PF CLI](https://man.freebsd.org/cgi/man.cgi?query=pfctl)

## Next steps

When the networking configuration does not work as expected, what to do?
This is the topic of the [next section](/run/network/troubleshoot/).
