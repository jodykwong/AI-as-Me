#!/usr/bin/env python3
"""Claude Code 模型选择器"""
import sys
import subprocess
import json

def get_available_models():
    """动态获取可用模型"""
    result = subprocess.run(
        ["python3", "scripts/query_claude_models.py"],
        capture_output=True, text=True
    )
    models = json.loads(result.stdout)
    
    # 映射：简单->第一个, 复杂->最后一个, 常规->中间
    return {
        "simple": models[0] if len(models) > 0 else "haiku",
        "normal": models[1] if len(models) > 1 else "sonnet",
        "complex": models[-1] if len(models) > 0 else "opus"
    }

def classify_task(prompt):
    """根据 prompt 分类任务复杂度"""
    lines = len(prompt.split('\n'))
    words = len(prompt.split())
    
    if words < 50 or lines < 5:
        return "simple"
    elif words > 200 or lines > 20:
        return "complex"
    return "normal"

def select_model(prompt):
    """选择合适的模型"""
    models = get_available_models()
    task_type = classify_task(prompt)
    return models[task_type]

if __name__ == "__main__":
    prompt = sys.stdin.read() if not sys.stdin.isatty() else sys.argv[1] if len(sys.argv) > 1 else ""
    print(select_model(prompt))
