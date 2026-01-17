#!/usr/bin/env python3
"""实时查询可用模型"""
import os
import requests

def query_deepseek_models():
    """查询 DeepSeek 可用模型"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return None
    
    resp = requests.get(
        "https://api.deepseek.com/models",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    return resp.json()["data"] if resp.ok else None

def query_openai_models():
    """查询 OpenAI 可用模型"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    
    resp = requests.get(
        "https://api.openai.com/v1/models",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    return resp.json()["data"] if resp.ok else None

def query_anthropic_models():
    """Anthropic 不提供 API，返回文档中的最新模型"""
    if not os.getenv("ANTHROPIC_API_KEY"):
        return None
    
    # 从官方文档获取最新模型列表
    return [
        {"id": "claude-3-5-sonnet-20241022"},
        {"id": "claude-3-5-haiku-20241022"},
        {"id": "claude-3-opus-20240229"}
    ]

if __name__ == "__main__":
    import json
    
    models = {
        "deepseek": query_deepseek_models(),
        "openai": query_openai_models(),
        "anthropic": query_anthropic_models()
    }
    
    print(json.dumps(models, indent=2))
