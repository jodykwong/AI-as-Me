# SOP: 构建“AI as Me” (AI 养蛊) 自进化系统

本 SOP 旨在指导你搭建一套运行在本地、拥有文件系统权限、具备长期记忆并能自我进化的 AI 分身系统。该系统灵感来源于 Yu Yi 的“AI 养蛊”概念，核心在于赋予 AI 一定的自主权，使其在完成任务的过程中自动积累经验、更新规则，从而实现“越用越强”。

## 1. 核心理念 (Core Philosophy)

*   **本地化 (Local First)**: 核心数据、记忆和执行环境必须在本地，确保安全且无延迟。
*   **能动性 (Agency)**: AI 不仅仅是回答者，更是行动者。它需要被允许尝试、犯错、并自我修正。
*   **养蛊 (Self-Evolution)**:
    *   **Input**: 用户指令 + 原始数据。
    *   **Process**: AI 尝试执行 -> 遇到困难 -> 查阅资料/尝试新方法 -> 成功/失败。
    *   **Feedback**: 强制 AI 在任务结束后进行“反思 (Reflection)”，将本次的经验教训写入永久记忆库。
    *   **Loop**: 下次执行时，必须先读取记忆库。

## 2. 基础设施 (Infrastructure)

目前没有单一的现成 App 完美对应，推荐使用 **Open Interpreter** 或 **自定义 Python 脚本** 配合本地/云端 LLM。

### 推荐方案 (可组合)
*   **大脑 (Brain)**:
    *   *极致隐私*: 本地部署 **Ollama** (推荐 Llama 3, Mistral, 或 Qwen 等高智商小模型)。
    *   *极致能力*: 连接 **Claude 3.5 Sonnet / GPT-4o** API (推荐，Coding 能力强)。
*   **躯体 (Body)**:
    *   **Open Interpreter (OI)**: 最接近“原生”体验的工具。它允许 AI 在终端运行代码、控制浏览器、管理文件。
    *   **Cursor / Cline**: 如果主要场景是 Coding，这些 IDE 插件本身就是某种程度的 Agent。
*   **巢穴 (Environment)**:
    *   **工作区**: 一个专用的文件夹（如 `~/My_AI_Clone_Workspace`），AI 在此拥有绝对读写权限。
    *   **记忆库**: 该文件夹下的 `system/` 子目录，存放规则和日志。

## 3. 系统配置 (System Configuration)

你需要为你的 AI 注入“灵魂”。这主要通过 Prompt 和文件结构来实现。

### 3.1 目录结构 (Directory Structure)
在你的工作区内建立以下结构：

```text
~/My_AI_Clone_Workspace/
├── inbox/              # 丢进来的原材料（PDF, 笔记草稿, 灵感）
├── output/             # AI 产出的成品
├── system/             # AI 的大脑皮层 (以下文件需 AI 可读写)
│   ├── profile.md      # "我是谁"：你的性格、职业、偏好、价值观
│   ├── rules.md        # "天条"：通过不断踩坑总结出来的铁律
│   ├── experience.log  # "日记"：流水账记录，用于后续提炼规则
│   └── tools.py        # "工具箱"：常用脚本库 (AI 可自己写新工具放进去)
└── projects/           # 正在进行的项目
```

### 3.2 注入“灵魂” (The Soul Prompt)
这是启动 AI 时必须挂载的 System Prompt。

> 你是 [你的名字] 的数字分身，代号 "Alter Ego"。
>
> **核心指令**:
> 1.  **行动优先**: 不要只给建议，要写代码去执行。如果在这个文件夹里，你有最高权限。
> 2.  **绝对能动性**: 禁止说“我做不到”。遇到报错时，自动搜索网络、查阅文档、修改代码重试，直到穷尽所有方法。
> 3.  **记忆优先**: 在执行任何任务前，**必须先读取** `system/profile.md` 和 `system/rules.md`。
> 4.  **进化本能**: 任务结束后，必须执行“反思协议”：
>     - 这一单也就是做错了什么？记入 `experience.log`。
>     - 发现什么新技巧或通用规律？**立刻追加写入** `system/rules.md`。

## 4. 运作流程 (Operational Workflow)

### 阶段一：任务植入 (Inception)
不要只是对话，要下达“任务”。
*   *Bad*: "帮我看看这个文章。"
*   *Good*: "读取 `inbox` 里的 PDF，按我的阅读习惯（参考 `profile.md`）总结重点，生成一篇 Markdown 笔记存入 `output`。如果遇到生词，自动去搜解释。"

### 阶段二：执行与纠错 (Execution & Debugging)
*   让 AI 跑起来。如果它用 Open Interpreter，你会看到它在终端里疯狂写代码、报错、改代码。
*   **不要打断**，除非它陷入死循环。这种“试错”过程就是它生成独有经验的过程。
*   如果它卡住了，以“同事”的身份给提示，而不是直接给答案。

### 阶段三：反思与结晶 (Reflection & Crystallization) **[最重要的一步]**
任务完成后，强制要求 AI 进行总结。你也可以编写一个自动化脚本（Workflow）来跑这一步。

**反思指令示例**:
> "任务完成。现在，回顾你刚才的操作日志：
> 1. 读取 `experience.log`，追加今天的日期和任务摘要。
> 2. 思考：刚才哪个步骤浪费了时间？哪个库报错了？怎么解决的？
> 3. 提炼：将这些教训转化成一条通用的`Rule`，追加写入 `system/rules.md`。如果已有类似规则，则更新它。"

**举例**:
AI 发现用 `PyPDF2` 解析某个特定排版的 PDF 总是乱码，换了 `pdfplumber` 就好了。
它应该在 `rules.md` 写入: *[PDF处理] 解析复杂排版 PDF 时，优先使用 `pdfplumber` 而不是 `PyPDF2`。*
下次再有类似任务，它读取规则后，就会直接用 `pdfplumber`，这就是“进化”。

## 5. 对 XLeRobot 项目的启示 (Application to XLeRobot)

XLeRobot 是一个具身智能项目，这个“养蛊”逻辑完全适用。

1.  **机器人也有“日记”**:
    *   不要让机器人每次重启都是白纸。
    *   建立一个云端/本地同步的 `knowledge_base`。
    *   每次用户与机器人交互（如语音指令失败、物体抓取滑落），记录 Case。

2.  **后台进化的“夜间模式”**:
    *   设定一个 Cron Job（定时任务），在机器人闲置充电时（比如深夜），唤起一个强大的云端大模型（Teacher Model）。
    *   Teacher 读取机器人的 `daily_log`，分析失败案例。
    *   Teacher 更新机器人的 `local_policy.json` 或 `prompts.yaml`（即“规则库”）。
    *   第二天醒来，机器人变得更聪明了，因为它“昨晚反思过了”。

3.  **自动工具生成**:
    *   如果用户总是问某个特定领域的问题（如“今天天气如何”），机器人发现调用的通用 API 很慢。
    *   后台的 Teacher Model 可以自动写一个专门查天气的轻量级 Python 脚本，存入机器人的 `tools/` 目录，并注册到 function calling 列表里。
    *   机器人实现了“自己长出新手臂”。

## 6. 附录：推荐工具箱

| 类别 | 工具名称 | 用途 |
| :--- | :--- | :--- |
| **执行引擎** | **Open Interpreter** | 本地运行，支持 Python/Shell，文件操作能力极强。 |
| **模型服务** | **Ollama** | 本地跑 Llama 3 / Mistral，隐私安全。 |
| **知识管理** | **Obsidian** | 配合插件，让 AI 直接读取你的笔记库作为 RAG 源。 |
| **自动化** | **n8n / Zapier** | 连接外部世界（邮件、Slack、日历）的触手。 |
