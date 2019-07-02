Title: Redirecting stdout and stderr in bash
Date: 2019-06-23 21:37
Category: Tip of the Week
Tags: totw,bash

A couple of weeks ago I covered some basic I/O redirection in bash (see
[I/O redirection in bash]({filename}io_redirection.md)). Well, there's actually
a lot more to it, so for this TOTW I thought I'd touch on a few more advanced
usages.

## Redirecting stderr
Sometimes, you may find that part or all of the output of a command isn't
properly redirected. As a quick example, navigate to any directory that is _not_
a Git repository, and run `git status`. You should see something like this:

```bash
$ git status
fatal: not a git repository (or any of the parent directories): .git
```

Yet, if you try to redirect it with a standard redirect, the output
is still displayed, and the file you redirect to remains empty.

```bash
$ git status > output
fatal: not a git repository (or any of the parent directories): .git
$ cat output
$ 
```

The reason is quite simple: the output from `git status` is an error message,
which is typically output on _standard error_ (stderr), while I/O redirection
operates on _standard output_ (stdout) by default. When redirecting output (or
input, for that matter), one can optionally provide a file descriptor specifying
which output stream to redirect. On a typical UNIX-like system, stdout is file
descriptor 1, and stderr is file descriptor 2. So if we want to catch that
stderr output, we just need to prepend  a 2 to the redirection operator.

```bash
$ git status 2> output
$ cat output
fatal: not a git repository (or any of the parent directories): .git
```

You can probably guess that if you leave the file descriptor out, it will
default to 1. In some cases, you may want to redirect both stderr and stdout to
the same file. But many programs output both on stderr and stdout, and we may
want to redirect both of them.

## Redirecting stderr and stdout
So, we can specify a file descriptor to redirect stdout or stderr (or any other
file descriptor, really), but many programs output on both stderr and stdout,
and it's often useful to redirect both. Here's a small Python script `print.py`
that outputs on line on stdout and one on stderr.

```python
import sys

print("some standard output", file=sys.stdout)
print("some error output", file=sys.stderr)
```

> **Note:** That's Python as in Python 3.

If we redirect stdout only, then the stderr line is still printed to the
terminal.

```bash
$ python3 print.py 1> stdout_output # recall that the 1 can be omitted
some error output
$ cat stdout_output
some standard output
```

Similarly, redirecting only stderr leaves the stdout output on the terminal.

```bash
$ python3 print.py 2> stderr_output
some standard output
$ cat stderr_output
some error output
```

Quite intuitively, if we want to redirect both stderr and stdout to one file
each, we can simply do two redirections following one another.

```bash
$ python3 print.py 1> stdout_output 2> stderr_output
$ cat stdout_output
some standard output
$ cat stderr_output
some error output
```

There's also the possibility to redirect both stdout and stderr to the same file
using the special `&` character in place of a file descriptor.

```bash
$ python3 print.py &> output
$ cat output
some standard output
some error output
```

And with that and the previous article, I've shared pretty much everything I
feel is useful with output redirection. In some future Tip of the Week, I'm sure
I'll get into input redirecton as well, as it's much the same.
