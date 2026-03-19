---
name: simulate-review
description: "模拟审稿专家对论文进行评审，给出审稿意见和推荐结果。Trigger when user wants simulated peer review."
argument-hint: "<论文文件路径>"
allowed-tools: [Read, Write, Bash, Glob, Grep]
---

# 审稿专家模拟

请以审稿专家的身份对论文 `$ARGUMENTS` 进行模拟评审：

1. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/doc_parser.md` 进行文档解析
2. 读取 `${CLAUDE_PLUGIN_ROOT}/knowledge/reviewer_simulator.md` 执行审稿专家模拟评审
3. 从创新性、技术正确性、实验充分性、写作质量、文献综述五个维度评估
4. 给出推荐意见（Accept / Minor Revision / Major Revision / Reject）
5. 输出审稿意见到 `./report/review_report.md`

**输出格式要求**：问题清单和修改建议中的每一条必须包含：位置（精确到章节段落）、问题类型、原文文本、修订后文本。以表格形式输出，不要只写笼统描述。
