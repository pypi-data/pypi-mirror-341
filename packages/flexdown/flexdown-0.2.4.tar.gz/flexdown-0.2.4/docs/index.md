---
title: Flexdown Docs
---

# Flexdown

Flexdown is a way to write interactive documentation using Markdown and Python.

It is designed to be used with [Reflex](https://reflex.dev/), a Python library for building reactive user interfaces.

Flexdown is a superset of Markdown with a few extra features: 

- You can execute Python code in your Markdown documents using the `python exec` code block.
- You can evaluate Python code and display interactive Reflex components in your Markdown documents using the `python eval` code block.
- You can reference variables defined in your Python code in your Markdown documents with the `\{variable_name}` syntax.

## Prerequisites

```python exec
MARKDOWN_CHEATSHEET = "https://commonmark.org/help/"
REFLEX_DOCS = "https://reflex.dev/docs/getting-started/introduction"
```

To use Flexdown, you should be familiar with [Markdown]({MARKDOWN_CHEATSHEET}) and [Reflex]({REFLEX_DOCS}).

You can install Flexdown using pip:

```bash
pip install flexdown
```

## Bring Python to Markdown

Execute Python code in your Markdown documents using the `python exec` code block.


```python exec
import flexdown

from datetime import datetime
current_year = datetime.now().year

def datetime_example():
    from datetime import datetime
    current_year = datetime.now().year

```

When rendering a Flexdown document, the code in the `python exec` code block is executed and the variables defined in the code block are available to reference in the Markdown document.

Use the `\{variable_name}` syntax to reference variables defined in the `python exec` code block.

```md
The current year is \{current_year}.
```

> The current year is {current_year}.

You can write any Python expression within the template syntax.

```md
Next year will be \{current_year + 1}.
```

> Next year will be {current_year + 1}.

You can also import modules and use them in your Markdown document.

```python exec
import random
```

```md
\```python exec
import random
\```
```

```md
A random number between 0 and 1 is \{random.random()}.
```

> A random number between 0 and 1 is {random.random()}.

## Bring Reflex to Markdown

Add interactive Reflex components to your Markdown documents using the `python eval` code block.

```python exec
import reflex as rx
```

```python exec
def alert_example():
    return rx.callout("Hello world!")
```
```python eval
alert_example()
```

## Frontmatter

Flexdown supports [front matter](https://jekyllrb.com/docs/front-matter/) in Markdown documents.
The front matter must be the first thing in the file and must take the form of valid YAML set between triple-dashed lines. 

This allows you to define variables that can be referenced in your Markdown document.

```md
---
title: My Document
author: John Doe
---
```

Then reference the variable in your Markdown document like so:

```md
This document was written by \{author}.
```

This is an alternative to using the `python exec` code block to define variables.

## Basic API

After installing `flexdown`, you can use the `flexdown.render` function to render the contents of a Flexdown document.

```python
import flexdown

markdown = """
---
author: John Doe
---

# My Document

This document was written by \{author}.
"""

component = flexdown.render(markdown)
```

You can use this component in your Reflex application like any other component.

You can also use the `flexdown.render_file` function to render a Flexdown document from a file.

```python
import flexdown

component = flexdown.render_file("path/to/document.md")
```

## CLI

Flexdown comes with a CLI that you can use to render Flexdown documents.

```bash
flexdown path/to/document.md
```

This will start a Reflex app that renders the given file.

You can also pass in a directory to create a multi-page app that renders all of the Markdown documents in the directory.

```bash
flexdown path/to/directory
```


## Examples

Flexdown is a work in progress, but you can see some early examples in the `reflex-web` [repository](https://github.com/reflex-dev/reflex-web/tree/main/docs).
