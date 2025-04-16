"""Table of contents component."""

import reflex as rx


def render_toc(toc: list[tuple[int, str]], path: str):
    """Render the table of contents."""

    def base_toc_link(text: str):
        return rx.link(
            text,
            font_size="0.875rem",
            color=rx.color("slate", 9),
            white_space="nowrap",
            overflow="hidden",
            text_overflow="ellipsis",
            transition="color 0.2s",
            underline="none",
            href=path + "#" + text.lower().replace(" ", "-"),
            _hover={"color": rx.color("slate", 11)},
            padding_vertical="0rem",
        )

    def toc_link(level: int, text: str):
        match level:
            case 1:
                padding_left = "0rem"
            case 2:
                padding_left = "1rem"
            case _:
                padding_left = "2rem"
        return rx.el.li(
            base_toc_link(text),
            padding_left=padding_left,
            padding_top="-0.2rem",
            margin_top="0",
            margin_bottom="0",
            padding_bottom="-0.2rem",
        )

    return rx.el.nav(
        rx.desktop_only(
            rx.box(
                rx.el.h5(
                    "On this page",
                    font_weight="600",
                    font_size="0.7rem",
                    color=rx.color("slate", 12),
                    line_height="0.5rem",
                    letter_spacing="-0.01313rem",
                    transition="color 0.2s",
                    _hover={"color": rx.color("violet", 9)},
                ),
                rx.el.ul(
                    *[toc_link(level, text) for level, text in toc],
                    class_name="flex flex-col gap-2 list-none",
                ),
                position="fixed",
                display="flex",
                flex_direction="column",
                justify_content="flex-start",
                gap="0.875rem",
                padding="0.875rem 0.5rem 0 0.5rem",
                width="100%",
                max_width="300px",
                max_height="80vh",
                overflow="hidden",
                right="0",
            )
        ),
        class_name="h-screen shrink-0 w-[16%]",
    )
