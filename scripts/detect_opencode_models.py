#!/usr/bin/env python3
"""检测 OpenCode 可用模型"""
import subprocess
import json

def get_available_models():
    """动态获取可用的免费模型"""
    result = subprocess.run(
        ["python3", "scripts/query_opencode_models.py"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout) if result.returncode == 0 else []

def detect():
    """返回首选模型"""
    models = get_available_models()
    return models[0] if models else None

if __name__ == "__main__":
    model = detect()
    print(json.dumps({"model": model, "available": get_available_models()}, indent=2))
