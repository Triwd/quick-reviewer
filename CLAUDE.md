# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Quick Reviewer is an academic paper review framework (v2.1) with two usage modes:
1. **Claude Code Plugin** — install via plugin system, use slash commands like `/quick-reviewer:review`
2. **Minimalist CLI** — standalone tool, configure API key and run `quick-reviewer review paper.pdf`

Both modes share the same `knowledge/` files containing detailed review prompts and criteria.

**Language**: All knowledge documents and prompts are written in Chinese (Simplified).

## Architecture

### Knowledge files (`knowledge/`)
Detailed prompt documents (moved from the original `skills/` directories). Each file is a self-contained review dimension with check criteria, output format, and examples.

- `knowledge/00-meta.md` — The **orchestrator**. Defines the complete 10-step review workflow and coordinates all other dimensions.
- `knowledge/doc_parser.md` — Document parsing & chunking guide
- `knowledge/grammar_spelling.md` — Grammar & spelling check
- `knowledge/structure_review.md` — Structure review
- `knowledge/figures_tables.md` — Figures & tables check
- `knowledge/references.md` — References check
- `knowledge/logic_content.md` — Logic & content review
- `knowledge/ai_detection.md` — AI-generated text detection
- `knowledge/reviewer_simulator.md` — Reviewer simulation
- `knowledge/writing_assistant.md` — Writing assistant

### Plugin skills (`skills/`)
Thin wrapper SKILL.md files with YAML frontmatter that reference knowledge files. Each maps to a slash command (e.g., `/quick-reviewer:review`).

### CLI (`cli/`)
Python CLI using Typer. Supports Anthropic and OpenAI-compatible providers with streaming output.

## Key Conventions

- Review output goes to `./report/review_report.md`. Temporary files are cleaned up after review unless the user requests otherwise.
- Issue severity levels: Critical > Major > Minor > Suggestion.
- Large documents (>20K characters) must be chunked; adjacent chunks overlap ~500 chars for context continuity.

## When Editing Knowledge Files

- Maintain the existing document structure: 概述 (overview), check dimensions/rules tables, output format templates, and usage examples.
- Keep prompts in Chinese to match the target audience.
- Cross-references between knowledge files use relative paths like `grammar_spelling.md`.

## When Editing Skills

- Each skill SKILL.md is a thin wrapper (20-40 lines) with YAML frontmatter.
- Skills reference knowledge files via `${CLAUDE_PLUGIN_ROOT}/knowledge/<name>.md`.

## CLI Development

- Entry point: `cli/main.py` (Typer app)
- Config priority: CLI flags > env vars > project config > user config
- Supports two LLM providers: Anthropic (native) and OpenAI-compatible
- Paper parsing supports .txt, .md, .pdf (optional pymupdf), .docx (optional python-docx)
