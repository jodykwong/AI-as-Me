---
project_name: 'AI-as-Me'
user_name: 'Jody'
date: '2026-01-10'
sections_completed: ['technology_stack', 'language_rules', 'framework_rules', 'testing_rules', 'code_quality', 'error_handling', 'critical_rules']
existing_patterns_found: 17
source_documents:
  - 'architecture.md'
  - 'prd.md'
status: 'complete'
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing code in this project. Focus on unobvious details that agents might otherwise miss._

---

## Technology Stack & Versions

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | ≥3.9 | 运行时 |
| Typer | ≥0.9.0 | CLI 框架 |
| openai | ≥1.0.0 | LLM API |
| python-dotenv | ≥1.0.0 | 环境变量 |
| PyYAML | ≥6.0 | 配置文件 |
| pytest | ≥7.0 | 测试框架 |
| black | latest | 代码格式化 |
| mypy | latest | 类型检查 |

**构建系统:** pyproject.toml + hatchling
**目标平台:** RDK X5 (Linux ARM64)

---

## Critical Implementation Rules

### Python 语言规则

- **类型提示必须:** 所有函数必须有完整的类型提示
- **导入顺序:** 标准库 → 第三方 → 本地模块，用空行分隔
- **字符串格式:** 使用 f-string，禁止 % 或 .format()
- **路径处理:** 使用 `pathlib.Path`，禁止字符串拼接路径
- **异步模式:** MVP 阶段使用同步代码，保持简单

### CLI 框架规则 (Typer)

- **命令命名:** 使用连字符分隔 `ai-as-me run`
- **参数类型:** 利用 Typer 自动类型推断
- **帮助文档:** 每个命令必须有 docstring 作为帮助
- **退出码:** 成功=0，用户错误=1，系统错误=2

### Testing Rules

- **位置:** `tests/` 目录，镜像 `src/` 结构
- **命名:** `test_<module>.py` / `test_<func>_<scenario>()`
- **Fixtures:** 共享 fixtures 放在 `conftest.py`
- **Mock:** 使用 `unittest.mock` 或 `pytest-mock`
- **覆盖率:** 核心模块目标 >80%

### Code Quality & Style Rules

- **格式化:** 必须通过 `black --line-length 88`
- **类型检查:** 必须通过 `mypy --strict`（可渐进启用）
- **命名:**
  - 文件/模块: `snake_case.py`
  - 类: `PascalCase`
  - 函数/变量: `snake_case`
  - 常量: `UPPER_SNAKE`
- **注释:** 只在逻辑不明显时添加，代码应自解释
- **Docstring:** 公共 API 必须有 Google 风格 docstring

### Error Handling Rules

- **自定义异常:** 使用 `AgentError` / `LLMError`
- **禁止:** 裸 `except:`，必须指定异常类型
- **禁止:** 静默忽略异常 `except: pass`
- **日志:** 错误必须记录到 JSON Lines 日志
- **用户反馈:** 错误消息必须包含解决建议
- **可恢复 vs 致命:** 明确区分，可恢复自动重试

### Critical Don't-Miss Rules

**MUST DO:**
- 所有文件操作使用 `with` 上下文管理器
- API 密钥只从环境变量读取
- 灵魂文件权限设为 600
- 日志使用 JSON Lines 格式

**MUST NOT:**
- 不要硬编码 API 密钥或敏感信息
- 不要使用 `print()` 调试，使用日志
- 不要使用相对导入跨模块
- 不要在循环中创建 LLM 客户端实例

**Edge Cases:**
- 灵魂文件不存在时优雅降级
- 网络断开时任务保持在 doing/ 状态
- SD 卡空间不足时停止写入日志

---

## Quick Reference

```python
# ✅ 正确示例
from pathlib import Path
from typing import Optional

def load_config(path: Path) -> Optional[dict]:
    """加载配置文件。

    Args:
        path: 配置文件路径

    Returns:
        配置字典，文件不存在返回 None
    """
    if not path.exists():
        return None
    with path.open() as f:
        return yaml.safe_load(f)

# ❌ 错误示例
def load_config(path):  # 缺少类型提示
    try:
        return yaml.load(open(path))  # 不安全的 yaml.load，无 with
    except:  # 裸 except
        return {}  # 静默失败
```

---

_Generated: 2026-01-10 | Source: architecture.md_
