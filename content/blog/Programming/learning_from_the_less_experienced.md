Title: The art of learning from the less experienced
Date: 2022-07-07T22:31:50.112260
Modified: 2022-08-07T23:59:50.112260
Author: Simon Larsén
Tags: learning,software engineering
Slug: learning-from-the-less-experienced

Software engineering is a lifelong journey of learning. Regardless of how
dedicated you are in your learning, there will never come a point where you
have learned it all. As such, it's important to use all learning resources
available to us. As is evident from the themes on my blog, I'm very partial to
books and other written media. Indeed, this blog post is such written media.
But perhaps the best source of learning for a software engineer is simply other
 software engineers.

Now, learning new things from those more experienced than you isn't that much a
leap of the imagination. Of course you're going to try to soak up anything you
can learn from your seasoned team lead, or that database expert who does magical
things with SQL queries, or anyone else you identify as being highly proficient
in something that interests you. No, there is no real challenge there, barring
the fact that these experienced engineers may not have the inclination to teach
you. But this blog post is about your disposition as a learner, so let's stick
to the topic. And actually get to the topic to begin with: learning from the
less experienced.

# A student can teach their teacher
When I attended university, I worked many years as a teaching assistant in
introductory computer science classes. During one class I held, there was at
some point a part of an assignment that required flipping the value of a
boolean variable. Something like: given a boolean variable `isOdd`, define a
new boolean variable `isEven` that is `true` if `isOdd` is `false`, and `false`
if `isOdd` is `true`. One student presented a solution like the one below.

```java
boolean isEven;
if (isOdd == true) {
    isEven = false;
} else {
    isEven = true;
}
```

Being an enthusiastic but still rather fresh teaching assistant with not all
that much programming experience, I said it was a viable solution but it would
be more concise to use a ternary operator.

```java
boolean isEven = isOdd ? false : true;
```

The students sat back in awe at my incredibly simple solution to the problem.
That is, until 5 seconds passed and another student had a bright idea: "why not
just negate `isOdd`?". What the student meant was the following:

```java
boolean isEven = !isOdd;
```

Not only is this solution the most concise, it also more clearly represents the
concept the task asked for. Something is "even" precisely if it is "not odd",
after all. I managed to humble myself enough to commend the student for a well
thought out solution.

# First year students routinely taught me new things
I taught the first year computer science courses for four years. I expanded my
skills exponentially during this time. And yet, every year there would be new
first year students that knew something I did not, or had some insight I
lacked. While these events definitely became less frequent as I gained more
experience, they never ceased. I'm confident that I could go back there now and
teach the same courses again, and there would be a student or two with
something to teach me.

The great insight that I gained from this is that regardless of how far ahead
you are of someone else, you are doing both yourself and them a disservice by
not being open to let them teach you things. It's also incredibly hard to
determine if someone is less experienced than you are. In the `!isOdd` scenario
outlined above, I was in a position of authority relative to the student who
had the best solution, but it's not unlikely that student had done a lot more
programming than I had, given that I didn't start until I was in university.

# The great challenge in keeping an open mind in disagreement
The reason I could so easily swallow my pride and commend the student with the
`!isOdd` solution is not that I at that time was particularly humble. I simply
agreed with the solution the student had in mind, it fit my mental model. I've
since been in situations where someone I've viewed as less experienced (and more
importantly, _less proficient_) than myself has come with a suggestion that I've
fundamentally disagreed with. In such scenarios keeping an open mind is a
lot more difficult, and all I can do is try to the best of my abilities. I will
argue my point, and I can argue fiercely, but I also try my absolute hardest not
to dismiss their point outright, and hear out their arguments. I also try not to
let my predetermined view of their experience and proficiency taint my
judgement. Sometimes I succeed on the spot, and sometimes I succeed in hindsight
when reflecting over a past conversation. And most assuredly, sometimes I
simply fail.

My point with all of this storytelling really boils down to one piece of advise:
avoid leaning on your impressions of someone's experience and proficiency when
evaluating their arguments for some point. I guarantee they know things you don't.
Like me, you are unlikely to always succeed, but you'll benefit from the times
you do. Not to mention that the other party of the argument will most often
appreciate you letting them make their case. Perhaps that's actually the more
important part of thes story. But it sure does not hurt that there's something
in it for you as well.
