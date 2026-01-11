# SOP: 打造 RDK X5 版 "AI as Me" (XLeRobot 专用) - 高能动性版

本 SOP 专为 **RDK X5 (Horizon Sunrise 5)** 硬件及 **Ubuntu Server (无界面)** 环境设计。
**核心目标**：不仅仅做一个“维保机器人”，而是打造一个**拥有你的人格、甚至能替你打工**的数字分身。

> **架构升级 (Architecture V2.0)**:
> *   **灵魂 (Soul)**: 注入你的简历、价值观、思维方式，让 AI 的决策像你。
> *   **大脑 (Brain)**: 云端高智商模型 (DeepSeek/Claude 3.5 Sonnet)，负责复杂规划与代码生成。
> *   **肉身 (Body)**: RDK X5，作为执行终端，负责跑代码、控制硬件、托管看板。
> *   **手脚 (Hands)**: 赋予其互联网访问、文件读写、系统控制权限。

## 1. 注入灵魂 (Soul Injection)

要让 AI 成为“你”，必须先喂给它你的背景。

### 1.1 建立知识库
在 `~/ai_agent_workspace/brain/` 目录下创建以下文件：

*   **`profile.md` (履历与人格)**:
    > *   **我是谁**: 你的详细简历、技能栈（Python专家/产品经理）、创业目标。
    > *   **性格**: "激进的行动派" 或 "保守的完美主义者"。
    > *   **决策偏好**: "遇到问题优先查 Google，而不是瞎猜"、"代码风格要求 PEP8"。
*   **`rules.md` (经验法则)**:
    > *   这是“养蛊”的核心。记录你过去的失败教训。
    > *   *例*: "不要在 RDK X5 上尝试编译 Rust 项目，内存会爆，直接下预编译包。"
*   **`mission.md` (长期使命)**:
    > *   *例*: "协助我完成 XLeRobot 的 100 个功能迭代，并在 Twitter 上通过 demo 视频获得 1000 关注。"

### 1.2 系统提示词 (System Prompt)
在 `agent.py` 启动时，必须加载以上内容：
> "你不是一个通用的助手，你是 [User Name] 的数字分身。你拥有我的履历 (`profile.md`) 和经验 (`rules.md`)。你的任务是主动推进 `mission.md`。遇到困难时，问自己：‘如果是本体在这里，他会怎么做？’"

## 2. 任务管理看板 (Task Management - The Kanban)

为了解决“无界面”且“任务不可见”的问题，我们采用 **文件级看板 (File-based Kanban)** + **轻量级 Web 仪表盘**。

### 2.1 目录级看板
在 `~/ai_agent_workspace/tasks/` 下建立三个文件夹：

```bash
mkdir -p ~/ai_agent_workspace/tasks/{0_inbox,1_todo,2_doing,3_done,9_archive}
```

*   **用法**:
    *   **下达命令**: 你只需在手机/电脑上写一个 `idea.md`，通过 SCP/Git 同步丢进 `0_inbox`。
    *   **AI 接单**: Agent 监控 `0_inbox`，读取文件，结合 `profile.md` 拆解步骤，移动到 `1_todo`。
    *   **执行中**: Agent 取出 `todo` 里的任务，移动到 `2_doing` 并开始跑代码。
    *   **完成**: 产出物（代码/视频/报告）放入 `output/`，任务卡片移入 `3_done` 并附上 `result_summary.md`。

### 2.2 极简 Web 看板 (Dashboard)
让 Agent 写一个简单的 Flask/FastAPI 服务，运行在 Robot 上，让你能通过浏览器查看。

*   **访问**: `http://<robot-ip>:8000`
*   **功能**:
    *   显示当前 `doing` 的任务。
    *   显示 CPU/内存 / 电池状态。
    *   显示 `experience.log` 的最新反思。

## 3. 能动性与工具箱 (Proactive Agency)

AI 不应只是在晚上反思，它应该**主动工作**。

### 3.1 核心循环 (The Work Loop)
`agent.py` 的主循环逻辑（不再只是 CronJob）：

```python
while True:
    # 1. 检查有没有加急任务 (Inbox)
    if inbox_has_files():
        task = parse_task()
        plan = brain.think(task, context=profile)
        move_to_todo(task, plan)

    # 2. 检查是否有积压任务 (Todo)
    elif todo_has_files() and not is_busy():
        task = pick_top_task()
        move_to_doing(task)
        execute_task(task) # 这里调用工具箱

    # 3. 闲时进化 (Reflection)
    elif is_charging() and is_night():
        self_reflect()
    
    time.sleep(60)
```

### 3.2 扩展工具箱 (Tools)
赋予 AI 更多权限，让它能真正“干活”：

1.  **Coding 能力**:
    *   工具: `edit_file`, `run_command`
    *   场景: "帮我给 XLeRobot 增加一个语音播报 IP 地址的 Python 脚本。"
2.  **互联网能力**:
    *   工具: `search_web`, `curl`
    *   场景: "每天早上搜集 AI 机器人领域的最新 arXiv 论文，总结成简报发到 `3_done`。"
3.  **多媒体能力**:
    *   工具: `ffmpeg`
    *   场景: "把昨天机器人视角的录像剪辑成 30 秒的高光时刻，配上字幕。"

## 4. 实施步骤

1.  **环境配置**:
    同 V1.0，安装 Python 依赖，但增加 web 框架: `pip install fastapi uvicorn`.
2.  **上传你的“灵魂”**:
    写好 `profile.md` (越详细越好)，`scp` 到机器人的 `~/ai_agent_workspace/brain/`。
3.  **部署看板**:
    让 AI (或者你自己) 写一个 `dashboard.py`，读取 `tasks/` 文件夹状态并渲染 HTML。
4.  **启动分身**:
    `nohup python3 agent.py > agent.log 2>&1 &`

## 5. 预期效果

*   **你**: 往 `inbox` 丢一个 "learn_slam.md" (内容: "帮我调研一下 RDK X5 跑 ORB-SLAM3 的可行性")。
*   **AI (分身)**:
    1.  发现任务，读取你的技术栈配置。
    2.  主动上网搜索 Horizon 论坛和 Github。
    3.  尝试下载编译（如果失败，记录 Error 到 `rules.md`）。
    4.  最终在 `3_done` 生成一份 `feasibility_report.md`，告诉你“内存不够，建议用 Docker 交叉编译”。
    5.  你通过 Dashboard 看到任务变绿（完成）。

这就是真正的 **AI as Me**：它在用你的逻辑、你的工具，并在帮你“踩坑”的过程中不断变强。
