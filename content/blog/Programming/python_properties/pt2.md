Title: Properties as Pythonic setters
Date: 2018-04-05T18:26:10Z
Author: Simon Larsén
Category: Programming
Tags: python

This is the second part in a two part series on Python properties. In
[Part 1]({filename}pt1.md) (which readers will be assumed to
have at least skimmed through), we saw how a property can be used to create a
read-only attribute that can be accessed like any data attribute (i.e with
`obj.attr`), but raises an `AttributeError` when written to. Now, we will look
at how to expand the property to also allow us to write to `count` like it's a
normal data attribute (i.e. with `t.count = 42`), while also doing input
validation.

### A property as a Pythonic setter
Using the `Ticker` class version from the final listing in 
[Part 1]({filename}pt1.md), we are unable to set the `count`
attribute to _any_ value.

```bash
>>> t = Ticker(24)  # valid range for count is thus [0, 23]
>>> t.count = 11    # this is well within that range
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: can't set attribute
can't set attribute

>>> for _ in range(11): # doing it the hard way ...
...     t.tick()
>>> t.count
11
```

This presents something of a usability issue, as the only way to set the
`Ticker`'s internal count to a specific value (using the public API) is by
calling `tick()` an appropriate amount of times. If we were to use the Ticker
as, say, a clock, we'd definitely want to be able to set `count` to a value
within the range `[0, _end)` by simple assignment. Fortunately, there is a
simple way to expand a property with a setter method using the `@<name>.setter`
decorator, where `<name>` is replaced with the name of the property. For the
`count` property of the `Ticker` class, it looks like this:

```python
@count.setter
def count(self, val):
    """Set the internal count to val."""
    if val < 0 or val >= self._end:
        raise ValueError(f"{val} is out of range for attribute count.")
    self._count = val
```

> **Note:** A string literal preceeded with an `f` is an _f-string_. This is a
> Python 3.6 feature. For backwards compatability, you could change to using
> `string.format` like this: 
>   `"{} is out of range for attribute count.".format(val)`
            
The code should be fairly self-explanatory. The setter takes a value `val` as
an argument. If `val` is outside of the allowed range `[0, _end)`, a
`ValueError` is raised.  Otherwise, `_count` is set to `val`. The error message
could be more informative, but I did not want to obscure the important parts
with a lot of text. We have thus defeated the aforementioned usability issue,
and usage now looks like this:

```python
>>> t = Ticker(24)
>>> t.count
0
>>> t.tick()
>>> t.count
1
>>> t.count = 11
>>> t.count
11
>>> t.tick()
>>> t.count
12
>>> t.count = 24
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 23, in count
ValueError: 24 is out of range for attribute count.
24 is out of range for attribute count.
```

Seems to work just the way we want it to!

### Ticker full listing (with getter/setter property)
Here is the full listing of the `Ticker` class.

```python
class Ticker:
    """A Ticker ticks from 0 to an upper limit, and then starts over."""

    def __init__(self, end: int):
        """Create a Ticker that starts over at end"""
        if end <= 0:
            raise ValueError("end must be greater than 0!")
        self._end = end
        self._count = 0

    def tick(self):
        """Increment the internal count by 1."""
        self._count = (self._count + 1) % self._end

    @property
    def count(self):
        """Return the current count."""
        return self._count

    @count.setter
    def count(self, val):
        """Set the internal count to val."""
        if val < 0 or val >= self._end:
            raise ValueError(f"{val} is out of range for attribute count.")
        self._count = val
```
