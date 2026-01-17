#!/usr/bin/env python3
"""Agent后台服务 - 自动执行doing中的任务."""
import sys
import time
from pathlib import Path
from ai_as_me.core.agent import Agent, setup_logging
from ai_as_me.llm.client import LLMClient
from ai_as_me.soul.loader import load_soul_context

def main():
    """启动Agent后台服务."""
    print("🤖 启动 AI-as-Me Agent 后台服务...")
    
    # 设置日志
    setup_logging(Path("logs"))
    
    # 初始化LLM和Soul
    try:
        llm_client = LLMClient()
        soul_context = load_soul_context(Path("soul"))
        print("✅ LLM Client 和 Soul Context 已加载")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        sys.exit(1)
    
    # 创建Agent
    kanban_dir = Path("kanban")
    agent = Agent(
        kanban_dir=kanban_dir,
        llm_client=llm_client,
        soul_context=soul_context,
        skip_clarification=True,  # 已在UI中澄清
        poll_interval=5  # 每5秒检查一次
    )
    
    print("✅ Agent 已初始化")
    print(f"📂 监控目录: {kanban_dir.absolute()}")
    print(f"⏱️  轮询间隔: 5秒")
    print("🔄 Agent 将自动执行 doing 目录中的任务")
    print("⏹️  按 Ctrl+C 停止服务\n")
    
    try:
        agent.start()
    except KeyboardInterrupt:
        print("\n✅ Agent 服务已停止")
    except Exception as e:
        print(f"\n❌ Agent 运行错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
