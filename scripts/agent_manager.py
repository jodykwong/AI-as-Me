#!/usr/bin/env python3
"""统一 Agent 管理器"""
import os
import sys
import subprocess
import json

def get_opencode_config():
    """获取 OpenCode 配置"""
    result = subprocess.run(
        ["python3", "scripts/detect_opencode_models.py"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout) if result.returncode == 0 else None

def get_claude_model(prompt):
    """获取 Claude 模型"""
    result = subprocess.run(
        ["python3", "scripts/select_claude_model.py"],
        input=prompt, capture_output=True, text=True
    )
    return result.stdout.strip()

def call_opencode(prompt):
    """调用 OpenCode"""
    config = get_opencode_config()
    if not config:
        return {"error": "No OpenCode API key configured"}
    
    env = os.environ.copy()
    env[config["env"]] = os.getenv(config["env"])
    
    result = subprocess.run(
        ["npx", "opencode-ai@latest", "-m", config["model"]],
        input=prompt, capture_output=True, text=True, env=env
    )
    return {"output": result.stdout, "model": config["model"]}

def call_claude(prompt):
    """调用 Claude Code"""
    model = get_claude_model(prompt)
    
    result = subprocess.run(
        ["npx", "@anthropic-ai/claude-code@latest", "--model", model],
        input=prompt, capture_output=True, text=True
    )
    return {"output": result.stdout, "model": model}

if __name__ == "__main__":
    agent = sys.argv[1] if len(sys.argv) > 1 else "opencode"
    prompt = sys.stdin.read()
    
    result = call_opencode(prompt) if agent == "opencode" else call_claude(prompt)
    print(json.dumps(result, indent=2))
