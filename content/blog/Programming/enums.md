Title: Don't use String for method options, use an enum!
Date: 2019-11-10 18:56
Author: Simon Larsén
Tags: java,enums

In this article, we are going to have a look at a method that accepts an option.
That is to say, it accepts an argument that somehow decides how it operates. If
you use a lot of libraries in your day-to-day programming, you're bound to come
across methods that accept `String` values as such options, and you've probably
been infuriated by you misspelling the options, or just trying to figure out
what options there are in the first place. That suggests that there must be a
better solution, and as you may have figured out by now,
[enums](https://docs.oracle.com/javase/tutorial/java/javaOO/enum.html) is that
solution.

> **Note:** This article discusses enums in Java, but the very same arguments
> are valid for any language that has support for enum types, or something
> comparable.


## The problem: What options do I have?
Consider the following method that formats a `String` according to an option
supplied as another `String`:

> Yes, this is a somewhat contrived example, but bear with me!

```java
public static String format(String str, String option) {
    switch (option) {
        case "upper":
            return str.toUpperCase();
        case "lower":
            return str.toLowerCase();
        default:
            throw new IllegalStateException("Internal errror, unmatched option " + option);
    }
}
```

We could then use the method something like this:

```java
format("hello", "upper");
```

Can you see any problems with this? Well first of all, if you don't have access
to the source, how do you know which options can be passed? There are an
infinite amount of strings, after all. At best, the Javadoc will say precisely
which values are valid options, [but that is not always the case even in the
Java standard
library](https://docs.oracle.com/javase/8/docs/api/java/nio/file/Files.html#getAttribute-java.nio.file.Path-java.lang.String-java.nio.file.LinkOption...-).
But even if all of the options are clearly documented at one point, it would be
so easy for a developer add or remove an option, and forget to enact the
corresponding change in the Javadoc. It is also difficult to have automatic
checks that actually verify that all possible options are documented. And even
assuming that all options are properly documented at all times, the compiler
can't distinguish which `String` values are valid and which are not, so a user
misspelling an option won't know until runtime.

## The solution: enums!
My goal here is not to explain the ins and outs of what enums are, but rather
show a use case. In short, an enum is a data type with a (typically very)
limited amount of possible values ([you can read more about it
here](https://docs.oracle.com/javase/tutorial/java/javaOO/enum.html)).
Now, let's instead define this enum type:

```java
public enum FormatOption {
    UPPER,
    LOWER;
}
```

And refactor the method with it:

```java
public static String format(String str, FormatOption option) {
    switch (option) {
        case UPPER:
            return str.toUpperCase();
        case LOWER:
            return str.toLowerCase();
        default:
            throw new IllegalStateException("Internal errror, unmatched option " + option);
    }
}
```

This method can then be used like:

```java
format("hello", FormatOption.UPPER);
```

With this small alteration, we have eliminated _all_ of the problems mentioned
before. The possible values for the `option` argument are now self-documented
in the `FormatOption` enum. Additionally, any modern IDE will kindly list the
possible values when you type `FormatOption.`, such that a programmer does not
even necessarily need to consult the documentation, assuming that the enum
values have descriptive enough names. The compiler can als distinguish between
`FormatOption.UPPER` and a misspelling such as `FormatOption.UPER`, as the
latter is not defined, so runtime errors due to invalid options is no longer a
problem.

## What's the catch?
So what's the catch? Well, if you have many methods like this, you'll end up
with a lot of enum types. Personally, I think that's totally worth it, and you
could also nest the nums inside the classes that use them to reduce their
overall footprint in the project. The whole thing could then look like this:

```java
public class Formatter {
    public static enum Option {
        UPPER,
        LOWER;
    }

    public static String format(String str, Option option) {
        String result;
        switch (option) {
            case UPPER:
                return str.toUpperCase();
            case LOWER:
                return str.toLowerCase();
            default:
                throw new IllegalStateException("Internal errror, unmatched option " + option);
        }
    }
}
```

Didn't add that much complexity now, did it?

## Summary
If you have a method that you want to pass options to, _use enums_.
That's really all there is to it. Enums are quite widely used in the Java
standard library as well, such as
[StandardCopyOption](https://docs.oracle.com/javase/8/docs/api/java/nio/file/StandardCopyOption.html),
[StandardOpenOption](https://docs.oracle.com/javase/8/docs/api/java/nio/file/StandardOpenOption.html) and
[LinkOption](https://docs.oracle.com/javase/8/docs/api/java/nio/file/LinkOption.html)
in the [`java.nio.file`
API](https://docs.oracle.com/javase/8/docs/api/java/nio/file/package-summary.html),
which are used much in the same way as I used the enum in this article.
Hopefully, having read this article, you won't be creating any more APIs that
accept `String` options!
