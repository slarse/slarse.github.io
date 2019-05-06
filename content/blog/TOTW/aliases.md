Title: Using bash aliases
Date: 2019-05-06 12:19
Category: Tip of the Week
Tags: totw,bash

For this _Tip of the Week_, I'd like to present something that took me a while
to figure out why it was useful. That something is bash aliases, and I'll now
walk you through how to create aliases, and the two main ways in which I use
them (although I'm sure there are more use cases).

# Using aliases
I think the `bash` manpage has a very good and concise description of what an
alias is:

> Aliases allow a string to be substituted for a word when it is used as the
> first word of a simple command

In other words, I can define a command that is substituted for some other
command. Creating an alias is very simple. The syntax looks like this:

```
alias <NAME>=<COMMAND>
```

So for example, if I want to have a command `hellofile` that creates a file with
the text "Hello, world!", I can achieve that with the following alias.

```bash
$ alias hellofile='echo "Hello, world!" > hellofile.txt'
```
Note the single quotes around the command definition. Without them, `bash`
would interpret the alias as being only `echo`, and the rest of the line as
another command. Now, if I run the command `hellofile`, it fill be substituted
with `echo "Hello, world!" > hellofile.txt`. You should think of aliases as pure
text substitution: precisely what you put in the alias definition will be put on
the command line when you invoke it. You can view all of your current aliases
by running `alias` without any options. Now, let's have a look at some common
use cases!

## Specifying "default" options for commands
This is probably the most common use case for aliases, and it's likely that you
already have some in play. A common one is to have `ls` aliased to `ls
--color=auto`. That is to say, the following alias is defined:

```bash
$ alias ls='ls --color=auto'
```

So if I now run e.g. `ls /etc`, the resulting command is actually `ls
--color=auto /etc`. Note how the alias does not have to be the _only_ word I
type for the command, it just has to be the first one. Another command that I
use an alias for is `xclip`, which is a small utility for copying stuff. I use
it almost exclusively to copy file contents to the clipboard, but that's not the
default functionality. In order to copy to the clipboard, I must write this
rather cumbersome command.

```bash
$ xclip -selection clipboard <FILEPATH>
```

So I have an alias for it so I can just type `xclip <FILEPATH>` to copy to the
clipboard.

```bash
$ alias xclip='xclip -selection clipboard'
```

As a side note, it may not be the best style to clobber an existing command with
an alias, but I still tend to do that for some of my most commonly used
commands. If you want to use the vanilla command, simply put it within single
quotes, which will hinder the alias from expanding (e.g. type `'ls'` to run `ls`
without `--color=auto`). Note that just defining an alias in a `bash` session
will not persist: it needs to be defined anew for each session. To have it
permanently defined, put the definition in a startup script (e.g. `.bashrc` or
`.bash_profile`).

## Creating throwaway commands
Now, the aliases I described above are useful to have defined permanently, and
should be defined in a startup script. The second use case I have for aliases is
when I have a repetitive command that I need to type over and over in the same
session, but isn't useful in general. An example would be when I need to run
some specific Java class in a project. Let's say I need to run the class
`se.slar.awesome.project.Main` over and over. Instead of typing `java
se.slar.awesome.project.Main` over and over, I define an alias for it.

```bash
$ alias runmain='java se.slar.awesome.project.Main'
```

And then, instead of writing all of that out, or having to do some
[reverse searching]({filename}reverse_search.md) or
[history lookups]({filename}history.md), I can just type `runmain`.
As defining an alias is so effortless, I tend to do it even if I know I'm just
gonna use the complex command a couple of times.

And that's all I wanted to cover, hope you enjoyed it and stay tuned for the
next TOTW coming next week!
