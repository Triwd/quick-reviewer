---
name: check-figures
description: "检查学术论文的图表规范性。Trigger when user wants figures/tables check."
argument-hint: "<论文文件路径>"
allowed-tools: [Read, Write, Bash, Glob, Grep]
---

# 图表审查

请对论文 `$ARGUMENTS` 进行图表审查：

1. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/doc_parser.md` 进行文档解析
2. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/figures_tables.md` 执行图表审查
3. 输出问题清单到 `./report/review_report.md`
4. 审查完成后清理临时文件
