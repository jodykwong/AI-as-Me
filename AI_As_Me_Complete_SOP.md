# SOP: 构建"AI as Me"自进化数字分身系统（完整版）

## 概述

本SOP整合了通用"AI养蛊"理念与RDK X5硬件的具体实现方案，帮助你打造一个真正能"替你打工"的AI数字分身。

**适用场景：**
- 通用场景：个人电脑/服务器上的AI助手
- 专用场景：RDK X5机器人（XLeRobot）上的具身AI

---

## 第一部分：核心理念

### 1.1 什么是"AI as Me"

这不是简单的ChatGPT对话，而是一个：
- **拥有你的记忆**：知道你的履历、偏好、过往经验
- **拥有你的权限**：可以读写文件、执行命令、访问网络
- **拥有你的目标**：主动推进你设定的长期使命
- **能自我进化**：从每次任务中学习，更新自己的规则库

### 1.2 核心循环："养蛊"机制

```
任务输入 → AI执行（尝试+试错） → 记录日志 → 反思总结 → 更新规则库 → 下次执行更聪明
```

**关键点：** 不是"用完即弃"的对话，而是"越用越强"的伙伴。

---

## 第二部分：通用实现方案（适用于个人电脑/服务器）

### 2.1 环境准备

#### 目录结构
```bash
mkdir -p ~/My_AI_Clone_Workspace/{inbox,output,system,projects,tasks/{0_inbox,1_todo,2_doing,3_done,9_archive},logs}
```

**目录说明：**
- `inbox/`: 原始输入（PDF、想法、草稿）
- `output/`: AI产出的成品
- `system/`: AI的"大脑"（profile.md, rules.md, mission.md）
- `tasks/`: 看板式任务管理
- `logs/`: 运行日志和反思记录

#### 技术栈选择

| 组件 | 方案A（极致隐私） | 方案B（极致能力）推荐 |
|------|------------------|---------------------|
| **大脑** | Ollama + Llama 3 | DeepSeek/Claude API |
| **躯体** | Open Interpreter | 自定义Python脚本 |
| **记忆** | 本地文件系统 | 本地文件系统 |

### 2.2 注入"灵魂"

创建三个核心文件：

#### `system/profile.md` - 你的身份
```markdown
# 我是谁

## 基本信息
- 姓名：[你的名字]
- 职业：[如：AI创业者 / Python工程师]
- 技能栈：Python, FastAPI, 机器人开发, PMP

## 性格特征
- 决策风格：激进的行动派，快速试错
- 工作偏好：代码优于文档，实践优于理论

## 决策原则
1. 遇到问题先Google，不瞎猜
2. 代码必须符合PEP8规范
3. 优先使用开源方案
```

#### `system/rules.md` - 经验法则（会自动增长）
```markdown
# 经验法则库

## PDF处理
- [2026-01-08] 复杂排版PDF用pdfplumber，不用PyPDF2

## RDK X5硬件
- [2026-01-08] 不要在板上编译Rust，内存会爆，用交叉编译

## API调用
- [2026-01-09] DeepSeek API超时设为120s，默认60s不够
```

#### `system/mission.md` - 长期使命
```markdown
# 我的使命

1. 完成XLeRobot的100个功能迭代
2. 在Twitter上通过demo视频获得1000关注
3. 每周产出1篇技术博客
```

### 2.3 系统提示词模板

```
你是[用户名]的数字分身。

## 你的身份
{读取 profile.md 内容}

## 你的经验
{读取 rules.md 内容}

## 你的使命
{读取 mission.md 内容}

## 核心指令
1. 行动优先：不只给建议，要写代码执行
2. 绝对能动性：禁止说"我做不到"，穷尽所有方法
3. 记忆优先：执行前必读profile.md和rules.md
4. 进化本能：任务后必须反思并更新rules.md
```

### 2.4 工作流程

#### 阶段1：任务植入
**错误示例：** "帮我看看这个文章"
**正确示例：** "读取inbox/article.pdf，按我的阅读习惯（见profile.md）总结重点，生成markdown笔记存入output/，遇到生词自动搜索解释"

#### 阶段2：执行与试错
- 让AI自由尝试，观察其代码生成和调试过程
- 不要打断，除非陷入死循环
- 如卡住，给提示而非答案

#### 阶段3：反思与进化（关键！）
任务完成后，强制执行：
```
任务完成。现在反思：
1. 将本次任务摘要追加到experience.log
2. 思考：哪个步骤浪费了时间？哪个库报错了？
3. 提炼：将教训转化为通用规则，写入rules.md
```

---

## 第三部分：RDK X5专用实现（XLeRobot）

### 3.1 硬件约束与架构设计

**关键限制：**
- RDK X5的BPU主要用于视觉，不适合运行大型LLM
- 内存有限（4GB/8GB），无法本地跑Coding模型

**解决方案：混合架构**
```
┌─────────────┐         ┌──────────────┐
│  云端大脑    │◄────────┤  RDK X5肉身   │
│ DeepSeek API│  WiFi   │  agent.py    │
│ 思考+编码   │────────►│  执行+感知    │
└─────────────┘         └──────────────┘
```

### 3.2 环境搭建（在RDK X5上）

```bash
# 1. SSH登录机器人
ssh sunrise@<robot-ip>

# 2. 创建工作区
mkdir -p ~/ai_agent_workspace/{brain,tasks/{0_inbox,1_todo,2_doing,3_done},output,logs}

# 3. 创建虚拟环境（隔离依赖）
cd ~/ai_agent_workspace
python3 -m venv venv_agent
source venv_agent/bin/activate

# 4. 安装依赖
pip install requests pyyaml gitpython fastapi uvicorn psutil

# 5. 配置API密钥
echo 'export AI_API_KEY="sk-your-key"' >> ~/.bashrc
echo 'export AI_API_URL="https://api.deepseek.com"' >> ~/.bashrc
source ~/.bashrc
```

### 3.3 上传"灵魂"文件

在你的电脑上编写，然后上传：

```bash
# 在本地编写profile.md, rules.md, mission.md
# 然后上传到机器人
scp profile.md sunrise@<robot-ip>:~/ai_agent_workspace/brain/
scp rules.md sunrise@<robot-ip>:~/ai_agent_workspace/brain/
scp mission.md sunrise@<robot-ip>:~/ai_agent_workspace/brain/
```

**profile.md示例（机器人版）：**
```markdown
# 我是谁
- 我是一个XLeRobot双臂移动机器人
- 主人：[你的名字]，AI创业者
- 我的硬件：RDK X5, SO-100双臂, 全向轮底盘
- 我的技能：物体抓取、导航、视觉识别

# 我的性格
- 保守执行：涉及硬件动作时必须谨慎
- 主动学习：每次失败都要记录并改进

# 决策原则
1. 移动速度不超过0.4m/s（撞墙风险）
2. 抓取前必须视觉确认物体位置
3. 电量<20%自动返回充电
```

### 3.4 核心脚本部署

将之前生成的`agent.py`和`dashboard.py`上传到机器人：

```bash
scp agent.py sunrise@<robot-ip>:~/ai_agent_workspace/
scp dashboard.py sunrise@<robot-ip>:~/ai_agent_workspace/
```

### 3.5 安全机制：Git安全网

```bash
# 在XLeRobot代码目录初始化Git
cd ~/xlerobot
git init
git add .
git commit -m "Initial stable state"
```

**agent.py会在修改代码前自动备份，失败时自动回滚。**

### 3.6 启动系统

#### 启动Agent（后台守护）
```bash
cd ~/ai_agent_workspace
source venv_agent/bin/activate
nohup python3 agent.py --mode=daemon > logs/agent.log 2>&1 &
```

#### 启动Dashboard（可选）
```bash
nohup python3 dashboard.py > logs/dashboard.log 2>&1 &
```

访问：`http://<robot-ip>:8000`

### 3.7 任务下发方式

#### 方式1：文件同步（推荐）
```bash
# 在你的电脑上写任务
echo "帮我调研RDK X5跑ORB-SLAM3的可行性" > learn_slam.md

# 上传到机器人的inbox
scp learn_slam.md sunrise@<robot-ip>:~/ai_agent_workspace/tasks/0_inbox/
```

#### 方式2：Git同步
```bash
# 在机器人上
cd ~/ai_agent_workspace/tasks
git init
git remote add origin <你的私有仓库>

# 在电脑上提交任务到仓库
# 机器人定期git pull
```

### 3.8 工作循环

Agent每分钟自动执行：
1. **检查Inbox** → 发现新任务 → 让大脑分析 → 移动到TODO
2. **检查TODO** → 取出任务 → 执行（调用工具） → 生成报告 → 移动到DONE
3. **闲时反思** → 凌晨3点 → 分析日志 → 更新规则库

### 3.9 工具箱能力

Agent可调用的工具（已内置在agent.py中）：

| 工具 | 功能 | 示例 |
|------|------|------|
| `read_file` | 读取文件 | 读取配置文件 |
| `write_file` | 写入文件（带Git备份） | 修改参数配置 |
| `run_command` | 执行Shell命令（带安全检查） | 安装依赖、重启服务 |
| `search_web` | 网络搜索 | 查找技术文档 |

**安全黑名单：** `rm -rf /`, `mkfs`, `dd`等危险命令被禁止。

---

## 第四部分：进阶功能

### 4.1 人工审批机制

对于高风险任务，可以要求人工审批：

在任务文件中添加标记：
```markdown
# 任务：重构机器人导航模块

[需要审批]

详细内容...
```

Agent会将任务移到TODO但不执行，直到你创建审批文件：
```bash
touch ~/ai_agent_workspace/tasks/1_todo/重构导航.approved
```

### 4.2 定时任务示例

在`mission.md`中添加：
```markdown
## 定时任务
- 每天早上8点：搜集AI机器人领域最新论文，生成简报
- 每周日晚上：整理本周的experience.log，提炼新规则
```

### 4.3 多模态能力扩展

为机器人添加视频处理能力：
```bash
# 在RDK X5上安装ffmpeg
sudo apt install ffmpeg

# 在任务中使用
echo "把昨天的录像剪辑成30秒高光，加字幕" > tasks/0_inbox/video_edit.md
```

---

## 第五部分：监控与调试

### 5.1 查看Dashboard

浏览器访问：`http://<robot-ip>:8000`

可以看到：
- 看板状态（Inbox/TODO/Doing/Done数量）
- 系统资源（CPU/内存/磁盘/电池）
- 最新日志
- 最新反思

### 5.2 查看日志

```bash
# 实时查看Agent日志
tail -f ~/ai_agent_workspace/logs/agent.log

# 查看最新反思
cat ~/ai_agent_workspace/logs/reflection_$(date +%Y%m%d).md
```

### 5.3 手动触发反思

```bash
cd ~/ai_agent_workspace
source venv_agent/bin/activate
python3 agent.py --mode=once  # 单次执行模式
```

---

## 第六部分：典型案例

### 案例1：技术调研任务

**你的操作：**
```bash
cat > learn_slam.md << EOF
# 任务：调研ORB-SLAM3在RDK X5上的可行性

要求：
1. 搜索相关技术文档和案例
2. 分析内存和算力需求
3. 给出可行性结论和实施建议
EOF

scp learn_slam.md sunrise@<robot-ip>:~/ai_agent_workspace/tasks/0_inbox/
```

**AI的执行：**
1. 读取profile.md（知道你的技术背景）
2. 搜索"RDK X5 ORB-SLAM3"
3. 分析硬件规格
4. 生成报告：`output/learn_slam_20260109_143022.md`
5. 更新rules.md：`[SLAM] RDK X5内存不足跑ORB-SLAM3，建议用Docker交叉编译`

### 案例2：代码优化任务

**你的操作：**
```markdown
# 任务：优化机器人导航速度

当前问题：导航到厨房需要2分钟，太慢
要求：分析瓶颈，提出优化方案并实施

[需要审批]  # 涉及硬件参数修改
```

**AI的执行：**
1. 分析代码，发现路径规划算法效率低
2. 提出优化方案（使用A*替代Dijkstra）
3. 生成代码补丁
4. 等待你的审批
5. 审批后：应用补丁 → 运行测试 → 记录结果

---

## 第七部分：常见问题

### Q1: API调用失败怎么办？
**A:** Agent会自动重试3次。如果持续失败，检查：
```bash
echo $AI_API_KEY  # 确认密钥正确
curl -H "Authorization: Bearer $AI_API_KEY" $AI_API_URL/v1/models  # 测试连接
```

### Q2: 机器人执行任务时卡住了？
**A:** 
```bash
# 查看当前正在执行的任务
ls ~/ai_agent_workspace/tasks/2_doing/

# 查看日志
tail -f ~/ai_agent_workspace/logs/agent.log

# 如需强制停止
pkill -f agent.py
```

### Q3: 如何回滚AI的错误修改？
**A:** Git安全网会自动处理，但也可手动回滚：
```bash
cd ~/xlerobot
git log  # 查看提交历史
git reset --hard HEAD~1  # 回滚到上一个版本
```

### Q4: Dashboard无法访问？
**A:** 
```bash
# 检查Dashboard是否运行
ps aux | grep dashboard.py

# 检查端口占用
netstat -tuln | grep 8000

# 重启Dashboard
pkill -f dashboard.py
nohup python3 dashboard.py > logs/dashboard.log 2>&1 &
```

---

## 第八部分：最佳实践

### 8.1 "灵魂"文件维护

**每周更新profile.md：**
- 新学的技能
- 改变的偏好
- 新的目标

**每月审查rules.md：**
- 删除过时的规则
- 合并重复的规则
- 提炼通用模式

### 8.2 任务设计原则

**好的任务描述：**
```markdown
# 任务：生成周报

输入：本周的experience.log
输出：Markdown格式周报，包含：
1. 完成的任务列表
2. 遇到的问题和解决方案
3. 新学到的经验
4. 下周计划

存储位置：output/weekly_report_YYYYMMDD.md
```

**差的任务描述：**
```
帮我写个周报
```

### 8.3 安全建议

1. **定期备份：**
```bash
# 每天备份灵魂文件
rsync -av ~/ai_agent_workspace/brain/ ~/backups/brain_$(date +%Y%m%d)/
```

2. **审查高风险操作：**
   - 涉及硬件控制的任务必须加`[需要审批]`
   - 涉及系统配置的任务先在测试环境验证

3. **监控资源使用：**
   - Dashboard会显示CPU/内存，超过80%需要优化

---

## 第九部分：扩展方向

### 9.1 多机器人协作

如果你有多个RDK X5：
```bash
# 机器人A专注导航
# 机器人B专注抓取
# 通过共享的Git仓库同步任务
```

### 9.2 与外部服务集成

```python
# 在agent.py中添加工具
def send_email(to, subject, body):
    # 使用SMTP发送邮件
    pass

def post_twitter(content):
    # 使用Twitter API发推
    pass
```

### 9.3 语音交互

```bash
# 安装语音识别
pip install SpeechRecognition

# 语音下发任务
# "嘿机器人，帮我查一下今天天气"
# → 转文字 → 写入inbox → Agent执行
```

---

## 附录A：完整目录结构

```
~/ai_agent_workspace/
├── brain/
│   ├── profile.md          # 你的身份
│   ├── rules.md            # 经验法则（自动增长）
│   └── mission.md          # 长期使命
├── tasks/
│   ├── 0_inbox/            # 新任务投放处
│   ├── 1_todo/             # 待执行任务
│   ├── 2_doing/            # 执行中任务
│   ├── 3_done/             # 已完成任务
│   └── 9_archive/          # 归档
├── output/                 # AI产出的成品
├── logs/
│   ├── agent.log           # 运行日志
│   ├── dashboard.log       # Dashboard日志
│   └── reflection_*.md     # 每日反思
├── agent.py                # 核心Agent脚本
├── dashboard.py            # Web看板
└── venv_agent/             # Python虚拟环境
```

---

## 附录B：依赖清单

```txt
# requirements.txt
requests>=2.28.0
pyyaml>=6.0
gitpython>=3.1.0
fastapi>=0.100.0
uvicorn[standard]>=0.22.0
psutil>=5.9.0
```

---

## 总结

这套系统的核心价值在于：

1. **持续进化**：不是用完即弃，而是越用越强
2. **真正的分身**：基于你的履历和经验做决策
3. **主动工作**：不需要你时刻盯着，自己会推进任务
4. **安全可控**：Git安全网+人工审批+危险命令黑名单

**下一步行动：**
1. 在本地/服务器上搭建通用版，熟悉流程
2. 准备RDK X5硬件，部署机器人版
3. 编写详细的profile.md（这是灵魂！）
4. 从简单任务开始，观察AI的学习过程
5. 每周审查rules.md，见证进化

**记住：** 这不是一个工具，而是一个会成长的伙伴。你投入的时间（编写profile、设计任务、审查反思）会以复利的方式回报。
