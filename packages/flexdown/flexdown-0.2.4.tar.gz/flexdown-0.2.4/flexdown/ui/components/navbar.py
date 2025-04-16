"""Navigation bar component for the Flexdown application."""

import reflex as rx


def render_navbar(title: str = "Docs") -> rx.Component:
    """Renders the top navigation bar."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    title,
                    class_name="text-xl font-bold",
                ),
                class_name="flex items-center space-x-4",
            ),
            rx.el.div(
                rx.color_mode.button(),
                class_name="flex items-center space-x-4",
            ),
            class_name="flex items-center justify-between h-16 px-4 max-w-screen-xl mx-auto",
        ),
        class_name="fixed top-0 left-0 right-0 z-50 border-b backdrop-blur-md border-gray-200 shadow-sm",
    )
