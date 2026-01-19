#!/usr/bin/env python3
"""OpenCode Agent 验证脚本"""
import sys
import json
import time
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ai_as_me.agents.opencode_agent import OpenCodeAgent
from ai_as_me.orchestrator.agent_cli import AgentCLI
from ai_as_me.kanban.models import Task


class VerificationReport:
    """验证报告"""
    def __init__(self):
        self.tests = []
        self.passed = 0
        self.failed = 0

    def add_test(self, name, success, message="", duration=0):
        """添加测试结果"""
        self.tests.append({
            'name': name,
            'success': success,
            'message': message,
            'duration': duration
        })
        if success:
            self.passed += 1
        else:
            self.failed += 1

    def print_report(self):
        """打印报告"""
        print("\n" + "="*60)
        print("OpenCode Agent 验证报告")
        print("="*60)

        for test in self.tests:
            status = "✅ 通过" if test['success'] else "❌ 失败"
            print(f"\n{status}: {test['name']}")
            if test['message']:
                print(f"   信息: {test['message']}")
            if test['duration'] > 0:
                print(f"   耗时: {test['duration']:.2f}秒")

        print("\n" + "="*60)
        print(f"总计: {self.passed} 通过, {self.failed} 失败")
        print(f"成功率: {self.passed}/{self.passed + self.failed} = {100*self.passed/(self.passed+self.failed):.1f}%")
        print("="*60 + "\n")

        return self.failed == 0


def test_opencode_installation():
    """测试1: OpenCode CLI安装"""
    report = VerificationReport()

    # 测试opencode命令
    import subprocess
    result = subprocess.run(
        ['which', 'opencode'],
        capture_output=True,
        text=True
    )
    report.add_test(
        "OpenCode CLI安装",
        result.returncode == 0,
        f"路径: {result.stdout.strip()}" if result.returncode == 0 else "未找到opencode命令"
    )

    # 测试版本
    result = subprocess.run(
        ['opencode', '--version'],
        capture_output=True,
        text=True
    )
    report.add_test(
        "OpenCode 版本检查",
        result.returncode == 0,
        f"版本: {result.stdout.strip()}" if result.returncode == 0 else result.stderr
    )

    return report


def test_agent_cli():
    """测试2: AgentCLI模块"""
    report = VerificationReport()

    try:
        cli = AgentCLI()
        report.add_test(
            "AgentCLI初始化",
            True,
            "成功创建AgentCLI实例"
        )

        # 检查opencode工具
        available = cli.available_tools.get('opencode', False)
        report.add_test(
            "OpenCode工具可用性",
            available,
            "OpenCode工具已注册" if available else "OpenCode工具未注册"
        )

    except Exception as e:
        report.add_test(
            "AgentCLI初始化",
            False,
            str(e)
        )

    return report


def test_opencode_agent():
    """测试3: OpenCodeAgent"""
    report = VerificationReport()

    try:
        agent = OpenCodeAgent()
        report.add_test(
            "OpenCodeAgent初始化",
            True,
            "成功创建OpenCodeAgent实例"
        )

        # 检查Agent是否可用
        is_available = agent.is_available()
        report.add_test(
            "OpenCodeAgent可用性",
            is_available,
            "Agent已准备就绪" if is_available else "Agent不可用"
        )

        # 检查能力列表
        capabilities = agent.get_capabilities()
        report.add_test(
            "OpenCodeAgent能力列表",
            len(capabilities) > 0,
            f"能力: {', '.join(capabilities)}"
        )

    except Exception as e:
        report.add_test(
            "OpenCodeAgent初始化",
            False,
            str(e)
        )

    return report


def test_agent_execution():
    """测试4: Agent执行（简单任务）"""
    report = VerificationReport()

    try:
        import uuid
        agent = OpenCodeAgent()

        # 创建一个简单的测试任务（需要提供id）
        task = Task(
            id=str(uuid.uuid4()),
            title="测试任务",
            description="编写一个hello world函数"
        )

        start = time.time()
        result = agent.execute(task, model="opencode/gpt-5-nano")
        duration = time.time() - start

        report.add_test(
            "Agent执行简单任务",
            result.success,
            f"输出长度: {len(result.output)} 字符" if result.success else f"错误: {result.error}",
            duration
        )

        if result.success:
            report.add_test(
                "执行结果验证",
                len(result.output) > 0,
                f"获得{len(result.output)}字符的输出"
            )

    except Exception as e:
        report.add_test(
            "Agent执行简单任务",
            False,
            str(e)
        )

    return report


def test_model_detection():
    """测试5: 模型检测"""
    report = VerificationReport()

    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/detect_opencode_models.py'],
            capture_output=True,
            text=True,
            timeout=30  # 增加超时时间到30秒
        )

        if result.returncode == 0:
            data = json.loads(result.stdout)
            models = data.get('available', [])
            report.add_test(
                "模型检测",
                len(models) > 0,
                f"检测到{len(models)}个可用模型: {', '.join(models[:3])}..." if len(models) > 3 else f"检测到{len(models)}个可用模型"
            )
        else:
            report.add_test(
                "模型检测",
                False,
                f"脚本执行失败: {result.stderr}"
            )

    except subprocess.TimeoutExpired:
        report.add_test(
            "模型检测",
            False,
            "脚本执行超时（可能是网络延迟），但OpenCode已安装"
        )
    except Exception as e:
        report.add_test(
            "模型检测",
            False,
            str(e)
        )

    return report


def test_agent_cli_duplicated_code():
    """测试6: 代码质量检查 - 重复代码"""
    report = VerificationReport()

    # 检查agent_cli.py是否有重复的call_with_fallback方法
    try:
        with open('src/ai_as_me/orchestrator/agent_cli.py', 'r') as f:
            content = f.read()

        # 查找call_with_fallback方法出现的次数
        count = content.count('def call_with_fallback')

        report.add_test(
            "代码质量: 重复方法检查",
            count == 1,
            f"发现{count}个call_with_fallback方法定义" if count != 1 else "没有重复代码"
        )

        if count > 1:
            lines = content.split('\n')
            duplicates = []
            for i, line in enumerate(lines, 1):
                if 'def call_with_fallback' in line:
                    duplicates.append(f"第{i}行")
            report.tests[-1]['message'] += f" ({', '.join(duplicates)})"

    except Exception as e:
        report.add_test(
            "代码质量: 重复方法检查",
            False,
            str(e)
        )

    return report


def main():
    """运行所有验证测试"""
    print("\n开始验证OpenCode系统...\n")

    all_passed = True

    # 运行所有测试
    reports = [
        ("安装检查", test_opencode_installation()),
        ("AgentCLI检查", test_agent_cli()),
        ("OpenCodeAgent检查", test_opencode_agent()),
        ("代码质量检查", test_agent_cli_duplicated_code()),
        ("模型检测", test_model_detection()),
        ("Agent执行测试", test_agent_execution()),
    ]

    for name, report in reports:
        print(f"\n{'='*60}")
        print(f"测试类别: {name}")
        print(f"{'='*60}")
        for test in report.tests:
            status = "✅" if test['success'] else "❌"
            print(f"{status} {test['name']}")
            if test['message']:
                print(f"   └─ {test['message']}")
            if test['duration'] > 0:
                print(f"   └─ 耗时: {test['duration']:.2f}s")

        if not report.print_report():
            all_passed = False

    # 总体结果
    print("\n" + "="*60)
    if all_passed:
        print("✅ 所有测试通过！OpenCode系统正常工作。")
    else:
        print("⚠️ 部分测试失败，需要修复。")
    print("="*60 + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
