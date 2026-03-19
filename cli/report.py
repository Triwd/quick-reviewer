from __future__ import annotations

from pathlib import Path


_MODE_SUFFIXES: dict[str, str] = {
    "review": "全面审查",
    "quick": "快速预审",
    "grammar": "语法拼写",
    "references": "参考文献",
    "figures": "图表审查",
    "structure": "结构审查",
    "logic": "逻辑内容",
    "ai": "AI检测",
    "writing": "写作辅助",
}


def ensure_report_dir(
    output: Path | None = None, source_file: str = "", mode: str = ""
) -> Path:
    """Ensure the report directory exists and return the output path."""
    if output is None:
        stem = Path(source_file).stem if source_file else ""
        suffix = _MODE_SUFFIXES.get(mode, "")
        parts = [p for p in (stem, suffix, "report") if p]
        filename = "-".join(parts) + ".md"
        output = Path("report") / filename
    output.parent.mkdir(parents=True, exist_ok=True)
    return output


def save_report(content: str, output: Path, source_file: str = "") -> None:
    """Save report content to file, with source file header."""
    header = f"> **源文件**：`{source_file}`\n\n" if source_file else ""
    output.write_text(header + content, encoding="utf-8")
