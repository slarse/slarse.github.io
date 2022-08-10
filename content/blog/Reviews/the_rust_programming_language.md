Title: Book Review: The Rust Programming Language
Date: 2022-08-10
Author: Simon Larsén
Tags: book review,software engineering,rust
Slug: book-review-the-rust-programming-language

I've been learning Rust on and off for the past few months, and _The Rust
Programming Language_ has been my [primary learning
resource]({filename}../Programming/learning_a_new_pl.md) during this time.
It's a great introduction to the language, and is even [freely available
online](https://doc.rust-lang.org/stable/book/).

Here, I'm reviewing the 2018 print version. Although a little bit out of date by
now, there's nothing that's become obsolete, so I can still recommend even this
version. For the most up to date version, the online one is however the way to
go.

```
The Rust Programming Language
by Steve Klabnik, Carol Nichols
Released June 2018
Publisher(s): No Starch Press
ISBN: 9781593278281
```

# The book in a nutshell
_The Rust Programming Language_ is really a book where the title perfectly
captures what the book is about. It teaches Rust mostly by practical examples,
and for the most part the examples are self-contained and executable. For some
concepts, examples are either missing or more illustrative than executable, but
these are few and far between.

The book also to a large extent explains programming concepts, and has a rather
elaborate section on concurrency. It however isn't on a beginner level, and
doesn't go out of its way to intuitively describe what a variable is, or how
looping works. I would rate this a great book for someone who is already
somewhat familiar with programming concepts, but it's not the best resource for
getting started with programming as a whole. It's the perfect "second language
book".

# What I liked
This book is incredibly well written and organized. Concepts to be learned are
first presented on a high level, and then the authors drill into the details.
But not too far into the details; at several points we are referred to other
resources to acquire a deeper understanding for certain concepts. It's also a
great standalone resource for learning Rust as it covers surrounding tooling
like `rustup` and `cargo` in addition to the language itself. You can learn Rust
to a decent level of proficiency from this book alone.

The well thought out pacing of the book carries over to the code samples, which
are excellent through-and-through. There are some rather tricky concepts to get
your head around in Rust compared to other programming languages, and the code
samples are crucial in getting the point across. These are also presented in a
top down fashion. By that, I mean that the higher level code is presented first
containing calls to yet to be defined functions that are presented later. 

As a crude example, imagine that we want to present a program that adds two
numbers and prints the result. That may look like so:

```rust
fn main() {
    let sum = add(1, 2);
    println!("{}", sum);
}
```

And then we define the `add` function after having presented the high-level idea
we want to implement:

```rust
fn add(lhs: i32, rhs: i32) -> i32 {
    lhs + rhs
}
```

This top down approach to presenting code samples really helps in getting a good
idea for _what_ needs to be done before _how_ it is actually implemented. I
strongly prefer this approach to a bottom up one, where you start with the low
level _how_ before getting to the high level _what_.

The book ends with a project on building a multithreaded web server, which is
meant to solidify many of the concepts taught throughout the book. It's a great
way to close out a great book.

# What I didn't like
This is my first book review where I can't come up with something that I overtly
did not like about a book. There are things the book lacks, such as more
beginner-friendly introductions to core programming concepts, but I feel that's
by design rather than thoughtless omission. The book would simply be way too
long if it had to include such things as well.

Perhaps I will find something to be annoyed with as I revisit this in the
future, but as it stands I am completely pleased with my reading experience.

# Conclusions
This is a great book to learn the Rust programming language. It's not
appropriate for absolute beginners, but I think that may be simply a consequence
of Rust being designed to tackle rather advanced problems. I would not
recommend a budding programmer to start out with Rust, and so it seems
completely natural to me that the official learning resource doesn't cater toward
such a crowd. That being said, you don't need to be a seasoned programmer
to get value out of this book, as concepts are explained with quite a lot of
"backstory". You don't need to be overly familiar with the problems Rust
attempts to solve (memory safety, for example) as the book clearly exemplifies
the problems before outlining the solutions.

As _The Rust Programming Language_ is [freely available
online](https://doc.rust-lang.org/stable/book/), I whole-heartedly recommend it
for those looking to dive into Rust. I see no good reason to go looking
elsewhere for resources when there's such a great one staring you right in the
face. This is _the_ starting place for a prospective Rustacean!
