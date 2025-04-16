# Demo Block

Using the `python demo exec toggle` tag in a multiline block will render a demo block looking like this : 

```python demo exec toggle
import reflex as rx

def demo_example():
    return rx.box(width="300px", height="300px", background_color="blue")
```

With two tab, where the first one is the rendered demo, and the second one is the code used to generate the demo. 
