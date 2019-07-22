Title: Git worktrees: work in parallel on multiple versions of a project
Date: 2019-07-22 22:01
Category: Tip of the Week
Tags: totw,bash,git

I've been AWOL for a month due to injury, sickness and conference-going. But
with all that finally out of the way, I have another Tip of the Week, this time
relating to Git: the `git worktree` command. With `git worktree`, you can check
out _multiple_ branches at once, which is super useful for when working on major
changes where you need to view multiple versions, or maybe you're just trying a
few different solutions to a single prodlem. If you've ever found yourself
frantically switching branches, stashing changes to be able to switch branches,
and even creating copies of the repository you're working in, then this article
is for you.

### An example repo
Let's first create an example repo. Here's a little terminal session where I
create a repository, add a README to it on the master branch, add another line
to the readme on a branch called other, and finally checking out to master.

```bash
[~] $ mkdir repo
[~] $ cd repo
[repo] $ git init
Initialized empty Git repository in /home/slarse/repo/.git/
[repo] $ echo "Hello!" > README.md
[repo] $ git add README.md && git commit -m 'Add README'
[master (root-commit) 6094baf] Add README
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
(master)[repo] $ git checkout -b other
Switched to a new branch 'other'
(other)[repo] $ echo "There!" >> README.md 
(other)[repo] $ git commit -am 'Add new line to README'
[other b779dfb] Add new line to README
 1 file changed, 1 insertion(+)
(other)[repo] $ git checkout master
Switched to branch 'master'
(master)[repo] $ 
```

It's not super important how you do it, just make sure to have two branches.

### Adding a new worktree
First of all: what is a _worktree_? Usually, you only have _the_ worktree, which
is the part of a repository where you actually do your work (edit files etc).
Running `git worktree list` on most repos will show the location of this single
worktree, and what commit/branch it is checked out to.

```bash
(master)[repo] $ pwd # just checking the current working directory
/home/slarse/repo
(master)[repo] $ git worktree list
/home/slarse/repo  6094baf [master]  # points to the cwd, checked out to master
```

> **Note:** When I run `git worktree list` after this point, it's just to show
> the results of commands.

With `git worktree add`, you can add additional worktrees checked out to
different commits. The most basic usage is `git worktree add <path>
<commit-ish>`, where `path` is a path to the new worktree (i.e. where you want
to put it), and `commit-ish` is something like a commit or branch (or a few
other things that are not important for every-day use). Let's check out `other`
in a new worktree. 

```bash
(master)[repo] $ git worktree add ../repo-other other
Preparing worktree (checking out 'other')
HEAD is now at b779dfb Add new line to README
(master)[repo] $ git worktree list
/home/slarse/repo        6094baf [master]
/home/slarse/repo-other  b779dfb [other]
(master)[repo] $ ls -a ../repo-other # have a look in the new working tree
.  ..  .git  README.md
```

As you can see, the new worktree has been created, and can be seen in the list
of worktrees. `.git` is usually a directory, but in the case of a non-primary
worktree, it's actually just a file with a path to the original `.git`
directory.

```bash
(master)[repo] $ cat ../repo-other/.git 
gitdir: /home/slarse/repo/.git/worktrees/repo-other
```

Like many things in Git, it's brilliantly simple. You can start working in your
new worktree like it's an entirely separate repository, with the caveat that you
can't check out to a branch that is checked out in some other worktree. That
includes checking out to other commits or branches, and even creating entirely
new branches.

### Moving a worktree
If for some reason you need to move a worktree, you should use `git worktree
move` to make sure that all of the references are correctly changed. It's very
simple, just type `git worktree move <src> <dst>`. For example, if I want to
move `../repo-other` to `../repo-work`, I do:

```bash
(master)[repo] $ git worktree move ../repo-other ../repo-work
(master)[repo] $ git worktree list
/home/slarse/repo       6094baf [master]
/home/slarse/repo-work  b779dfb [other]
```

That's all there is to moving worktrees. Not very exciting, and I can't recall
ever actually doing it, but I can see how it could be useful.

### Removing a worktree
To remove a worktree, run `git worktree remove <path>`.

```bash
(master)[repo] $ git worktree remove ../repo-work/
(master)[repo] $ git worktree list
/home/slarse/repo  6094baf [master]
```

You can also just remove the directory with the worktree and the reference to it
will be removed automatically (but not necessarily immediately). Run `git
worktree prune` to trigger this removal process.

### The other worktree commands
There are a few more `git worktree` commands that I've never felt the need to
use. Have a look at them
[in the git-worktree documentation](https://git-scm.com/docs/git-worktree).

### Summary
In this short article I showcased `git worktree`. It's super useful to work in
parallel on different versions of the same project, without having to create
copies of the repository and thereby having to deal with synchronizing multiple
local copies (which can quickly get hard to manage). I find myself using this
more and more, and if you find it useful yourself I highly recommend reading up
on it more in its man-page (either with `man git-worktree` or
[online](https://git-scm.com/docs/git-worktree)).
