Title: Java's Optional: Why you should prefer it over null
Date: 2019-10-11 16:57
Author: Simon Larsén
Tags: java

Null references are problematic, to say the least. Tony Hoare (inventor of the
null reference) even went as far to say call them his ["billion dollar
mistake"](https://en.wikipedia.org/wiki/Tony_Hoare#Apologies_and_retractions).
In this article, I first make a cursory exploration of why null references are
so problematic, and then have a look at Java's proposed solution: the
[`Optional<T>` class](https://docs.oracle.com/javase/8/docs/api/java/util/Optional.html).

# Why null is problematic
There are many reasons why null is problematic, but there are a few that are
particularly easy to illustrate. I will be using the
[`Map.get`](https://docs.oracle.com/javase/8/docs/api/java/util/Map.html#get(java.lang.Object))
method as an example, as it returns null if the key provided to it is not in
the map. For all of the examples, assume that there is a variable `Map<Integer,
String> map` in the current scope.

## null circumvents the type system
Java has a fairly rigorous type system (although it's not entirely sound, I may
do an article on that later!). The type system can't help with null, however.
Any variable of reference type can either contain a reference to an object of
that type, or null. This leads to a whole lot of code that looks like this:

```java
String value = map.get(10);
String valueUpper;
if (value != null) {
    valueUpper = value.toUpperCase();
}
// else do something different with the knowledge that value is null
```

While you may argue that null checks are pretty ugly, the real problem is that
they are not enforced by the type system. The above might just as well have
been written like this, and the type checker would have been none the wiser:

```java
String value = map.get(10);
String valueUpper = value.toUpperCase();
```

This program could crash with a `NullPointerException`. That's not great. But
it can be even worse. What if the call to `value.toUpperCase()` occurs in an
entirely different part of the program, perhaps hours or even days after
`Map.get` returned null? Then, not only do you have a crash, but a crash that
can potentially be very difficult to diagnose.

## It's easy to miss that a method can return null
The cause of the previous problem is often that it's not always obvious that a
method may return null. If you have a look at the [documentation for
Map.get](https://github.com/openjdk/jdk/blob/0dbfc97c05218ffd10242901d73c0715ccb53bf3/src/java.base/share/classes/java/util/Map.java#L217-L242),
you'll see that it says that it may return null a little here and there, and
it's pretty clear about that. But still, a careless developer might miss this,
and there's also the fact that many methods are _not_ this well documented.

## Why not just throw an exception instead?
One question you may ask is, why even return null, why not just throw an
exception? Indeed, throwing an exception may be a good solution in many cases,
but sometimes it just isn't desirable. In the case of `Map.get`, it's mostly
about efficiency. If `Map.get` were to throw an exception when the key was
missing, you'd essentially have two alternatives. 

### Ask for forgiveness (catch the exception)

```java
String value;
try {
    value = map.get(10);
} catch (NoSuchElementException e) {
    // handle error
}
```

That's both ugly, and very inefficient if it is often the case that the key is
missing. Catching an exception involves a whole lot of work for the JVM, so you
really do not want to do this for an operation that you often perform.

### Look before you leap

```java
String value;
if (map.containsKey(10)) {
    value = map.get(10);
}
// else handle missing keys
```

This is not too ugly, but it is inefficient as the map has to be traversed twice:
once to check if it contains the key, and once more to fetch the value
associated with the key. Throwing an exception becomes even more undesirable if
you're using
[Streams](https://docs.oracle.com/javase/8/docs/api/java/util/stream/Stream.html).
So, I think we can safely conclude that throwing an exception is not the
be-all-end-all solution.

# `Optional<T>` to the rescue
Using the [`Optional<T>`
class](https://docs.oracle.com/javase/8/docs/api/java/util/Optional.html), we
solve the issues discussed previously. `Optional` is simply a container for
another object that may or may not be null.
[`Optional.get`](https://docs.oracle.com/javase/8/docs/api/java/util/Optional.html#get--)
returns the contained object if present, or throws a `NoSuchElementException` if
it is not (i.e. it is null).
[`Optional.isPresent`](https://docs.oracle.com/javase/8/docs/api/java/util/Optional.html#isPresent--)
lets us check first if the value is present, to avoid an exception if it is not.
**Let's pretend** like there's a method `Map.getOptional` that returns an
`Optional<T>` instead of just `T`. We then have several options.

> **Important:** There is no `Map.getOptional` method, this is just
> hypothetical. We'll see toward the end of the article how one can wrap
> `Map.get` to create a `getOptional` method.

## Retrieve the value without checking if it is present
If you're certain that the value will be present, you may simply retrieve it
immediately.

```java
Optional<String> opt = map.getOptional(10);
String value = opt.get(); // `value` will either be non-null, or we crash
```

This may at first glance just look like more work than previously, two `get`
calls instead of one. The benefit here is that the programmer is extremely
unlikely to miss the fact that the returned value may not be present, as the
return value itself has the type `Optional<String>`, and the type system will
scream bloody murder if they try to use the `Optional<String>` value like a
`String`. Requiring that extra `get` _forces_ the programmer to make a conscious
choice of how to handle errors. Now, this may crash with a
`NoSuchElementException`, but as `Optional` values typically are not passed
around, the is unlikely to happen far from where the `Optional` was produced.

## Check if the object is present
If you're uncertain whether the value will be present, you may simply check for
it:

```java
Optional<String> opt = map.getOptional(10);
String value;
if (opt.isPresent()) {
    value = opt.get();
}
```

This is very much like the null check we had before, but it's supported by the
type system.

## Use a fallback value
Often when we don't want the code to crash, we have a fallback value. `Optional`
has a method to handle that.

```java
String value = map.getOptional(10).orElse("Nothing here :)");
```

If the value is present, it is returned. Otherwise, we get `"Nothing here :)"`.
This, I think, is one of the cleanest and tidiest uses of `Optional`.

## What about drawbacks?
Of course, `Optional` has drawbacks. As every single object is wrapped in
another object, there will be an increase in memory consumption. The extra
method call _may_ result in a noticeable performance penalty, but I don't dare
say anything concrete about that without running some tests (the JVM is pretty
darn good at inlining and optimizing). Perhaps, your most performance critical
segments of code should not use `Optional`. But the vast majority of your code
is not performance critical, so most often it will be a moot point. Finally,
there's also a little bit of extra boilerplate to deal with, which also may not
be desirable.

# Alright, I'm sold, how do I `Optional`?
We've already had a look at how to consume `Optional`s. But how do we produce
them? It's really quite easy. The three most important methods are:

1. [`static <T> Optional.of(T value)`](https://docs.oracle.com/javase/8/docs/api/java/util/Optional.html#of-T-)
    - A static method that wraps a value in an `Optional` instance. Throws an
      exception if `value` is `null`.
2. [`static <T> Optional.empty()`](https://docs.oracle.com/javase/8/docs/api/java/util/Optional.html#empty--)
    - A static method that returns an empty `Optional` instance.
3. [`static <T> Optional.ofNullable(T value)`](https://docs.oracle.com/javase/8/docs/api/java/util/Optional.html#ofNullable-T-)
    - A static method that wraps a value in an `Optional`. The value may be
      `null`, which essentially produces an empty `Optional`.

The `of` and `empty` methods are the ones you want to produce `Optional` values
from scratch. Here's a useless but simple example: an identity function for
integer values that is only defined for `n >= 0`. Using null, it would look
like this.

```java
/**
 * @param n An Integer value.
 * @return n iff n >= 0, otherwise null
 */
public Integer id(Integer n) {
    if (n >= 0) {
        return n;
    }
    return null;
}
```

This comes with all of the previously discussed problems associated with null
return values. Here's the equivalent method using `Optional`.

```java
/**
 * @param n An Integer value.
 * @return An Optional with n iff n >= 0, otherwise an empty Optional.
 */
public Optional<Integer> id(Integer n) {
    if (n >= 0) {
        return Optional.of(n);
    }
    return Optional.empty();
}
```

Notice how both the documentation, and the return value itself, clearly states
that the value returned from the method may not be present. It is more or less
impossible to miss that this method may return an empty value (as long as you
know what `Optional` is, that is).

The `ofNullable` method is great for wrapping existing methods that may return
null. For example, assuming that we have the `Map<Integer, String> map` field
from earlier, we can wrap its `get` method in our own `getOptional`.

```java
public getOptional(Integer key) {
    String value = map.get(key); // might be null!
    return Optional.ofNullable(value);
}
```

This lets us easily create APIs that contain two versions of, for example, a
getter method: one that returns `T`, and one that returns `Optional<T>`. And
that's all the essentials. Not that hard, right?

# Summary
`Optional` solves most of the problems with null references in a mostly
elegant way. The most important thing with `Optional` is that it is a strong
form of documentation, which states both to the programmer and to the compiler
that the value asked for may be present. There's also the fact that
`Optional` provides both the null-check approach using `isPresent`, and the
exception-throwing approach by calling `get` without checking for presence. As
such, the caller of a method gets to decide which of these approaches to use,
increasing flexibility. `Optional` is also a critical part of the [Stream
API](https://docs.oracle.com/javase/8/docs/api/java/util/stream/Stream.html),
which would be forced to throw exceptions left and right without it (and you'd
be forced to catch them!). Although the use of `Optional` may incur a
performance penalty, it is trivial to provide two versions of performance
critical methods: one that returns an `Optional<T>` and one that just returns
`T`. If you want to learn more about `Optional`, I recommend first checking out
[the API
documentation](https://docs.oracle.com/javase/8/docs/api/java/util/Optional.html).
I also encourage having a look at the [source
code for
`Optional`](https://github.com/openjdk/jdk/blob/a95a39a04e066548764e15bfc793a6c242a22bb7/src/java.base/share/classes/java/util/Optional.java),
it's a surprisingly simple class that provides all of this functionality!
