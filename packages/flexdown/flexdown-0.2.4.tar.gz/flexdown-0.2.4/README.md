This is a README for the Flexdown project, a tool for rendering Markdown documents with custom blocks and components into a Reflex App.

# Installation

To run a local demo of flexdown (assuming a folder called docs), you can use the following command:

```bash
uv pip install -e .
```

# Usage

```bash
flexdown docs
```

If you are using any `reflex-enterprise` component in your docs page, run with the following command:
```bash
flexdown docs -e
```