---
name: review
description: "对学术论文进行全面审查。Trigger when user wants a complete paper review."
argument-hint: "<论文文件路径>"
allowed-tools: [Read, Write, Bash, Glob, Grep]
---

# 全面审查

请对论文 `$ARGUMENTS` 执行完整审查：

1. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/00-meta.md` 了解完整工作流
2. 按工作流步骤依次读取各知识文档并执行审查：
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/doc_parser.md` — 文档解析与分片
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/structure_review.md` — 结构审查
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/grammar_spelling.md` — 语法拼写审查
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/figures_tables.md` — 图表审查
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/references.md` — 参考文献审查
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/logic_content.md` — 逻辑内容审查
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/ai_detection.md` — AI痕迹检测
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/reviewer_simulator.md` — 审稿专家模拟
3. 输出综合审查报告到 `./report/review_report.md`
4. 审查完成后清理临时文件
