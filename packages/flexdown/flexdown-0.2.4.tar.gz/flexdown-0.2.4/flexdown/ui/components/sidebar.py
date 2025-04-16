"""Sidebar components."""

from dataclasses import dataclass
from typing import List

import reflex as rx

from flexdown.namespace import FxNamespace, FxPage


@dataclass
class LinkItem:
    """A link item in the sidebar."""

    title: str
    target: str
    order: int | None = None

    def __gt__(self, other: "LinkItem") -> bool:
        """Compare the pages by route."""
        if self.order is not None:
            if other.order is not None:
                return self.order < other.order
            return True
        return self.title < other.title


@dataclass
class SidebarSection:
    """A section in the sidebar."""

    title: str
    links: List["LinkItem | SidebarSection"]
    target: str | None = None
    order: int | None = None

    def __gt__(self, other: "SidebarSection") -> bool:
        """Compare the pages by route."""
        if self.order is not None and other.order is not None:
            return self.order < other.order
        return self.title < other.title


def docs_link(text: str, target: str) -> rx.Component:
    """Create a link to a documentation page."""
    return rx.el.a(
        text,
        href=target,
        class_name="hover:text-indigo-600 transition-colors duration-200 block py-1 text-sm",
    )


def sidebar_section(section: SidebarSection) -> rx.Component:
    """Create a sidebar section."""
    return rx.el.div(
        rx.el.h4(
            docs_link(section.title, section.target)
            if section.target
            else section.title,
            class_name="font-semibold mb-2",
        ),
        *[
            docs_link(link.title, link.target)
            if isinstance(link, LinkItem)
            else sidebar_section(link)
            for link in section.links
        ],
        class_name="mb-6",
    )


def render_sidebar(
    title: str = "Documentation",
    sections: List[SidebarSection | LinkItem] | None = None,
) -> rx.Component:
    """Create a sidebar."""
    if sections is None:
        sections = []
    return rx.el.div(
        rx.el.div(
            rx.el.a(rx.el.h3(title, class_name="text-lg font-bold mb-4"), href="/"),
            *[
                sidebar_section(section)
                if isinstance(section, SidebarSection)
                else docs_link(section.title, section.target)
                for section in sections
            ],
            class_name="p-6",
        ),
        class_name="w-64 fixed top-16 left-0 h-screen border-r border-gray-200 overflow-y-auto",
    )


def make_sections(namespace: FxNamespace) -> list[LinkItem | SidebarSection]:
    """Generate sections for the sidebar based on a namespace."""
    sections = []
    for name, child in namespace.children().items():
        if isinstance(child, FxNamespace):
            sections.append(
                SidebarSection(
                    title=child.index.title if child.index else name,
                    target=child.index.route if child.index else None,
                    links=make_sections(child),
                    order=child.index.doc.metadata.get("order"),
                )
            )
        elif isinstance(child, FxPage) and name != "index":
            sections.append(
                LinkItem(
                    title=child.title,
                    target=child.route,
                    order=child.doc.metadata.get("order"),
                )
            )
    return sorted(sections, reverse=True)
