Title: Cleaning up unused packages with Pacman
Date: 2025-10-04
Author: Simon Larsén
Tags: linux,arch linux,pacman
Slug: cleaning-up-with-pacman

Every once in a while, I make a vain attempt to clean up packages. Lately, I've
been upping my game in searching for packages I don't use anymore or don't have
any recollection I even installed. In this article, I'll run through one full
cleanup cycle using `pacman` to declutter my Arch Linux machine.

# Removing installed packages
There are two kinds of packages to look at:

* Native - packages that appear in the sync database(s)
    - You installed these with `pacman -S`[ref]Or if you're a good citizen,
      you installed them with `pacman -Syu` to ensure you're all up to date
* Foreign - packages you've installed from other sources
    - For example, you downloaded a PKGBUILD from the [AUR](https://wiki.archlinux.org/title/Arch_User_Repository) and installed it with `makepkg`

I usually deal with these one at a time.

## Pruning foreign packages
I typically start with foreign packages. I prune these aggressively as foreign
packages have no particular security standard - it'll vary by where you got the
package from.

You can list foreign packages like so:

```bash
$ pacman -Qqme
autojump
kanata-bin
wdisplays
[...]
```
The options are as follows:

* `Q` - query, we're querying the local database
* `q` - quiet, show less output
* `m` - foreign, as described above
* `e` - explicitly installed, as opposed to having been installed as a
  dependency of something else

Let's say I want to uninstall `wdisplays`. I'd do that like so:

```bash
$ sudo pacman -Rsn wdisplays
checking dependencies...

Packages (2) wayland-protocols-1.45-1  wdisplays-1.1.3-1

Total Removed Size:  1.02 MiB

:: Do you want to remove these packages? [Y/n]
```

Note that the we're prompted to approve the removal[ref]For scripts, you can
bypass the need for a prompt with `--noconfirm`. I tend to not script my system
maintenance, however, as I like to be hands on when it comes to what's installed
on my system.[/ref], and also that prompt lists _two_ packages for removal:
`wdisplays` and `wayland-protocols`. The latter is a dependency of `wdisplays`,
which shows up due to the use of the `s` option, as specified below:

* `R` - remove, we're removing a local package
* `s` - recursive, remove all dependencies of the package provided that they
  have no other dependents and were not explicitly installed by the user
* `n` - nosave, prevents Pacman from backing up removed files (I really want
  them gone)

> **Aside:** Another useful option `-c|--cascade`. By specifying this, you
> will remove not only the target package, but any package that depends on it,
> recursively. I rarely use this myself, but it can be very convenient if
> there's a "middle of the dependency chain" package that you for one reason or
> another really need to remove.

## Pruning native packages
Now, we follow precisely the same procedure for native packages. To list native
packages, we simply substitute the `m` option with the `n` argument.

```bash
$ pacman -Qqne
[... very long list ...]
```

This list is going to be _way_ larger than your list of foreign packages, so you
might want to pipe the result to `less` and have a little look through it.
Generally, I do not prune this as aggressively as I prune my foreign packages as
the security standards in the official Arch repositories are adequate for my
needs. That being said, it's still worth a little look every now and then, as
every installed package makes system updates slower.

When you find something to uninstall, you use precisely the same command as for
a foreign package above.

## Pruning orphaned packages
As a final step, I prune _orphaned_ packages. These are packages that were
installed as dependencies at one point, but no longer have any dependents. I
typically accrue quite a few of these by forgetting the `s` option when removing
packages, but they can also come about from e.g. a system update (`pacman -Syu`)
where some updated package(s) no longer require prior dependencies. A system
update _does not_ remove orphans, meaning that you'll accumulate orphans in the
system through normal usage.

You can list orphaned packages like so:

```bash
$ pacman -Qqdt
[...]
```

The _new_ arguments are as follows:

* `d` - dependencies, only shows packages that were _not_ explicitly installed
* `t` - unrequired, lists packages that have no dependents

This will often be quite a large list, typically with dozens or hundreds of
entries depending on how often you clean up your system, so it's typically
necessary to pipe it to the removal command.

```bash
$ pacman -Qqdt | sudo pacman -Rsn -
[...]

:: Do you want to remove these packages? [Y/n]
```

As usual, you need to confirm your action via the prompt, and the presence of
the `s` option will likely cause the prompt to show more packages than the list
you piped into it.

> **Important:** The `q` option is actually important in the above command chain, as
> the extra information that's printed if you don't specify it causes `pacman
> -R` to error out.

> **Tip:** You can trim the list a bit by adding the `t` option to exclude
> packages that are dependencies of other packages. Most often, I find that
> these packages _are_ indeed packages that I want to keep, and I only
> explicitly installed them to resolve some issue with an update.

## Further reading
If you want to learn more about how to maintain your system, here are a few additional resources to have a look at.

* The [System maintenance](https://wiki.archlinux.org/title/System_maintenance) page in the Arch Linux Wiki is a must-read for maintaining your system properly
* The [pacman/Tips and tricks](https://wiki.archlinux.org/title/Pacman/Tips_and_tricks) page in the Arch Linux Wiki is a great place to get ideas for what you can do with `pacman`. It's essentially a much more comprehensive version of this very article.
* The manual page (`man pacman`) is very useful once you already know roughly what you want to do

# And that's it!
With that, you've learned how to prune packages on your system! It's not
difficult to do, you just need a little bit of discipline to do it regularly.
Pruning packages may seem unnecessary, but it has several benefits, not least of
which is a smaller attack surface, less wasted disk space and faster system
updates.
