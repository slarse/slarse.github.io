Title: Bash
Slug: wiki/bash

[TOC]

# Shortcuts
These shortcuts are provided by the `readline` library, so any shell using
`readline` (e.g. Bash, zsh, etc) should provide these.

## Terminology

* `M-<key>` - indicates a key combination with the Meta key
    - Meta is usually bound to the Alt key
    - On macOS, the built-in Terminal program allows you to bind Meta to Option
* `C-<key>` - indicates a key combination with the Control key
* Kill - delete text and put it in the kill ring
* Kill ring - `readline`'s variant of a clipboard with multiple temporary buffers
* Yank - paste the top of the kill ring at the cursor

## Navigation

* `M-f` - move forward one word
* `M-b` - move back one word
* `C-f` - move forward one character
* `C-b` - move back one character
* `C-a` - move to the start of the line
* `C-e` - move to the end of the line

## Text manipulation

* `M-d` - kill one word forward
* `C-w` - kill one word backward
* `C-u` - kill from the cursor to the beginning of the line
* `C-k` - kill from the cursor to the end of the line
* `M-l` - make the word after the cursor lowercase
* `M-u` - make the word after the cursor uppercase
* `C-y` - yank the top of the kill ring after the cursor
* `M-y` - if you've just yanked, use this to cycle through the kill ring
