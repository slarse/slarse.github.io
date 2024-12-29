Title: Networking
Slug: wiki/networking

This page summarizes networking concepts in software engineering.

[TOC]

# Open Systems Interconnection (OSI) model
The OSI model is a reference model for network communications. It partitions networking into 7 isolated layers, as follows.

1. Physical layer
    - The actual cables and radio signals that transmit data from point A to point B
    - As a software engineer, you are very rarely concerned with this layer other than its throughput (e.g. "gigabit ethernet")
2. Data Link layer
    - Low-level networking using ARP, Mac addresses and frames
    - Switches are (typically) layer 2 devices
3. Network layer
    - a.k.a the "IP layer"
    - Uses the Internet Protocol (IP) address hosts
4. Transport layer
    - In short, adds ports to be able to address specific sockets (processes) on hosts
    - E.g. TCP, UDP, QUIC
    - Firewalls are (typically) layer 4 devices. They need to keep track of
      ports!
5. Session layer
    - Layer of dubious value in today's network architecture
    - Supposedly responsible for establishing, maintaining and releasing connections, but that is also often performed at the transport layer by e.g. TCP
    - I suppose TLS could be considered a session layer protocol?
6. Presentation layer
    - a.k.a "encoding layer"
    - Character encoding, data compression etc
    - Rarely meaningful to separate from the application layer
7. Application layer
    - The communication protocols used at the application level
    - E.g. HTTP, FTP, DNS, SMTP etc

The OSI model is often critiqued for being too granular. For example, it is
rarely meaningful to distinguish bewteen layers 6 and 7. This is addressed by
the more concise TCP/IP model.

# Internet Protocol Suite (TCP/IP model)
The TCP/IP model is a less granular networking model than the OSI model, having
only 4 layers. Layers 5-7 of the OSI model have been collapsed into a single
layer, and the physical layer has been omitted entirely.

The layers are as follows:

* Application layer
    - Everything from layers 5-7 in the OSI model
* Transport layer
    - Same as the OSI model's transport layer (5)
* Internet layer
    - Same as the OSI model's Network layer (3)
* Link layer
    - Same as the OSI model's Data Link layer (2)

This model is significantly more concise and granular enough to model most
modern applications.

# The Internet Protocol (IP)
IP is the foundation of host addressing.

## CIDR notation and netmasks
There are two major versions of IP: IPv4 and IPv6. IPv4 addresses are 32 bit
while IPv6 addresses are 64 bit. Overall, the governing principles are the same
so these notes focus on IPv4 for simplicity.

An IPv4 address range is usually denoted using Classless Inter-Domain Routing
(CIDR) notation[ref]There used to be a [Classful network
notation](https://en.wikipedia.org/wiki/Classful_network), but it has been
obsolete for a long time due to a lack of flexibility[/ref].

The CIDR format is `a.b.c.d/x`, where `x` is the size of the _netmask_ (or
subnet mask).

* Example range: `192.0.0.0/24`[ref]This is a reserved address range for
  private networks, see [Wikipedia for details](https://en.wikipedia.org/wiki/Reserved_IP_addresses)[/ref]
    - `a.b.c.d = 192.0.0.0`, this is the network part (or prefix) of any IP address in this
      range
    - `x=24`, meaning that the network part of any IP address in this network
      has 24 bits, leaving 8 bits for the host part
    - The netmask is as many leading 1s (in binary) as the size of the network
      prefix. In this case, it is `255.255.255.0`.

### Applying a netmask
The purpose of the netmask is to determine if an IP address is part of the
network that the netmask belongs to. You apply the netmask by performing a
logical AND with the IP address you wish to check. If the IP address belongs to
the network, its network part will match the network's network part.

Examples of applying the netmask for the network `192.0.0.0/24`:

* IP address: `192.0.0.1`
    - `192.0.0.1 & 255.255.255.0 = 192.0.0.0`
    - Network part of address matches routing prefix, it belongs to the
      network!
* IP address: `192.0.1.1`
    - `192.0.1.1 & 255.255.255.0 = 192.0.1.0`
    - Network part of address does _not_ match routing prefix, it belongs to
      some other network!

For example, the address `192.168.0.1` belongs to the network `192.168.0.0/16`,
as `192.168.0.1 & 255.255.0.0 = 192.168.0.0`. However, the address `192.169.0.1`
does not, as `192.169.0.1 & 255.255.0.0 = 192.169.0.0`
