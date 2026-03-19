from __future__ import annotations

from pathlib import Path


_KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"

# Mapping from review mode to required knowledge files
_MODE_FILES: dict[str, list[str]] = {
    "review": ["00-meta"],
    "quick": ["doc_parser", "reviewer_simulator"],
    "grammar": ["doc_parser", "grammar_spelling"],
    "references": ["doc_parser", "references"],
    "figures": ["doc_parser", "figures_tables"],
    "structure": ["doc_parser", "structure_review"],
    "logic": ["doc_parser", "logic_content"],
    "ai": ["doc_parser", "ai_detection"],
    "writing": ["doc_parser", "writing_assistant"],
}

# For full review, load all knowledge files in workflow order
_ALL_FILES = [
    "00-meta",
    "doc_parser",
    "structure_review",
    "grammar_spelling",
    "figures_tables",
    "references",
    "logic_content",
    "ai_detection",
    "reviewer_simulator",
    "writing_assistant",
]


def load_knowledge(mode: str) -> str:
    """Load and concatenate knowledge files for the given review mode."""
    if mode == "review":
        files = _ALL_FILES
    else:
        files = _MODE_FILES.get(mode, [])
        if not files:
            raise ValueError(f"Unknown review mode: {mode}")

    parts: list[str] = []
    for name in files:
        path = _KNOWLEDGE_DIR / f"{name}.md"
        if not path.is_file():
            raise FileNotFoundError(f"Knowledge file not found: {path}")
        parts.append(path.read_text(encoding="utf-8"))

    return "\n\n---\n\n".join(parts)


_MODE_LABELS: dict[str, str] = {
    "review": "全面审查",
    "quick": "快速预审",
    "grammar": "语法拼写专项审查",
    "references": "参考文献专项审查",
    "figures": "图表专项审查",
    "structure": "结构专项审查",
    "logic": "逻辑内容专项审查",
    "ai": "AI痕迹检测",
    "writing": "写作辅助",
}


def build_prompts(mode: str, paper_content: str) -> tuple[str, str]:
    """Build system prompt and user prompt for the LLM call.

    Returns:
        (system_prompt, user_prompt)
    """
    knowledge = load_knowledge(mode)
    label = _MODE_LABELS.get(mode, mode)

    if mode == "review":
        instruction = (
            "你是一位学术论文审查专家。请严格按照以下审查知识文档中的规则和流程，"
            "对用户提供的论文内容进行全面审查，并输出结构化的审查报告。"
        )
    else:
        instruction = (
            f"你是一位学术论文审查专家。本次任务为【{label}】。"
            f"请**仅**按照以下审查知识文档中的规则，聚焦于该维度进行审查。"
            f"不要超出该维度范围进行其他方面的审查。输出结构化的审查报告。"
        )

    system_prompt = f"{instruction}\n\n{knowledge}"
    user_prompt = f"请对以下论文进行{label}：\n\n{paper_content}"

    return system_prompt, user_prompt
