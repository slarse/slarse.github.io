Title: Fix 3D graphics in Arch Linux on Dell XPS 15 9520
Date: 2022-12-26
Author: Simon Larsén
Tags: blog,linux,xps15
Slug: xps-15-9520-arch-linux-intel-dri2

I recently got myself a Dell XPS 15 9520 to replace my aging laptop. it's
highly Linux-compatible and just following the [official installation
guide](https://wiki.archlinux.org/title/Installation_guide) got me 90% of the
way of having a well-behaved Arch Linux laptop, but the final 10% took me quite
a while to iron out. One big thing wasn't working, though: 3D graphics!

## Symptoms: glitchy 2D graphics and unusable 3D graphics
2D graphics worked mostly fine after installing `xf86-video-intel`, `nvidia` and
`nvidia-prime`. Websites, most desktop applications as well as 2D games like
Terraria worked without issue. Anything with the slightest hint of 3D would
however glitch out terribly with Intel graphics and just be completely black
with 3D graphics.

Some applications, such as Steam, wouldn't render properly unless in fullscreen.
3D benchmark software like `fire` (from `mesa-demo`) and `glmark2` wouldn't
update properly with Intel and would again be black with NVIDIA.

## Solution: Using DRI2 for the Intel driver
The solution I found to this problem was to [use
DRI2 for the Intel
driver](https://wiki.archlinux.org/title/Intel_graphics#DRI3_issues). I have no
idea of why this works, but it does. You can configure the Intel driver to use
DRI2 by creating a configuration file for X.

```
# /etc/X11/xorg.conf.d/20-intel.conf
Section "Device"
  Identifier "Intel Graphics"
  Driver "intel"
  Option "DRI" "2"
EndSection
```

> **Note:** The [modesetting driver also works](https://wiki.archlinux.org/title/Intel_graphics#Issues_with_selecting_Qt_elements_within_Plasma_Desktop_on_Alder_Lake.2FUHD_770), but it interferes with PRIME offloading s.t. the NVIDIA GPU is always active. This butchers battery life and so wasn't acceptable to me.

## Need more tweaks?
This wasn't the only tweak I put in to get my XPS 15 in tip-top shape, although
it was the most crucial one. I've got a bunch of other tweaks listed [over on
my Wiki page for the XPS 15]({filename}/pages/wiki/xps15.md).
