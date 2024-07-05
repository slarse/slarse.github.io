Title: Book Review: Cybersecurity Myths and Misconceptions
Date: 2024-07-05
Author: Simon Larsén
Tags: book review,software engineering,cybersecurity
Slug: book-review-cybersecurity-myths-and-misconceptions

The world of cybersecurity is full of perils. Many of those perils stem from
misconceptions about the nature of cybersecurity. If you come to the insight
that perfect security is unachievable, you may reach the conclusion that
being concerned with cybersecurity at all is a waste of your time. After all,
the bad guys will get in anyway. Or you may have the notion that your particular
company is too small of a target for anyone to bother with, and so you don't
bother to defend yourself appropriately. Or perhaps you experience a security
breach and take action before you even know what's going on, because surely,
some action is better than no action. If reading about 175 statements of this
kind and why they're flawed, then _Cybersecurity Myths and
Misconceptions: Avoiding the Hazards and Pitfalls that Derail Us_ may be the
book for you.

```
Cybersecurity Myths and Misconceptions: Avoiding the Hazards and Pitfalls that Derail Us
by Eugene Spafford, Josiah Dykstra, Leigh Metcalf
Released October 2009
Publisher(s): O'Reilly Media, Inc.
ISBN: 9780596518387
```

# The book in a nutshell
The book covers 175 myths and misconceptions in cybersecurity. These are divided
into 16 chapters covering different topics ranging from faulty assumptions
(e.g. "I am too small to be a target"[ref]You are not. A lot of cyber mischief
isn't even targeted, but rather automated processes scanning vast amounts of the
Internet to find servers with known vulnerabilities.[/ref]) to misconceptions
about digital forensics (e.g. "Incidents are discovered as soon as they
occur"[ref]They are not. In 2022, the average time to discovery of a breach was
207 days.[/ref]).

The vast majority of the myths are presented in the following format.

1. Present some background information for the topic to make sense.
2. Make a bold statement (the myth or misconception)
3. Dismantle the statement and show how it does not hold water
    - Although some myths are acknowledge to be partially true, given the right
      circumstances

In some cases, there's also a small fictitious case study of a manager wanting
to apply some technology or rule motivated by the myth. These can be a bit on
the nose, but also occasionally hit too close to home to be comfortable.

For the most part, this is not a technical book. Most myths are presented on high
enough a level that you do not need to be a software engineer to appreciate it.
There are some things that may fly over your head if you're not a software
engineer, such as talk about the OSI network model and interprocess
communication, but such technical dives are so infrequent that they barely need
mention.

# What I liked
This book is a leisure read. It does not require you to sit at a computer and
apply concepts to benefit from it, all you need to do is read the book and
ponder its implications. At the same time, it will surely grant you insights
that will have tangible effects on your ability to perform in a technical role.

As a concrete example, there is a section about cognitive biases. One such bias
is so-called _action bias_, where you are prone to take action as a response to
a cybersecurity threat, even before you have understood the situation well
enough to make a qualified decision about _what_ action to take. In reality,
sometimes no action is the best solution, and rather often I'd say that no
action is better than the _wrong_ action. While I have experience enough to know
not to act prematurely, and sometimes not to act at all, I am definitely
predisposed with an action bias. As, I think, are a lot of software engineers.
We want to _fix_ things, not just wait for them to resolve themselves. Reading
about action bias in the way it is framed in this book has caused me to reflect
on how I act, especially in incident response, and I think it will help me take
an even more measured approach in the future.

In addition to expanding my own mind, I also found that the book framed a whole
lot of the complaints that I've had to managers and peers over the years. For
example, the notion that "I'm to small to be a target" is something I've seen a
lot, and the next time I come across it I very well may use this book as a
reference to attempt to dissuade it.

A lot of what is covered in the book is also applicable to software engineering
as a whole (or even business as a whole), rather than just cybersecurity. The
sunk cost fallacy[ref]The idea that an existing investment in something warrants
further investment into the same thing [(see
Wikipedia)](https://en.wikipedia.org/wiki/Sunk_cost#Fallacy_effect)[/ref] is
universally applicable when it comes to any costly investment, as is the fact
that basing decisions on anecdotal evidence isn't necessarily the best idea.
There's also this really insightful chapter on how analogies and abstractions
can be damaging to understanding when they don't fit well enough. For example,
the name _firewall_ comes from physical walls intended to impede the spread of
fire. A firewall in computing is built to stop some traffic ("fire"), but also
let some traffic through. The latter does not fit the analogy, a physical
firewall shouldn't let _any_ fire through.

As a final note on what I liked, there is a running theme in the book that
insulting people for their lack of cybersecurity awareness serves no purpose,
and that guiding others to better decisions rather than berating bad ones is
often the most effective path. However, there is also an undertone that
at least some cybersecurity issues stem from software engineers with
insufficient skills. When discussing cross-platform compatibility in high-level
programming languages, one footnote reads as follows.

> We are glossing over many things such as numerical precision, interprocess
> communication, and character sets. For this discussion, assume those things do
> not matter, although they certainly do in real life. If you do not know what
> we mean by that **and** you are writing production software, then you need to
> study more software engineering.

This makes it clear that even though the authors believe in helping and
educating your peers to the best of your abilities, a base level of
understanding is to be expected from your peers. And that understanding is, at
least in part, their responsibility to attain.

# What I didn't like
There's a large amount of footnotes throughout the book, a lot of which contain
useful and interesting snippets of information as well as sources for
statements. These, I do not mind at all. But, unfortunately, there is a bit of
an oversaturation of footnotes that only contain jokes, puns and witty remarks.
While they are all well written and give the book a lighter tone, there's at
times simply too many of them. As many of the footnotes are useful, I would stop
to read every single one. When that caused me to read three jokes in a row, I
would get a little bit frustrated.

Don't get me wrong, I don't mind light-hearted writing, and a few of these kinds
of footnotes would only have made the book more enjoyable to read. But when
you interrupt your reading flow to read a footnote and find your third witty
remark in a row, it does get a bit annoying.

# Conclusions
This book widened my view of software engineering and cybersecurity. While most
of the topics were familiar to me from my education and professional experience,
some were forgotten, some brand new, and many were simply framed in a way I had
previously not considered them in. Given the rather limited amount of effort I
put into reading the book, I got a whole lot of value out of it.

If you're a practicing software engineer, you should read this book, especially
if you feel like your grasp of cybersecurity topics isn't where it should be. It
won't teach you what you need to know on a technical level, but it will help
build up the basic mindset you ought to adopt as well as illuminate a lot of
what you don't yet know.

If you're a technical manager in charge of software engineers, you should read
this book. It will give you better insight into why software engineers sometimes
say "no" and hopefully allow you to make more measured decisions when it comes
to acquiring new or retaining existing software.
