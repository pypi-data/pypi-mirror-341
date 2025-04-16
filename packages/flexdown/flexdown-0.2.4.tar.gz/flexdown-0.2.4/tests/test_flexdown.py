"""Tests for the flexdown module."""

from flexdown.blocks import EvalBlock, ExecBlock, MarkdownBlock
from flexdown.flexdown import Flexdown


def test_parse():
    """Test parsing a markdown file with code blocks."""
    fd = Flexdown()
    source = 'This is a markdown block.\n\n```python exec\nprint("Hello, world!")\n```\n\nThis is another markdown block.\n\n```python eval\n2 + 2\n```'
    expected_blocks = [
        MarkdownBlock(lines=["This is a markdown block.", ""], start_line_number=0),
        ExecBlock(
            lines=["```python exec", 'print("Hello, world!")', "```"],
            start_line_number=2,
        ),
        MarkdownBlock(
            lines=["This is another markdown block.", ""], start_line_number=6
        ),
        EvalBlock(lines=["```python eval", "2 + 2", "```"], start_line_number=8),
    ]
    actual_blocks = list(fd.get_blocks(source))
    assert actual_blocks == expected_blocks
