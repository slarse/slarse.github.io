Title: Reverse search in bash
Date: 2019-04-09 23:23
Category: Tip of the Week
Tags: totw,bash

Have you ever found yourself furiously tapping the UP-arrow (or `ctrl+p`) to
find a command that's probably waaaay up there? Would you be surprised if I
told you there's a better way? When you want to re-use a command you've written
previously, and you know it's not the previous command, or the one before that,
your first resort should be a _reverse search_. This can be accessed with
`ctrl+r`. If you press that button combination, you should see something like this:

```bash
(reverse-i-search)`': 
```

Just start typing the beginning of the command you're looking for, and most
often, it will pop up. For example, I sometimes need to re-run the
previous`git` command that I ran a while back. I then press `ctrl+r` and type
`git` to get something like this:

```bash
(reverse-i-search)`git': git push
```

Note how the initial `git` before the `:` is what I've actually written here,
and the text after the `:` (in this case `git push`) is what's been found with
the reverse search. Pressing `tab` now will terminate the search and put the
result of the search on the command line for editing. Then, simply press
`enter` to execute the command as usual. You can also skip over the editing
part and press `enter` right away to execute the command as-is. Sometimes,
however, the result you get first isn't what you want (obviously, just typing
`git push` would have been faster in this case).  You can then press `ctrl+r`
again to cycle to the next hit.

```
(reverse-i-search)`git': git commit -a -m 'Add module docstring to github_api module'
```

Now there's a command that I might not want to have to type out again in its
entirety, better showing why a reverse search may be useful. That's it for this
week's TotW, check back next week for more!
