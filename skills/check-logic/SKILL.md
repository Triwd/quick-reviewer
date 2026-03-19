---
name: check-logic
description: "检查学术论文的逻辑与内容质量。Trigger when user wants logic/content review."
argument-hint: "<论文文件路径>"
allowed-tools: [Read, Write, Bash, Glob, Grep]
---

# 逻辑内容审查

请对论文 `$ARGUMENTS` 进行逻辑内容审查：

1. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/doc_parser.md` 进行文档解析
2. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/logic_content.md` 执行逻辑内容审查
3. 输出问题清单到 `./report/review_report.md`
4. 审查完成后清理临时文件
