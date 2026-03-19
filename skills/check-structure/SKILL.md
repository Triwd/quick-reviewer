---
name: check-structure
description: "检查学术论文的结构规范性。Trigger when user wants structure review."
argument-hint: "<论文文件路径>"
allowed-tools: [Read, Write, Bash, Glob, Grep]
---

# 结构审查

请对论文 `$ARGUMENTS` 进行结构审查：

1. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/doc_parser.md` 进行文档解析
2. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/structure_review.md` 执行结构审查
3. 输出问题清单到 `./report/review_report.md`
4. 审查完成后清理临时文件
