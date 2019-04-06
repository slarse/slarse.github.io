Title: A binary search tree in Kotlin pt. 2: Generic node
Date: 2018-10-30T08:26:05Z
Author: Simon Larsén
Tags: bst,kotlin,data structures

Welcome to part 2 of my series on the idiomatic Kotlin binary tree! In this
part, we're gonna have a look at how to make the node representation from part 1
capable of carrying any kind of data (i.e. _generic_).

## Series index
1. [Representing a node]({filename}binary_search_tree_kotlin_pt1.md)
2. Generic node (this part!)
3. Generic BST with insert, contains and traversal (coming soon!)

## Attribution and reading recommendations
In this part, we'll start working a little bit with binary tree algorithms. More
specifically, we'll complete the `contains` function from part 1. All of the
algorithms I implement in this series are based on
[this article by Stefan Nilsson](https://yourbasic.org/algorithms/binary-search-tree/).
If you are unfamiliar with the concepts of binary trees, I highly recommend that
you sift through that article before continuing with this one.

## Improving `contains`
Recall the `contains` function that we started working on in part 1. Before we
start working on generics, I want us to complete this function. It will make
some of the decisions about generics much more apparent. Anyway, here's
`contains` as we wrote it in part 1.

```kotlin
// check if data is contained in node
fun contains(node: ANode, data: Int): Boolean = when (node) {
    is Empty -> false
    is Node -> data == node.data // note implicit cast
}
```

It's not a particularly useful function, as it only checks the current node.
What we'd rather have it do is check the entire subtree, in which `node` is the
root. This can quite easily be performed with recursion. The `Empty` case still
stands, if we hit an empty node, the data is not contained in the tree. If
`node` is a `Node`, on the other hand, there are three possibilities:

1. `data < node.data`, in which case we keep searching in the left subtree.
2. `data > node.data`, in which case we keep searching in the right subtree.
3. `data` is neither smaller or larger than `node.data`, so they are comparably
equal. If this actually means that they are equal or not is implementation
specific, but it is _highly_ recommended that ordering is consistent with
`equals`. We will assume that this is the case.

As we have three distinct cases, we can again use a `when` expression.

```kotlin
// check if data is contained in the tree rooted in node
fun contains(node: ANode, data: Int): Boolean = when (node) {
    is Empty -> false
    is Node -> when { // no-argument when so we can do arbitrary comparisons
        data < node.data -> contains(node.left, data)
        data > node.data -> contains(node.right, data)
        else -> true
    }
}
```

Note that the nested `when` expression has no argument in parentheses, allowing
us to perform more complex operations in the matchings. And that's it for the
`contains` operation. It's really quite elegant. We can quickly ammend the
`main` function to try it out:

```kotlin
fun main(args: Array<String>) {
    // create the tree
    //          6
    //         / \
    //        3   9
    //         \
    //          4
    val root = Node(6,
            left = Node(3,
                    right = Node(4)),
            right = Node(9))

    println("Search for elements in the tree")
    for (data in listOf(6, 3, 4, 9)) {
        println(contains(root, data))
    }
    println("Search for elements not in the tree")
    for (data in listOf(10, 2, 1, -12)) {
        println(contains(root, data))
    }
}
```

With that out of the way, let's dive into making the whole thing generic!

## Getting generic
Now, how do we make the node classes generic? A first attempt might be to just
change the `Node` class, and do something like this:

```kotlin
data class Node<T>(val data: T, var left: ANode = Empty, var right: ANode = Empty) : ANode()

fun <T : Comparable<T>> contains(node: ANode, data: T): Boolean = when (node) {
    is Empty -> false
    is Node<T> -> when {
        data < node.data -> contains(node.left, data)
        data > node.data -> contains(node.right, data)
        else -> true
    }
}
```

This is a reasonable attempt. Before we dive into the problems, let's analyze
what we just did. After `fun` we write `<T : Comparable<T>>`, which makes this
function generic. The addition states that the type parameter `T` can be
substituted by any type that implements `Comparable<T>` (which we need to be
able to use `<` and `>`). `Node<T>` simply defines a type parameter `T` that
can be substituted with _any_ type. It is a bit inconvenient that we could put
non-comparable types in a `Node` object, but we'll see that it sorts itself out
when we create the `Tree` class in part 3. For now, just ignore that detail.

Now, the above code won't compile, for multiple reasons. The first problem is
that we can't ask at runtime if `node is Node<T>` (the compiler will say _Cannot
check for erased type: Node<T>_), becuase information about generics is erased
at runtime. We could succesfully match against a wildcard type parameter
(meaning _any_ type) with `is Node<*>`, but then we run into the real
showstopper: we don't know whether `data` and `node.data` are actually
comparable, as they might not have the same type. With the current class
hierarchy, there is _no_ reasonable way around this. An `ANode` is not
parameterized, and therefore the dynamic type of an `ANode` can be any `Node`
type (e.g. `Node<Int>`, `Node<String>` etc) or `Empty`. We have to put the type
parameter `T` higher up in the inheritance chain. 

### Inheriting from a generic class
Since `ANode` is the only class higher up in the inheritance chain (apart from
`Any`), this is where we need to put our type parameter. For `ANode` and `Node`,
it is straightforward.


```kotlin
sealed class ANode<T>

data class Node<T>(val data: T, var left: ANode<T> = Empty, var right: ANode<T> = Empty) : 
        ANode<T>()
```

Note that `Node<T>` is inheriting from `ANode<T>`. We cannot (and wouldn't want
to, anyway) leave it as `ANode`, because unlike Java, Kotlin does not support
raw types. Now, since we cannot inherit from `ANode`, but must specify the type
parameter with a concrete type, what do we put there for `Empty`? In the case of
`Node<T>`, we simply inherit from `ANode<T>`, because `T` is declared as a
parameter to `Node<T>` and is therefore concrete for for `ANode`. We can't
however just do something like

```kotlin
object Empty : ANode<T>()
```

because `T` is not declared in that scope. We also can't give `Empty` a type
parameter, because `Empty` is a singleton object, and type parameters simply
don't work with singletons (it wouldn't make much sense, if you stop to think
about it for a while). What we actually want to put as the type parameter, is
nothing. Literally. We wan't `Nothing`, a concrete type in Kotlin which is a
subtype of every non-nullable type. 

```kotlin
object Empty : ANode<Nothing>()
```

Note that we don't want to put `Any` (which is the supertype of every
non-nullable type), because the we wouldn't be able to assign `Empty` to any
concrete type of `ANode<T>`. Now you may be angrily shouting that you
_still_ can't assign `Empty` to _any_ type of `ANode<T>`. Unfortunately,
`ANode<T>` (for any substition of `T`) is _invariant_. Let's fix that.

## Generics are invariant by default, but Kotlin can stretch the rules
Any generc class is invariant by default. What does this mean? In short, it
means that a generic type (e.g. `ANode<Int>`) is not a supertype, nor subtype,
of any other type. Formally, it means that if we have two types `A` and `B`
such that `B` is a subtype of `A`, `ANode<B>` is _not_ a subtype of `ANode<A>`.
Take for example `Empty`, which subtypes `ANode<Nothing>`. It is not a subtype
of `ANode<Int>`, even though `Nothing` is a subtype of `Int`. Inconvenient, we
want `Empty` to be a subtype of _any_ concrete `ANode`. We can achieve this by
using the `out` modifier, and declaring `Anode<out T>`. Formally, we make
`ANode` _covariant_ on the type parameter `T`. We can only do this if every use
of `T` is in an _out_ position (i.e.  return values). Note that this
restriction applies only to the body of `ANode`, the `T` in `Node<T>` is _not_
the same type parameter as in `ANode<out T>`.  If you found all of that
confusing (I sure did the first time I read about it), you can read more about
variance in the
[Kotlin docs on generics](https://kotlinlang.org/docs/reference/generics.html).
Here is what the working class hierarchy looks like:

```kotlin
sealed class ANode<out T>

object Empty : ANode<Nothing>()

data class Node<T>(
        val data: T,
        var left: ANode<T> = Empty,
            var right: ANode<T> = Empty) : ANode<T>()
```

`contains` now looks like this:

```kotlin
// check if data is contained in node
fun <T : Comparable<T>> contains(node: ANode<T>, data: T): Boolean = when (node) {
    is Empty -> false
    is Node<T> -> when {
        data < node.data -> contains(node.left, data)
        data > node.data -> contains(node.right, data)
        else -> true
    }
}
```

Now, you may be asking yourself why in the world we can do the `is Node<T>`
check _now_, while we could not before? Well, we're not actually checking at
runtime whether `node` is `Node<T>`, because the compiler knows any variable
with the static type `ANode<T>` is either `Empty`, or `Node<T>`. So, for
example, `ANode<Int>` must have dynamic type `Empty` or `Node<Int>`, there are
no other possibilities. As the compiler knows this, we can in fact skip the
`<T>` and just write `is Node`. That's all we need of our node classes, so we
can move on to implement the `Tree` class in part 3!

## Final code listing
This is the final state of the code that we'll be using for part 3.

```kotlin
sealed class ANode<out T>

object Empty : ANode<Nothing>()

data class Node<T>(
        val data: T,
        var left: ANode<T> = Empty,
        var right: ANode<T> = Empty) : ANode<T>()

// check if data is contained in node
fun <T : Comparable<T>> contains(node: ANode<T>, data: T): Boolean = when (node) {
    is Empty -> false
    is Node<T> -> when {
        data < node.data -> contains(node.left, data)
        data > node.data -> contains(node.right, data)
        else -> true
    }
}

fun main(args: Array<String>) {
    // create the tree
    //          6
    //         / \
    //        3   9
    //         \
    //          4
    val root = Node(6,
            left = Node(3,
                    right = Node(4)),
            right = Node(9))

    println("Search for elements in the tree")
    for (data in listOf(6, 3, 4, 9)) {
        println(contains(root, data))
    }
    println("Search for elements not in the tree")
    for (data in listOf(10, 2, 1, -12)) {
        println(contains(root, data))
    }
}
```
