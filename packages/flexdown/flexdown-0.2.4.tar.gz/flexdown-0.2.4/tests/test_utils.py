"""Tests for the utility functions in the `flexdown.utils` module."""

import pytest

from flexdown import types, utils


@pytest.mark.parametrize(
    "line, env, expected_output",
    [
        ("This is a test line.", {}, "This is a test line."),
        ("The answer is {2 + 2}.", {}, "The answer is 4."),
        (
            "The sum of {a} and {b} is {a + b}.",
            {"a": 2, "b": 3},
            "The sum of 2 and 3 is 5.",
        ),
        ("This is a \\{placeholder\\}.", {}, "This is a \\{placeholder\\}."),
    ],
)
def test_evaluate_templates(line: str, env: types.Env, expected_output: str):
    """Test evaluating Python expressions within template placeholders.

    Args:
        line: The line of text to evaluate.
        env: The environment variables to use for evaluation.
        expected_output: The expected output after evaluation.
    """
    assert utils.evaluate_templates(line, env) == expected_output


@pytest.mark.parametrize(
    "line, env",
    [
        ("The answer is {2 +}.", {}),
        ("The sum of {a} and {b} is {a + b}.", {"a": 2}),
        ("The sum of {a} and {b} is {a + b}.", {"a": 2, "b": "three"}),
    ],
)
def test_evaluate_templates_errors(line: str, env: types.Env):
    """Test that the function raises the expected exceptions for error cases.

    Args:
        line: The line of text to evaluate.
        env: The environment variables to use for evaluation.
    """
    with pytest.raises(ValueError):
        utils.evaluate_templates(line, env)
