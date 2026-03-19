---
name: quick-review
description: "对学术论文进行快速预审。Trigger when user wants a quick pre-review."
argument-hint: "<论文文件路径>"
allowed-tools: [Read, Write, Bash, Glob, Grep]
---

# 快速预审

请对论文 `$ARGUMENTS` 执行快速预审：

1. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/doc_parser.md` 进行文档解析
2. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/reviewer_simulator.md` 进行综合评审
3. 输出简版审查报告到 `./report/review_report.md`
4. 审查完成后清理临时文件
