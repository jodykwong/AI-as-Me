#!/usr/bin/env python3
"""从 opencode 查询可用模型"""
import subprocess
import json

def get_opencode_models():
    """查询 opencode 支持的模型"""
    result = subprocess.run(
        ["npx", "opencode-ai", "models"],
        capture_output=True, text=True, cwd="/home/sunrise/AI-as-Me"
    )
    
    if result.returncode != 0:
        return []
    
    # 解析输出，每行一个模型
    models = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    return models

def get_free_models():
    """获取免费模型"""
    all_models = get_opencode_models()
    # 过滤包含 free 或 opencode provider 的模型
    return [m for m in all_models if 'free' in m or m.startswith('opencode/')]

if __name__ == "__main__":
    models = get_free_models()
    print(json.dumps(models, indent=2))
