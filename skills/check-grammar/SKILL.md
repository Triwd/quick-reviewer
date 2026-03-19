---
name: check-grammar
description: "检查学术论文的语法、拼写和标点问题。Trigger when user wants grammar/spelling check."
argument-hint: "<论文文件路径>"
allowed-tools: [Read, Write, Bash, Glob, Grep]
---

# 语法拼写审查

请对论文 `$ARGUMENTS` 进行语法拼写审查：

1. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/doc_parser.md` 进行文档解析
2. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/grammar_spelling.md` 执行语法拼写审查
3. 输出问题清单到 `./report/review_report.md`
4. 审查完成后清理临时文件
