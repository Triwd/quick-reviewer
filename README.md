# Quick Reviewer - 学术论文智能审查框架

> **版本**: v2.1 | **更新日期**: 2026-03-19

Quick Reviewer 是一套学术论文审查框架，通过结构化的大模型提示词（Prompt），帮助作者系统性地提升论文质量。支持 **Claude Code 插件** 和 **命令行工具** 两种使用方式。

---

## 使用方式一：Claude Code 插件

### 安装

```bash
claude plugin add /path/to/quick-reviewer
# 或通过 Git URL
claude plugin add https://github.com/your-username/quick-reviewer.git
```

### 使用

```bash
# 全面审查
/quick-reviewer:review paper.pdf

# 快速预审
/quick-reviewer:quick-review paper.pdf

# 专项审查
/quick-reviewer:check-grammar paper.pdf
/quick-reviewer:check-references paper.pdf
/quick-reviewer:check-figures paper.pdf
/quick-reviewer:check-structure paper.pdf
/quick-reviewer:check-logic paper.pdf
/quick-reviewer:detect-ai paper.pdf

# 写作辅助
/quick-reviewer:writing-assist paper.pdf
```

---

## 使用方式二：命令行工具（CLI）

### 安装

```bash
pip install -e .

# 可选：PDF 支持
pip install -e ".[pdf]"

# 可选：DOCX 支持
pip install -e ".[docx]"
```

### 配置

设置 API Key（二选一）：

**macOS / Linux：**

```bash
# Anthropic
export ANTHROPIC_API_KEY=sk-ant-...

# OpenAI 兼容
export OPENAI_API_KEY=sk-...
export QR_PROVIDER=openai
export QR_BASE_URL=https://api.openai.com/v1  # 或其他兼容端点
```

**Windows (CMD)：**

```cmd
set ANTHROPIC_API_KEY=sk-ant-...

:: OpenAI 兼容
set OPENAI_API_KEY=sk-...
set QR_PROVIDER=openai
set QR_BASE_URL=https://api.openai.com/v1
```

**Windows (PowerShell)：**

```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."

# OpenAI 兼容
$env:OPENAI_API_KEY = "sk-..."
$env:QR_PROVIDER = "openai"
$env:QR_BASE_URL = "https://api.openai.com/v1"
```

也可以使用配置文件（推荐，跨平台通用）`~/.quick-reviewer/config.yaml`：

```yaml
provider: anthropic
api_key: sk-ant-...
model: claude-sonnet-4-20250514
```

### 使用

```bash
# 全面审查
quick-reviewer review paper.pdf

# 快速预审
quick-reviewer quick paper.pdf

# 专项审查
quick-reviewer check grammar paper.pdf
quick-reviewer check references paper.pdf
quick-reviewer check figures paper.pdf
quick-reviewer check structure paper.pdf
quick-reviewer check logic paper.pdf
quick-reviewer check ai paper.pdf

# 自定义选项
quick-reviewer review paper.pdf --provider openai --base-url http://localhost:11434/v1 --model qwen2.5
quick-reviewer review paper.pdf --output ./my-report.md
```

---

## 项目结构

```
quick-reviewer/
├── .claude-plugin/          # Claude Code 插件配置
│   └── plugin.json
├── knowledge/               # 审查知识文档（核心提示词）
│   ├── 00-meta.md           # 协调器：完整工作流
│   ├── doc_parser.md        # 文档解析
│   ├── grammar_spelling.md  # 语法拼写审查
│   ├── structure_review.md  # 结构审查
│   ├── figures_tables.md    # 图表审查
│   ├── references.md        # 参考文献审查
│   ├── logic_content.md     # 逻辑内容审查
│   ├── ai_detection.md      # AI痕迹检测
│   ├── reviewer_simulator.md# 审稿专家模拟
│   └── writing_assistant.md # 写作助手
├── skills/                  # 插件 Skill（斜杠命令）
│   ├── review/              # /quick-reviewer:review
│   ├── quick-review/        # /quick-reviewer:quick-review
│   ├── check-grammar/       # /quick-reviewer:check-grammar
│   ├── check-references/    # /quick-reviewer:check-references
│   ├── check-figures/       # /quick-reviewer:check-figures
│   ├── check-structure/     # /quick-reviewer:check-structure
│   ├── check-logic/         # /quick-reviewer:check-logic
│   ├── detect-ai/           # /quick-reviewer:detect-ai
│   └── writing-assist/      # /quick-reviewer:writing-assist
├── cli/                     # 命令行工具
├── pyproject.toml           # Python 项目配置
├── CLAUDE.md                # Claude Code 开发指南
└── README.md                # 本文件
```

## 审查维度

| 维度 | 核心检查点 |
|------|-----------|
| **语法拼写** | 错别字、英文拼写、标点、中英文混排 |
| **结构审查** | 章节完整性、标题层级、逻辑连贯 |
| **图表审查** | 编号连续性、中英文对应、引用准确 |
| **参考文献** | 引用匹配、格式规范、时效性 |
| **逻辑内容** | 摘要、方法、实验设计、结论质量 |
| **AI检测** | AI生成痕迹、语言模式分析 |
| **审稿模拟** | 创新性、技术正确性、推荐意见 |
| **写作助手** | 润色、重构、审稿回复 |

---

## 注意事项

1. **大文件处理**：论文 > 20,000字时自动分片解析
2. **结果一致性**：不同大模型的审查结果可能有差异
3. **学术诚信**：AI痕迹检测仅作为自查参考
4. **隐私保护**：敏感内容建议使用本地部署的大模型

---

*Quick Reviewer - 让论文审查更智能、更便捷*
