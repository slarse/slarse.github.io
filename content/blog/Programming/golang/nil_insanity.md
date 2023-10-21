Title: The sheer insanity of interfaces and nil in Go
Category: Programming
Date: 2023-10-21
Author: Simon Larsén
Tags: go,nil,null,software engineering

If you've only dabbled briefly in Go, you might think that its `nil` is
analogous to the good ol' ["billion dollar mistake"](https://en.wikipedia.org/wiki/Tony_Hoare#Apologies_and_retractions)
known as `null`. I thought so, too, up until just a few weeks ago when I
decided to make a pass through Thorsten Ball's neat little book
[Writing an Interpreter in Go]({filename}/blog/Reviews/writing_an_interpreter_in_go.md).
That's when I first cut myself real bad on `nil`, or more specificaly, an
interface with a `nil` value.

# The sensible kind of `nil`
First let's look at `nil` behaving like we'd expect. Here's a code snippet of a
"parser" that somewhat shows the situation I had.

```go
package main

import (
	"fmt"
	"strings"
)

type IfExpression struct {
	raw string
}

func parseIf(s string) *IfExpression {
	if strings.HasPrefix(s, "if") {
		return &IfExpression{raw: s}
	}

	return nil
}
```

So, we have a parse function that returns a pointer to an `IfExpression` struct
if the input is an `if` expression (with an incredibly loose definition of what
constitutes an `if` expression). Let's add a `main` function and try it out.

```go
func main() {
	ifExpr := parseIf("if a == b")
	fmt.Println("ifExpr", ifExpr, ifExpr == nil)

	notIfExpr := parseIf("not an expression")
	fmt.Println("notIfExpr", notIfExpr, notIfExpr == nil)
}
```

Running this results in completely sensible output; `ifExpr` is not `nil` while
`notIfExpr` is.

```
$ go run main.go
&{if a == b} false
<nil> true
```

Say what you want about `nil`, this at least makes complete sense and is
intuitively understandable. But when we throw interfaces into the mix,
that goes way out the window.

# The completely insane kind of `nil`
As my parser came along, it turned out I needed multiple kinds of expressions,
and so had to abstract the parse function to be able to return multiple kinds
of expressions. So let's generalize the expression in an interface and add
another one.

```go
type Expression interface {
	Raw() string
}

type IfExpression struct {
	raw string
}

func (ie *IfExpression) Raw() string { return ie.raw }

type ForExpression struct {
	raw string
}

func (fe *ForExpression) Raw() string { return fe.raw }
```

And then we adapt the parsing as well.

```go
func parse(s string) Expression {
	if ifExpr := parseIf(s); ifExpr != nil {
		return ifExpr
	} else {
		return parseFor(s)
	}
}

func parseFor(s string) *ForExpression {
	if strings.HasPrefix(s, "for") {
		return &ForExpression{raw: s}
	}

	return nil
}

func parseIf(s string) *IfExpression {
	if strings.HasPrefix(s, "if") {
		return &IfExpression{raw: s}
	}

	return nil
}
```

Now, we have a more generalized `parse` function that tries to parse an `if`
expression, and falls back on parsing a `for` expression if it turns out not to
be an `if`. We then adapt our `main` function to make use of this.

```go
func main() {
	ifExpr := parse("if a == b")
	fmt.Println("ifExpr", ifExpr, ifExpr == nil)

	forExpr := parse("for a in b")
	fmt.Println("forExpr", forExpr, forExpr == nil)
}
```

And at first glance, this seems to work as expected.

```
$ go run main.go 
ifExpr &{if a == b} false
forExpr &{for a in b} false
```

But what happens when you try to parse something that is neither an `if` nor a
`for`? We add the following to `main` to find out.

```go
	notAnExpr := parse("not an expression")
	fmt.Println("notAnExpr", notAnExpr, notAnExpr == nil)
```

Clearly, as `"not an expression"` is neither an `if` expression nor a `for`
expression, both `parseIf` and `parseFor` will return `nil`, and as such `parse`
should return `nil`. But that's not _really_ what happens.

```
$ go run main.go 
ifExpr &{if a == b} false
forExpr &{for a in b} false
notAnExpr <nil> false
```

What? `notAnExpr` is `<nil>`, but it does not compare true to a literal`nil`?
What does that mean?

# The confusing type-and-value composition of interfaces
In Go, an interface is represented at runtime as a
[type and a value](https://go.dev/doc/faq#nil_error). You can think of it as a
struct with two fields.

```go
type Interface struct {
	type  string
	value interface{}
}
```

So, when `parseIf(s)` returns `nil`, the `parse(s)` function's return statement
wraps the `nil` value into something like this.

```go 
Interface {
    Type: "IfExpression",
    Value: nil,
}
```

Armed with this knowledge, we can actually check for `nil` using
[runtime reflection](https://pkg.go.dev/reflect).

```go
func IsNil(value interface{}) bool {
    return reflect.ValueOf(value).IsNil()
}

func main() {
	ifExpr := parse("if a == b")
	fmt.Println("ifExpr", ifExpr, IsNil(ifExpr))

	forExpr := parse("for a in b")
	fmt.Println("forExpr", forExpr, IsNil(forExpr))

	notAnExpr := parse("a == b")
	fmt.Println("notAnExpr", notAnExpr, IsNil(notAnExpr))
}
```

And running this, we now seem to have a functioning way to check for `nil`
interfaces.

```
ifExpr &{if a == b} false
forExpr &{for a in b} false
notAnExpr <nil> true
```

But do we really? Of course not.

# Actually, interfaces can also be "completely" `nil`

Let's make this even more confusing, and refactor our `parse` function a bit.
Instead of "falling back" on `parseFor`, we simply return `nil` explicitly if
we can't parse any known expression.

```go
func parse(s string) Expression {
	if ifExpr := parseIf(s); ifExpr != nil {
		return ifExpr
	} else if forExpr := parseFor(s); forExpr != nil {
		return forExpr 
	}

	return nil
}
```

Now let's run it again.

```
$ go run main.go 
ifExpr &{if a == b} false
forExpr &{for a in b} false
panic: reflect: call of reflect.Value.IsNil on zero Value
```

Suddenly, `notAnExpr` _is_ `nil`, causing our check to panic. What in the world
is going on here? As it turns out, explicitly returning `nil` from a function
that returns an interface is semantically different to returning a [variable
contaning `nil` value, and typed with something implementing the
interface](https://go.dev/doc/faq#nil_error).

```go
return nil // actually returns nil

var value *ForExpression = nil
return nil // returns an interface with type *ForExpression and value nil
```

So a way around this is of course to always return `nil` in the form of a typed
variable. But I'm not satisfied with that, because even if I'm very strict
about it myself, others may not be. And I may also just make an honest mistake.
So let's tweak our `IsNil()` function to account for true `nil`.

```go
func IsNil(value interface{}) bool {
    return value == nil || reflect.ValueOf(value).IsNil()
}
```

If you run this, you'll see that the runtime panic is replaced with the
following.

```
notAnExpr <nil> true
```

So we're done? Unfortunately, not quite.

# Structs are a problem
Our `IsNil()` handles true `nil` and interfaces with `nil` values. But,
unfortunately, it does not handle structs.

```go
value := IfExpression{raw: "if"}
fmt.Println(IsNil(value)) // panic: reflect: call of reflect.Value.IsNil on struct Value
```

Poop. It appears we missed a critical part of
[`IsNil()`'s documentation](https://pkg.go.dev/reflect#Value.IsNil).
And by missed, I of course mean that we didn't read it, but here's the relevant
part.

> IsNil reports whether its argument v is nil. The argument must be a chan,
> func, interface, map, pointer, or slice value; if it is not, IsNil panics.

So, we need to check if the value is of any of these `nil`-able types,
and otherwise assume that it is not `nil`.

```go
func IsNil(value interface{}) bool {
	if value == nil {
		return true
	}

	reflected := reflect.ValueOf(value)
	switch reflected.Kind() {
		case
		reflect.Chan,
		reflect.Func,
		reflect.Interface,
		reflect.Map,
		reflect.Ptr,
		reflect.Slice:
		return reflected.IsNil()
	}
	return false
}
```

And with this, the panic is abated.

```go
value := IfExpression{raw: "if"}
fmt.Println(IsNil(value)) // false
```

This will work so long as Go doesn't add some other `nil`-able type. Given how
conservative the language is, such an addition to the core types seems an
unlikely prospect. But of course, it could happen, and then this function would
return `false` incorrectly in some cases.

# Footguns
All languages have [footguns](https://en.wiktionary.org/wiki/footgun). Some
languages, like C++ and JavaScript, are seemingly built exclusively of them.
Go is a small-ish and conservative language, and so naturally has fewer such
contraptions. But how `nil` is handled differently in different contexts and how
the type of a variable can change the actual value that's returned from a
function, is a big one.

Of course, all of this may just be symptoms of my not knowing Go very well, and
this whole article could just be the frustrated ramblings of an apprentice. But,
I'm an experienced programmer, and this confused me quite a bit. That alone
should be sufficient evidence that some design choices made here aren't optimal.
