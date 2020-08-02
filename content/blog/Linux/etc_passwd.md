Title: The Linux /etc/passwd file, and why it doesn't contain passwords
Date: 2020-08-02T11:51:33Z
Author: Simon Larsén
Tags: linux
Slug: etc-passwd

On any Linux distribution, there's a file located at `/etc/passwd`. This file
contains information about users that exist on the system, including their
username, user id, group id and more. In this short article, I'll outline the
structure of the `/etc/passwd` file, and also illuminate why it doesn't
typically contain any passwords.

## Layout of the `/etc/passwd` file
The layout of the `/etc/passwd` file is fairly simple. Each line represents a
user on the system, with different fields being separated by colons as follows:

```
name:password:UID:GID:GECOS:directory:shell
```

`name` and `password` are the username and password of the user, `UID` is the
user's numerical ID, `GID` is the id of the _first_ group the user belongs to,
`GECOS` is an optional comment, `directory` is the user's home directory, and
`shell` is the path to the executable that launches the user's preferred
shell. As an example, a part of my `/etc/passwd` file looks like this:

> **Note:** You can find the groups users belong to in the `/etc/group` file.

```
root:x:0:0::/root:/bin/bash
slarse:x:1000:985::/home/slarse:/bin/bash
mysql:x:970:970:MariaDB:/var/lib/mysql:/sbin/nologin
```

We can see that the root user has the fields set as follows:

```bash
password=x
UID=0
GID=0
GECOS=
directory=/root
shell=/bin/bash
```

The user and group IDs of the root user are always 0, and it typically has its
home directory in `/root`. But is the password of root user really `x`? No, it
isn't. An `x` in the password field means that the password is located in the
_shadow_ file. More on that in the next section. The entry for my own user,
slarse, is largely similar to that of the root user.

The entry for the mysql user is however a bit different. For starters, it has a
comment in the `GECOS` field saying _MariaDB_, which indicates that the mysql
it actually used by the `MariaDB` fork of the `MySQL` database system. It also
has in interesting login shell, namely `/sbin/nologin`. The description of the
`nologin` program from its manpage simply reads: _nologin - politely refuse a
login_. This program simply refuses a login, regardless of what credentials are
supplied.

And that's pretty much it for what the `/etc/passwd` file contains. For more
details, you can read the `passwd (5)` manpage. Now, what about that shadow
file?

> **Hint:** To access section `Y` of a manpage `PAGE`, type `man PAGE.Y` into a
> terminal. For example, to access `passwd (5)`, you type `man passwd.5`.

## The `/etc/shadow` file
The `/etc/passwd` file is a so-called _world-readable_, meaning that any user on
the system can read it. Many programs use this file to map users to their ids,
for example, and so its broad accessibility is necessary. A side effect is that
storing encrypted passwords in the `/etc/passwd` file lets any user that has
access to the system read the encrypted password of any other user. In times
long past, when cracking encrypted passwords was computationally infeasible,
this wasn't really a problem. Nowadays however, cracking an encrypted password
is only a matter of (feasible) time.

> **Note:** The `/etc/passwd` file is word-readable, but it's only writeable by
> root to avoid other users tampering with it, such as by replacing an `x` with
> an actual password.

The `/etc/shadow` file presents a solution to this problem. It is readable only
by the root user, and contains the encrypted passwords of users with an `x` in
the password field of their `/etc/passwd` entry. The shadow file is technically
optional, but you will probably never find a system that doesn't use it.

I won't go into detail on how the shadow file is structured, as it's not a file
that's typically accessed by user space programs. If you want to know more about
it, you can read the manpage of `shadow (5)`.

And that's it for this article, hope you learned something!
