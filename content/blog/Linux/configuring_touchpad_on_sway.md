Title: Configuring touchpad tap in Sway
Date: 2024-03-24
Author: Simon Larsén
Tags: linux,wayland,sway,libinput
Slug: configuring-touchpad-in-sway

One thing that didn't carry over from my i3 setup [when moving over to
Sway (i.e. Wayland)]({filename}wayland_first_impressions.md) was the touchpad
configuration. Input devices was a display server concern under X.Org, so the
window manager had nothing to do with it. Notably, now click-on-tap is not
working for me, which is massively annoying.

If you're just here for the touchpad click-on-tap configuration, it looks like this.

```conf
input "type:touchpad" {
    dwt enabled
    dwtp enabled
    tap enabled
    tap_button_map lrm
}
```

But if you want to improve your understanding of how to configure input devices
such as touchpads and mice in a Wayland compositor, then read on!

# Configuring a libinput device in Sway
We need to add a libinput[ref]libinput is a stack for common input devices, such
as keyboards, touchpads and mice. Read more [in the Wayland
wiki](https://wayland.freedesktop.org/libinput/doc/latest/what-is-libinput.html).[/ref]
configuration into the Sway config file, which is usually located at
`~/.config/sway/config`. The Sway wiki [has a small example for libinput
devices](https://github.com/swaywm/sway/wiki#libinput-config-options) but it
doesn't really say all that much. Generally, an input configuration should look
like this.

```conf
input <selector> {
    option value
}
```

For the selector, we can use either the device identifier, or the type of the
device. I prefer the device type, i.e. `"type:touchpad"`, as I use the same
configuration file for multiple devices that don't share touchpad
identifiers[ref]Note that the type selector will select _all_ devices of that
type. If you have multiple devices that identify as touchpads, you may want to
be more specific and use the identifier.[/ref].

You can run `swaymsg -t get_inputs` to get information about your devices. You
will get a ton of output, but somewhere you'll find a device that has `Type:
Touchpad`. Mine looks like this.

```bash
$ swaymsg -t get_inputs
...
Input device: SYNA1D31:00 06CB:CD48 Touchpad
  Type: Touchpad
  Identifier: 1739:52552:SYNA1D31:00_06CB:CD48_Touchpad
  Product ID: 52552
  Vendor ID: 1739
  Libinput Send Events: enabled
...
```

We can however get a whole lot more information about each device with the
`--raw` option[ref]When piping `swaymsg` output to another command, `--raw` is
implicit. I use it here explicitly for clarity.[/ref]. Combining that with
`jq`[ref]If you don't know how to use `jq`, do yourself the biggest favor of the
year and learn it.[/ref] we can get only touchpads out of the command. On all my
devices, I only have a single touchpad device. It should look something like
this.

```bash
$ swaymsg -t get_inputs --raw | jq '.[] | select(.type=="touchpad")'
{
  "identifier": "1739:52552:SYNA1D31:00_06CB:CD48_Touchpad",
  "name": "SYNA1D31:00 06CB:CD48 Touchpad",
  "vendor": 1739,
  "product": 52552,
  "type": "touchpad",
  "scroll_factor": 1.0,
  "libinput": {
    "send_events": "enabled",
    "tap": "disabled",
    "tap_button_map": "lrm",
    "tap_drag": "enabled",
    "tap_drag_lock": "disabled",
    "accel_speed": 0.0,
    "accel_profile": "adaptive",
    "natural_scroll": "disabled",
    "left_handed": "disabled",
    "click_method": "button_areas",
    "middle_emulation": "disabled",
    "scroll_method": "two_finger",
    "dwt": "enabled",
    "dwtp": "enabled"
  }
}
```

This gives us everything we need to configure the touchpad, and we can also see
if our configuration takes effect correctly. The options shown under `libinput`
is what we have to play with. The names aren't necessarily self-explanatory, but
you can find decent descriptions of them in the `sway-input(5)`[ref]Run `man 5
sway-input` to get the given page. See my article on [man page
sections]({filename}man_page_number.md) if the `5` is confusing to you.[/ref]man
page under the `LIBINPUT CONFIGURATION` section.

I'm going to set the options that are crucial for how I use a touchpad,
regardless of what their defaults are. These options are:

```conf
input "type:touchpad" {
    tap enabled         # enables click-on-tap
    tap_button_map lrm  # tap with 1 finger = left click, 2 fingers = right click, 3 fingers = middle click
    dwt enabled         # disable (touchpad) while typing
    dwtp enabled        # disable (touchpad) while track pointing
}
```

Putting this in my `~/.config/sway/config`[ref]To see exactly how I use this in
my Sway config, refer to [my config
repository](https://github.com/slarse/config/commit/21b524a956bd942424aa944fa70cce01dd005ea8).[/ref],
reloading the environment and then checking the settings shows that `tap` is
now enabled.

```bash
$ swaymsg reload
$ swaymsg -t get_inputs | jq '.[] | select(.type=="touchpad")'
{
  "identifier": "1739:52552:SYNA1D31:00_06CB:CD48_Touchpad",
  [...]
  "libinput": {
    [...]
    "tap": "enabled",
    "tap_button_map": "lrm",
    [...]
    "dwt": "enabled",
    "dwtp": "enabled"
  }
}
```

And that's that, click-on-tap now works again!

# Summary
In this article, I outlined how to configure a touchpad in Sway. The principles
shown here carry over to any kind of libinput device, and should also be
applicable in most other Wayland compositors.
