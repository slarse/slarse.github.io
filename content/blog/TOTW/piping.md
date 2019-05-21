Title: Piping commands in bash
Date: 2019-05-21
Category: Tip of the Week
Tags: totw,bash

Many, many bash commands are built around and meant to be used with a
fundamental feature of the bash shell (actually, most shells), called _piping_.
Put simply, piping takes the output of one command and provides it as input to
the next. Here's a simple example of running `ls` and filtering the result with
`grep` to find all `.py` files in the current directory.

```bash
$ ls # just run ls 
file1.md  file2.md  file3.md  script1.py  script2.py
$ ls | grep '\.py$'
script1.py
script2.py
```

To be precise, the `|` (pipe) operator takes the output from the command on the
left, and provides it as input to the command on the right. Pipes can be chained
practically as much as you'd like. For example, if we want to get amount of
`.py` files in the current directory, we can pipe the output from `grep` to the
`wc` (word count) command, with the `-l` option to count lines only.

```bash
$ ls | grep '\.py$' | wc -l
2
```

`wc` counts two lines, which is precisely the amount of `.py` files that we
found. Let's move on to I/O redirection. Piping allows you to easily compose
powerful programs from simple commands, and is a very intuitive way to work.
Next week, I'll cover I/O redirection, which is another super useful feature of
bash that's a bit more complicated.
