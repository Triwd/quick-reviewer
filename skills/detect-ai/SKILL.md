---
name: detect-ai
description: "检测学术论文中的AI生成痕迹。Trigger when user wants AI detection."
argument-hint: "<论文文件路径>"
allowed-tools: [Read, Write, Bash, Glob, Grep]
---

# AI痕迹检测

请对论文 `$ARGUMENTS` 进行AI痕迹检测：

1. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/doc_parser.md` 进行文档解析
2. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/ai_detection.md` 执行AI痕迹检测
3. 输出检测报告到 `./report/review_report.md`
4. 审查完成后清理临时文件
