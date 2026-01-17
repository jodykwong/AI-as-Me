#!/usr/bin/env python3
"""
OpenCode和Claude Code集成测试
验证实际调用是否能工作
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from src.ai_as_me.orchestrator.agent_cli import AgentCLI

def test_opencode():
    """测试OpenCode调用"""
    print("=" * 60)
    print("测试 OpenCode 集成")
    print("=" * 60)
    
    agent = AgentCLI()
    
    # 简单测试：让AI回答一个问题
    prompt = "请用一句话回答：1+1等于几？"
    
    print(f"\n提示词: {prompt}")
    print("调用中...")
    
    result = agent.call('opencode', prompt, timeout=30, use_soul=False)
    
    print(f"\n结果:")
    print(f"  成功: {result['success']}")
    print(f"  工具: {result['tool']}")
    
    if result['success']:
        print(f"  输出: {result['output'][:200]}")
        return True
    else:
        print(f"  错误: {result['error']}")
        return False


def test_claude_code():
    """测试Claude Code调用"""
    print("\n" + "=" * 60)
    print("测试 Claude Code 集成")
    print("=" * 60)
    
    agent = AgentCLI()
    
    prompt = "请用一句话回答：2+2等于几？"
    
    print(f"\n提示词: {prompt}")
    print("调用中...")
    
    result = agent.call('claude-code', prompt, timeout=30, use_soul=False)
    
    print(f"\n结果:")
    print(f"  成功: {result['success']}")
    print(f"  工具: {result['tool']}")
    
    if result['success']:
        print(f"  输出: {result['output'][:200]}")
        return True
    else:
        print(f"  错误: {result['error']}")
        return False


def test_fallback():
    """测试自动切换功能"""
    print("\n" + "=" * 60)
    print("测试 自动切换功能")
    print("=" * 60)
    
    agent = AgentCLI()
    
    prompt = "请用一句话回答：3+3等于几？"
    
    print(f"\n提示词: {prompt}")
    print("调用中（自动切换）...")
    
    result = agent.call_with_fallback(prompt, timeout=30, use_soul=False)
    
    print(f"\n结果:")
    print(f"  成功: {result['success']}")
    print(f"  使用工具: {result['tool']}")
    print(f"  尝试次数: {len(result.get('attempts', []))}")
    
    if result['success']:
        print(f"  输出: {result['output'][:200]}")
        return True
    else:
        print(f"  错误: {result['error']}")
        for attempt in result.get('attempts', []):
            print(f"    - {attempt['tool']}: {attempt['error'][:100]}")
        return False


if __name__ == "__main__":
    print("\n🧪 AI-as-Me OpenCode/Claude Code 集成测试\n")
    
    results = {
        "OpenCode": test_opencode(),
        "Claude Code": test_claude_code(),
        "自动切换": test_fallback()
    }
    
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    for name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✅ 所有测试通过！集成正常工作。")
        sys.exit(0)
    else:
        print("\n❌ 部分测试失败。请检查配置和依赖。")
        sys.exit(1)
