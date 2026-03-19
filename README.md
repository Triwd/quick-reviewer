# Quick Reviewer - 学术论文智能审查框架

> **版本**: v2.1 | **更新日期**: 2026-03-19

Quick Reviewer 是一套学术论文审查框架，通过结构化的大模型提示词（Prompt），帮助作者系统性地提升论文质量。

支持两种使用方式：

- **Claude Code 插件** — 通过斜杠命令直接调用，无需安装 Python
- **命令行工具（CLI）** — 独立运行，支持 Anthropic 和 OpenAI 兼容接口（如 DeepSeek、Ollama 等）

---

## 审查功能

| 功能 | 插件命令 | CLI 命令 | 说明 |
|------|---------|---------|------|
| 全面审查 | `/quick-reviewer:review` | `review` | 10 步完整审查流程 |
| 快速预审 | `/quick-reviewer:quick-review` | `quick` | 快速评估 + 审稿意见 |
| 审稿模拟 | `/quick-reviewer:simulate-review` | `simulate` | 模拟审稿专家评审，给出推荐意见 |
| 语法拼写 | `/quick-reviewer:check-grammar` | `check grammar` | 错别字、标点、中英文混排 |
| 结构审查 | `/quick-reviewer:check-structure` | `check structure` | 章节完整性、标题层级 |
| 图表审查 | `/quick-reviewer:check-figures` | `check figures` | 编号连续性、引用准确 |
| 参考文献 | `/quick-reviewer:check-references` | `check references` | 引用匹配、格式规范 |
| 逻辑内容 | `/quick-reviewer:check-logic` | `check logic` | 方法、实验设计、结论质量 |
| AI 检测 | `/quick-reviewer:detect-ai` | `check ai` | AI 生成痕迹分析 |
| 写作辅助 | `/quick-reviewer:writing-assist` | — | 润色、重构、审稿回复（仅插件） |

问题严重程度分为四级：**Critical** > **Major** > **Minor** > **Suggestion**

审查报告自动保存到 `./report/{源文件名}-{审查类型}-report.md`，可通过 `-o` 指定路径。

---

## 使用方式一：Claude Code 插件

### 1. 克隆项目

```bash
git clone https://github.com/Triwd/quick-reviewer.git
```

### 2. 加载插件并启动

在**论文所在目录**中，通过 `--plugin-dir` 加载插件：

```bash
cd ~/papers/my-thesis
claude --plugin-dir ~/tools/quick-reviewer
```

启动后输入 `/` 可查看所有可用命令。

---

## 使用方式二：命令行工具（CLI）

### 1. 安装

```bash
git clone https://github.com/Triwd/quick-reviewer.git
cd quick-reviewer

# 创建并激活虚拟环境
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows CMD
# .venv\Scripts\Activate.ps1     # Windows PowerShell

# 安装（按需选择）
pip install -e .                 # 基础安装
pip install -e ".[pdf]"          # + PDF 支持
pip install -e ".[docx]"         # + Word 支持
```

> 每次打开新终端需先激活虚拟环境（`source .venv/bin/activate`）。

### 2. 配置 API Key

三种方式任选其一（优先级：命令行参数 > 环境变量 > 配置文件）：

#### 环境变量

<details>
<summary><strong>macOS / Linux</strong></summary>

```bash
# Anthropic（默认）
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# 或 OpenAI 兼容服务
export OPENAI_API_KEY=your-key-here
export QR_PROVIDER=openai
export QR_BASE_URL=https://api.deepseek.com
```

</details>

<details>
<summary><strong>Windows CMD</strong></summary>

```cmd
set ANTHROPIC_API_KEY=sk-ant-your-key-here
:: 或 OpenAI 兼容服务
set OPENAI_API_KEY=your-key-here
set QR_PROVIDER=openai
set QR_BASE_URL=https://api.deepseek.com
```

</details>

<details>
<summary><strong>Windows PowerShell</strong></summary>

```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-your-key-here"
# 或 OpenAI 兼容服务
$env:OPENAI_API_KEY = "your-key-here"
$env:QR_PROVIDER = "openai"
$env:QR_BASE_URL = "https://api.deepseek.com"
```

</details>

#### 配置文件（推荐）

| 级别 | 路径 | 说明 |
|------|------|------|
| 用户级 | `~/.quick-reviewer/config.yaml` | 所有项目生效 |
| 项目级 | `.quick-reviewer.yaml` | 当前项目生效，优先级更高 |

**Anthropic：**

```yaml
provider: anthropic
api_key: sk-ant-your-key-here
```

**OpenAI 兼容服务（DeepSeek、Ollama 等）：**

```yaml
provider: openai
api_key: your-key-here
base_url: https://api.deepseek.com    # 不需要带 /v1 后缀
model: deepseek-chat
```

> `provider` 只支持 `anthropic` 和 `openai` 两个值。所有 OpenAI 兼容服务都填 `openai`，通过 `base_url` 区分。

#### 命令行参数

```bash
quick-reviewer review paper.pdf --api-key your-key --provider openai --base-url https://api.deepseek.com --model deepseek-chat
```

### 3. 运行审查

```bash
quick-reviewer review paper.pdf              # 全面审查
quick-reviewer quick paper.pdf               # 快速预审
quick-reviewer simulate paper.pdf            # 审稿专家模拟
quick-reviewer check grammar paper.pdf       # 语法拼写
quick-reviewer check structure paper.pdf     # 结构审查
quick-reviewer check figures paper.pdf       # 图表审查
quick-reviewer check references paper.pdf    # 参考文献
quick-reviewer check logic paper.pdf         # 逻辑内容
quick-reviewer check ai paper.pdf            # AI 检测
```

支持的文件格式：`.txt`、`.md`、`.pdf`（需安装 pdf 扩展）、`.docx`（需安装 docx 扩展）。

---

## 项目结构

```
quick-reviewer/
├── knowledge/          # 审查知识文档（核心提示词）
├── skills/             # 插件斜杠命令入口
├── cli/                # 命令行工具源码
├── .claude-plugin/     # Claude Code 插件配置
└── pyproject.toml      # Python 项目配置
```

---

## 常见问题

**Q：论文太长怎么办？**
超过 20,000 字会自动分片处理，相邻分片保留约 500 字重叠。

**Q：如何保护论文隐私？**
可使用本地部署的模型（如 Ollama），将 `base_url` 指向本地地址。

**Q：AI 痕迹检测准确吗？**
仅供自查参考，不构成原创性最终判定。
