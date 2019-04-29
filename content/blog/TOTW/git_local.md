Title: Git local
Date: 2019-04-29 22:58
Category: Tip of the Week
Tags: totw,bash,git

Nowadays, Git is almost ubiquitous in software development. Most developers also
know that Git is a _decentralized_ version control system, meaning that every
copy of the repository carries the full revision history, and there is no
"central" repository. A consequence of the decentralized aspect of Git is that
you can create repositories locally, and version control documents in them
locally, without ever setting up a remote repository on e.g. GitHub or GitLab.
In this TOTW, I'll show you how to use Git locally, and also how to change your
mind and put it on e.g. GitHub at a later time.

> **Note:** This also touches on an important and often misunderstood point: Git
> and GitHub are _not_ the same thing. Git is a version control system, while
> GitHub is a service which allows hosting of remote repositories, issue
> management etc. GitHub is also not the only service around,
> [GitLab](https://gitlab.com) and [BitBucket](https://bitbucket.com) are two
> other prominent services which host Git repositories.

### Using Git locally
How do you use Git locally, then? It's simple. Just create a directory and run
`git init` to initialize it as a Git repository. Here's an example command line
session of what it looks like.

```bash
[~] $ mkdir repo
[~] $ cd repo
[repo] $ ls -a
. ..            # repo is empty
[repo] $ git init
Initialized empty Git repository in /home/slarse/repo/.git/
[repo] $ ls -a
.  ..  .git     # the .git directory indicates that this is now a Git repo
```

I often use Git to version control stuff that I have no intention of ever
putting up in a remote repository. This is useful for when you accidentally
remove stuff, or just need to try out a bunch of different ideas that you can
swap back and forth between by simply switching branches.

### Changing your mind (also called adding a remote)
If you suddenly feel like that local repo should be put up on a hosting service
after all, maybe just to back it up, or maybe to collaborate with someone else,
it's very simple to do so. First, create an empty repository (as in completely
empty, don't initialize it with a README or license). Then copy the address to
the repository (I prefer to use SSH). Let's say I have a repo at
`git@github.com:slarse/superrepo.git`. I can then add it as a remote to my local
repo, and push my master branch to it.

```bash
[repo] $ git remote add origin git@github.com:slarse/superrepo.git
[repo] $ git branch
* master  # I'm on the master branch, which is what I want to push
[repo] $ git push --set-upstream origin master
Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Writing objects: 100% (3/3), 213 bytes | 213.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0)
To github.com:slarse/superrepo.git
 * [new branch]      master -> master
Branch 'master' set up to track remote branch 'master' from 'origin'.
```

Now my previously local-only repo is also in GitHub, and I can push and pull
from it as usual. That's all for this tip of the week, it's just meant to spark
an idea that took me quite a while to come up with myself!
