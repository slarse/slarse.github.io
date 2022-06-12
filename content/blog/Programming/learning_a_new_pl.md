Title: Learning a new programming language as a practicing software engineer
Date: 2022-11-06
Author: Simon Larsén
Tags: rust,programming languages,learning
Slug: learning-a-new-programming-language

When it comes to programming languages, I consider myself something of a
polyglot. To me, learning a new language is one of the most enjoyable
things in all of software engineering. This is especially true when you
start to venture into new paradigms; going from procedural to functional,
functional to logical and logical to constraint-based. Exploring programming
languages is one of the best way to improve your craft, even if you don't
end up using that language in your daily work.

Having learned (to varying degrees of proficiency) a good few languages over
the years, I figured it's about time I share my process for learning a new one.
And when I say learn here, I mean _really_ learn the language and become
proficient in it, as opposed to learning just enough to become dangerous.
There is a time and place for the latter as well, but that is not the focus
of this article. This article is also not about learning your _first_
programming language, as that's a process where you need to also learn
programming as a skill.

I'm currently in the process of learning the Rust programming language, and in
this article I'll take you through how I go about learning it. My process, which
I will detail throughout this article, is as follows:

1. Identify learning resources
2. Start learning
3. Build a project
4. Maintain knowledge

# Step 1: Identify learning resources

The first thing I do is to identify the learning resources that I intend to use.
This does not have to be an exhaustive list of resources, as sometimes I stumble
upon more of them as I go along, but I always put in some amount of research
into which learning resources are the most well received by others. I divide
these into _primary_ and _secondary_ learning resources, where the primary ones
guide me through the learning experience while the secondary ones are
supplementary and can be skipped altogether if time is tight.

## Primary learning resources

My primary learning resources are one or more structured overviews of the
language I'm about to learn. I usually only aim for one or two primary resources,
and in the vast majority of cases I go with books. The reason I prefer books
over things like video courses is that I find books to be better suited to
active learning. It is incredibly easy for me to watch a video and just start
thinking about something else. In fact, that's something I do even when reading
a book, but to a lesser extent.

Sometimes, finding a good primary learning resource is easy. In the case of
Rust, the community maintains a book called [_The Rust Programming
Language_](https://doc.rust-lang.org/stable/book/), which is the recommended
starting point for newcomers. After that, I intend to continue with
[_Programming
Rust_](https://www.oreilly.com/library/view/programming-rust-2nd/9781492052586/),
which appears to be more in-depth. In some cases, identifying a good primary
resource may be far from trivial, and requires a fair amount of looking around.
But for Rust it did not take me much time at all to find what I was looking for.

I am aware that many prefer video resources over books nowadays. If that fits
your learning style, then that's all good. Books are just where it's at for me
personally. Sites like [Udemy](https://udemy.com) and
[Pluralsight](https://pluralsight.com) provide an ample selection of courses
suitable as primary learning resources for most programming languages in use
today. In my experience, such courses do however often cater to people learning
_programming_, rather than software engineers just looking to add a new language
to their repertoire.

An important note on my primary learning resource is that I never follow more
than one at any one time. That's essentially what makes it a primary resource.
So right now, I'm going with _The Rust Programming Language_ first and will then
move on to _Programming Rust_, but I don't read them at the same time.

## Secondary learning resources

Secondary learning resources are complementary, both to primary learning
resources and other secondary learning resources. I most often have at one or
two secondary resources that I utilize in parallel with a primary one. My
favourite sources of secondary learning resources are conference talks and
podcasts.

For Rust, I found a rather high-quality podcast called [New
Rustacean](https://newrustacean.com/), which features the host's journey of
learning the Rust programming language. It's a nice complement to my reading,
and I enjoy being able to listen to it on the go. If you're about to learn
Python, see my post on [Awesome Python
Podcasts]({filename}awesome_python_podcasts.md) for some inspiration.

Talks are most easily found on YouTube. Many of today's popular programming
languages have at least one yearly conference, while a lot of them have many
more. Python as various incarnations of [PyCon](https://pycon.org/), Rust has
[RustConf](https://rustconf.com/) and C++ has [CppCon](https://cppcon.org/), and
you'll find that pretty much any language has a yearly conference named
`<Language>Con(f)`. Some put all talks on YouTube, while others are a bit
less easy to get a hold of.

There is one more detail about secondary learning resources that I think is
worth noting, namely that they keep being useful to me long after I've stopped
investing time in primary learning resources. Secondary learning resources can
also enter my radar when I'm already a well-rounded programmer in a given
language. I will touch more on this when I discuss maintaining knowledge of a
programming language.

# Step 2: Start to learn

In the initial step of learning, I simply sit down with my chosen primary
learning resource and consume only that. As I'm a book person, this entails
sitting down for a nice read. Although a very common advice is to learn actively
by trying out examples and writing your own code as soon as possible, I
personally prefer to just read for a while before I start dabbling with code
myself. Sometimes I'll try a small example or other that looks extra
interesting, but I generally wait with any serious amount of programming until
Step 3 of my learning process. The goal of Step 2 is not really to learn the
language, but to get a good overview of it.

I often start using my chosen secondary resources immediately after my first
sitting with a primary resource, at least if there's at least one podcast lined
up. What I mostly seek from secondary resources is to get an idea of the
community surrounding the programming language, what the ecosystem (e.g
libraries and frameworks) looks like and keep up to date with the development of
the core language. More on this in Step 4.

# Step 3: Build a project

As soon as I feel like I have touched all subjects I need to sit down and start
up a small project, that's exactly what I do. This point usually rolls around
when I know how to create a project in the language, how to write unit tests and
how to write documentation. I'll often have a particular project in mind, and
then I may also know about a few additional things I need to learn about before
I get going.

My chosen project for learning Rust is to create a compiler and runtime
environment for a statically typed Python-like programming language that I call
_Rusthon_. This is an open source project and you can find it over at [Rusthon's
GitHub page](https://github.com/slarse/rusthon) if you're interested.

Like I mentioned in Step 2, this is where the advice of active learning comes
into play. It's virtually impossible to become proficient with a new language
you're confined to following along with examples and solving tiny problems
without context. You need something larger to work on, I really do think this is
essential.

# Step 4: Maintain knowledge

Once I've learned a language well enough to become proficient in it, I need to
maintain that knowledge and also keep up-to-date with developments in the
community and ecosystem. These are two rather separate concerns. Maintaining a
working knowledge of the language requires one to write code in it. For this I
keep using my project, or find new things to do. I often try to get involved in
open source projects, such as [RepoBee](https://github.com/repobee/repobee)
(Python) and [Spoon](https://github.com/inria/spoon) (Java) to make meaningful
contributions to the community.

Keeping up-to-date with the community and ecosystem is where I mostly keep using
secondary learning resources, mostly podcasts but also talks from conferences.
This may be less important in older languages with less vibrant ecosystems, but
in "newer" languages like Java, Python and Rust, knowing your way around the
package ecosystem and keeping up-to-date with new language features is rather
important.

# Final thoughts

Learning a new programming language is something I enjoy greatly. I go about it
in a rather rigorous fashion where my goal is to become really proficient. I
_immerse_ myself in the language, its community and its ecosystem. This also
entails that I spend some amount of effort in maintaining my knowledge and grasp
on the language, leading to the selection of languages I call myself proficient
in being small. When I learn a new language it often effectively replaces
something already in my repertoire. Rust is a contender to replace C, although I
can't say I've been all that thorough in maintaining my skills in C in the past
few years.

It is also worth considering that learning a new language without maintaining
your skills in it for any considerable amount of time can still be worthwhile. I
think this is especially true when exploring different paradigms, as I alluded
to in the introduction of this article. I learned Haskell many years back but
did not maintain a working knowledge of it for very long. Yet, the concepts that
I learned from being forced to code in a purely functional fashion are valuable
to me to this day. It was thanks to programming in Haskell that I really grasped
the concepts of recursion and higher-order functions, and understanding that has
greatly benefited me in all languages I've practiced since.

To summarize, learning a new language can be greatly beneficial. Even if you
don't intend to add it to your repertoire, it can still be a worthwhile effort
to step out of your comfort zone and explore new programming paradigms. The
things you learn from programming in one language can benefit your programming
in another, and make you a more well-rounded software engineer.
