"""Content components."""

import reflex as rx


def _h_comp(
    text: rx.vars.StringVar,
    heading: str,
    style: dict | None = None,
    mt: str = "4",
    class_name: str = "",
) -> rx.Component:
    id_ = text.lower().split(" ").join("-")
    href = "#" + id_

    if style is None:
        style = {}

    return rx.link(
        rx.heading(
            text,
            id=id_,
            as_=heading,
            style=rx.Style(style),
            class_name=class_name + " scroll-m-[5rem] mt-" + mt,
        ),
        rx.icon(
            tag="link",
            size=18,
            class_name="!text-violet-11 invisible transition-[visibility_0.075s_ease-out] group-hover:visible mt-"
            + mt,
        ),
        underline="none",
        href=href,
        on_click=lambda: rx.set_clipboard(href),
        class_name="flex flex-row items-center gap-6 hover:!text-violet-11 text-slate-12 cursor-pointer mb-2 transition-colors group",
    )


@rx.memo
def h1_comp(text: list[rx.vars.StringVar]) -> rx.Component:
    """Create an h1 component."""
    return _h_comp(
        text=text[0],
        heading="h1",
        class_name="font-x-large lg:font-xx-large",
    )


@rx.memo
def h2_comp(text: list[rx.vars.StringVar]) -> rx.Component:
    """Create an h2 component."""
    return _h_comp(
        text=text[0],
        heading="h2",
        mt="8",
        class_name="font-large lg:font-x-large",
    )


@rx.memo
def h3_comp(text: list[rx.vars.StringVar]) -> rx.Component:
    """Create an h3 component."""
    return _h_comp(
        text=text[0],
        heading="h3",
        mt="4",
        class_name="font-large",
    )


@rx.memo
def h4_comp(text: list[rx.vars.StringVar]) -> rx.Component:
    """Create an h4 component."""
    return _h_comp(
        text=text[0],
        heading="h4",
        mt="2",
        class_name="font-md-smbold",
    )
