# Team Python Example — Reference Only

Open only when a style judgment in `team-python.md` is borderline. It shows the team conventions together: imports grouped and alphabetized, Google-style docstrings, type hints, `lower_case_with_underscores` functions, `CamelCase` classes, lines up to 120 characters.

**Note for reviewers:** `statistics` and `pandas` are imported but never used in this example. They are there only to show the three import groups. In real code an unused import is a finding (or a linter error) — do not treat it as acceptable because it appears here.

```python
"""Utilities for summarizing sample sequencing results."""

import csv
import statistics
from pathlib import Path

import pandas as pd

from my_project.config import DEFAULT_THRESHOLD


class SampleSummarizer:
    """Computes summary statistics for a set of samples.

    Attributes:
        threshold: Minimum score for a sample to be counted as passing.
    """

    def __init__(self, threshold: float = DEFAULT_THRESHOLD) -> None:
        self.threshold = threshold

    def pass_rate(self, scores: list[float]) -> float:
        """Returns the fraction of scores at or above the threshold.

        Args:
            scores: Per-sample scores.

        Returns:
            A value between 0.0 and 1.0.

        Raises:
            ValueError: If `scores` is empty.
        """
        if not scores:
            raise ValueError("scores must not be empty")
        return sum(score >= self.threshold for score in scores) / len(scores)


def load_scores(path: Path) -> list[float]:
    """Reads scores from the `score` column of a CSV file."""
    with path.open() as handle:
        return [float(row["score"]) for row in csv.DictReader(handle)]
```

Matching tests — one parametrized unit test, one error-path unit test, and one end-to-end test on a small dataset:

```python
"""Tests for sample summarization."""

from pathlib import Path

import pytest

from my_project.summary import SampleSummarizer, load_scores


@pytest.mark.parametrize("scores, expected", [([1.0, 0.0], 0.5), ([1.0, 1.0], 1.0)])
def test_pass_rate(scores: list[float], expected: float) -> None:
    assert SampleSummarizer(threshold=0.5).pass_rate(scores) == expected


def test_pass_rate_empty_raises() -> None:
    with pytest.raises(ValueError):
        SampleSummarizer().pass_rate([])


def test_end_to_end(tmp_path: Path) -> None:
    """Runs load + summarize on a small dataset."""
    data = tmp_path / "scores.csv"
    data.write_text("score\n0.9\n0.1\n")
    assert SampleSummarizer(threshold=0.5).pass_rate(load_scores(data)) == 0.5
```
