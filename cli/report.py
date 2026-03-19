from __future__ import annotations

from pathlib import Path


def ensure_report_dir(output: Path | None = None) -> Path:
    """Ensure the report directory exists and return the output path."""
    if output is None:
        output = Path("report") / "review_report.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    return output


def save_report(content: str, output: Path) -> None:
    """Save report content to file."""
    output.write_text(content, encoding="utf-8")
