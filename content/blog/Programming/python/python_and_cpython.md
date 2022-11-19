Title: The difference between Python and CPython
Date: 2022-11-19
Author: Simon Larsén
Category: Programming
Tags: python
Slug: the-difference-between-python-and-cpython

At one point or another, every Python developer or hobbyist encounters the word
_CPython_. For example, the [dis
module](https://docs.python.org/3/library/dis.html) states that it exposes an
"implementation detail of the CPython interpreter". What does that mean?
Some ask themselves how CPython differs from Python, and then
they move on with their lives without ever getting to the bottom of it. But if
you're one of the curious ones who couldn't put that thought down, this article
is for you.

# Python is a language specification
Python is a programming language. A programming language is an abstract concept.
It's fundamentally a set of rules saying what you're allowed to write in the
language, the _syntax_ of the language, and another set of rules saying what
should happen if you execute some (syntactically valid) code, the _semantics_ of
the language.

For example, take the [`pass`
statement](https://docs.python.org/3/reference/simple_stmts.html#the-pass-statement).
The syntax of the `pass` statement is incredibly simple, it's just the keyword
`pass`:

```
pass_stmt ::=  "pass"
```

The semantics are equally simple.

> pass is a null operation — when it is executed, nothing happens. It is useful
> as a placeholder when a statement is required syntactically, but no code needs
> to be executed, [...]

For example:

```python
def funtion_that_does_nothing():
    pass
```

The pass statement could be _implemented_ in any number of ways. It could
correspond to a NOOP instruction that when executed does nothing. It could also
correspond to _nothing_, i.e. no instruction is generated for it. There are
really endless possibilities in producing the semantic behavior described by the
Python language reference.

# CPython is an implementation of the Python language specification
CPython is an implementation of the Python language specification. In fact, it
is the [_reference_ implementation](https://wiki.python.org/moin/CPython),
meaning that its runtime semantics are the law. It is necessarily the case that
not all runtime semantics are precisely described in the Python documentation,
and then whatever CPython does is considered the desired behavior. Unless, of
course, it is identified as a bug in the runtime.

When it comes to the `pass` statement, CPython takes the "nothing" approach of
not generating an instruction. This has less overhead than generating and
executing a NOOP instruction. However, as the _effect_ of those two approaches
are the same, it would be equally correct to take the NOOP instruction approach.
So CPython is a reference for what happens when you execute some code, not _how_
that happens.

There are [other
implementations](https://wiki.python.org/moin/PythonImplementations?action=show&redirect=implementation)
of the Python programming language, such as [PyPy](https://www.pypy.org/). It is fundamentally different
to CPython in a variety of ways. For one, PyPy is implemented in Python, whereas
CPython is to a large extent implemented in C. PyPy also employs a JIT
(just-in-time) compiler that can compile hot code to machine code to
substantially speed up running times, often making it [substantially faster than
CPython](https://speed.pypy.org/).

# Closing words
The difference between Python and CPython is that the former is a language
specification while the latter is an implementation of said language
specification. However, in most everyday conversations among developers, they
are one and the same. There is also the fact that CPython being the reference
implementation makes it part of the specification of the language. Python as a
programming language and CPython as an implementation are to some extent
mutually dependent: you can't really define one without the other.

Distinguishing at all between the two may seem nit-picky, and in the vast
majority of cases I'd argue it is. But when module documentation mentions
implementation details of CPython or you find mentions of other implementations
altogether, the distinction becomes important for it all to make sense.
For me personally, just the urge to understand why two different words were used
for seemingly the same thing was enough of a justification to dig into it, but
I'm also hoping that this article brings more sense into the Python worlds of
others.
