# Quick Reviewer - 学术论文智能审查框架

> **版本**: v2.1 | **更新日期**: 2026-03-19

Quick Reviewer 是一套学术论文审查框架，通过结构化的大模型提示词（Prompt），帮助作者系统性地提升论文质量。

支持两种使用方式：

- **Claude Code 插件** — 在 Claude Code 中通过斜杠命令直接调用
- **命令行工具（CLI）** — 独立运行，支持 Anthropic 和 OpenAI 兼容接口（如 DeepSeek、Ollama 等）

---

## 前置要求

| 依赖 | 版本要求 | 说明 |
|------|---------|------|
| Python | >= 3.10 | CLI 工具必需 |
| pip | 最新版 | Python 包管理器 |
| Git | 任意 | 克隆仓库 |
| API Key | - | Anthropic 或 OpenAI 兼容服务商的 API Key |

> 插件模式不需要安装 Python，只需 Claude Code 即可。

---

## 使用方式一：Claude Code 插件

### 第 1 步：克隆项目

```bash
git clone https://github.com/Triwd/quick-reviewer.git
```

### 第 2 步：加载插件并启动 Claude Code

在你的**论文所在目录**（或任意工作目录）中，通过 `--plugin-dir` 参数加载插件：

```bash
cd /path/to/your/paper-project
claude --plugin-dir /path/to/quick-reviewer
```

例如，如果你把 quick-reviewer 克隆到了 `~/tools/quick-reviewer`，论文在 `~/papers/my-thesis/`：

```bash
cd ~/papers/my-thesis
claude --plugin-dir ~/tools/quick-reviewer
```

启动后可通过输入 `/` 查看可用的斜杠命令，确认插件已加载。

### 第 3 步：使用斜杠命令

在 Claude Code 对话中输入以下命令：

| 命令 | 功能 | 示例 |
|------|------|------|
| `/quick-reviewer:review` | 全面审查（10 步完整流程） | `/quick-reviewer:review paper.pdf` |
| `/quick-reviewer:quick-review` | 快速预审（解析 + 审稿模拟） | `/quick-reviewer:quick-review paper.pdf` |
| `/quick-reviewer:check-grammar` | 语法拼写检查 | `/quick-reviewer:check-grammar paper.pdf` |
| `/quick-reviewer:check-structure` | 结构审查 | `/quick-reviewer:check-structure paper.pdf` |
| `/quick-reviewer:check-figures` | 图表审查 | `/quick-reviewer:check-figures paper.pdf` |
| `/quick-reviewer:check-references` | 参考文献审查 | `/quick-reviewer:check-references paper.pdf` |
| `/quick-reviewer:check-logic` | 逻辑内容审查 | `/quick-reviewer:check-logic paper.pdf` |
| `/quick-reviewer:detect-ai` | AI 痕迹检测 | `/quick-reviewer:detect-ai paper.pdf` |
| `/quick-reviewer:writing-assist` | 写作辅助 | `/quick-reviewer:writing-assist paper.pdf` |

审查报告将自动保存到 `./report/review_report.md`。

---

## 使用方式二：命令行工具（CLI）

### 第 1 步：克隆仓库（如已克隆可跳过）

```bash
git clone https://github.com/Triwd/quick-reviewer.git
cd quick-reviewer
```

### 第 2 步：创建虚拟环境并安装

```bash
# 创建虚拟环境（仅需执行一次）
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows CMD
# .venv\Scripts\Activate.ps1     # Windows PowerShell

# 安装基础依赖
pip install -e .

# 如需审查 PDF 文件
pip install -e ".[pdf]"

# 如需审查 Word 文件（.docx）
pip install -e ".[docx]"
```

安装完成后验证：

```bash
quick-reviewer --help
```

> **注意**：每次打开新终端都需要先激活虚拟环境（`source .venv/bin/activate`），否则 `quick-reviewer` 命令不可用。

### 第 3 步：配置 API Key

CLI 需要通过 API 调用大模型服务。请根据你使用的服务商，选择以下任一方式配置。

#### 方式 A：环境变量（临时生效，关闭终端后失效）

<details>
<summary><strong>macOS / Linux</strong></summary>

```bash
# 使用 Anthropic（默认）
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# 或使用 OpenAI 兼容服务（DeepSeek、Ollama 等）
export OPENAI_API_KEY=your-key-here
export QR_PROVIDER=openai
export QR_BASE_URL=https://api.deepseek.com   # 你的服务商 API 地址
```

</details>

<details>
<summary><strong>Windows CMD</strong></summary>

```cmd
:: 使用 Anthropic（默认）
set ANTHROPIC_API_KEY=sk-ant-your-key-here

:: 或使用 OpenAI 兼容服务
set OPENAI_API_KEY=your-key-here
set QR_PROVIDER=openai
set QR_BASE_URL=https://api.deepseek.com
```

</details>

<details>
<summary><strong>Windows PowerShell</strong></summary>

```powershell
# 使用 Anthropic（默认）
$env:ANTHROPIC_API_KEY = "sk-ant-your-key-here"

# 或使用 OpenAI 兼容服务
$env:OPENAI_API_KEY = "your-key-here"
$env:QR_PROVIDER = "openai"
$env:QR_BASE_URL = "https://api.deepseek.com"
```

</details>

#### 方式 B：配置文件（持久生效，推荐）

在以下**两个位置之一**创建配置文件（注意文件名，不要写错）：

| 级别 | 文件路径 | 说明 |
|------|---------|------|
| 用户级 | `~/.quick-reviewer/config.yaml` | 对所有项目生效 |
| 项目级 | `项目根目录/.quick-reviewer.yaml` | 仅当前项目生效，优先级更高 |

> **注意**：项目级配置的文件名是 `.quick-reviewer.yaml`（以点开头），不是 `config.yaml`。

配置文件示例（二选一，不要同时启用两个 provider）：

**使用 Anthropic：**

```yaml
provider: anthropic
api_key: sk-ant-your-key-here
model: claude-sonnet-4-20250514         # 可选，不填则使用默认模型
```

**使用 OpenAI 兼容服务（DeepSeek、Ollama、通义千问等）：**

```yaml
provider: openai                        # 必须填 openai，不要填服务商名称
api_key: your-key-here
base_url: https://api.deepseek.com      # 服务商 API 地址（不需要带 /v1 后缀）
model: deepseek-chat                    # 模型名称
```

> `provider` 只支持两个值：`anthropic` 和 `openai`。所有 OpenAI 兼容的服务（DeepSeek、Ollama、通义千问等）都填 `openai`，通过 `base_url` 区分不同服务商。

> **配置优先级**（从高到低）：命令行参数 > 环境变量 > 项目级配置文件 > 用户级配置文件

#### 方式 C：命令行参数（一次性使用）

```bash
quick-reviewer review paper.pdf --api-key your-key --provider openai --base-url https://api.deepseek.com --model deepseek-chat
```

### 第 4 步：运行审查

#### 全面审查

对论文执行完整的 10 步审查流程，输出综合报告：

```bash
quick-reviewer review paper.pdf
```

#### 快速预审

快速评估论文整体质量，给出审稿意见和推荐结果：

```bash
quick-reviewer quick paper.pdf
```

#### 专项审查

只检查论文的某个特定维度：

```bash
quick-reviewer check grammar paper.pdf       # 语法拼写
quick-reviewer check structure paper.pdf      # 结构规范
quick-reviewer check figures paper.pdf        # 图表规范
quick-reviewer check references paper.pdf     # 参考文献
quick-reviewer check logic paper.pdf          # 逻辑内容
quick-reviewer check ai paper.pdf             # AI 痕迹检测
```

#### 指定输出路径

默认报告保存到 `./report/review_report.md`，可通过 `-o` 指定其他路径：

```bash
quick-reviewer review paper.pdf -o ./my-report.md
```

### 支持的文件格式

| 格式 | 扩展名 | 是否需要额外安装 |
|------|--------|-----------------|
| 纯文本 | `.txt` | 不需要 |
| Markdown | `.md` | 不需要 |
| PDF | `.pdf` | 需要：`pip install -e ".[pdf]"` |
| Word | `.docx` | 需要：`pip install -e ".[docx]"` |

---

## 审查维度一览

| 维度 | CLI 命令 | 核心检查点 |
|------|---------|-----------|
| **语法拼写** | `check grammar` | 错别字、英文拼写、标点、中英文混排 |
| **结构审查** | `check structure` | 章节完整性、标题层级、逻辑连贯 |
| **图表审查** | `check figures` | 编号连续性、中英文对应、引用准确 |
| **参考文献** | `check references` | 引用匹配、格式规范、时效性 |
| **逻辑内容** | `check logic` | 摘要、方法、实验设计、结论质量 |
| **AI 检测** | `check ai` | AI 生成痕迹、语言模式分析 |
| **审稿模拟** | `review` / `quick` | 创新性、技术正确性、推荐意见 |
| **写作辅助** | 插件 `writing-assist` | 润色、重构、审稿回复 |

问题严重程度分为四级：**Critical**（必须修改） > **Major**（强烈建议） > **Minor**（建议修改） > **Suggestion**（可选优化）

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
│   ├── ai_detection.md      # AI 痕迹检测
│   ├── reviewer_simulator.md# 审稿专家模拟
│   └── writing_assistant.md # 写作助手
├── skills/                  # 插件 Skill（斜杠命令入口）
├── cli/                     # 命令行工具源码
├── pyproject.toml           # Python 项目配置
├── CLAUDE.md                # Claude Code 开发指南
└── README.md                # 本文件
```

---

## 常见问题

**Q：论文太长怎么办？**
超过 20,000 字的论文会自动按章节分片处理，相邻分片保留约 500 字重叠以保持上下文连贯。

**Q：不同模型的审查结果会不同吗？**
会。不同大模型的能力和风格不同，审查结果会有差异。建议使用能力较强的模型（如 Claude Sonnet/Opus、GPT-4o、DeepSeek-R1 等）以获得更高质量的审查报告。

**Q：如何保护论文隐私？**
论文内容会通过 API 发送到大模型服务商。如有保密需求，建议使用本地部署的模型（如通过 Ollama），将 `base_url` 指向本地服务地址即可。

**Q：AI 痕迹检测准确吗？**
AI 痕迹检测仅供自查参考，不构成对论文原创性的最终判定。

---

*Quick Reviewer - 让论文审查更智能、更便捷*
