#!/usr/bin/env python3
"""从 claude-code 查询可用模型"""
import subprocess
import re

def get_claude_models():
    """从 --help 提取支持的模型别名"""
    result = subprocess.run(
        ["npx", "@anthropic-ai/claude-code", "--help"],
        capture_output=True, text=True
    )
    
    # 提取别名示例: 'sonnet' or 'opus'
    match = re.search(r"'(\w+)'\s+or\s+'(\w+)'", result.stdout)
    if match:
        return list(match.groups())
    
    # 默认别名
    return ["haiku", "sonnet", "opus"]

if __name__ == "__main__":
    import json
    print(json.dumps(get_claude_models()))
