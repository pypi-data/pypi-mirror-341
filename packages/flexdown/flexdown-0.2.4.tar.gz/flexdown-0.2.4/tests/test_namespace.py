"""Test the namespace module."""

from flexdown.namespace import FxNamespace, FxPage


def test_namespace():
    """Test the FxNamespace class."""
    nm = FxNamespace("./docs")
    pages = nm.all_pages()
    assert len(pages) == 4
    assert type(pages[0]) is FxPage
    assert pages[0].route == "/docs"
    assert pages[0].title == "Docs • Index"
