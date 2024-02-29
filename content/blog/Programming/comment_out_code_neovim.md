Title: Extending NeoVim for commenting and uncommenting code blocks
Date: 2024-02-29
Author: Simon Larsén
Tags: neovim
Slug: comment-and-uncomment-code-in-neovim

I've been using some variation of Vim for going on a decade now, yet I've never
bothered with an efficient way of commenting out code. It just isn't something
that I do very often. But I saw a colleague comment out and uncomment lines of
code like a breeze in VS Code, so obviously I had to also have that capability.
And then choose to not use it. Let's see how you can get that option, too.

> This article contains Lua code for configuring NeoVim. To follow along, paste
> the Lua code presented into any `.lua` file and run `:luafile %` with the
> file in the current buffer. This makes the commands defined within available
> in your current NeoVim session.

# Commenting out code the hard way
A simple no-preparation way of commenting out code in any variation of Vim is to
simply select a few lines of code in visual mode and then make a substitution.
Let's say we're writing Python where the inline comment character is `#`, then
commenting out a line would look like this.

```vim
:s/^/#/
```

The `^` character is the "start of line" character, so here we're simply
replacing the start of line with `#`. And don't worry, the start of line isn't
actually a character; there'll be a new start of line just in front of the `#`
after the substitution. Select a range of lines in visual mode and run the same
substitution and you'll comment out the entire range.

If you do this rarely it's fine. But if you do it regularly it becomes rather
cumbersome. Luckily for us, NeoVim is easy to extend.

# Defining a command to comment out code
To make the above substitution a bit less of an effort, we can define a command
for it. First, we need to define a function that executes the code. A very
simple first effort would look like this.

```lua
function comment_out()
    vim.api.nvim_command("s:^:#:")
    vim.api.nvim_command("noh")
end
```

There are a couple things to note about this function.

1. `vim.api.nvim_command` synchronously executes a command.
2. We use `:` instead of `/` as the substitution delimiter in anticipation of
   the C-style `//` inline comment.
3. We clear the search highlight with `noh` after doing the substitution.
    - Figuring out what happens if you don't do that is left as an exercise to
      the reader.

So that's our function for performing the substitution, and if we simply place
our cursor on a line we wish to comment out we can execute it like so.

```vim
:lua comment_out()
```

It should insert a `#` character at the start of the line. But this isn't
terribly ergonomic, it'd be nicer if we could just call a native NeoVim command.
Fortunately, defining such a command is pretty simple.

```lua
vim.api.nvim_create_user_command("CommentOut", comment_out, {})
```

This exposes the `:CommentOut` command, and we can now invoke our commenting out
function like so.

```vim
:CommentOut
```

Still, this feels like some amount of effort, so let's add a couple of handy
keybindings to do this. I like `<leader>co` which is a mnemonic for **c**omment
**o**ut.

```lua
vim.keymap.set("v", "<leader>co", ":CommentOut<CR>") -- visual mode keymap
vim.keymap.set("n", "<leader>co", ":CommentOut<CR>") -- normal mode keymap
```

Now we can simply invoke the commenting out routing with `<leader>co`, or
whatever else you've decided to put in there. There are however two big problems
left to address:

1. The `:CommentOut` command doesn't work with a range
    - If you try to select a range of lines and run the function, you will
      encounter an error saying `E481: No range allowed`
2. The commenting character is hard-coded as `#`
    - That approach works great if you only work with a single language, but if
      you like me work daily with multiple languages that have different line
      comment styles it's not ideal

Let's address these in turn.

## Adding support for range selection
Being able to run our little `:CommentOut` command only on one line at a time
is hardly useful, so let's make our command compatible with range selection.
First we need to modify the creation of the command, which by default does
not allow ranges.

```lua
vim.api.nvim_create_user_command("CommentOut", comment_out, { range = true })
```

With this modification, you'll be able to execute `:CommentOut` when a range is
selected, but only the first line of the selection will actually be commented
out. We need to add a few lines of code to the `comment_out()` function to
actually act on the entire range. While we're at it, we'll also make the
function `local` as it doesn't need to be accessible outside the module anymore.

```lua
local function comment_out(opts)
    local start = math.min(opts.line1, opts.line2)
    local finish = math.max(opts.line1, opts.line2)
    vim.api.nvim_command(start .. "," .. finish .. "s:^:#:")
    vim.api.nvim_command("noh")
end
```

Options for NeoVim commands are passed in via the `opts` table, and the line
numbers of the selection are stored in `line1` and `line2`. Other available
options are [detailed in the NeoVim API
docs](https://neovim.io/doc/user/api.html#nvim_create_user_command()).

Note that depending on where you start the selection, either line may be the one
at the top and bottom, respectively, so we do some rudimentary math to get the
start and finish of our substitution in the right order.

Selecting a few lines of code and running `:CommentOut` (or using the
keybind for it) now actually comments out those lines! Let's now figure out how
to select the correct kind of line comment for the given file type.

## Choosing line comment style by filetype
While there's probably a super clever way of accomplishing this, I went with
something really rudimentary: a table with line comment styles by filetype. It
looks something like this:

```lua
local non_c_line_comments_by_filetype = {
    lua = "--",
    python = "#",
    sql = "--",
}
local default_line_comment = "//"

local function comment_out(opts)
    local line_comment = non_c_line_comments_by_filetype[vim.bo.filetype] or default_line_comment
    local start = math.min(opts.line1, opts.line2)
    local finish = math.max(opts.line1, opts.line2)

    vim.api.nvim_command(start .. "," .. finish .. "s:^:" .. line_comment .. ":")
    vim.api.nvim_command("noh")
end
```

Basically, we default to the `//` line comment style _unless_ we find a match in
the `non_c_line_comments_by_filetype` table. We use `vim.bo.filetype` to get the
current buffer's filetype. Then we do some more string concatenation in the
substitution command, and that's pretty much that. If you need other line
comment styles, just add them to the table.

If you now run the `:CommentOut` command in a Python file, it'll use `#` as the
comment style. But if you do it in a SQL file, it'll use `--`, and in a Go file
it'll use `//`.

# Uncommenting code
We now have a neat way of commenting out code, but what about _uncommenting_
code? Let's straight up copy `comment_out()` and just replace the substitution
expression with something that removes a line comment start.

```lua
local function uncomment(opts)
    local line_comment = non_c_line_comments_by_filetype[vim.bo.filetype] or "//"
    local start = math.min(opts.line1, opts.line2)
    local finish = math.max(opts.line1, opts.line2)

    vim.api.nvim_command(start .. "," .. finish .. "s:^" .. line_comment .. "::")
    vim.api.nvim_command("noh")
end

vim.api.nvim_create_user_command("Uncomment", uncomment, { range = true })
vim.keymap.set("v", "<leader>uc", ":Uncomment<CR>")
vim.keymap.set("n", "<leader>uc", ":Uncomment<CR>")
```

> Note: The keybinding is a mnemonic for **u**n**c**omment.

This mostly works. If you first run `:CommentOut` and then `:Uncomment`, the
latter cancels out the former. But there are two notable shortcomings.

1. If you run `:Uncomment` on a line that deos not start with a line comment
   start you encounter an error saying `Pattern not found:`
2. The line must _start_ with a line comment start; leading whitespace causes
   the substitution to fail
   - If you have a formatter that indents line comments, you'll be in trouble!

The first issue is simple to resolve: we wrap the call to `vim.api.nvim_comand`
in a _protected call_ using the [pcall() function](https://www.lua.org/pil/8.4.html).
This allows us to handle errors, but in fact all we want is to prevent any error
from bubbling up to the surface; we don't really care if the substitution fails
or not as a failure simply indicates there was no comment to uncomment.

The second issue requires a little bit more thought. We want to be able to
uncomment lines even if there's leading whitespace to be give the command some
more flexibility. With `#` as the line comment, a first attempt could look like
this.

```vim
:s:^\s\{-\}#::
```

`^` is the line start meta character, `\s` denotes any whitespace except for
linebreaks, and `\{-\}` means "zero or more`. This mostly works, but it removes
both the leading whitespace and the comment character, effectively dedenting the
line. We need to _capture_ the whitespace and put it back after removing the
line comment start.

```vim
:s:^\(\s\{-\}\)#:\1:
```

The escapes makes the pattern a bit difficult to read, but all we've done here
is to wrap the "zero or more whitespace" in a capture group (denoted by
parentheses), and then we reference that capture group in the replacement part
of the expression with `\1`.

Putting all of this together, we end up with the following `uncomment()`
function.

```lua
local function uncomment(opts)
	local line_comment = non_c_line_comments_by_filetype[vim.bo.filetype] or "//"
	local start = math.min(opts.line1, opts.line2)
	local finish = math.max(opts.line1, opts.line2)

	pcall(vim.api.nvim_command, start .. "," .. finish .. "s:^\\(\\s\\{-\\}\\)" .. line_comment .. ":\\1:")
	vim.api.nvim_command("noh")
end
```

Now it should work pretty well!

# Summary and full code
That's pretty much it for commenting and uncommenting code, at least as far as
my semi-imagined needs for it go. This represents among the first non-trivial
extensions I've made to NeoVim using only its API and made me realise just how
much power I've left untapped for so many years. I will undoubtedly return with
more blog posts on extending NeoVim in the future; it's just too much fun not
to.

The full code can be found below. You can just copy and paste it into your root
`init.lua` file and it should work without any further tweaks. For a more
segregated placement, you can draw inspiration from [my NeoVim
configuration](https://github.com/slarse/config/commit/fe1ab5bcd24f4a1ad0a111b67a652de1c330a18d).

```lua
local non_c_line_comments_by_filetype = {
	lua = "--",
	python = "#",
	sql = "--",
}

local function comment_out(opts)
	local line_comment = non_c_line_comments_by_filetype[vim.bo.filetype] or "//"
	local start = math.min(opts.line1, opts.line2)
	local finish = math.max(opts.line1, opts.line2)

	vim.api.nvim_command(start .. "," .. finish .. "s:^:" .. line_comment .. ":")
	vim.api.nvim_command("noh")
end

local function uncomment(opts)
	local line_comment = non_c_line_comments_by_filetype[vim.bo.filetype] or "//"
	local start = math.min(opts.line1, opts.line2)
	local finish = math.max(opts.line1, opts.line2)

	pcall(vim.api.nvim_command, start .. "," .. finish .. "s:^\\(\\s\\{-\\}\\)" .. line_comment .. ":\\1:")
	vim.api.nvim_command("noh")
end

vim.api.nvim_create_user_command("CommentOut", comment_out, { range = true })
vim.keymap.set("v", "<leader>co", ":CommentOut<CR>")
vim.keymap.set("n", "<leader>co", ":CommentOut<CR>")

vim.api.nvim_create_user_command("Uncomment", uncomment, { range = true })
vim.keymap.set("v", "<leader>uc", ":Uncomment<CR>")
vim.keymap.set("n", "<leader>uc", ":Uncomment<CR>")
```

Happy editing!
