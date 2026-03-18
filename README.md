# Quick Reviewer - 学术论文智能审查框架

> **版本**: v2.0 | **更新日期**: 2026-03-19

Quick Reviewer 是一套**纯SKILL模式**的学术论文审查框架，通过结构化的大模型提示词（Prompt），帮助作者系统性地提升论文质量。

**核心理念**：将论文审查的专业知识封装为可复用的 SKILL 模块，大模型通过阅读这些 SKILL 文档，自主完成多维度审查任务。

---

## 🚀 快速开始

### 前提条件

- 支持文件上传的大模型（Kimi、GPT-4、Claude 等）
- 待审查的论文文件（.doc/.docx/.pdf/.txt/.md）

### 使用方式

将本项目的 `skills/` 目录作为上下文提供给大模型，然后使用以下指令：

#### 一键全面审查（推荐）

```markdown
请对附件论文进行全面审查：

1. 读取 @skills/00-meta/SKILL.md 了解完整工作流
2. 按需读取各审查SKILL完成审查
3. 输出综合审查报告到 ./report/ 目录

要求：审查完成后清理临时文件，仅保留最终报告
```

#### 快速预审

```markdown
请快速审查附件论文：

1. 读取 @skills/doc_parser/SKILL.md 进行文档解析
2. 读取 @skills/reviewer_simulator/SKILL.md 进行综合评审
3. 输出简版审查报告到 ./report/review_report.md
```

#### 专项审查

```markdown
请检查论文的语法和格式问题：

1. 读取 @skills/grammar_spelling/SKILL.md
2. 读取 @skills/figures_tables/SKILL.md
3. 输出问题清单
```

---

## 📁 项目结构

```
quick-reviewer/
├── README.md              # 本文件
├── AGENTS.md              # 开发指南
└── skills/                # 审查SKILL目录
    ├── 00-meta/           # 协调器：定义完整工作流
    ├── doc_parser/        # 文档解析
    ├── grammar_spelling/  # 语法拼写审查
    ├── structure_review/  # 结构审查
    ├── figures_tables/    # 图表审查
    ├── references/        # 参考文献审查
    ├── logic_content/     # 逻辑内容审查
    ├── ai_detection/      # AI痕迹检测
    ├── reviewer_simulator/# 审稿专家模拟
    └── writing_assistant/ # 写作助手
```

## 🎯 SKILL 一览

| SKILL | 功能 | 核心检查点 |
|-------|------|-----------|
| **00-meta** | 协调器 | 定义完整工作流，协调各SKILL执行 |
| **doc_parser** | 文档解析 | 分片策略、元数据提取 |
| **grammar_spelling** | 语法拼写 | 错别字、英文拼写、标点 |
| **structure_review** | 结构审查 | 章节完整性、标题层级 |
| **figures_tables** | 图表审查 | 编号连续性、中英文对应 |
| **references** | 参考文献 | 引用匹配、格式规范 |
| **logic_content** | 逻辑内容 | 摘要、实验设计、结论 |
| **ai_detection** | AI痕迹检测 | 语言模式分析 |
| **reviewer_simulator** | 审稿模拟 | 创新性、推荐意见 |
| **writing_assistant** | 写作助手 | 润色、回复审稿意见 |

---

## 🧹 临时文件管理

大模型在完成审查后会**自动清理**临时文件（分片文件、提取的文本等），仅保留 `./report/review_report.md`。

如需保留中间文件，请在审查前说明：
```markdown
请审查论文，保留所有中间文件供我检查。
```

---

## 💡 进阶用法

**自定义审查维度**：
```markdown
请进行"投稿前快速审查"：
1. 读取 @skills/grammar_spelling/SKILL.md
2. 读取 @skills/reviewer_simulator/SKILL.md
3. 仅输出Critical和Major级别的问题
```

**增量审查**：
```markdown
我已修改了论文的第3章和第4章，
请仅审查这两章，读取 @skills/logic_content/SKILL.md。
```

---

## ⚠️ 注意事项

1. **大文件处理**：论文 > 20,000字时，大模型会自动分片解析
2. **结果一致性**：不同大模型的审查结果可能有差异
3. **学术诚信**：AI痕迹检测仅作为自查参考
4. **隐私保护**：敏感内容建议使用本地部署的大模型

---

*Quick Reviewer - 让论文审查更智能、更便捷*
