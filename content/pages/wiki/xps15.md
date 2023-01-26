Title: Arch Linux on XPS 15 9520
Slug: wiki/arch-linux-on-xps-15-9520

Many things work out of the box on the XPS 15 9520, but a few tweaks are
necessary to get the most out of the machine. For reference, here's the config I
got:

```
CPU: i7 12700H
RAM: 32 GB
GPU: NVIDIA RTX 3050Ti
Monitor: 3.5k OLED
```

## Set SSD to AHCI/NVME to save battery
For some reason, setting the SSD to AHCI/NVME in BIOS (instead of RAID which
was default for me) causes power consumption in idle and light workloads to
absolutely plummet. Consumption dropped by as much as 20-50% for me, depending
on the scenario.

With this tweak, I get around 6-8 hours of battery life with light use and
screen brightness at 50%. I find that perfectly acceptable considering I have
the OLED screen and a power-hungry i7 in the machine.

## Intel and NVIDIA Graphics

* Kernel parameters: `nvidia_drm.modesetting=1 ibt=off`
    - `ibt=off` was required for me to be able to start the X server with NVIDIA's proprietary drivers, [see this issue](https://github.com/NVIDIA/open-gpu-kernel-modules/issues/256)
* Intel driver config:
    - Must use DRI2, as the default DRI3 causes all kinds of problems with 3D graphics acceleration
```
# /etc/X11/xorg.conf.d/20-intel.conf

Section "Device"
  Identifier "Intel Graphics"
  Driver "intel"
  Option "DRI" "2"
EndSection
```

> **Note:** The [modesetting driver also
> works](https://wiki.archlinux.org/title/Intel_graphics#Issues_with_selecting_Qt_elements_within_Plasma_Desktop_on_Alder_Lake.2FUHD_770),
> but it interferes with PRIME offloading s.t. the NVIDIA GPU is always active.
> This butchers battery life.

## Touchpad
The touchpad worked great without any configuration with the exception of
tap-to-click. I don't have any problems with lag that I've seen some other
people have.

```
# /etc/X11/xorg.conf.d/30-touchpad.conf

Section "InputClass"
Identifier "touchpad"
Driver "libinput"
	MatchProduct "VEN_06CB:00 06CB:CE7E Touchpad"
	Option "Tapping" "on"
	Option "ClickMethod" "clickfinger"
	Option "ScrollMethod" "two-finger"
	Option "NaturalScrolling" "on"
EndSection
```

## Media controls
Using [xbindkeys](https://wiki.archlinux.org/title/Xbindkeys), the example
config works great for volume. `xbacklight` can be used for brightness
controls.

```
# ~/.xbindkeysrc

# Volume controls
"pactl set-sink-volume @DEFAULT_SINK@ +1000"
   XF86AudioRaiseVolume

"pactl set-sink-volume @DEFAULT_SINK@ -1000"
   XF86AudioLowerVolume

"pactl set-sink-mute @DEFAULT_SINK@ toggle"
   XF86AudioMute

"pactl set-source-mute @DEFAULT_SOURCE@ toggle"
   XF86AudioMicMute

# Brightness controls
"xbacklight -inc 5"
    XF86MonBrightnessUp

"xbacklight -dec 5"
    XF86MonBrightnessDown
```
