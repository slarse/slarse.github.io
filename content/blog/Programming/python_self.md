Title: What the self? Python's self demystified!
Date: 2018-05-01T16:04:01Z
Author: Simon Larsén
Tags: python

Any Python programmer will sooner or later want to (or have to) write a class.
With classes come `self`, the _seemingly_ (do note the emphasis there)
magical keyword that you just have to write out as the first parameter to every
method. To really understand classes, you need to understand what `self`
actually is: neither magical, nor a keyword. Let's demystify this integral part
of Python classes!

## `self` is not a keyword
This is pretty easy to prove. Just open a Python interpreter and import the
`keyword` module.

```python
>>> keyword.iskeyword("for")
True                            # aha, makes sense
>>> keyword.iskeyword("else") 
True                            # seems to be working
>>> keyword.iskeyword("self")
False                           # proof!
```
    
Alternatively, one can always consult the
[list of keywords in the Python docs](https://docs.python.org/3/reference/lexical_analysis.html#keywords).
Since `self` is not a keyword, it has no special significance in the language
itself. We can also verify that it's not some funky builtin by simply typing
it out in the interpreter.

```python
>>> self
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
NameError: name 'self' is not defined
name 'self' is not defined
```

This can [verified here](https://docs.python.org/3.6/library/constants.html)).
So, what in the world is `self`? Actually, it's just a variable name.

> **Trivia:** If you try `keyword.iskeyword("True")` and
> `keyword.iskeyword("False")` in both Python2 and Python3, you will find that
> both are keywords in Python3, but not in Python2 (in 2, `True` and `False`
> are just builtin constants). In fact, `True` and `False` are not even
> write-protected in Python2, leading to shenanigans such as `True, False =
> False, True` being possible. In Python3, the keyword status of `True` and
> `False` make such an assignment a syntax error.

## `self` is just a variable name
Consider the following code snippet of a (pretty useless) class that just
stores two values (that are just assumed to be addable with each other),
and defines a method that returns the sum of the values.

```python
class Tuple:
    """A class for storing two values."""
    
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def sum(self):
        """Return the sum of 'first` and 'second'."""
        return self.first + self.second
```

Okay, so the class is terrible, but that really doesn't matter for the
purposes of this article. Now we see `self` in action for the first time.
From the code, it's purpose is quite clear: it refers to the object instance
on which the method is called. Usage looks something like this:

```python
>>> t = Tuple(4, 3)
>>> t.first
4
>>> t.second
3
>>> t.sum()  # `self` in `sum` refers to `t`
7
```

So, `self` is just a reference to the object on which the method is called (in
this case, `t`). This will probably become more apparent when reading
[Two ways to call methods](#two-ways-to-call-methods) further down, but just
suspend your disbelief for moment and assume it is so.
But, considering the `self` is just a variable to which `t` is assigned, what
happens if we replace `self` with, say, `donkey`?

```python
class Tuple:
    """A class for storing two values."""
    
    def __init__(donkey, first, second):
        donkey.first = first
        donkey.second = second

    def sum(donkey):
        """Return the sum of 'first' and 'second'."""
        return donkey.first + donkey.second
```

In fact, this will work exactly the same as when the first parameter was called
`self`, and usage is unchanged:

```python
>>> t = Tuple(4, 3)
>>> t.first
4
>>> t.second
3
>>> t.sum()
7
```

To summarize, the first parameter in a method is simply a variable that refers to
the instance on which the method was called. Naming it `self` is
[just a convention](https://docs.python.org/3.6/howto/descriptor.html#functions-and-methods)
, and we could name it anything. Note also that there is no technical
need for consistency across methods, we could name the first parameter to the
`__init__` method `donkey`, and the first (only) parameter to the `sum` method
`shrek`, and it'd still work.

```python
class Tuple:
    """A class for storing two values."""
    
    def __init__(donkey, first, second):
        donkey.first = first
        donkey.second = second

    def sum(shrek):
        """Return the sum of 'first' and 'second'."""
        return shrek.first + shrek.second
```

> **IMPORTANT:** _Always_ name the first parameter to a method `self`. The
> convention exists for a reason: it makes your code more readable.

We could leave it at this, and hopefully walk away with a slightly better
understanding of why we put `self` everywhere in methods. But I think diving
just a little bit deeper into where the first argument to methods actually
comes from will prove fruitful.

## Two ways of calling methods
Methods are defined on the class itself, and not on the instance. There is
actually a way to call a method directly on the class, that is equivalent to
the way we usually call methods on the instance.

```python
>>> t = Tuple(5, 6)
>>> t.sum()         # regular method call
11
>>> Tuple.sum(t)    # calling the method on the class itself, and passing
11                  # `t` as the `self` argument
```

The second way of calling `sum` is explicit about where `self` comes from: it's
passed in as the first argument. If we think of the first, "regular" way of
calling methods as shorthand for the second, it's suddenly entirely clear what
the first argument actually is (the instance itself). Calling a method that has
more parameters than just `self` works as expected: simply pass in the
additional arguments. To be super clear, with the following method added to
`Tuple`

```python
def sum_mod(self, mod):
    """Return the sum of the members modulo 'mod'."""
    return (self.first + self.second) % mod
```

the following two method calls are equivalent

```python
>>> t = Tuple(5, 7)
>>> t.sum_mod(5)
2
>>> Tuple.sum_mod(t, 5)
2
```
    
And that pretty much concludes what I wanted to cover in this article!

## Summary
In the beginning, someone (probably Guido) said _let there be `self`_. And there was.
The first parameter to a method is since then, _by convention_, called `self`, and
refers to the object on which the method was called.
Calling a method on some object `t` (e.g. `t.sum()`) can be viewed as shortand for
calling the method on its class, and passing in a reference to `t` as the first
argument (e.g. `Tuple.sum(t)`). If you are interested in learning about the dark magic
going on behind the scenes, you can read up on the official documentation for the
[descriptor protocol](https://docs.python.org/3.6/howto/descriptor.html), and
more specifically the
[Functions and Methods](https://docs.python.org/3.6/howto/descriptor.html#functions-and-methods)
part of it. It is however somewhat advanced, and I don't find it essential to
understanding the semantics of method calls in Python. I hope you have found
this article enlightening, stay tuned for more Python in the coming week!
