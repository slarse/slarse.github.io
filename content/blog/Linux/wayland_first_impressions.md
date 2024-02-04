Title: First impressions of Wayland on Arch Linux
Date: 2024-02-04
Author: Simon Larsén
Tags: linux,wayland,xorg,x11
Slug: wayland-one-month-later

Wayland appears to be the future of window systems in the world of Linux,
replacing the aging X.Org window system. The [Arch Wiki article on
X.Org](https://wiki.archlinux.org/title/Xorg) refers to it as "the alternative
and successor [of X.Org]" and Canonical even dropped its own [Mir display
server in favor of Wayland on Ubuntu](https://wiki.ubuntu.com/Wayland).
So when it became time for me to configure a new laptop in the beginning of
January, I decided to do give Wayland a go. Here's what I think of it so far.

# What the heck is a window system?
First of all, what the heck is a window system? In short, it's the component
that renders graphical windows to your screen and communicates the user's input
to the underlying operating system. The X Window System, or just X for short, is
the reigning king of window systems in UNIX-like operating systems (excepting
macOS which uses [Quartz](https://en.wikipedia.org/wiki/Quartz_Compositor)). You
will often see it referred to as X.Org; this is simply the most commonly used
[open source implementation of X](https://www.x.org/wiki/).

I could try to outline what X.Org's problems are and how Wayland solves many of
them, but I simply don't have the level of understanding necessary to do so
confidently. One thing to note is that Wayland is first and foremost a
_protocol_ for the communication between a display server and applications. A
display server can implement the Wayland protocol and is then referred to as a
Wayland _compositor_.

If you want to learn more, [here's a brief article on the
subjecp](https://linuxiac.com/xorg-x11-wayland-linux-display-servers-and-protocols-explained/).

# Wayland first impressions with Sway
I recently setup Wayland on a brand new work computer, and going from a clean
slate setup was really effortless. I chose [Sway](https://swaywm.org/) as my
compositor and started it. And it just kind of worked. Outside of [configuring
Sway to my
liking](https://github.com/slarse/config/blob/d8ba6671a2245be75c5fa3b4fdfef3df61cc93a0/sway/config),
I didn't really have to do much of anything for it to work.

On my private Dell XPS 15 [where I'm already running
X.Org]({filename}/blog/Blog/xps_15_arch_linux_3d_graphics.md), setting up
Wayland was similarly effortless. I just installed Sway, and even though it
doesn't support [NVIDIA's proprietary
drivers](https://github.com/swaywm/sway/wiki#nvidia-users), running Sway with
the `--unsuported-gpu` option just worked.

All-in-all, setup was a breeze and I did not encounter any problems at all.

## Upsides of Sway
I immediately noticed some improvements in my desktop experience. The first came
when connecting an external display, which Sway just found and started
outputting an image to. In almost a decade of using X.Org on just shy of a half
dozen devices, that has never happened before without effort on my part.

I was also treated with a complete lack of screen tearing when scrolling
websites and documents, which I had a lot of under X.Org. I'm sure there's a way
to configure that away with X and I never bothered to look into it more than
stating that it wasn't as easy as toggling a flag, but it was just for free with
Wayland. Now that it's gone I would have a hard time going back to it.

Finally, most things just kind of work. It's a _big_ accolade to note that over
a whole month of use, I haven't encountered a single show-stopping problem. But
I have definitely encountered quite a few lesser ones.

## Downsites of Sway
Pretty much all of the downsides I've encountered have to do with the fact that
a lot of applications I've used over the years were written for X.Org. This
means that many applications run under the the 
[XWayland](https://wayland.freedesktop.org/xserver.html) compatibility layer,
which nullifies the performance improvements of Wayland's architecture. I've
especially noted that startup times for GUI apps that run under XWayland are
slow compared to running X.Org directly.

Another problem is that apps directly related to X.Org typically just do not
function. For example, I've been using the [`import` command from
`imagemagick`](https://imagemagick.org/script/import.php) to grab snippeted
screenshots for nigh on a decade, and it doesn't work at all with Wayland as it
expects to work with an X.Org backend. Similarly,
[Redshift](https://wiki.archlinux.org/title/Redshift) which I've been using for
years to adjust color temperature does not support Wayland. It results in a whole
lot of [<insert program> alternative for
Wayland](https://www.reddit.com/r/wayland/comments/si49y1/redshift_alternatives_for_wayland/?rdt=39794)
kinds of searches, but they usually bear fruit. I found [`grim` as a replacement
for `import`](https://sr.ht/~emersion/grim/) and [`gammastep` as a replacement
for `redshift`](https://gitlab.com/chinstrap/gammastep) that way.

The incompatibility with Redshift does bring up another interesting point,
namely that Wayland is still neither complete nor stable. [Color management is for
example still not
standardized](https://gitlab.freedesktop.org/wayland/wayland-protocols/-/merge_requests/14).
In some respects, stepping into the land of Way feels a bit like using a beta
product.

# Conclusions
Will I keep using Wayland? Definitely. I've only encountered a few very minor
problems with application compatibility, and most I've found alternatives for.
I'm even a little bit excited to find some need completely unfulfilled in the
land of Wayland applications, because that would give me a good reason to
implement it myself.
