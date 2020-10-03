Title: Essential pytest pt. 3: Rerunning failed tests (and the pytest cache)
Date: 2020-10-03 19:00:00
Author: Simon Larsén
Slug: essential-pytest-3
Tags: python,pytest,testing

This is the third part of a series of small articles detailing some of the
functionality of the [pytest](https://docs.pytest.org/en/latest/) testing
framework that I find most essential. The series assumes you know how to run
tests with `pytest` already.

In this third part, we'll take a super quick look at the `--lf` flag that lets
us rerun failed tests, as well as the caching mechanism that makes it possible.

## Using `--lf` to rerun failed tests
In this article, we'll use the test suite from [the first
article]({filename}essential_pytest_1.md).

```python
# test_mul.py
def mul(lhs, rhs):
    return lhs * lhs

def test_multiply_equal_numbers():
    assert mul(5, 5) == 25

def test_multiply_by_zero():
    assert mul(1, 0) == 0

def test_multiply_different_numbers():
    assert mul(5, 3) == 15
```

Just like in that article, the implementation of `mul` is broken.

```bash
$ pytest -v --tb=no
========================== test session starts ===========================
platform linux -- Python 3.8.5, pytest-6.1.0, py-1.9.0, pluggy-0.13.1
cachedir: .pytest_cache
rootdir: /home/slarse/python
collected 3 items                                                        

test_mul.py::test_multiply_equal_numbers PASSED                    [ 33%]
test_mul.py::test_multiply_by_zero FAILED                          [ 66%]
test_mul.py::test_multiply_different_numbers FAILED                [100%]

======================== short test summary info =========================
FAILED test_mul.py::test_multiply_by_zero - assert 1 == 0
FAILED test_mul.py::test_multiply_different_numbers - assert 25 == 15
====================== 2 failed, 1 passed in 0.05s =======================
```

Note how 2 tests failed. `pytest` caches the failed tests from the last run,
which enables us to rerun them with the `--lf|--last-failed` flag. So let's do
that, and show some more traceback information while we're at it. Note that
only the failing tests are executed.

```bash
$ pytest -v --lf --tb=short
========================== test session starts ===========================
platform linux -- Python 3.8.5, pytest-6.1.0, py-1.9.0, pluggy-0.13.1
cachedir: .pytest_cache
rootdir: /home/slarse/python
collected 2 items                                                        
run-last-failure: rerun previous 2 failures

test_mul.py::test_multiply_by_zero FAILED                          [ 50%]
test_mul.py::test_multiply_different_numbers FAILED                [100%]

================================ FAILURES ================================
_________________________ test_multiply_by_zero __________________________
test_mul.py:8: in test_multiply_by_zero
    assert mul(1, 0) == 0
E   assert 1 == 0
E     +1
E     -0
____________________ test_multiply_different_numbers _____________________
test_mul.py:11: in test_multiply_different_numbers
    assert mul(5, 3) == 15
E   assert 25 == 15
E     +25
E     -15
======================== short test summary info =========================
FAILED test_mul.py::test_multiply_by_zero - assert 1 == 0
FAILED test_mul.py::test_multiply_different_numbers - assert 25 == 15
=========================== 2 failed in 0.12s ============================
```

My primary use case for `--lf` is for sorting out bugs. Every time a test
passes, it is removed from the last-failed cache, and thus does not run the next
time `--lf` is specified. This way, it's easy to quickly target only failing
tests, and systematically eliminate them one by one.

> **Pitfall:** A common mistake is to use `--lf` to eliminate the failing tests
> one by one, and then forget to run all tests when the last of the initially
> failing tests passes. It's entirely possible to fix the implementation such
> that a test `A` passes, and then subsequently reintroduce the same problem in
> addressing another test, but at that point `A` is no longer executing with
> `--lf`.

## Interacting with the cache
I mentioned that the failed tests from the last run are stored in a cache. This
cache is located in the `.pytest_cache` directory of the current working
directory. There are a few flags to interact with said cache. First, you can
execute `pytest` with the `--cache-show` flag to show the current contents of
the cache.

```bash
pytest --cache-show
========================== test session starts ===========================
platform linux -- Python 3.8.5, pytest-6.1.0, py-1.9.0, pluggy-0.13.1
rootdir: /home/slarse/python
cachedir: /home/slarse/python/.pytest_cache
-------------------------- cache values for '*' --------------------------
cache/lastfailed contains:
  {'test_mul.py::test_multiply_by_zero': True,
   'test_mul.py::test_multiply_different_numbers': True}
cache/nodeids contains:
  ['test_mul.py::test_multiply_by_zero',
   'test_mul.py::test_multiply_different_numbers',
   'test_mul.py::test_multiply_equal_numbers']
cache/stepwise contains:
  []

========================= no tests ran in 0.00s ==========================
```

Here, we can for example see the contents of the last-failed cache
(`cache/lastfailed`), and the tests currently known by `pytest`
(`cache/nodeids`). It's possible to supply `--cache-show` with an optional
value, in order to show only some part of the cache. For example,
`--cache-show=lastfailed` shows only the last-failed cache contents.

On occasion, the cache may get into an inconsistent state, typically due to
strange interactions by the user. This has happened to me on several occasions,
with tests simply not executing as I expect them to. At that point, supplying
the `--cache-clear` flag to a test run will clear the cache. Alternatively, you
may simply remove the `.pytest_cache` directory.

## Summary
Being able to execute only the failing tests from the previous test run is a
very handy feature when addressing bugs, both saving time in test execution and
limiting the amount of output shown to the user. It's however important to
remember to execute all tests after the last failing test passes, so as to check
for regressions. One should also be aware that the functionality hinges on
caching in the `.pytest_cache` directory, which on rare occasions may need to be
cleared.
