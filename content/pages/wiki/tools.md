Title: Tools for Software Engineering
Slug: wiki/tools

I love tinkering with my environment. So much so that I've been known to spend
more time tinkering than I actually end up using the particular tool or utility
I just put in place. Regardless, I'm a huge fan of neat tools that improve my
software engineering workflows or just general usage of my machines. I'm
continuously expanding this list as I find new tools and recall ones that I
already use.

[TOC]

# Command Line Tools
Command line tools are my bread and butter. Here's a selection of my favorite
tools.

## [autojump](https://github.com/wting/autojump) - `cd` that learns!
* Instead of `cd ~/path/to/my/best-project`, just type `j best-project`!
* Finds the directory I want the vast majority of the time

## [neovim](https://neovim.io/) - The future (and present) of Vim
* You know what it is, it's Vim. But better.
* I use it for everything. That's the largest appeal for me. One editor for all
    my editing needs.

## [nushell](https://www.nushell.sh/) - A shell with data processing capabilities
* Modern and powerful shell
* Incorporates functionality equivalent of tools like `jq` and `awk` directly into the shell
* You kind of have to try it out to understand - I use it more and more when I need to do quick data processing

## [fzf](https://github.com/junegunn/fzf) - The best fuzzy finder around
* A _fuzzy finder_ allowing you to search through text with inexact (fuzzy) search terms
* Great integration with `neovim`

## [ghostty](https://ghostty.org/) - A powerful GPU-accelerated terminal emulator
* A new and shiny terminal emulator
* GPU-accelerated => very fast and supports things like inline images

## [hl](https://github.com/pamburus/hl) - An incredibly useful JSON log viewer
* View JSON-formatted log output in a nicely formatted fashion
* Easily search and filter logs

## [jq](https://jqlang.github.io/jq/) - Command line JSON processor
* Allows for easy querying of JSON data in pretty much any shell
* Essential tool unless you use a shell like `nushell`

## [kanata](https://github.com/jtroo/kanata) - QMK but for any keyboard
* A keyboard manager with powerful functionality like tap-hold
* More or less QMK that runs on the host machine instead of on the keyboard

## [kitty](https://sw.kovidgoyal.net/kitty/) - Another powerful GPU-accelerated terminal emulator
* Pretty much the same thing as ghostty

## [pgcli](https://www.pgcli.com/) - A powerful CLI client for PostgreSQL
* More user friendly version of `psql`
* Can do stuff like
    - Auto-complete `ON` of `JOIN`-clause based on foreign keys
    - Saved queries with parameters that can be invoked by name

## [ripgrep](https://github.com/BurntSushi/ripgrep) - `grep`, but fast!
* An incredibly fast implementation of the classic `grep` utility
* Great integration with `neovim`

## [tmux](https://github.com/tmux/tmux) - The best terminal multiplexer!
* A great terminal multiplexer, letting you run multiple programs in a single terminal!
* Large amount of plugins and themes to customize it to your liking
    - But I run [mostly vanilla](https://github.com/slarse/config/blob/main/tmux/tmux.conf)

## [tmuxp](https://tmuxp.git-pull.com/) - Session manager for `tmux`
* Define session layouts through simple configuration files
* Must-have extension to the `tmux` experience!

## [tldr](https://github.com/tldr-pages/tldr) - Short and concise man pages
* Super short man pages that give just the bare minimum of information to use a tool
* Very often, precisely what you need!

## [tshark](https://www.wireshark.org/docs/wsug_html_chunked/AppToolstshark.html)
* CLI version of Wireshark

## [qmk](https://qmk.fm/) - Keyboard software for microcontrollers
* The most popular keyboard software for home-built keyboards
* [My QMK configuration](https://github.com/slarse/qmk_firmware/tree/slarse)

## [yazi](https://yazi-rs.github.io/) - Terimnal file manager on steroids
* Fast and easy-to-use terminal file manager
* Integrates very well with GPU-powered terminal emulators (kitty, ghostty) - can show image previews and the like

## [zellij](https://zellij.dev/) - Modern alternative to tmux
* A terminal multiplexer that shares many of the features of tmux
* Easy to get into thanks to the always-on-screen keyboard bindings - I recommend this to anyone that isn't yet entrenched in tmux!
* Unlike tmux, provides a good experience out-of-the-box

# GUI utilities
I don't use a whole lot of GUI utilities, but I've found a few really neat ones
over the years.

## [Edgeshark](https://edgeshark.siemens.io/#/)
* Show network topologies of containers
* Incredibly easy to get up and running with Docker
* Can be integrated with Wireshark/TShark via [cshargextcap](https://github.com/siemens/cshargextcap)

## [i3](https://i3wm.org/) - Improved tiling window manager
* A tiling window manager - once you go tiling, you never go back!
    - Seriously, try it. You'll wonder why you ever had floating windows.
* Relatively easy to get started with
* Highly customizable

## [warpd](https://github.com/rvaiya/warpd) - Navigate GUIs with your keyboard
* Navigate your GUIs using your keyboard
* Fantastic for use with a laptop

## [Wireshark](https://www.wireshark.org/)
* Capture and analyze network traffic

## [zeal](https://github.com/zealdocs/zeal) - Offline docs
* Keep your docs locally on your machine instead of having to navigate to a
    docs website
* Comes out-of-the-box with docs for most major programming languages, like
    Python, Java, Kotlin, JavaScript, GoLang, Rust, C etc.
* If that's not enough, [you can create your own docsets](https://github.com/zealdocs/zeal#create-your-own-docsets)
* For MacOs users, [dash](https://kapeli.com/dash) does exactly the same
    thing

## [slimbook-battery](https://github.com/Slimbook-Team/slimbookbattery) - Battery/performance management
- Neat GUI for managing battery and performance settings
- **Note:** The current release (v4.0.8) does not work with newer
  versions of the Linux kernel (6.4.2 or later). Prerelease of  v4.0.9 exists
  and [works fine](https://github.com/Slimbook-Team/slimbookbattery/issues/110).

## [sway](https://swaywm.org/) - i3 under Wayland
- Tiling compositor for Wayland
- Nearly drop-in replacement for the i3 window manager

# Note taking and blogging
While apps like [LoqSeq](https://logseq.com/), [Obsidian](https://obsidian.md/)
and [Notion](https://www.notion.so/) are all the rage right now, I prefer
simpler solutions.

## [pelican](https://getpelican.com/) - An extensible static site generator
- Write Markdown (or reStructuredText), get a static web site!
- This blog is created with Pelican
