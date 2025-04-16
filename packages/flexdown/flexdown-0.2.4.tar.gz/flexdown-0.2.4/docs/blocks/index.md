---
title: Blocks
---

# Flexdown Blocks

In markdown, you can render code blocks by wrapping some content in triple backticks. This is a standard feature of Markdown, but Flexdown extends this functionality to allow you to create custom blocks with specific tags.

Flexdown provides some predefined blocks that can be used to enhance your Markdown documents. These blocks are designed to be easy to use and integrate seamlessly with the rest of your Markdown content.

Some examples of blocks you can create with Flexdown include:

```md alert
# An alert block
```

```python demo exec toggle
import reflex as rx

def demo_example():
    return rx.box(rx.text("A demo block"), width="300px", height="100px", background_color="blue")
```
