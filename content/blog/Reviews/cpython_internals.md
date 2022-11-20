Title: Book Review: CPython Internals
Date: 2022-11-20
Author: Simon Larsén
Tags: book review,software engineering,python
Slug: book-review-cpython-internals

About a month ago I signed myself up to do a talk at a Python meetup hosted by
[HiQ](https://hiq.se/). I brazenly set my topic as _Under the Hood of CPython_,
thinking I had sufficient understanding of its inner workings to produce a
riveting talk. As I started preparing the talk, I came to the gut-wrenching
conclusion that my knowledge was too shallow, I simply didn't know enough of
the details to put together an in-depth talk on the subject. Thankfully, I knew
where to turn to for the details I needed: Anthony Shaw's _CPython Internals_
book. Here's what I think of it.

```
CPython Internals
by Anthony Shaw
Released May 2021
Publisher(s): Real Python (realpython.com)
ISBN: 9781775093344
```

> Confused about the difference between Python and CPython? See [The difference
> between Python and
> CPython]({filename}/blog/Programming/python/python_and_cpython.md).

# The book in a nutshell

_CPython Internals_ gives you a guided tour of the CPython project, from
parsing source code to compiling bytecode to interpreting said bytecode. The
book is meant to serve as a starting point for budding CPython contributors or
Python developers that simply want to learn a bit more about the reference
implementation. It highlights the most important files in the project for each
of the respective parts and guides you through their execution. Throughout the
book we also get to follow along with a worked example of extending the language
with an "almost equal" operator, written as `~=`.

The book concludes with three concrete ways in which you can use the knowledge
you've attained: 1) creating C extensions, 2) improving existing Python programs
by leveraging knowledge of the internals and 3) contributing to the CPython
project. While point 2) is potentially a little bit vague, points 1) and 3) are
concrete and well described.

Before writing the book, Anthony wrote an in-depth article on the same topic.
You can find it over on [Real
Python](https://realpython.com/cpython-source-code-guide/). It is something of
an appetizer for the book, but stands strong on its own. Having a brief look at
that article will give you a better understanding of what the book is about
than anything I could write here.

# What I liked
I went from surface-level understanding of the CPython project to being pretty
confident about where to poke around to do what just from reading this book.
It's comprehensive in scope and the worked example of the `~=` operator helps _a
lot_ in facilitating an understanding for how to extend CPython with your own
silly things.

I also appreciated the nods to other respectable sources. The [Python
Developer's Guide](https://devguide.python.org/) is a great resource for quickly
refreshing how to do something (but going from 0 knowledge about the project
it's a bit to terse). Luciano Ramalho's book [Fluent Python 2nd
ed](https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/) is
also noted as an excellent reference on the Python object model, which I
absolutely agree with.

There is enough context in each chapter that you don't really need much
pre-existing understanding of any of the subjects. If you can read Python code
and have a little bit of experience with reading C code, you're all good to go.
Concepts relevant to the book such as parallelism and memory management are
explained both on an abstract level and in how they are implemented in CPython.
The book is to a great extent a standalone resource and it should be very
approachable even to developers without much experience. There's even an
appendix at the end to explain what little you need to know about the C
programming language to be able to understand the code samples.

# What I didn't like
There was nothing about the book that I thought was _bad_, but for me
personally, I would have preferred less explanation of fundamental concepts
(such as threading), and more in-depth details on CPython itself. That being
said, I think Anthony overall has made good calls on the tradeoffs between depth
and approachability. Given that the book is meant to be a starting point for
CPython development as opposed to a complete reference, I think that this
nit-pick of mine is nothing more than personal preference, and perhaps that I'm
slightly outside the target audience of the book. It's clearly meant to contain
everything you'd need to know to go from zero to hero, and it's a lot easier to
skip over content you feel is redundant than it is to find content you didn't
know you needed.

# Conclusions
CPython Internals saved my neck. I had three weeks to go from a shallow
understanding of the CPython project to being able to explain it to others in a
~30-minute talk, and [I made
it](https://github.com/slarse/talks/tree/80503786d4587abdadba9913c55c7d133269f3a2/under-the-hood-of-cpython).
Without this book I wouldn't have. It was so approachable that I could use it
for "Sunday reading" before bedtime and in spare minutes on public transport.

I highly recommend this book to anyone who's interested in the CPython project.
It's not necessary to have future CPython contributions as a goal to get a lot
out of this book, I found it incredibly interesting in its own right. The fact
that Anthony has managed to pack so much information, with so much context
(recall that I thought there was too much of that) in less than 400 pages is
nothing short of spectacular.
