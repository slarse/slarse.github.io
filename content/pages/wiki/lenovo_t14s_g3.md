Title: Arch Linux on Lenovo T14S Gen 3 (Intel)
Slug: wiki/arch-linux-on-lenovo-t14s-g3-intel

Almost everything works out of the box. A few tweaks are required for audio and
video to function properly.

## Intel graphics
I had the exact same problems with glitchy 2D graphics and non-functional 3D
graphics that I did with the [Dell XPS 15]({filename}xps15.md). The solution
is to use the modesetting driver:

```
# /etc/X11/xorg.conf.d/20-intel.conf

Section "Device"
  Identifier "Intel Graphics"
  Driver "modesetting"
EndSection
```

Note that the T14S does not take a battery life hit like the [XPS
15]({filename}xps15.md) did as, unlike the Dell, it does not have a dedicated
GPU to offload from.

## Audio
ALSA couldn't recognize any audio devices (be that input or output) when I
initially used the system. Installing the
[`sof-firmware` package](https://archlinux.org/packages/?name=sof-firmware)
fixed the problem.


## Refers to
* [Arch Linux on XPS 15 9520]({filename}xps15.md)
