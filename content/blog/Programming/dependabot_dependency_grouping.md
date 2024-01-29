Title: Dependabot's dependency grouping is awesome
Date: 2024-01-29
Author: Simon Larsén
Tags: dependabot,github,dependencies
Slug: dependabots-dependency-grouping

I've been using GitHub's Dependabot since it was [released around 4 years
ago](https://github.blog/2020-06-01-keep-all-your-packages-up-to-date-with-dependabot/),
and to a large extent, it's been great. Except for one thing: the sheer amount
of pull requests Dependabot would open for dependency updates. For some of my
repositories it became more of a chore to keep up with Dependabot's pull request
spamming than to just manually update dependencies every once in a while.

Well. Turns out that's been fixed.

# Dependabot's big problem: Pull request spam
Since Dependabot was released, it's only mode of operation has been to open one
pull request per dependency update. As you can imagine, that leads to a whole
bunch of pull requests being opened. I would routinely get dozens of dependency
pull requests a week for some of my more dependency heavy repositories. Needless
to say, that's just not manageable.

One of my projects, [Spork](https://github.com/kth-assert/spork), which is
mostly in maintenance mod is one such example where I just gave up on keeping up
with the updates. It ended up looking like this:

<img alt="Spork dependency spam" src="/images/dependabot_dependency_grouping/pr-spam.png" style="max-width: 95%;">

What a mess. But there's light at the end of the tunnel.

# The fix: Grouped dependencies
To address that problem GitHub recently released
[Grouped Version Updates](https://github.blog/changelog/2023-08-24-grouped-version-updates-for-dependabot-are-generally-available/)
as a feature for Dependabot. In short, this means that you can get Dependabot
to open pull requests containing multiple dependency updates, grouped in three
different ways.

## A configuration example
For my project [Spork](https://github.com/kth-assert/spork), I decided to group
dependencies in three groups:

1. Updates to GitHub Actions dependencies
2. Updates to production dependencies
3. Updates to development dependencies

Configuring this was really straightforward, all it took was [this
commit](https://github.com/ASSERT-KTH/spork/commit/ac3051e07bc6632c4f41f74feb60ffc555fce1cd).

```diff
     directory: "/"
     schedule:
       interval: "daily"
+    groups:
+      actions-deps:
+        patterns:
+          - "*"
 
   - package-ecosystem: "maven"
     directory: "/"
     schedule:
       interval: "daily"
+    groups:
+      dev-deps:
+        dependency-type: "development"
+      prod-deps:
+        dependency-type: "production"
```

In full, the configuration looks like so.

```yaml
version: 2
updates:

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "daily"
    groups:
      actions-deps:
        patterns:
          - "*"

  - package-ecosystem: "maven"
    directory: "/"
    schedule:
      interval: "daily"
    groups:
      dev-deps:
        dependency-type: "development"
      prod-deps:
        dependency-type: "production"
```

For each package ecosystem, you must group on _something_. For
`github-actions`, I just wanted a single group, and the way to achieve such an
"everything group" is to simply use a wildcard pattern. For `maven`, I ended up
splitting by the `dependency-type` attribute instead, which can be either
`development` or `production`.

But that's just two ways to group, you said there were three ways? Very
attentive of you! In addition to the `pattern` and `dependency-type` groupings,
you can also group by `update-type`, which can be `patch`, `minor` or `major`
and only really works for dependencies that comply with [Semantic
Versioning](https://semver.org/)

## Effects of the configuration
Within minutes, Dependabot had closed all\* of the single dependency pull requests
and created two new pull requests. One PR contained the GitHub Actions updates,
which I could immediately merge.

> \*For reasons I don't quite get at this point,
> [one single-dependency PR for `gumtree-spoon-ast-diff` remained
> open](https://github.com/ASSERT-KTH/spork/pull/458)

<img alt="Merged GitHub Actions dependencies" src="/images/dependabot_dependency_grouping/actions_deps.png" style="max-width: 95%;">

Note that the `actions-deps` name, which is one of the keys in the YAML config
file, ends up being written out in the pull request title. Another PR was opened
for the grouped production dependencies, but it did not pass CI.

<img alt="Production dependencies PR" src="/images/dependabot_dependency_grouping/prod-deps.png" style="max-width: 95%;">

This showcases the one downside with grouped dependency updates: there's no
indication as to which dependency caused the CI failure. If you scroll up to the
first image of this article, you'll similarly see the one benefit of single
dependency pull requests: the update for `jgit` is failing.

> Note: As stated above, `gumtree-spoon-ast-diff` wasn't included in the grouped
> dependency update for some reason, so we'll ignore that it's also failing.

So I decided to try to get Dependabot to open a new pull request without `jgit`.

## Ignoring certain dependencies in a group
I knew that `jgit` was the issue in this case and decided to ignore it. It
seemed like ignoring minor version updates was the best path forward, so I
issued an `@dependabot ignore <dependency_name> minor version` command.

<img alt="Ignore minor version updates of jgit" src="/images/dependabot_dependency_grouping/ignore_minor.png" style="max-width: 95%;">

This didn't quite have the effect I was looking for, as Dependabot then
proceeded to
[open a new pull request](https://github.com/ASSERT-KTH/spork/pull/485)
with the previous minor version of `jgit`, which is also incompatible with
Spork. At this point I decided to bring out the big guns and ignore `jgit`
altoghether for now, as I knew I needed to put in some manual work to update it
anyway.

<img alt="Ignore all version updates of jgit" src="/images/dependabot_dependency_grouping/ignore.png" style="max-width: 95%;">

This finally resulted in what I wanted, a new PR without a bump to `jgit` that
does not break the build. Thus, it's ready to merge.

<img alt="Ignore all version updates of jgit" src="/images/dependabot_dependency_grouping/green-prod-pr.png" style="max-width: 95%;">

Of course, this comes with the caveat that I need to remember to [unignore `jgit`
when I get around to updating it](https://github.com/ASSERT-KTH/spork/issues/487).
But I have 8 dependency updates with not too much effort, which is kind of cool!

# Closing thoughts
I had somewhat given up on keeping dependencies up to date in my lesser loved
projects. With grouped dependency updates, I feel like it will be possible for
me to get back to keeping dependencies in good shape even for projects that I no
longer actively work on.

The one downside is that it's no longer evident which dependency update breaks
the build. However, over many years of maintaining projects built in various
languages and technologies, experience tells me that it's way more common for
dependencies to update just fine than for them to break something, so I think
it's a tradeoff well worth taking. As patterns of which dependencies break the
build more often start to become apparent, one can also refine the groupings and
separate dependencies that break often from those that rarely or never do so.

To summarize, grouped dependency updates is a killer feature that makes
Dependabot viable again. Everyone should use it, and it's honestly a shame that
backwards compatibility demands makes it such that groups will probably never be
the default.
