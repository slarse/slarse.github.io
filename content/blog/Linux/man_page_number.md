Title: What does the number in a man page mean?
Date: 2023-10-24
Author: Simon Larsén
Tags: linux,man
Slug: man-page-numbering

If you open a `man` page on a *NIX system (such as a Linux distro), you'll
always see a number next to the subject of the `man` page. Like `GIT(1)`,
`SUDO(8)` or `open(n)`. What's that thing in parentheses? To cut a long
story short, it's the _section_ the `man` page belongs to. Let's discover
what that means.

# `man` pages are divided into sections
`man` pages act as a system reference manual on any *NIX system. All `man` pages
have a heading containing the name of the page, its section and a very short
description. Something like this.

```
<name>(<#section>)     <description>     <name>(<#section>)
```

As a concrete example, here's the first line you get if you execute `man git`.

```
GIT(1)                         Git Manual                        GIT(1)
```

The name is self-explanatory, is is the short description, but the section
number is not so transparent in its meaning. To find out what it means,
we can actually consult the `man` page for the `man` program itself.

```
$ man man
MAN(1)                     Manual pager utils                    MAN(1)
[...]
The table below shows the section numbers of the manual followed
by the types of pages they contain.

1   Executable programs or shell commands
2   System calls (functions provided by the kernel)
3   Library calls (functions within program libraries)
4   Special files (usually found in /dev)
5   File formats and conventions, e.g. /etc/passwd
6   Games
7   Miscellaneous (including macro  packages  and  conventions),
    e.g. man(7), groff(7), man-pages(7)
8   System administration commands (usually only for root)
9   Kernel routines [Non standard]
[...]
```

This sectioning makes it possible to have multiple `man` pages with the same
name, but in different sections. By default, you'll get only one result when
executing `man <name>`, and which one you get is dependent on a pre-defined
search order. Which, of course, we can also find in the `man` page for `man`.

```
The  order  of sections to search may be overridden by the envi‐
ronment  variable  $MANSECT  or  by  the  SECTION  directive  in
/etc/man_db.conf.  By default it is as follows:

      1 1p n l 8 3 3p 0 0p 2 3type 5 4 9 6 7
```

In my personal experience, the default search order most often gives you what
you want. But sometimes it doesn't, and then you need to figure out how to find
the man page you're after.

# Selecting man pages from different sections
To select a page from a particular section, you specify the section before the
name. For example, as indicated by the excerpt from `MAN(1)` above, there's also
a `man(7)`. We can get it like so.

```
$ man 7 man
man(7)              Miscellaneous Information Manual             man(7)
[...]
```

But what if you don't actually know which section the man page you're looking
for is in, you only know that the one you're looking at isn't the one? Then you
can use `whatis`. For example, I have four different man pages named `open` on
my machine.

```
$ whatis open
open (2)             - open and possibly create a file
open (3p)            - open file
open (3perl)         - perl pragma to set default PerlIO layers for input and output
open (n)             - Open a file-based or command pipeline channel
```

Here you can also see a couple of section numbers that look a bit different,
namely `3perl` and `n`. These don't belong to any of the standard sections, but
you can open them just the same. For example, `man 3perl open` would open the
`open` page from the custom `3perl` section.

> Note: If you don't see all available man pages when running `whatis` for a
> particular page, your `man` database is out-of-date, you may want to run
> `mandb` manually (or whatever is equivalent on your system) to rebuild the
> search index.

# And that's all!
Now you should hopefully be a bit more confident in finding the man page you're
looking for. And if at any point you forget what I've written here, almost all
of the information is available just a `man man` away!
