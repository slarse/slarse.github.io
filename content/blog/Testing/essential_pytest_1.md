Title: Essential pytest 1: Controlling the verbosity of output
Date: 2020-07-31T20:07:56Z
Author: Simon Larsén
Slug: essential-pytest-1
Tags: python,pytest,testing

This is the first part of a series of small articles detailing some of the
functionality of the [pytest](https://docs.pytest.org/en/latest/) testing
framework that I find most essential. The series assumes you know how to run
tests with `pytest` already.

In this first part, we'll take a look at the `-v` and `--tb` options to control
the verbosity of the output.

## The test suite
For the purposes of this article, I've implemented a very simple multiplication
function called `mul`, along with a few tests. Here's the entire thing, in a
file called `mul.py`:

```python
# mul.py
def mul(lhs, rhs):
    return lhs * lhs

def test_multiply_equal_numbers():
    assert mul(5, 5) == 25

def test_multiply_by_zero():
    assert mul(1, 0) == 0

def test_multiply_different_numbers():
    assert mul(5, 3) == 15
```

Obviously, the implementation of `mul` is broken, and running `pytest` gives
the following output.

```bash
$ pytest mul.py 
========================== test session starts ===========================
platform linux -- Python 3.8.3, pytest-5.4.3, py-1.9.0, pluggy-0.13.1
rootdir: /home/slarse/Documents/github/python/mul
collected 3 items                                                        

mul.py .FF                                                         [100%]

================================ FAILURES ================================
_________________________ test_multiply_by_zero __________________________

    def test_multiply_by_zero():
>       assert mul(1, 0) == 0
E       assert 1 == 0
E        +  where 1 = mul(1, 0)

mul.py:8: AssertionError
____________________ test_multiply_different_numbers _____________________

    def test_multiply_different_numbers():
>       assert mul(5, 3) == 15
E       assert 25 == 15
E        +  where 25 = mul(5, 3)

mul.py:11: AssertionError
======================== short test summary info =========================
FAILED mul.py::test_multiply_by_zero - assert 1 == 0
FAILED mul.py::test_multiply_different_numbers - assert 25 == 15
====================== 2 failed, 1 passed in 0.08s =======================
```

Let's learn how to control how much of this we see.

## Using the `--tb` option to control traceback verbosity
Most of what you're seeing in the output of the previous section is the
_traceback_ information. While the traceback shown above is manageable as is,
consider that it stems from a single-line function and single-line tests. With
that in mind, it's actually pretty freaking verbose. We can show less of it by
using the `--tb` option. We can even shut it off completely.

```bash
$ pytest mul.py --tb=no
========================== test session starts ===========================
platform linux -- Python 3.8.3, pytest-5.4.3, py-1.9.0, pluggy-0.13.1
rootdir: /home/slarse/Documents/github/python/mul
collected 3 items                                                        

mul.py .FF                                                         [100%]

======================== short test summary info =========================
FAILED mul.py::test_multiply_by_zero - assert 1 == 0
FAILED mul.py::test_multiply_different_numbers - assert 25 == 15
====================== 2 failed, 1 passed in 0.02s =======================
```

This is useful when you're just trying to figure out what tests are failing, and
when test output is just entirely overwhelming. I find myself using it quite
frequently. Another useful traceback value is `line`.

```bash
$ pytest mul.py --tb=line
========================== test session starts ===========================
platform linux -- Python 3.8.3, pytest-5.4.3, py-1.9.0, pluggy-0.13.1
rootdir: /home/slarse/Documents/github/python/mul
collected 3 items                                                        

mul.py .FF                                                         [100%]

================================ FAILURES ================================
/home/slarse/Documents/github/python/mul/mul.py:8: assert 1 == 0
/home/slarse/Documents/github/python/mul/mul.py:11: assert 25 == 15
======================== short test summary info =========================
FAILED mul.py::test_multiply_by_zero - assert 1 == 0
FAILED mul.py::test_multiply_different_numbers - assert 25 == 15
====================== 2 failed, 1 passed in 0.03s =======================
```

This lets us see the exact lines where the test failures occurred. In this case,
it shows the lines of the assertions, but it could also for example show the
line where an exception was raised. There are more ways to manipulate the
traceback, but these are the two I use the most, aside from the default. To see
the other options, refer to `pytest -h` and look for the `--tb` option.

## Using `-v` to show more verbose test output
The `-v` option controls the verbosity of test output while the tests are
running. It's really useful when tests take a long time to run, and you want to
know approximately where you're at.

```bash
$ pytest mul.py --tb=no -v
========================== test session starts ===========================
platform linux -- Python 3.8.3, pytest-5.4.3, py-1.9.0, pluggy-0.13.1 -- /usr/bin/python
cachedir: .pytest_cache
rootdir: /home/slarse/Documents/github/python/mul
collected 3 items                                                        

mul.py::test_multiply_equal_numbers PASSED                         [ 33%]
mul.py::test_multiply_by_zero FAILED                               [ 66%]
mul.py::test_multiply_different_numbers FAILED                     [100%]

======================== short test summary info =========================
FAILED mul.py::test_multiply_by_zero - assert 1 == 0
FAILED mul.py::test_multiply_different_numbers - assert 25 == 15
====================== 2 failed, 1 passed in 0.03s =======================
```
Note how each test is now shown on a line of its own, as opposed to just `.` and
`F` in the previous runs. The lines show up as the tests are running, and I find
it useful to track long-running tests.

And that's pretty much it for basic output verbosity control with `pytest`, hope
you learned something!
