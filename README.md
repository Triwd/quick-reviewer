# Quick Reviewer - 学术论文智能审查框架

> **版本**: v2.0  
> **更新日期**: 2026-03-19  
> **适用对象**: 大模型（AI Agent）与论文作者  
> **适用范围**: 中/英文学术论文（学位论文、期刊论文、会议论文）

---

## 📋 框架简介

Quick Reviewer 是一套**纯SKILL模式**的学术论文审查框架，通过结构化的大模型提示词（Prompt），帮助作者系统性地提升论文质量。

**核心理念**：将论文审查的专业知识封装为可复用的 SKILL 模块，大模型通过阅读这些 SKILL 文档，自主完成多维度审查任务。

---

## 🚀 快速开始

### 前提条件

- 一个支持文件上传的大模型（如 Kimi、GPT-4、Claude 等）
- 待审查的论文文件（.doc/.docx/.pdf/.txt/.md）

### 使用方式

将本项目的 `skills/` 目录作为上下文提供给大模型，然后按以下方式使用：

#### 方式一：一键全面审查（推荐）

```markdown
请对附件论文进行全面审查：

1. 读取 @skills/00-meta/SKILL.md 了解完整工作流
2. 按需读取各审查SKILL：
   - @skills/doc_parser/SKILL.md
   - @skills/structure_review/SKILL.md
   - @skills/grammar_spelling/SKILL.md
   - @skills/figures_tables/SKILL.md
   - @skills/references/SKILL.md
   - @skills/logic_content/SKILL.md
   - @skills/reviewer_simulator/SKILL.md
3. 输出综合审查报告到 ./report/ 目录

要求：
- 审查完成后清理所有临时文件
- 仅保留最终审查报告
```

#### 方式二：快速预审（适合时间紧张）

```markdown
请快速审查附件论文的主要问题：

1. 读取 @skills/doc_parser/SKILL.md 进行文档解析
2. 读取 @skills/reviewer_simulator/SKILL.md 进行综合评审
3. 重点关注：创新性、实验设计、写作质量
4. 输出简版审查报告到 ./report/review_report.md
```

#### 方式三：专项审查（针对特定问题）

```markdown
请仅检查论文的语法和格式问题：

1. 读取 @skills/grammar_spelling/SKILL.md
2. 读取 @skills/figures_tables/SKILL.md
3. 检查论文的语法、拼写、标点、图表规范
4. 输出问题清单
```

---

## 📚 使用示例

### 示例1：完整审查流程

**用户输入**：
```
请帮我全面审查论文 manuscript.doc
```

**大模型执行流程**：

```
Step 1: 读取 00-meta/SKILL.md，了解协调工作流

Step 2: 文档解析
    ├── 评估文件大小（27KB，>20KB需分片）
    ├── 提取元数据（标题、摘要、关键词、章节结构）
    └── 规划分片策略（按章节分5片）

Step 3: 分片审查
    ├── 分片1：引言 + 相关工作
    │   └── 读取 structure_review + logic_content SKILL
    ├── 分片2：问题定义 + 方法
    │   └── 读取 logic_content + grammar_spelling SKILL
    ├── 分片3：实验设计
    │   └── 读取 logic_content SKILL
    ├── 分片4：结果分析
    │   └── 读取 logic_content + figures_tables SKILL
    └── 分片5：结论 + 参考文献
        └── 读取 references + grammar_spelling SKILL

Step 4: 综合评审
    └── 读取 reviewer_simulator SKILL，生成审稿意见

Step 5: 整合报告
    ├── 汇总所有分片发现的问题
    ├── 去重和分级
    └── 生成结构化报告

Step 6: 清理收尾
    ├── 保存报告到 ./report/review_report.md
    └── 删除所有临时文件
```

**输出结果**：
```
./report/
└── review_report.md    # 仅保留最终审查报告
```

### 示例2：针对期刊投稿的审查

```markdown
我准备投稿某期刊，请按期刊标准审查我的论文：

1. 读取 @skills/structure_review/SKILL.md 检查章节结构
2. 读取 @skills/references/SKILL.md 检查参考文献格式
3. 读取 @skills/reviewer_simulator/SKILL.md 模拟审稿人视角
4. 重点关注：
   - 创新性是否突出
   - 实验是否充分
   - 是否存在拒稿风险
5. 输出期刊投稿版审查报告
```

### 示例3：毕业论文预审

```markdown
请按学位论文标准审查我的毕业论文：

1. 读取 @skills/structure_review/SKILL.md
   - 检查必备章节（封面、声明、摘要、目录、正文、参考文献、致谢）
   - 检查章节层级规范性

2. 读取 @skills/grammar_spelling/SKILL.md
   - 检查错别字、语法错误
   - 检查中英文标点规范

3. 读取 @skills/figures_tables/SKILL.md
   - 检查图表编号连续性
   - 检查中英文标题对应

4. 输出修改建议清单
```

---

## 📁 目录结构

```
quick-reviewer/
├── README.md                      # 本文件（用户使用指南）
├── AGENTS.md                      # 大模型开发指南
└── skills/                        # 审查SKILL目录
    ├── 00-meta/                   # 元SKILL：协调器
    │   └── SKILL.md               # 定义完整审查工作流
    ├── doc_parser/                # 文档解析SKILL
    │   └── SKILL.md               # 指导如何解析和分片
    ├── grammar_spelling/          # 语法拼写审查SKILL
    │   └── SKILL.md
    ├── structure_review/          # 结构审查SKILL
    │   └── SKILL.md
    ├── figures_tables/            # 图表审查SKILL
    │   └── SKILL.md
    ├── references/                # 参考文献审查SKILL
    │   └── SKILL.md
    ├── logic_content/             # 逻辑内容审查SKILL
    │   └── SKILL.md
    ├── ai_detection/              # AI痕迹检测SKILL
    │   └── SKILL.md
    ├── reviewer_simulator/        # 审稿专家模拟SKILL
    │   └── SKILL.md
    └── writing_assistant/         # 写作助手SKILL
        └── SKILL.md
```

---

## 🎯 SKILL 一览

| SKILL | 功能 | 核心检查点 |
|-------|------|-----------|
| **00-meta** | 协调器 | 定义完整工作流，协调各SKILL执行顺序 |
| **doc_parser** | 文档解析 | 分片策略、元数据提取、大文件处理 |
| **grammar_spelling** | 语法拼写审查 | 错别字、英文拼写、标点、格式 |
| **structure_review** | 结构审查 | 章节完整性、标题层级、逻辑连贯性 |
| **figures_tables** | 图表审查 | 编号连续性、中英文对应、格式统一性 |
| **references** | 参考文献审查 | 重复检测、引用匹配、格式规范 |
| **logic_content** | 逻辑内容审查 | 摘要五要素、实验设计、结论质量 |
| **ai_detection** | AI痕迹检测 | 语言模式分析、风格一致性 |
| **reviewer_simulator** | 审稿专家模拟 | 创新性、技术正确性、推荐意见 |
| **writing_assistant** | 写作助手 | 润色、重构、回复审稿意见 |

---

## 🧹 临时文件管理

### 自动清理机制

大模型在完成审查后会**自动清理**所有临时文件：

| 临时文件类型 | 说明 | 清理时机 |
|-------------|------|---------|
| 分片解析文件 | 大文件分片产生的临时文本 | 审查完成后 |
| 提取的原始文本 | 从PDF/DOC提取的文本内容 | 审查完成后 |
| 中间JSON数据 | 结构化审查数据（可选保留） | 审查完成后 |

### 保留文件

```
./report/                      # 审查报告目录（自动创建）
└── review_report.md          # 最终审查报告（必须保留）
```

### 如需保留中间文件

如果希望保留中间文件用于检查，请在审查前明确说明：

```markdown
请审查论文，并保留所有中间文件供我检查，不要删除临时文件。
```

### 手动清理

如果需要手动清理临时文件，可以指示大模型：

```markdown
请清理所有审查产生的临时文件，只保留 ./report/ 目录下的报告。
```

---

## 💡 进阶使用

### 自定义审查维度

可以组合不同的SKILL，创建自定义审查流程：

```markdown
请进行"投稿前快速审查"：

1. 读取 @skills/grammar_spelling/SKILL.md - 检查低级错误
2. 读取 @skills/reviewer_simulator/SKILL.md - 评估接收概率
3. 仅输出Critical和Major级别的问题
4. 预估修改所需时间
```

### 增量审查

针对已修改的部分进行增量审查：

```markdown
我已根据上次审查意见修改了论文的第3章和第4章，
请仅审查这两章的修改内容，读取 @skills/logic_content/SKILL.md。
```

### 对比审查

对比两个版本的论文：

```markdown
我有两个版本的论文：v1.doc 和 v2.doc

请对比两个版本，识别v2的改进之处和新增问题，
读取 @skills/00-meta/SKILL.md 和 @skills/reviewer_simulator/SKILL.md。
```

---

## ⚠️ 注意事项

1. **大文件处理**
   - 论文 > 20,000字时，大模型会自动分片解析
   - 分片审查可能需要更多时间，请耐心等待

2. **结果一致性**
   - 不同大模型的审查结果可能有差异
   - 建议对重要论文使用同一模型进行多轮审查

3. **学术诚信**
   - AI痕迹检测仅作为自查参考，不能作为判定依据
   - 所有审查建议需作者最终确认

4. **隐私保护**
   - 涉及敏感内容的论文，建议使用本地部署的大模型
   - 审查前可删除作者个人信息

---

*Quick Reviewer - 让论文审查更智能、更便捷*
