Title: Book Review: Writing an Interpreter in Go
Date: 2023-10-14
Author: Simon Larsén
Tags: book review,software engineering,go
Slug: book-review-writing-an-interpreter-in-go

I love programming languages, both using them and implementing them. As such, I
found the concept of learning Go by creating a programming language to be just
delightful. And, to put it briefly, it was. Let's talk about Thorsten Ball's
book on interpreters. In Go.

```
Writing an Interpreter in Go
by Thorsten Ball
Publisher: Thorsten Ball
ISBN: 9783982016115
```

> You can buy the book directly from Thorsten Ball's website at
> [https://interpreterbook.com/](https://interpreterbook.com/).

# The book in a nutshell
_Writing an Interpreter in Go_ is precisely what it sounds like; a practical
guide to writing a fully functioning interpreter in Go. You go from source
code, to tokens, to abstract syntax tree and tree evaluation. The parser
is based on the pretty fascinating
[_Pratt parsing_](https://en.wikipedia.org/wiki/Operator-precedence_parser#Pratt_parsing)
technique, while the evaluation is based on simple tree-walking. This relative
simplicity allows Ball to cram a whole lot of functionality into a very concise
200 pages worth of book. The result is impressive, and I am somewhat astonished
by just how much content is actually in here, and how well written said content
is.

# What I liked
There is so much to like about this book. First of all, it is wonderfully
standalone. I wrote around 3500 lines of code based entirely on descriptions
and code samples from the book's 200 printed pages. Although the source code
for the interpreter is available as part of the book, I never needed to
reference it.

Something else I just barely needed to reference was documentation for Go
itself. While this book doesn't teach you programming and is therefore not for
complete beginners, it does somewhat teach you Go by example. There are little
to no explanations for how Go works, but due to how simple Go is I think the
examples speak for themselves. A caveat to that is that I have done some Go
programming in the past, and I think that a complete beginner to Go should
probably go through the interactive [A Tour of Go](https://go.dev/tour/)
tutorial first. The only thing that I personally needed to reference was some
details around how interfaces and `nil` work together in Go (it's [really quite
unintuitive](https://go.dev/doc/faq#nil_error)). It should also be noted that
there is nothing about concurrency in this book, which being a major selling
point of Go entails that this book omits some important parts of the language.
I do however find that completely reasonable given the scope of the book.

The book is also for the most part organized in a way that fit me very well.
In the first few parts of the book, the implementation is given up front and
then tests are added to verify the behavior. The majority of the later parts of
the book are however laid out in the opposite order, with descriptions of
functionality and tests being followed by the actual implementation. This
allowed me to read the tests and the descriptions to get a good idea of the
intended behavior, and then try my own hand at coming up with a solution.
Comparing my solution to the author's after the fact was a great way to cement
the knowledge.

The source code exhibits a splendid balance between proper design and being
simple enough to put into a book this short. There were several design decisions
that I did not fully agree with, especially with the parsing of strings, but I
can also see that certain simplifications had to be made to fit the format. For
the most part, I think these simplifications are well chosen.

Concepts are explained clearly and intuitively. Pratt parsing is by far the most
involved topic in the book, and I think Ball presents it in a very digestible
fashion. I needed to run through it a couple of times and mentally step through
the code, but when it clicked I found no fault in how the concepts were
explained. At no point did I need to reference external sources to understand
something.

The last part of the book adds in a few extra features, such as arrays and hash
maps. All of these extra features are implemented in a very satisfying loop,
going all the way from the lexing to the finished evaluation in one short
chapter for each feature. Adding one feature at a time in this way really aids
in understanding the workings of each part of the interpreter. And that, in
fact, is a perfect segue to the one part of this book that I did not entirely
like.

# What I didn't like
I actually started this book around five years ago, but never finished it. In
fact, I got just barely halfway due to what I perceive as the one flaw of this
otherwise fantastic piece of literature: it has a rather slow start. It's not
until halfway through that you actually get to evaluation and thereby create a
complete path from source code to output. The fantastic pacing of the last
quarter of the book where you add features one at a time highlights that the
first half isn't as satisfying as it probably could be. While I recognize that
the amount of groundwork to put down before getting to the exciting parts is a
tough one to make, I think the book would have been better off closing the path
from source code to evaluation earlier. For instance, I don't see any need to
parse function definitions before evaluating arithmetic expressions.

# Conclusions
This is a great book. It's clear, concise and packed full of learnings. Due to
the way the last quarter of the book is laid out, adding feature upon feature
from start to finish, I was able to quite effortlessly add features completely
of my own design by the time I finished the book. The only complaint I have
about the book is that not more of it is laid out in that fashion, because it's
just so good.

If you've dipped your toes in Go and want an exciting project to learn the
language better, I think this is a great way to do it. It takes a little while
before the book gets going for real, but when it does, it really takes off.
