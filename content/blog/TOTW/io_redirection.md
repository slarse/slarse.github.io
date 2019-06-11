Title: I/O redirection in bash
Date: 2019-06-11 23:16
Category: Tip of the Week
Tags: totw,bash

Alright, so Tip of the Week has turned somewhat into "tip every two or three
weeks". It turns out that it's pretty difficult to find the time to actually
write something every week. but I'll keep trying. With that out of the way,
let's head into the subject matter of this post: _I/O redirection_. 
We'll just have a look at the most basic but also most generally applicable use
of redirection: taking the output from a program and storing it in a file.

> **Important:** Files will both be created and clobbered in this TOTW. When
> trying this stuff out, first create a new directory and do everything in
> there, so you don't litter your filesystem with strange files, or
> accidentally overwrite something important.

## Redirecting output
To set the stage, I'll be working in a directory with the following contents:

```bash
[tmp] $ ls
file1.txt  file2.txt  image1.png file2.txt
```

Redirecting output is fairly simple, and useful when you want to save the
output of some command in a file. There are two primary ways of redirecting
output: _appending_ and _truncating_. Appending is the one I use the most,
so let's start with that one.

### Appending output redirection
With `>>`, we can make an appending redirect.

```bash
[tmp] $ ls >> ls_output.txt  # output from ls saved to output.txt
[tmp] $ cat ls_output.txt    # let's have a look... 
file1.txt
file2.txt
image1.png
image2.png
ls_output.txt
[tmp] $ ls >> ls_output.txt  # append new output
[tmp] $ cat ls_output.txt    # let's have a look again
file1.txt
file2.txt
image1.png
image2.png
ls_output.txt
file1.txt
file2.txt
image1.png
image2.png
ls_output.txt
```

There are three things to note here. First, the `ls_output.txt` file does not
exist in the initial directory, and so it is created with the first redirect.
Note however that `ls_output.txt` is present in the first redirected output
from `ls`: `ls_output.txt` is actually created _before_ `ls` is run as there
needs to be an open
[file descriptor](https://en.wikipedia.org/wiki/File_descriptor)\* to the file
pass along. 

> ** \* ** A file descriptor can simply be thought of as a pointer to a file.
> There is no need to understand file descriptors intimately to use basic I/O
> redirection efficiently.

The second redirect is then appended to the file, which at that
point already exists. And that pretty much sums up how an appending redirect
functions: it appends output to the specified file if it exists, and creates a
file with the output if it does not exist. I find that this is most often the
functionality that I want, but in some cases, you want to re-create the file
from scratch with each redirect. That can be achieved with a truncating
redirect.

> **Note:** You may note that the output of `ls` is formatted differently when
> output to the terminal, and when redirected to a file. `ls` checks whether
> the stdout file descriptor points to a terminal, or something else, and
> formats the output accordingly. The details are somewhat out of scope.

### Truncating output redirection
Let's assume that we start over from the initial state of the directory, before
`ls_output.txt` existed. We can then make a truncating redirect with `>`.

```bash
[tmp] $ rm ls_output.txt    # restore initial directory state
[tmp] $ ls > ls_output.txt  # make a truncating redirect
[tmp] $ cat ls_output.txt   # and inspect the results
file1.txt
file2.txt
image1.png
image2.png
ls_output.txt
[tmp] $ ls > ls_output.txt  # another truncating redirect
[tmp] $ cat ls_output.txt
file1.txt
file2.txt
image1.png
image2.png
ls_output.txt
```

If you did not know what truncating meant before, you can probably figure it out
now. With a single `>`, the specified file is created if it does not exist, just
like with `>>`, but it is entirely overwritten (truncated, clobbered) if it
already does exist. I rarely use a truncating redirect, as it is an easy thing
to accidentally truncate a file you did not mean to touch. I recommend to always
use an appending redirect, unless you have a good reason to truncate the
targeted file.

And that's it for this TOTW!
