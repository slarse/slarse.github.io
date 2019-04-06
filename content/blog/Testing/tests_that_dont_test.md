Title: Testing tips: Tests that don't test
Date: 2019-03-05T22:07:56Z
Author: Simon Larsén
Slug: tests-that-dont-test
Tags: unit testing,testing tips

Unit testing is a skill that takes some time to develop, and there are numerous
pitfalls for the beginner. As I've done my fair share of unit testing, and
taught a lot of students what I know, I've decided to share my top tips of
things to think about when testing. First up is one that may seem obvious, but
beginners and experienced testers alike fail with on occasion: make sure you
are actually testing something.

## Tests that don't test
Quite often, I find tests written by students that don't actually test anything,
and will pass regardless of what the student's code is doing. Sometimes, I find
tests written by yours truly that are similarly ineffective. A test that passes
when it should not is dangerous, because it makes you feel confident about code
that isn't properly tested. On the flip side, a test that fails when it should
not is annoying and may hamper productivity, but unlike a falsely positive test,
it is highly noticeable. The devious part of tests that don't test is that they
easily slip by unnoticed, you don't often investigate a test that passes! These
tests generally come in four flavors:

1. Not calling the function under test.
2. Copy mistakes with references/pointers.
3. Mistakes during setup.
4. Mistakes with assertions.

Even though I have a few years worth of testing experience, and have written
thousands upon thousands of tests, I still make these mistakes from time to
time. Let's first go over them one by one to get a feel for what can go wrong.
After that, I'll share my techniques for catching these errors. For all of the
examples, we will look at a test case for sorting a randomly ordered list with
an in-place sorting algorithm. The implementation under test is called `mysort`.
Assume that, for all examples, a list called `random_list` with randomly ordered
elements is setup in a fixture. The tests will be written in `pytest` syntax,
but most problems and solutions are easily transferable to many other languages
and testing frameworks (e.g. JUnit in Java). Here is the test header and
docstring. Note the inclusion of the `random_list` fixture as a parameter. In the test,
it can simply be used as a list.

```python
def test_sort_randomly_ordered_list(random_list):
    """Sort a randomly ordered list and ensure that the result for
    ``mysort`` is the same as the built-in ``list.sort``
    """
```

For brevity, the docstring will be excluded from now on.  Let's get to it the,
shall we?

### Not calling the function under test
This mistake definitely sits in the top two most common ones that I encounter. A
typical example of this is when using _redundant computation_ to produce a test
oracle. That is, using some other implementation of the function under test to
compute the expected result. What I've seen happen many times is that the
student by mistake uses the other implementation for both the expected value,
and the actual value. Here's an example.

```python
def test_sort_randomly_ordered_list(random_list):
    # calculate test oracle
    expected = list(random_list) # note the copy for later!
    expected.sort()

    # calculate actual value, use ``sort`` by mistake
    # should be ``mysort(random_list)``
    random_list.sort()

    assert random_list == expected
```

Obviously, this test will always pass as `list.sort` is used for both
computations. This is a very common mistake, and if made once in a test suite, I
often find it propagating elsewhere due to copy-paste errors. This kind of
mistake is applicable in most any language, and is especially easy to make if
the redundant function and the function under test have similar names and usage
(which was actually not the case here!).

### Copy mistakes with references/pointers
Another very common issue that is often related to redundant computation is
failing to make a proper copy of a data structure. If you have a look at the
previous example, there is comment telling you to note the copy. Compare that
with this example:

```python
def test_sort_randomly_ordered_list(random_list):
    # calculate test oracle
    expected = random_list # this is not a copy!
    expected.sort()

    # calculate actual value
    mysort(random_list)

    assert random_list == expected
```

Just assigning `expected = random_list` will not create a copy of `random_list`,
but copy the reference to the list. Therefore, both `expected` and `random_list`
reference the _same list_. The assertion is then semantically equivalent to
`assert random_list == random_list`, which is obviously true no matter what
`mysort` did with the list. This is a problem in any language that uses
references (not C++ references, but pointer-like references), such as Java and
Python, or when dealing with pointers in pretty much any language that has them.

### Mistakes during setup
This is also fairly common, and can manifest in a variety of ways. The general
idea is that the setup is performed such that the outcome of the test is very
likely to be the same even if the production code is anything but correct. One
example would be that the supposedly randomly ordered list is actually
comprised of duplicates of a single element. Let's have a look at an incorrect
implementation of the `random_list` fixture. Note that `_` is used as a
variable name when we don't care about the value of it.

```python
@pytest.fixture
def random_list():
    """Generate a randomly ordered list with 100 elements."""
    lst = []
    for _ in range(100):
        random.seed(5234) # seed to make list generation deterministic
        lst.append(random.randint(-100, 100))
    return lst
```

It is good practice to _seed_ the pseudo-random generator (PRG) when testing to
make tests reproducible. A PRG is actually a deterministic function that, given
an initial state (a seed), will always produce the same sequence of numbers.
`random.seed(5234)` sets this initial state to `5234`. This fixture is actually
fairly well implemented, but has a critical error. Since the seed is set inside
the loop, before the call to `random.randint`, the latter will always produce
the same value. As the list is already sorted, `mysort` can do almost anything
but remove an element and still pass the test. This is a fairly sophisticated
error that an intermediate tester may accidentally make. There are infinite
variations on how setup may go wrong, and this is applicable to pretty much any
programming language. As a side note, the correct way to do this would of
course be to seed _before_ the loop. Note that even with the correct
configuration, there is a very small chance that the random elements are
generated in ascending order.

### Mistakes with assertions
The final issue is also common, and comes in many shapes and forms. One thing I
sometimes see is that the assertions are tautologies, such as `assert
random_list == random_list` (obviously true), and probably mostly result from
typos and unchecked auto-completion. Another common one is that assertions are
simply missing, and is most often found in tests that are large enough that a
missing line or two is not immediately apparent.

## Finding tests that don't test
There are essentially two ways I know of to find tests that (pretty much) never
fail.

1. Write the tests first (Test-driven development)
2. Inject errors into production code and expect tests to fail

### Test-driven development (TDD)
TDD involves writing the test cases before you implement the functionality.
You first write the test cases, ensure that the test cases fail, and then
implement the production code such that the tests pas. I typically use TDD
when:

* The functionality I need to implement is strictly defined.
    - Fox example when implementing well-defined algorithms and data structures.
* I'm fixing a bug.
    - Reproduce the bug with a test-case, then fix it!

This approach will catch many incarnations of the errors I've brought up in
this article simply because the tests should definitely not pass before the
production code is even written. There is one caveat, though. Some
practitioners of TDD think that test cases should be written even before the
function skeletons have been written, and argue that a compilation failure is
also a test failure. With that approach, you probably will not catch any of the
errors brought up here, except maybe
[the first one](#not-calling-the-function-under-test). My recommendation for
TDD is to write function skeletons and make sure the function can actually be
called (it's perfectly fine if it crashes after being called). _Then_ write
your tests, and make sure they fail before you start implementing production
code. I don't think TDD is always practical to use, however, especially when
I'm a bit unsure of what to do and need to experiment with different APIs.
That's when the second technique comes in real handy.

### Inject errors into production code and expect tests to fail
This is a highly useful technique that can always be performed, and I do this
almost every time I implement tests after production code. The idea is simply to
consider what your test is testing, and inject errors into the production code
such that the test should fail. `test_sort_randomly_ordered_list` is a fairly
broad test case, so we can inject fairly general errors. A simple example would
simply be to return early such that `mysort` does not sort at all. Narrower test
cases may require more sophisticated errors to be injected.

> **Aside: Mutation testing** There is actually a whole field of testing
> dedicated to this kind of error (or _fault_) injection called
> [mutation testing](https://en.wikipedia.org/wiki/Mutation_testing). Faults are
> automatically injected into production code, and the test suite is run to
> determine whether the fault is found (_killed_) or not. There are frameworks
> for this, such as the [Pitest](http://pitest.org/) for Java, and
> [Cosmic Ray](https://github.com/sixty-north/cosmic-ray) for Python. In
> general, it takes a _long_ time to run mutation testing on a test suite, as
> often the whole test suite needs to be run for a single fault. And there are
> many, many possible faults.

## Summary
While I framed this as a unit testing article, these concepts are applicable to
most kinds of testing. You should always attempt to make sure that your test is
doing what it claims to be doing. A single typo may be what stands between a
test that does not test, and a test that does. This article focused on finding
tests that don't test, but there are also things you can do to _prevent_ tests
that don't test from manifesting. Copy/pasting test code and then making minor
changes is for example a common source of most of the discussed errors. But
ultimately, there is no surefire way of avoiding tests that don't test, so I
strongly recommend that you actively search for them no matter what precautions
you take!
