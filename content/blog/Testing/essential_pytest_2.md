Title: Essential pytest pt. 2: Selecting tests to run
Date: 2020-10-03 14:00:00
Author: Simon Larsén
Slug: essential-pytest-2
Tags: python,pytest,testing

This is the second part of a series of small articles detailing some of the
functionality of the [pytest](https://docs.pytest.org/en/latest/) testing
framework that I find most essential. The series assumes you know how to run
tests with `pytest` already.

In this second part, we'll take a look at the `-k` and `-m` options to control
which tests in the test suite are executed.

## The test suite
In this article, we'll use the test suite from [the first
article]({filename}essential_pytest_1.md).

```python
# test_mul.py
def mul(lhs, rhs):
    return lhs * rhs

def test_multiply_equal_numbers():
    assert mul(5, 5) == 25

def test_multiply_by_zero():
    assert mul(1, 0) == 0

def test_multiply_different_numbers():
    assert mul(5, 3) == 15
```

Note that `mul` is now correctly implemented, so all tests will pass.

```bash
$ pytest -v
========================== test session starts ===========================
platform linux -- Python 3.8.5, pytest-6.1.0, py-1.9.0, pluggy-0.13.1
cachedir: .pytest_cache
rootdir: /home/slarse/python
collected 3 items                                                        

mul.py::test_multiply_equal_numbers PASSED                         [ 33%]
mul.py::test_multiply_by_zero PASSED                               [ 66%]
mul.py::test_multiply_different_numbers PASSED                     [100%]

=========================== 3 passed in 0.01s ============================
```

Now, let's learn how to run subsets of these tests, without modifying the
source code.

## Using the `-k` option to select tests by substring matching
The `-k` option is wonderful, and allows us to select a subset of tests to
execute based on simple substring matching. The simplest use of `-k` is to
provide it with a whitespace-less string. Any test with a name that _contains_
that string will be executed. To be clear, the name of a test is e.g.
`mul.py::test_multiply_equal_numbers`, that is to say, the qualified path to it.

As a simple example, we can select only the test that multiplies by zero like
so.

```bash
$ pytest -v -k zero
========================== test session starts ===========================
platform linux -- Python 3.8.5, pytest-6.1.0, py-1.9.0, pluggy-0.13.1
cachedir: .pytest_cache
rootdir: /home/slarse/python
collected 3 items / 2 deselected / 1 selected                            

test_mul.py::test_multiply_by_zero PASSED                          [100%]

==================== 1 passed, 2 deselected in 0.05s =====================
```

Note that 2 tests were deselected. It is also possible to create logical
expressions using `not`, `or` and `and`.  `not` simply inverts the condition:
any test that does _not_ match the substring is executed.

```bash
$ pytest -v -k 'not zero'
========================== test session starts ===========================
platform linux -- Python 3.8.5, pytest-6.1.0, py-1.9.0, pluggy-0.13.1
cachedir: .pytest_cache
rootdir: /home/slarse/python
collected 3 items / 1 deselected / 2 selected                            

test_mul.py::test_multiply_equal_numbers PASSED                    [ 50%]
test_mul.py::test_multiply_different_numbers PASSED                [100%]

==================== 2 passed, 1 deselected in 0.05s =====================
```

With `or`, we can select tests that match any of a number of substrings.

```bash
$ pytest -v -k 'equal or different'
========================== test session starts ===========================
platform linux -- Python 3.8.5, pytest-6.1.0, py-1.9.0, pluggy-0.13.1
/usr/bin/python
cachedir: .pytest_cache
rootdir: /home/slarse/python
collected 3 items / 1 deselected / 2 selected                            

test_mul.py::test_multiply_equal_numbers PASSED                    [ 50%]
test_mul.py::test_multiply_different_numbers PASSED                [100%]

==================== 2 passed, 1 deselected in 0.06s =====================
```

Finally, `and` allows us to select tests that match multiple substrings.

```bash
$ pytest -v -k 'multiply and equal'
========================== test session starts ===========================
platform linux -- Python 3.8.5, pytest-6.1.0, py-1.9.0, pluggy-0.13.1
/usr/bin/python
cachedir: .pytest_cache
rootdir: /home/slarse/python
collected 3 items / 2 deselected / 1 selected                            

test_mul.py::test_multiply_equal_numbers PASSED                    [100%]

==================== 1 passed, 2 deselected in 0.05s =====================
```

And that's pretty much all there is to the `-k` option. It's extremely useful
when test suites grow in size, and I use it daily.

## Using the `-m` option to select by marker
With `-m`, we can select tests by _markers_. You can mark a test function (or
class) by placing a decorator above it.

```python
# test_mul.py
import pytest

def mul(lhs, rhs):
    return lhs * rhs

@pytest.mark.normcase
def test_multiply_equal_numbers():
    assert mul(5, 5) == 25

@pytest.mark.edgecase
def test_multiply_by_zero():
    assert mul(1, 0) == 0

@pytest.mark.normcase
def test_multiply_different_numbers():
    assert mul(5, 3) == 15
```

Note that we must actually import the `pytest` module to be able to mark tests
with `@pytest.mark.x`. Now, we can run all tests marked with e.g. `normcase`
like so.

```bash
$ pytest -v -m normcase
========================== test session starts ===========================
platform linux -- Python 3.8.5, pytest-6.1.0, py-1.9.0, pluggy-0.13.1
cachedir: .pytest_cache
rootdir: /home/slarse/python
collected 3 items / 1 deselected / 2 selected                            

test_mul.py::test_multiply_equal_numbers PASSED                    [ 50%]
test_mul.py::test_multiply_different_numbers PASSED                [100%]

============================ warnings summary ============================
test_mul.py:6
  /home/slarse/python/test_mul.py:6: PytestUnknownMarkWarning: Unknown pytest.mark.normcase - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/mark.html
    @pytest.mark.normcase

[... 2 WARNINGS OMITTED ...]

-- Docs: https://docs.pytest.org/en/stable/warnings.html
============== 2 passed, 1 deselected, 3 warnings in 0.01s ===============
```

Note that this resulted in 3 warnings, one for each of the markings. The reason
for this is that newer versions of `pytest` want you to _register_ markers, [as
described
here](https://docs.pytest.org/en/stable/example/markers.html#registering-markers).
The purpose of this is to avoid users misspelling markers, and registering them
will make the warnings go away.

As might be expected, the `-m` option also accepts logical expressions using
`not`, `and` and `or`, just like the `-k` option does. Personally, I very rarely
use `-m` when using `pytest`, but some people swear by it, which is why I wanted
to include it in this article.

## Trick: Grouping related tests into classes makes selection easier
A trick that I like to employ is to group related tests into classes. The class
name is then incorporated into the test's name, and it becomes very easy to
select tests that are part of the same class. Here's a simple example, where I'm
testing two functions in the same module `test_arithmetics.py`:

```python
# test_arithmetics.py
def mul(lhs, rhs):
    return lhs * rhs

def div(lhs, rhs):
    return lhs / rhs

class TestMul:
    """Tests for the mul function."""

    def test_multiply_equal_numbers(self):
        assert mul(5, 5) == 25

    def test_multiply_by_zero(self):
        assert mul(1, 0) == 0

    def test_multiply_different_numbers(self):
        assert mul(5, 3) == 15

class TestDiv:
    """Tests for the div function."""

    def test_divide_equal_numbers(self):
        assert div(10, 10) == 1
```

Note that in grouping test functions into test classes, the `self` argument
must be added. This is a little bit annoying, as I rarely if ever use the
`self` argument in a test case, but it's something that has to be done.

Now, I can for example run only the tests in `TestDiv` like so.

```bash
$ pytest -v -k TestDiv
========================== test session starts ===========================
platform linux -- Python 3.8.5, pytest-6.1.0, py-1.9.0, pluggy-0.13.1
cachedir: .pytest_cache
rootdir: /home/slarse/python
collected 4 items / 3 deselected / 1 selected                            

test_arithmetics.py::TestDiv::test_divide_equal_numbers PASSED      [100%]

==================== 1 passed, 3 deselected in 0.05s =====================
```

Note that the test name that's printed above includes the class name, which is
why it is possible to select it with `-k`. Of course, grouping related tests
into modules is equally viable, as the module name (here, `test_arithmetics.py`)
is also part of the test name. I typically do both by creating one test module
per module of production code, and one test class per production code function.
This allows me to easily select tests at two levels of granularity, which comes
in very handy.

## Summary
Selecting a subset of test cases to run is crucial to my development workflow.
When there are 100s or even 1000s of tests to run, running all of them is often
not what you want to do. My preferred way of selecting test cases is by using
the `-k` option to match substrings of test names, but the `-m` option is also
there for those that like to put marker decorators in their code. Finally,
grouping related tests into modules and classes allows for easy selection of
tests on two levels of granularity, which is something that I exploit daily.
