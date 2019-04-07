Title: A binary search tree in Kotlin pt. 1: Representing a node
Date: 2018-10-28T15:13:08Z
Modified: 2018-10-30T08:27:09Z
Author: Simon Larsén
Category: Programming
Tags: bst,kotlin,data structures

In my journey to become a somewhat competent Kotlin developer, I've decided to
implement a few of the basic data structures that I've picked up during my
three years of computer science studies. First up, we have a generic binary
tree. This is an interesting case, because it lets us both delve into generics
in Kotlin, and some aspects of inheritance that differ from inheritance in
Java (in a good way!). As I want to cover some topics in depth, this will be
a three-part series with the following content:

1. In the first part, we'll develop a basic class hierarchy for representing
   nodes. It covers **object** types, **data classes** and **sealed classes**,
   as well as some other related topics. The node is however restricted to only
   carry `Int` data.
2. In the second part, we'll expand upon the class hierarchy from part 1 to
   create a generic node class that can hold any type of data.
3. Finally, we'll use the results of part 2 to develop a rudimentary binary tree
   in (what is in my opinion) idiomatic Kotlin.

If you already know about object types, data classes and sealed classes, I
recommend that you skip directly to part 2. If you are already comfortable with
generics, including generic inheritance, you may skip directly to part 3.

## Series index

1. Representing a node (this part!)
2. [Generic node]({filename}pt2.md)
3. Generic BST with insert, contains and traversal (coming soon!)

## Goals and intended audience
I write articles mostly for myself, and as such, this article series is intended
for developers with some experience with Java looking to get into Kotlin. Let's
get at it then, shall we?

## Representing a node: A Java-like attempt
As I see it, a tree node can be one of two things: existent, or non-existent.
In other words, it can be a node or an empty node. As Kotlin is, thankfully,
quite adverse to using `null`, I will refrain from doing so as well. So what we
want is an abstract node class `ANode` and sub-classes `Node` and `Empty`. Let's
give it a first try in a pretty Java-like manner, and then improve upon it with
some neat Kotlin language constructs.

```kotlin
abstract class ANode

class Empty : ANode()

class Node : ANode {
    val data: Int
    var left: ANode
    var right: ANode

    constructor(data: Int) : super() {
        this.data = data;
        right = Empty()
        left = Empty()
    }
}
```

If you've had any experience with any remotely Java-looking language, you can
probably guess what's going on here. There's the abstract `ANode` class, the
`Empty` class representing the absence of a node and the `Node` class
representing an actual node. Note also that we have not delved into generics
yet, this is a node that can only hold `Int` data. That's fine for now, we'll
expand upon this implementation with generics in part 2. When we later implement
the binary tree, we will often want to distinguish between a `Node` and `Empty`.
One such case is when we search the tree for a given value, to see if it is
contained in the tree. This operation can be succinctly expressed using
recursion, but let us leave that for part 2. For now, let's just check the first
node (the _root_), without exploring its children.


```kotlin
// check if data is contained in node
fun contains(node: ANode, data: Int): Boolean = when (node) {
    is Empty -> false
    is Node -> data == node.data // note implicit cast
    else -> throw IllegalArgumentException("node argument was neither Empty nor Node!")
}
```

This is of course a pretty stupid function at this point, but we'll make it much
more worthwhile in part 2. Note the 
[expression body](https://kotlinlang.org/docs/reference/basic-syntax.html)
used here, in combination with a
[`when` expression](https://kotlinlang.org/docs/reference/control-flow.html).
If you are unfamiliar with those concepts, follow the links and read up on them,
they will be crucial when implementing the tree algorithms in parts 2 and 3.
Also note the
[implicit cast](https://kotlinlang.org/docs/reference/typecasts.html) occurring
on the second line of the function. Since we used `is Node` to match `node`, the
compiler can infer that `node` is in fact a `Node` object, and we can safely
dereference it with `node.data`! Finally, note that the `else` case is needed as
the compiler does not know that there are only two subclasses of `ANode` (even
though we currently do, in this very small project). We'll see how to resolve
that shortly. Let's try this function out:

```kotlin
>>> contains(Empty(), 2)
false
>>> contains(Node(2), 2)
true
>>> contains(Node(2), 3)
false
```

It seems to work just fine. We _could_ leave the class hierarchy like this and
jump straight into generics. There are, however, three notable problems with the
node classes.

1. For each empty node we need, a new instance of `Empty` is created. This is
   wasteful.
2. The body of `Node` is a whole lot of code for very little functionality.
3. The compiler can't tell that `Node` and `Empty` are the only subtypes of
   `ANode`, forcing us to use an `else` in the `when` expression.

As it turns out, all of these problems are easy to solve in Kotlin!

### Problem 1 solution: Singleton objects
Problem number 1 can be solved very easily, as Kotlin has language support for
the singleton pattern. We simply swap this declaration

```kotlin
class Empty : ANode()
```

for this declaration

```kotlin
object Empty : ANode()
```

`Empty` is now a singleton object, so we can assign it without instantiating
`Empty`s all over the place. The constructor for `Node` now looks like this:

```kotlin
constructor(data: Int) : super() {
    this.data = data;
    right = Empty       // note the lack of parentheses!
    left = Empty
}
```
    
One problem solved, two to go!

### Problem 2 solution: Primary constructors and data classes
We can solve problem number 2 with Kotlin's syntax for
[primary constructors](https://kotlinlang.org/docs/reference/classes.html).
Instead of defining `Node` the Java way, we do it the Kotlin way:

```kotlin
class Node(val data: Int, var right: ANode = Empty, var left: ANode = Empty) : ANode()
```

This is _almost_ equivalent to the previous declaration, with the exception that
`right` and `left` are assigned default values in the header such that they can
be replaced by explicit arguments when calling the constructor. Note that
`ANode` must be instantiated right there in the header as well. However, since
we know that `Node` will always be a simple container, we can do one better here
by prepending `data` to the declaration.

```kotlin
data class Node(val data: Int, var right: ANode = Empty, var left: ANode = Empty) : ANode()
```

This makes `Node` a
[data class](https://kotlinlang.org/docs/reference/data-classes.html), which
among other things come with implementations of `equals` and `toString`. A
fortunate accident here is that the `toString` of `Node` will actually let us
view the whole tree with very little effort, as `toString` will be called on
both `left` and `right`, recursively (this will be demonstrated in part 3). Do
be careful not to create a cycle, though, as this will cause a stack overflow,
endlessly calling `toString` (a tree, by definition, has no cycles, so we are
good in this case).

### Problem 3 solution: Sealed classes
To reiterate, the problem was that the compiler can't tell that `Node` and
`Empty` are the only subtypes of `ANode`. Therefore, we needed the `else` in the
`when` expression to cover up the non-existent case of the argument to
`contains` being anything else.

```kotlin
// check if data is contained in node
fun contains(node: ANode, data: Int): Boolean = when (node) {
    is Empty -> false
    is Node -> data == node.data
    else -> throw IllegalArgumentException("node argument was neither Empty nor Node!")
}
```

We can, however, _tell_ the compiler that `Node` and `Empty` _are_ the only
subtypes by making `ANode` a
[`sealed` class](https://kotlinlang.org/docs/reference/sealed-classes.html_).
Any subclass of a sealed class must be declared inside the same file, which lets
the compiler know precisely which subtypes can exist. To accomplish this, we
simply replace the `abstract` modifier with `sealed` (because `sealed` implies
`abstract`, we don't need the latter).

```kotlin
sealed class ANode
```

We can now drop the `else` from `contains`, because the compiler knows that a
variable with static type `ANode` is either `Empty`, or a `Node`, there are no
other possibilities.

```
// check if data is contained in node
fun contains(node: ANode, data: Int): Boolean = when (node) {
    is Empty -> false
    is Node -> data == node.data
}
```

Let's give it a try

```kotlin
>>> contains(Node(2), 2)
true
>>> contains(Empty, 2)
false
```

Neat, now we have a good base for venturing into the fraught land of generics in
[part 2]({filename}pt2.md).

## Final code listing
The final version of the code, that we'll use in part 2, can be found below.
I've also included a main function such that you can run the code in your
preferred way, right off the bat!

```kotlin
sealed class ANode

object Empty : ANode()

data class Node(val data: Int, var left: ANode = Empty, var right: ANode = Empty) : ANode()

// check if data is contained in node
fun contains(node: ANode, data: Int): Boolean = when (node) {
    is Empty -> false
    is Node -> data == node.data // note implicit cast
}

fun main(args: Array<String>) {
    println(contains(Empty, 2))
    println(contains(Node(2), 2))
    println(contains(Node(2), 3))
}
```
