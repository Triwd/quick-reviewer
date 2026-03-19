---
name: check-references
description: "检查学术论文的参考文献规范性。Trigger when user wants reference check."
argument-hint: "<论文文件路径>"
allowed-tools: [Read, Write, Bash, Glob, Grep]
---

# 参考文献审查

请对论文 `$ARGUMENTS` 进行参考文献审查：

1. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/doc_parser.md` 进行文档解析
2. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/references.md` 执行参考文献审查
3. 输出问题清单到 `./report/review_report.md`
4. 审查完成后清理临时文件
