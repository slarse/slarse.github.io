Title: 
Date: 2018-11-14T17:57:34Z
Author: Simon Larsén
Category: Programming
Tags: html,css,javascript

Sections that collapse and expand at the click of a button is fairly ubiquitous
across the web nowadays. It's especially handy for mobile, where the display is
much smaller than your typical computer monitor. In this article, I'll walk you
through how to create a basic collapsible content-area using almost only CSS,
along with a few lines of close-to-trivial JavaScript. The focus is on CSS, not
JavaScript, so you should be able to follow this even with the most rudimentary
programming experience.

# The fictional sidebar
For this toy example, we will be creating a collapsible `div` (it could really
be just about any element) that can be collapsed and expanded by clicking a
"trigger". Just for the purpose of showing the effects more clearly, we'll do
it inside of another `div` element, which we'll imagine is a sidebar of a
website (like the sidebar with recent posts and tags on this site). Here's the
markup for the sidebar:

```html
<div class="sidebar">
    <!- our content goes in here! -->
</div>
```

And the CSS:

```html
.sidebar {
  width: 30%;
  border: black solid 2px;
}
```

This is really _not_ important for this demo, I just mention it so that you
don't wonder about some unknown HTML and CSS in the final demo. Now, let's fill
that sidebar up with some content.

```html
<div class="sidebar">
  <div id="trigger">Cool content heading</div>
  <div id="content">
    <p>
      This content would be neat to hide and show at the click of a button!
    </p>
  </div>
</div>
```

We have 3 `div` tags in total: one is the container (sidebar) which really has
little to do with this article. The second is a heading for the content, which
will act as the trigger for showing and hiding the content. The third is the
one containing the content that we want to hide/show (a single paragraph).
Let's get to it! Note the `id` attributes on the two inner `div` tags. When I
later refer to the `#trigger`, I mean the div with `id="trigger"`, and likewise
for the `#content`. The `id` attributes serve no other purpose here, you can
remove them if you wish and everything will still work as expected.

## Collapsing and expanding the `div`
To collapse and expand `#content`, we will use two classes: `collapse-trigger`
and `collapse`. The basic idea is this:

1. An element with the `collapse` is hidden by default.
2. If a `collapse` element follows an element with the `collapse-trigger` AND
   the `active` classes, the `collapse` is visible.

You can probably guess where to put the classes in the markup already:

```html
<div class="sidebar">
  <div id="trigger" class="collapse-trigger">Cool content heading</div>
  <div id="content" class="collapsible">
    <p>
      This content would be neat to hide and show at the click of a button!
    </p>
  </div>
</div>
```

For the CSS, fulfilling point 1 above (`collapsible` hidden by default) is
simple:

```css
.collapsible {
    display: none;
}
```

This will simply not display the element.  But how do we fulfill the second
requirement? We can use the
[adjacent sibling combinator](https://developer.mozilla.org/en-US/docs/Web/CSS/Adjacent_sibling_selectors)
(`+`). It's a selector combinator that allows us to match some element, only if
it is immediately preceded by some other element. For example, the selector `h1
+ p` will match any `p` tag that is immediately preceded by an `h1` tag:

```htlm
<h1>This is a heading</h1>
<p>This paragraph will be matched by "h1 + p"</p>
```

So, to show our `collapsible` when it is directly preceded by a
`collapse-trigger` AND `active` element, we do this:

```css
.collapse-trigger.active + .collapsible {
    display: block;
}
```

We display it as a `block` here, but one could use other display modes as well,
depending on what visual effect is sought.  Note that we are chaining two
classes in the left hand side of the `+` combinator, which means that an
element matches only if it's `class` attribute contains both of those classes
(and possibly more of them). The order of the classes is however not important,
i.e. `.active.collapse-trigger` would be equivalent.

That's actually all there is to it, as far as the CSS goes. Now, we can
collapse and expand the `#content` by opening the developer tools (`F12` in
Firefox and Chrome) and manually assigning the `active` class to `#trigger`.
But that's not very convenient in every day use. This is where we need the
tiniest bit of JavaScript to be able to toggle `active`.

## Toggling the `active` class with the click of a button
What we want to do is to remove and add the `active` class from any
`collapse-trigger` element by clicking it. Here, we need JavaScript, because
there is no way to change the class of an element with only CSS. For every
`collapse-trigger` in the page, we need to attach an event listener that
toggles the `active` class every time the element is clicked. It can be done
like this:

```javascript
function attachCollapseTriggers() {
    var colTriggers = document.getElementsByClassName("collapse-trigger");
    for (var colTrig of colTriggers) {
        colTrig.addEventListener("click",  function() {
            this.classList.toggle("active");
        });
    }
}
```

Essentially, we use the `getElementsByClassName` DOM method to find all
elements with the `collapse-trigger` class. Then, we iterate over those
elements, and add an event listener to it. The first argument to
`addEventListener` is an event (in this case a button click). The second
argument is a callback function, for which we provide an anonymous function. If
you have a hard time wrapping your head around anonymous functions, this will
accomplish the same thing:


```javascript
function collapseTrigger() {
    this.classList.toggle("active");
}

function attachCollapseTriggers() {
    var colTriggers = document.getElementsByClassName("collapse-trigger");
    for (var colTrig of colTriggers) {
        colTrig.addEventListener("click", collapseTrigger);
    }
}
```

When the element is clicked, the `collapseTrigger` function is called.  Of
course, we need to call `attachCollapseTriggers` sometime after the page has
loaded for this to take effect. And that's it for the JavaScript, clicking the
`#trigger` will now cause `#content` to collapse and expand!  However, it's not
very clear to the user that the `#trigger` even can be clicked. Let's make that
just a little bit more clear by adding some visual cues.

## Finishing touches using the `::after` pseudo class
A typical visual cue that a drop down can be expanded is a down-triangle (▼).
An up-triangle (▲) is as recognizable a cue that a menu can be collapsed. The
down-triangle should be appended to any `collapse-trigger` that is not active,
while the up-triangle should be appended to any `collapse-trigger` that also
has the `active` class. We can do that simply use the `::after` pseudo class.

```css
.collapse-trigger::after {
    content: "▼";
    float: right; /* float to the right-hand side of the content box */
}

.collapse-trigger.active::after {
    content: "▲";
}
```

So, what happens here, exactly? When a `collapse-trigger` is not `active`, it
doesn't match the `.collapse-trigger.active` selector, so the content will
simply be the down-triangle. When a `collapse-trigger` _is_ active, it will
match both selectors. However, `.collapse-trigger.active` is more specific than
`.collapse-trigger`, so it wins out, and the content will be an up-triangle.
And that's it, all done!

# Code listing and JSFiddle link
The full code is available in the following subsections, and you can find a
[JSFiddle here](https://jsfiddle.net/p3qtev5w/).

### Markup

```html
<!- the outer div with the class "sidebar" isn't important, it's just any container -->
<div class="sidebar">
  <div class="collapse-trigger">Cool content heading</div>
  <div class="collapsible">
    <p>
      This content would be neat to hide and show at the click of a button!
    </p>
  </div>
</div>
```

### CSS

```css
/* the sidebar class is just an arbitrary container for this example */
.sidebar {
  width: 30%;
  padding: 1em;
  border: black solid 2px;
}

.collapse-trigger::after {
    content: "▼";
    float: right;
}

.collapse-trigger.active::after {
    content: "▲";
}

.collapsible {
    display: none;
}

.collapse-trigger.active + .collapsible {
    display: block;
}
```

### JavaScript

```javascript
function attachCollapseTriggers() {
    var colTriggers = document.getElementsByClassName("collapse-trigger");
    for (var colTrig of colTriggers) {
        colTrig.addEventListener("click",  function() {
            this.classList.toggle("active");
        });
    }
}

attachCollapseTriggers();
```
