---
name: writing-assist
description: "学术写作助手，提供润色、重构和审稿回复支持。Trigger when user wants writing assistance."
argument-hint: "<论文文件路径>"
allowed-tools: [Read, Write, Bash, Glob, Grep]
---

# 写作助手

请对论文 `$ARGUMENTS` 提供写作辅助：

1. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/doc_parser.md` 进行文档解析
2. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/writing_assistant.md` 了解写作辅助功能
3. 根据用户需求执行：语言润色、结构优化、内容补充或审稿回复
4. 输出修改建议到 `./report/review_report.md`
