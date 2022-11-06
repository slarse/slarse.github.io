Title: The pre Python 2.5 ternary operator hack
Date: 2022-11-06
Author: Simon Larsén
Tags: python
Slug: python-24-ternary

The modern day ternary operator is well-known to most Pythonistas:

```python
<expr_if_true> if <condition> else <expr_if_false>
```

It's officially known as a _conditional expression_ and was introduced
back in Python 2.5 with [PEP
308](https://www.regular-expressions.info/atomic.html). Some like it, some
don't, and while discussing it with a colleague of mine he mentioned that there
"used to be something a whole lot worse" around the code bases written by
developers favoring ternary operators. He couldn't remember what it looked like
as these events are [15 years in the past](https://peps.python.org/pep-0356/),
but a few days later he came back to me with a code snippet like this:

```python
["nope", "yep"][False]
```

What?

## No ternary operator you say?

Developers are creative and opinionated. Sometimes this mix leads to
monstrosities, such as when creative developers who really liked ternaries
created this pattern:

```python
[<expr_if_false>, <expr_if_true>][<condition>]
```

You're reading that right. It's a list with two elements, the first of which
is returned if the condition is `False` and the second if it's `True`. Here is
an example:

```python
condition = True

message_modern = "success" if condition else "failure"
print(message_modern)   # success

message_old = ["failure", "success"][condition]
print(message_old)      # success
```

This will make perfect sense to a C programmer: `True` and `1` are
interchangeable, as are `False` and `0`. And that's precisely how this works,
the underlying [function that implements the list index
access](https://github.com/python/cpython/blob/2db55e0c0069a928775fa819973a76f840c5ab5a/Objects/listobject.c#L242-L255)
performs some rudimentary checks and then just uses the provided index as an
offset to the base pointer of the list.

## But the hack isn't quite the same

At first glance, it may seem like the old hack with the list is functionally
equivalent to the modern ternary operator. It isn't quite, though, because it
lacks one very important property: lazy evaluation of the branches. In short,
the ternary operator only evaluates the branch that it returns. Here's an
example:

```python
condition = False

result_modern = 1 / 0 if condition else 42
print(result_modern) # 42

result_old = [42, 1 / 0][condition] # raises ZeroDivisionError: division by zero
print(result_old)
```

The ternary operator does not result in a crash on division by zero as it does
not evaluate the expression in the true-branch, whereas the old hack crashes
immediately as it first evaluates both expressions and then returns one of them.
To fully emulate the modern behavior we'd need something like this:

```python
condition = False

result_old = [lambda: 42, lambda: 1 / 0][condition]()
print(result_old) # 42
```

Here we get lazy evaluation by virtue of wrapping the two branches in lambdas,
and then executing the lambda that's returned. I think we can all agree that's
not a pretty sight.

## Conditional expressions are a good thing
Regardless of your stance on using ternary operators (or conditional
expressions, as they're called in Python), it's probably a good thing they
exist. Otherwise creative and opinionated programmers get around to hacks to
emulate the behavior that end up being completely unreadable to others.
