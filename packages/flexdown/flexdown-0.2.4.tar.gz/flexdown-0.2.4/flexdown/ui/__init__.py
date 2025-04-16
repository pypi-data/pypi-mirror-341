"""Components of the standalone UI."""

from . import components
from .components.content import h1_comp, h2_comp, h3_comp, h4_comp

component_map = {
    "h1": lambda text: h1_comp(text=text),
    "h2": lambda text: h2_comp(text=text),
    "h3": lambda text: h3_comp(text=text),
    "h4": lambda text: h4_comp(text=text),
}

__all__ = ["component_map", "components"]
