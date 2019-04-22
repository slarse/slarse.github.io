Title: History and history expansion in bash
Date: 2019-04-22 11:59
Category: Tip of the Week
Tags: totw,bash

Admittedly, this TOTW is one day late, so this week there will be 2xTOTW! In
any case, the tip I want to bring up here is very much related to last week's
TOTW on [Reverse search in bash]({filename}reverse_search.md). Sometimes,
reverse searching just doesn't work out. You may not be quite sure what you
are looking for, or there are just too many recent commands that look samey.
In such cases, using the `history` command is a good alternative. 

### `history`
The `history` command will display the last commands that you have entered, and
looks something like this:

```
$ history
 1009  fg
 1010  git status
 1011  git commit -a -m 'Add module docstring to github_api module'
 [***OUTPUT TRUNCATED***]
 2007  history
```

Each command is called an _event_, and the output is formatted as `<event_nr>
<event>`. Precisely how many commands are returned by the `history` is
determined by the `HISTSIZE` and `HISTFILESIZE` environment variables. Setting
these to something like `5000` and `10000`, respectively, should be manageable
even for the weakest of computers. You can also limit the output of `history`
by providing an integer argument, so e.g. `history 5` will display the last 5
commands. Now, the real power of `history` becomes apparent when using it
with _history expansion_.


### History expansion
History expansion can be used to expand an event number into the whole command
it corresponds to. To expand an event, one simply types `!<event_nr>`. For
example, looking at the `history` output above I can see that event number 1010
corresponds to `git status`. I can execute the command again with history
expansion like so:

```bash
$ !1010
git status         # Command is echoed
On branch master   # Output from executing the command
[***REST OF OUTPUT OMITTED***]
```

The command is first echoed, and then executed. There are a few other ways to
specify the event number.

* `!`: Execute the last event.
    - I.e. type `!!` in the terminal.
    - Can be useful to re-execute a command that you realized you needed `sudo`
      for with `sudo !!`.
* `-n`: Execute the nth previous event.
    - E.g. type `!-1` to execute the last event, `!-2` to execute the one
      before that, and so on.
    - I personally don't find this very useful.

There is one more very useful feature that I often use, and that is the ability
to only print the command. This can be achieved by appending `:p` to the
history expansion command. Here is an example:

```bash
$ !1011:p
git commit -a -m 'Add module docstring to github_api module'
```

The command can then be accessed by pressing UP-arrow or `ctrl-p`, which is
very useful if you need to do minor modifications to it. There are tons of
more ways to use history expansion, and I strongly recommend reading the man-page
on it. Type `man bash` and then search for `HISTORY EXPANSION`, or do the same
in [this online bash man page](https://linux.die.net/man/1/bash).

### Filtering history
A final tip on using history expansion is to filter the output with `grep`. For
example, if I only want to find commands that include the word `git`, I can
filter the output of `history` by _piping_ to `grep` with the `|` character.

```bash
$ history | grep git
 1010  git status
 1011  git commit -a -m 'Add module docstring to github_api module'
```

I will most likely do another TOTW on piping, but the basic principle is that
`|` takes the output from the command on the left and feeds it as input to the
command on the right. That's it for this TOTW, stay tuned for the next one
coming on Sunday the 28th of April!
