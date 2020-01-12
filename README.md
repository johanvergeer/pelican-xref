# Pelican Xref: A Plugin for Pelican

A Pelican plugin that allows you to cross-reference articles in an easy way

## Motivation for this plugin

In Pelican, you can reference other articles in the following way:

```markdown
Title: The second article
Date: 2012-12-01 10:02

See below intra-site link examples in Markdown format.

[a link relative to the current file]({filename}category/article1.rst)
[a link relative to the content root]({filename}/category/article1.rst)
```

The issue I have with this is that your file structure becomes very rigid.
When you move or rename a file or directory all your references are broken.

That is why I created this plugin.

## Usage

### Step 1: Add `xref` attribute to your articles

You have to add an attribute named `xref` to the article attributes, which is only required for articles you want to reference to.
The attribute value can contain upper- and lowercase letters, numbers, hyphens (`-`) and underscores (`_`).

```markdown
---
Title: The first article
xref: ref-1
---

...
```

After you add the `xref` attribute to an article, you can use it in other articles:

```markdown
---
Title: The second article
---

This article references the first article with the following syntax: [xref:ref-1]
```

The syntax has two optional attributes: `title` and `blank`.
You can use the `title` attribute if you want to use a custom text instead of the title of the referenced article.
The `blank` attribute is used in case you want the created link to open a new window.

Input | Generated html
--- | ---
<code>[xref:ref-1]</code> | `<a href="/category/the-first-article">The first article</a>`
<code>[xref:ref-1 title="Title override"]</code> | `<a href="/category/the-first-article">Title override</a>`
<code>[xref:ref-1 blank=1]</code> | `<a href="/category/the-first-article" target="_blank">The first article</a>`
<code>[xref:ref-1 title="Title override" blank=1]</code> | `<a href="/category/the-first-article" target="_blank">Title override</a>`

## Installation

This plugin can be installed via:

    pip install pelican-xref


## Contributing

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/johanvergeer/pelican-xref/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html
