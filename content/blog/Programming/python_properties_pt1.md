Title: Properties as Pythonic getters
Date: 2018-04-05T18:25:55Z
Author: Simon Larsén
Tags: python

If you come from either Java or C++, you've probably written your fair
share of getter and setter (also called accessor and mutator) methods.
It is common for programmers that transition from such a language to Python
to carry over this practice. In many cases in Python, we simply forego the
abstraction and access the attributes directly. Sometimes, however, getters
and setters are useful for providing write-protection and input validation.
In this two-part series, we are going to explore how to make Pythonic setters
and getters using one of my favorite Python features: **properties**. 

### Part 1 (this part): Properties as Pythonic getters
In this first part, we take a look at how to use a property
to implement a read-only data attribute that can be accessed just like any other
data attribute (e.g. like `obj.attr`). Writing to it will, however, result in an
`AttributeError`. This is useful for preventing users
from accidentally changing the internal state of an object in an unintended
way, while still providing a uniform API. For example, we might want a 
way to access the root element of a binary tree, but without risking to alter 
its container.

### [Part 2: Properties as Pythonic setters]({filename}python_properties_pt2.md)
In the second part, we'll have a look at how we can use properties to also
implement a setter method, with input validation, that can be utulized just 
like any plain ol' data attribute (e.g. like `obj.attr = 42`). This is useful
when the attribute has some legal set of values.

## The Ticker class
For the purpose of learning properties, we will develop a fairly useless class
called `Ticker`. All it does is tick from `0` to some boundary, and then restart
from `0`. Two `Ticker` instances could, for example, represent a rudimentary
clock with hour and minute counts. The first version of `Ticker` is outlined
below.

```python
class Ticker:
    """A Ticker ticks from 0 to an upper limit, and then starts over."""
    
    def __init__(self, end: int): # ': int' is an optional type hint
        """Create a Ticker that starts over at end"""
        if end <= 0:
            raise ValueError("end must be greater than 0!")
        self._end = end
        self.count = 0
        
    def tick(self):
        """Increment the internal count by 1."""
        self.count = (self.count + 1) % self._end    
```
            
We can use this class something like this:

```python
>>> t = Ticker(5)
>>> t.count
0
>>> t.tick()
>>> t.tick()
>>> t.count
2
>>> for _ in range(3):
...     t.tick()
>>> t.count
0
>>> t.count = 42    # uh oh...
>>> t.count
42                  # this is an illegal state
>>> t.tick()        # back to a legal state in the next tick
>>> t.count
3
```
    
As long as the `count` variable is only read from, there are no issues with this
design. Unfortunately, directly assigning to `count` may put the `Ticker` in an
illegal state, i.e. such that `count` is outside of its expected range of
`[0, _end)`. This isn't so much an issue for the `Ticker` itself, as it is
returned to a legal state on the next tick. Other functionality
depending on the `Ticker` to keep within the `[0, _end)` range could however be
in for a nasty surprise, meaning that there is a serious usability issue here.

Thus to the crux:

> How do we protect the `count` variable from being put in an illegal state,
> while still allowing access to it?

## Solving the problem
First of all, we should make the `count` variable private (which in Python
equates to prepending an underscore). The issue that remains to be resolved is
how to expose `_count` in the public API of the class.

### Solution 1: A Java-style getter
A Java or C++ programmer might instinctevly think of a traditional getter method.

```python
def get_count(self):
    """Return the current count."""
    return self._count
```
            
This solution has two issues: it breaks the api, and it makes us think about
`count` as something more complicated than the mere data attribute that it
is. It would be much preferable if we could access `_count` just like we
accessed it before it was made private (i.e. with `t.count`), but at the same 
time provide write protection (such that `t.count = 42` raises an error).
Enter the _property_.

### Solution 2: Using a property as a read-only data attribute
Implementing the same functionality as `get_count()` with a property is dead 
simple.

```python
@property
def count(self):
    """Return the current count."""
    return self._count
```
        
We use the `@property` decorator to say that the `count` method is a property.
This will let us invoke the `count` method without providing the parens, so
it will look like we are just accessing a data attribute named `count`.
Usage now looks like below:

```python
>>> t = Ticker(5)
>>> t.count
0
>>> t.tick()
>>> t.tick()
>>> t.count
2
>>> for _ in range(3):
...     t.tick()
>>> t.count
0
>>> t.count = 42
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: can't set attribute
can't set attribute
```
    
Excellent! We have the exact same API as when `count` was a public attribute,
but without the risk of accidental overwriting. This is precisely what we wanted,
and a Pythonic way of dealing with the issue of providing read access to fragile
state variables.

### Ticker full listing
It always annoys me when I get to the conclusion of some tutorial, and the end
result is just assumed to be obvious. Therefore, here is the full listing of
`Ticker` with a property as a getter.

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
```
            
Now is about the time to move on to
[Part 2]({filename}python_properties_pt2.md), in which we expand on the `count`
property to allow us to set the internal count, but only within the range `[0,
_end)`!
