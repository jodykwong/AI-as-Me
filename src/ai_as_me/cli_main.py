"""AI-as-Me CLI入口点"""
import click
import sys
import subprocess
from pathlib import Path
import os
from ai_as_me import __version__


@click.group()
@click.version_option(version=__version__, prog_name="ai-as-me")
def cli():
    """AI-as-Me: 自进化AI数字分身系统"""
    pass


# Story 6.1: Web 服务启动命令
@cli.command()
@click.option('--port', default=8080, help='Web 服务端口')
@click.option('--host', default='127.0.0.1', help='绑定地址')
def serve(port: int, host: str):
    """启动 Web 仪表板"""
    click.echo(f"🚀 启动 AI-as-Me Web 仪表板...")
    click.echo(f"📍 访问地址: http://{host}:{port}")
    click.echo(f"⏹️  按 Ctrl+C 停止服务\n")
    
    try:
        import uvicorn
        from ai_as_me.kanban.api import app
        
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info"
        )
    except KeyboardInterrupt:
        click.echo("\n✅ 服务已停止")
    except Exception as e:
        click.echo(f"❌ 启动失败: {e}", err=True)
        sys.exit(1)


@cli.command()
def version():
    """显示版本信息"""
    click.echo(f"ai-as-me version {__version__}")


@cli.group()
def soul():
    """Soul 管理命令"""
    pass


@soul.command()
def status():
    """检查 Soul 状态"""
    from ai_as_me.soul.loader import SoulLoader
    loader = SoulLoader(Path("soul"))
    status = loader.check_status()
    
    click.echo("📊 Soul Status:")
    click.echo(f"  Profile: {'✓' if status['profile'] else '✗'}")
    click.echo(f"  Rules: {'✓' if status['rules'] else '✗'}")
    click.echo(f"  Mission: {'✓' if status['mission'] else '✗'}")
    
    # v3.0: 检查规则目录
    rules_dir = Path("soul/rules")
    if rules_dir.exists():
        core_count = len(list((rules_dir / "core").glob("*.md")))
        learned_count = len(list((rules_dir / "learned").glob("*.md")))
        click.echo(f"\n📚 Rules Structure (v3.0):")
        click.echo(f"  Core rules: {core_count}")
        click.echo(f"  Learned rules: {learned_count}")


@soul.command()
def migrate():
    """迁移 Soul 到 v3.0 结构"""
    from ai_as_me.soul.migrator import SoulMigrator
    migrator = SoulMigrator(Path("soul"))
    migrator.migrate()
    click.echo("✓ Migration complete")


@cli.command()
def check_env():
    """检查运行环境依赖"""
    click.echo("🔍 检查运行环境依赖...\n")
    
    all_passed = True
    
    # 检查Python版本
    py_version = sys.version_info
    if py_version >= (3, 9):
        click.echo(f"✅ Python {py_version.major}.{py_version.minor}.{py_version.micro} (>= 3.9)")
    else:
        click.echo(f"❌ Python {py_version.major}.{py_version.minor}.{py_version.micro} (需要 >= 3.9)")
        all_passed = False
    
    # 检查Node.js
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            node_version = result.stdout.strip()
            version_num = int(node_version.lstrip('v').split('.')[0])
            if version_num >= 16:
                click.echo(f"✅ Node.js {node_version} (>= 16)")
            else:
                click.echo(f"❌ Node.js {node_version} (需要 >= 16)")
                all_passed = False
        else:
            click.echo("❌ Node.js 未安装")
            all_passed = False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        click.echo("❌ Node.js 未安装")
        click.echo("   安装指导: https://nodejs.org/")
        all_passed = False
    
    # 检查npx
    try:
        result = subprocess.run(
            ["npx", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            npx_version = result.stdout.strip()
            click.echo(f"✅ npx {npx_version}")
        else:
            click.echo("❌ npx 不可用")
            all_passed = False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        click.echo("❌ npx 不可用 (通常随Node.js安装)")
        all_passed = False
    
    click.echo()
    if all_passed:
        click.echo("✅ 所有依赖检查通过！")
    else:
        click.echo("❌ 部分依赖检查失败，请安装缺失的依赖")
        sys.exit(1)


@cli.command()
@click.option('--force', is_flag=True, help='强制重新初始化，覆盖已存在的目录')
def init(force):
    """初始化AI-as-Me配置和目录结构"""
    click.echo("🚀 初始化 AI-as-Me 系统...\n")
    
    # 定义目录结构
    dirs = ['soul', 'kanban', 'logs']
    cwd = Path.cwd()
    
    created = []
    skipped = []
    
    # 创建目录
    for dir_name in dirs:
        dir_path = cwd / dir_name
        if dir_path.exists() and not force:
            click.echo(f"⏭️  {dir_name}/ 已存在，跳过")
            skipped.append(dir_name)
        else:
            dir_path.mkdir(mode=0o700, exist_ok=True)
            click.echo(f"✅ 创建 {dir_name}/ (权限: 700)")
            created.append(dir_name)
    
    # 创建.env模板
    env_file = cwd / '.env'
    if env_file.exists() and not force:
        click.echo(f"⏭️  .env 已存在，跳过")
        skipped.append('.env')
    else:
        env_template = """# AI-as-Me 环境配置
# 生成时间: 自动生成

# API密钥配置 (根据需要配置)
# ANTHROPIC_API_KEY=your_api_key_here
# OPENAI_API_KEY=your_api_key_here

# Agent CLI 工具配置
CLAUDE_CODE_VERSION=2.0.76
OPENCODE_VERSION=1.1.3

# 系统配置
LOG_LEVEL=INFO
"""
        env_file.write_text(env_template)
        os.chmod(env_file, 0o600)
        click.echo(f"✅ 创建 .env (权限: 600)")
        created.append('.env')
    
    click.echo()
    if created:
        click.echo(f"✅ 初始化完成！创建了 {len(created)} 个项目")
    if skipped:
        click.echo(f"ℹ️  跳过了 {len(skipped)} 个已存在的项目")
    
    click.echo("\n📝 下一步:")
    click.echo("  1. 编辑 .env 文件配置API密钥")
    click.echo("  2. 运行 'ai-as-me check-tools' 检查工具可用性")


@cli.group()
def soul():
    """Soul个性化管理命令"""
    pass


@soul.command()
@click.option('--force', is_flag=True, help='强制重新初始化，覆盖已存在的文件')
def init(force):
    """初始化Soul档案文件"""
    import os
    
    soul_dir = Path.cwd() / "soul"
    if not soul_dir.exists():
        click.echo("❌ soul/ 目录不存在，请先运行 'ai-as-me init'")
        return
    
    profile_file = soul_dir / "profile.md"
    rules_file = soul_dir / "rules.md"
    
    created = []
    skipped = []
    
    # 创建profile.md
    if profile_file.exists() and not force:
        click.echo("⏭️  soul/profile.md 已存在，跳过")
        skipped.append('profile.md')
    else:
        profile_template = """# Soul Profile - 个人档案

## 基本信息
- **姓名**: [你的名字或昵称]
- **角色**: [例如: 技术型独立AI创业者]
- **技术背景**: [你的技术栈和经验]

## 编程风格
- **偏好语言**: [Python, JavaScript, etc.]
- **代码风格**: [简洁/详细, 注释风格等]
- **架构偏好**: [微服务/单体, 函数式/面向对象等]

## 工作偏好
- **沟通风格**: [直接/委婉, 技术细节程度等]
- **文档偏好**: [详细文档/代码注释, Markdown格式等]
- **测试态度**: [TDD, 单元测试覆盖率要求等]

## 个人约束
- **时间限制**: [快速原型/生产级质量]
- **技术限制**: [避免使用的技术或框架]
- **其他偏好**: [任何其他重要的个人偏好]
"""
        profile_file.write_text(profile_template)
        os.chmod(profile_file, 0o600)
        click.echo("✅ 创建 soul/profile.md (权限: 600)")
        created.append('profile.md')
    
    # 创建rules.md
    if rules_file.exists() and not force:
        click.echo("⏭️  soul/rules.md 已存在，跳过")
        skipped.append('rules.md')
    else:
        rules_template = """# Soul Rules - 工作规则

## 代码规则
- 使用Python 3.9+特性
- 遵循PEP 8代码规范
- 函数和类必须有docstring
- 变量命名使用有意义的英文

## 项目规则
- 使用Git进行版本控制
- 提交信息使用中文，格式: [类型] 简短描述
- 每个功能一个分支

## 质量规则
- 代码必须通过类型检查
- 关键功能必须有单元测试
- 性能敏感代码需要基准测试

## 禁止规则
- 不使用全局变量
- 不硬编码敏感信息
- 不提交未测试的代码

## 学习规则
- 记录遇到的问题和解决方案
- 总结每次任务的经验教训
- 持续优化和改进工作流程
"""
        rules_file.write_text(rules_template)
        os.chmod(rules_file, 0o600)
        click.echo("✅ 创建 soul/rules.md (权限: 600)")
        created.append('rules.md')
    
    click.echo()
    if created:
        click.echo(f"✅ Soul初始化完成！创建了 {len(created)} 个文件")
    if skipped:
        click.echo(f"ℹ️  跳过了 {len(skipped)} 个已存在的文件")
    
    click.echo("\n📝 下一步:")
    click.echo("  1. 编辑 soul/profile.md 填写个人信息")
    click.echo("  2. 编辑 soul/rules.md 定义工作规则")
    click.echo("  3. 使用 'ai-as-me task start' 时自动应用Soul")


@soul.command()
@click.option('--output', '-o', default='soul_backup.tar.gz', help='备份文件名')
def backup(output):
    """备份Soul数据"""
    import tarfile
    import os
    
    soul_dir = Path.cwd() / "soul"
    if not soul_dir.exists():
        click.echo("❌ soul/ 目录不存在")
        return
    
    output_path = Path.cwd() / output
    
    try:
        with tarfile.open(output_path, 'w:gz') as tar:
            tar.add(soul_dir, arcname='soul')
        
        os.chmod(output_path, 0o600)
        click.echo(f"✅ Soul数据已备份到: {output}")
        click.echo(f"   文件大小: {output_path.stat().st_size} bytes")
        click.echo(f"   权限: 600")
    except Exception as e:
        click.echo(f"❌ 备份失败: {str(e)}")


@soul.command()
@click.argument('backup_file')
@click.option('--force', is_flag=True, help='强制恢复，覆盖现有文件')
def restore(backup_file, force):
    """从备份恢复Soul数据"""
    import tarfile
    import os
    
    backup_path = Path(backup_file)
    if not backup_path.exists():
        click.echo(f"❌ 备份文件不存在: {backup_file}")
        return
    
    soul_dir = Path.cwd() / "soul"
    if soul_dir.exists() and not force:
        click.echo("⚠️  soul/ 目录已存在")
        click.echo("   使用 --force 选项强制恢复")
        return
    
    try:
        with tarfile.open(backup_path, 'r:gz') as tar:
            tar.extractall(Path.cwd())
        
        # 恢复文件权限
        for file in soul_dir.glob('*.md'):
            os.chmod(file, 0o600)
        
        click.echo(f"✅ Soul数据已恢复")
        click.echo(f"   文件权限已设置为 600")
    except Exception as e:
        click.echo(f"❌ 恢复失败: {str(e)}")


@soul.command()
def check():
    """检查Soul文件权限和安全性"""
    import os
    import stat
    
    soul_dir = Path.cwd() / "soul"
    if not soul_dir.exists():
        click.echo("❌ soul/ 目录不存在")
        return
    
    click.echo("🔒 检查Soul安全性...\n")
    
    issues = []
    
    # 检查目录权限
    dir_mode = oct(soul_dir.stat().st_mode)[-3:]
    if dir_mode != '700':
        issues.append(f"soul/ 目录权限为 {dir_mode}，建议 700")
    else:
        click.echo(f"✅ soul/ 目录权限: {dir_mode}")
    
    # 检查文件权限
    for file in soul_dir.glob('*.md'):
        file_mode = oct(file.stat().st_mode)[-3:]
        if file_mode != '600':
            issues.append(f"{file.name} 权限为 {file_mode}，建议 600")
        else:
            click.echo(f"✅ {file.name} 权限: {file_mode}")
    
    # 检查.env文件
    env_file = Path.cwd() / ".env"
    if env_file.exists():
        env_mode = oct(env_file.stat().st_mode)[-3:]
        if env_mode != '600':
            issues.append(f".env 权限为 {env_mode}，建议 600")
        else:
            click.echo(f"✅ .env 权限: {env_mode}")
    
    click.echo()
    if issues:
        click.echo("⚠️  发现安全问题:")
        for issue in issues:
            click.echo(f"   - {issue}")
    else:
        click.echo("✅ 所有安全检查通过！")


@cli.command()
def reflect():
    """分析执行历史并生成反思报告"""
    from ai_as_me.yangu import ExecutionHistory
    
    history = ExecutionHistory()
    all_records = history.get_history()
    
    if not all_records:
        click.echo("📊 暂无执行历史")
        return
    
    click.echo("🤔 分析执行历史...\n")
    
    # 分析高分和低分任务
    high_rated = history.get_rated_tasks(min_rating=4)
    low_rated = history.get_rated_tasks(max_rating=2)
    
    click.echo(f"📈 执行统计:")
    click.echo(f"   总任务数: {len(all_records)}")
    click.echo(f"   高分任务 (4-5分): {len(high_rated)}")
    click.echo(f"   低分任务 (1-2分): {len(low_rated)}")
    
    if high_rated:
        click.echo(f"\n✅ 成功模式:")
        tools = {}
        for r in high_rated:
            tool = r.get('tool', 'unknown')
            tools[tool] = tools.get(tool, 0) + 1
        for tool, count in tools.items():
            click.echo(f"   - {tool}: {count}次成功")
    
    if low_rated:
        click.echo(f"\n❌ 需要改进:")
        for r in low_rated[:3]:
            click.echo(f"   - 任务 {r['task_id']}: {r.get('feedback', '无反馈')}")
    
    # 生成简单报告
    report_file = Path.cwd() / "logs" / f"reflection_{datetime.now().strftime('%Y%m%d')}.md"
    report_content = f"""# 反思报告

**生成时间**: {datetime.now().isoformat()}

## 执行统计
- 总任务数: {len(all_records)}
- 高分任务: {len(high_rated)}
- 低分任务: {len(low_rated)}

## 成功模式
{chr(10).join([f'- {tool}: {count}次' for tool, count in tools.items()]) if high_rated else '暂无数据'}

## 改进建议
- 继续使用高分工具
- 优化低分任务的提示词
"""
    report_file.write_text(report_content)
    click.echo(f"\n📄 报告已保存: {report_file}")


@cli.command()
def stats():
    """显示学习效果统计"""
    from ai_as_me.yangu import ExecutionHistory
    
    history = ExecutionHistory()
    all_records = history.get_history()
    
    if not all_records:
        click.echo("📊 暂无统计数据")
        return
    
    click.echo("📊 学习效果统计\n")
    
    # 计算评分趋势
    rated = [r for r in all_records if r.get('rating')]
    if rated:
        avg_rating = sum(r['rating'] for r in rated) / len(rated)
        click.echo(f"平均评分: {avg_rating:.1f}/5.0")
        
        # 简单趋势
        if len(rated) >= 2:
            first_half = rated[:len(rated)//2]
            second_half = rated[len(rated)//2:]
            avg_first = sum(r['rating'] for r in first_half) / len(first_half)
            avg_second = sum(r['rating'] for r in second_half) / len(second_half)
            improvement = ((avg_second - avg_first) / avg_first) * 100
            
            if improvement > 0:
                click.echo(f"满意度提升: +{improvement:.1f}%")
            else:
                click.echo(f"满意度变化: {improvement:.1f}%")
    
    # 工具使用统计
    tools = {}
    for r in all_records:
        tool = r.get('tool', 'unknown')
        tools[tool] = tools.get(tool, 0) + 1
    
    click.echo(f"\n工具使用:")
    for tool, count in tools.items():
        click.echo(f"   {tool}: {count}次")
    
    click.echo(f"\n✅ 系统已执行 {len(all_records)} 个任务")


@cli.group()
def task():
    """任务管理命令"""
    pass


@task.command()
@click.argument('description')
def add(description):
    """添加新任务"""
    from ai_as_me.kanban import TaskManager
    
    tm = TaskManager()
    task = tm.add_task(description)
    
    click.echo(f"✅ 任务已创建")
    click.echo(f"   ID: {task['id']}")
    click.echo(f"   描述: {task['description']}")
    click.echo(f"   状态: {task['status']}")


@task.command()
@click.option('--status', help='按状态过滤 (todo/doing/done)')
def list(status):
    """列出所有任务"""
    from ai_as_me.kanban import TaskManager
    
    tm = TaskManager()
    tasks = tm.list_tasks(status)
    
    if not tasks:
        click.echo("📋 暂无任务")
        return
    
    click.echo(f"📋 任务列表 ({len(tasks)} 个任务)\n")
    for t in tasks:
        status_icon = {"todo": "⏳", "doing": "🔄", "done": "✅", "failed": "❌"}.get(t["status"], "❓")
        click.echo(f"{status_icon} [{t['id']}] {t['description']}")
        click.echo(f"   状态: {t['status']} | 创建: {t['created_at'][:19]}")
        click.echo()


@task.command()
@click.argument('task_id')
@click.option('--tool', default='claude-code', help='使用的工具 (claude-code/opencode)')
@click.option('--fallback/--no-fallback', default=True, help='失败时自动切换备用工具')
@click.option('--no-soul', is_flag=True, help='不使用Soul注入')
def start(task_id, tool, fallback, no_soul):
    """开始执行任务"""
    from ai_as_me.kanban import TaskManager
    from ai_as_me.orchestrator import AgentCLI
    from pathlib import Path
    
    tm = TaskManager()
    task = tm.get_task(task_id)
    
    if not task:
        click.echo(f"❌ 任务不存在: {task_id}")
        return
    
    if task['status'] != 'todo':
        click.echo(f"⚠️  任务状态为 {task['status']}，只能执行 todo 状态的任务")
        return
    
    # 更新状态为doing
    tm.update_task_status(task_id, 'doing')
    click.echo(f"🔄 开始执行任务 [{task_id}]")
    click.echo(f"   描述: {task['description']}")
    click.echo(f"   工具: {tool}")
    if fallback:
        click.echo(f"   备用: 启用自动切换")
    if not no_soul:
        click.echo(f"   Soul: 启用个性化注入")
    click.echo()
    
    # 调用Agent CLI
    agent = AgentCLI()
    click.echo("⏳ 调用 Agent CLI...")
    
    use_soul = not no_soul
    
    if fallback:
        # 使用备用机制
        tools = [tool, 'opencode' if tool == 'claude-code' else 'claude-code']
        result = agent.call_with_fallback(task['description'], tools, timeout=10, use_soul=use_soul)
        
        if 'attempts' in result and len(result['attempts']) > 1:
            click.echo(f"\n🔄 已尝试 {len(result['attempts'])} 个工具:")
            for attempt in result['attempts']:
                status = "✅" if attempt['success'] else "❌"
                click.echo(f"   {status} {attempt['tool']}")
    else:
        result = agent.call(tool, task['description'], timeout=10, use_soul=use_soul)
    
    # 保存结果
    results_dir = Path.cwd() / "kanban" / "results"
    results_dir.mkdir(exist_ok=True)
    result_file = results_dir / f"{task_id}.md"
    
    result_content = f"""# 任务执行结果

**任务ID**: {task_id}
**描述**: {task['description']}
**工具**: {result.get('tool', tool)}
**Soul注入**: {'是' if use_soul else '否'}
**状态**: {'成功' if result['success'] else '失败'}

## 输出

```
{result['output'] or '无输出'}
```

## 错误信息

```
{result['error'] or '无错误'}
```
"""
    result_file.write_text(result_content)
    
    # 更新最终状态
    final_status = 'done' if result['success'] else 'failed'
    tm.update_task_status(task_id, final_status)
    
    if result['success']:
        click.echo(f"\n✅ 任务完成！")
    else:
        click.echo(f"\n❌ 任务失败: {result['error'][:100]}")
        click.echo(f"\n💡 建议:")
        click.echo(f"   1. 检查网络连接")
        click.echo(f"   2. 运行 'ai-as-me check-tools' 验证工具")
        click.echo(f"   3. 查看日志: logs/agent_calls.log")
    
    click.echo(f"\n📄 结果已保存: kanban/results/{task_id}.md")
    
    # 收集用户反馈
    click.echo("\n📊 请对任务执行结果评分:")
    rating = click.prompt("   评分 (1-5分，回车跳过)", type=int, default=0, show_default=False)
    
    feedback = None
    if rating > 0:
        feedback = click.prompt("   反馈 (可选，回车跳过)", default="", show_default=False)
        if not feedback:
            feedback = None
        
        # 保存到执行历史
        from ai_as_me.yangu import ExecutionHistory
        history = ExecutionHistory()
        history.add_execution(
            task_id=task_id,
            tool=result.get('tool', tool),
            prompt=task['description'],
            output=result.get('output', ''),
            success=result['success'],
            rating=rating,
            feedback=feedback
        )
        click.echo(f"\n✅ 反馈已记录，感谢！")


if __name__ == "__main__":
    cli()


# v3.0: Soul 管理命令
@cli.group()
def soul():
    """Soul 管理命令"""
    pass


@soul.command()
def status():
    """检查 Soul 状态"""
    from ai_as_me.soul.loader import SoulLoader
    loader = SoulLoader(Path("soul"))
    status = loader.check_status()
    
    click.echo("📊 Soul Status:")
    click.echo(f"  Profile: {'✓' if status['profile'] else '✗'}")
    click.echo(f"  Rules: {'✓' if status['rules'] else '✗'}")
    click.echo(f"  Mission: {'✓' if status['mission'] else '✗'}")
    
    # v3.0: 检查规则目录
    rules_dir = Path("soul/rules")
    if rules_dir.exists():
        core_count = len(list((rules_dir / "core").glob("*.md")))
        learned_count = len(list((rules_dir / "learned").glob("*.md")))
        click.echo(f"\n📚 Rules Structure (v3.0):")
        click.echo(f"  Core rules: {core_count}")
        click.echo(f"  Learned rules: {learned_count}")


@soul.command()
def migrate():
    """迁移 Soul 到 v3.0 结构"""
    from ai_as_me.soul.migrator import SoulMigrator
    migrator = SoulMigrator(Path("soul"))
    migrator.migrate()
    click.echo("✓ Migration complete")



@cli.command()
def check_tools():
    """检查Agent CLI工具可用性"""
    click.echo("🔧 检查 Agent CLI 工具可用性...\n")
    
    tools = [
        {
            'name': 'Claude Code',
            'command': ['npx', '@anthropic-ai/claude-code@2.0.76', '--version'],
            'package': '@anthropic-ai/claude-code@2.0.76'
        },
        {
            'name': 'OpenCode',
            'command': ['npx', 'opencode-ai@1.1.3', '--version'],
            'package': 'opencode-ai@1.1.3'
        }
    ]
    
    all_passed = True
    
    for tool in tools:
        click.echo(f"检测 {tool['name']}...")
        try:
            result = subprocess.run(
                tool['command'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0 or 'version' in result.stdout.lower() or 'version' in result.stderr.lower():
                click.echo(f"✅ {tool['name']}: 可用")
            else:
                click.echo(f"⚠️  {tool['name']}: 可能不可用 (返回码: {result.returncode})")
                click.echo(f"   建议: npx -y {tool['package']}")
        except subprocess.TimeoutExpired:
            click.echo(f"⏱️  {tool['name']}: 检测超时 (>30秒)")
            click.echo(f"   建议: 工具可能需要首次下载，请稍后重试")
        except FileNotFoundError:
            click.echo(f"❌ {tool['name']}: npx 不可用")
            click.echo(f"   建议: 先运行 'ai-as-me check-env'")
            all_passed = False
    
    click.echo()
    click.echo("✅ Agent CLI 工具检查完成")
    click.echo("\n💡 提示: 首次使用时工具会自动下载")


@cli.group()
def evolve():
    """进化相关命令"""
    pass


@evolve.command()
@click.option('--days', default=7, help='统计天数')
def stats(days):
    """显示进化统计"""
    from ai_as_me.evolution.logger import EvolutionLogger
    logger = EvolutionLogger(Path("logs/evolution.jsonl"))
    stats_data = logger.get_stats(days)
    
    click.echo(f"📊 进化统计（最近 {days} 天）")
    click.echo(f"  规则生成: {stats_data['total_rules']} 条")
    click.echo(f"  模式识别: {stats_data['total_patterns']} 个")
    click.echo(f"  经验记录: {stats_data['total_experiences']} 次")


@evolve.command()
@click.option('--limit', default=10, help='显示数量')
def history(limit):
    """显示进化历史"""
    from ai_as_me.evolution.logger import EvolutionLogger
    logger = EvolutionLogger(Path("logs/evolution.jsonl"))
    events = logger.get_recent_events(limit)
    
    if not events:
        click.echo("暂无进化记录")
        return
    
    click.echo(f"📜 最近 {len(events)} 次进化事件:\n")
    for i, event in enumerate(events, 1):
        timestamp = event['timestamp'][:19]
        task_id = event['task_id']
        rules = event.get('rules_generated', 0)
        patterns = event.get('patterns_found', 0)
        
        click.echo(f"{i}. [{timestamp}] {task_id}")
        click.echo(f"   模式: {patterns}, 规则: {rules}")
        if event.get('rule_categories'):
            click.echo(f"   类别: {', '.join(event['rule_categories'])}")
        click.echo()
