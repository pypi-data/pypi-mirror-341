"""Layout for Flexdown app."""

from typing import Any

import reflex as rx


def default_layout(navbar: Any, sidebar: Any, toc: Any, content: Any):
    """Default layout for Flexdown."""
    return rx.el.div(
        navbar,
        rx.el.div(
            rx.el.div(
                sidebar,
                class_name="hidden md:block md:w-64 shrink-0 pt-16",
            ),
            rx.el.main(
                content,
                class_name="flex-1 p-10 md:p-12 lg:p-16 overflow-y-auto",
            ),
            rx.el.div(
                toc,
                class_name="hidden lg:block md:w-64 shrink-0 pt-16 top-18",
            ),
            class_name="flex min-h-screen",
        ),
    )
