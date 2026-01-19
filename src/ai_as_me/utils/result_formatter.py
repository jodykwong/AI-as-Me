"""执行结果格式化工具."""
import time
from datetime import datetime
from typing import Dict, Any, Union


def format_result_metadata(result: Union[Dict, Any]) -> str:
    """格式化执行结果的元数据部分.

    支持两种格式：
    1. AgentResult 对象（包含属性）
    2. 字典格式的结果（从CLI或其他来源）

    Args:
        result: AgentResult 对象或字典，包含以下属性/键：
            - success: bool
            - output: str (可选)
            - error: str (可选)
            - agent_name: str (可选)
            - duration: float (可选)
            - metadata: Dict (可选)
            - tool: str (可选)
            - timestamp: float (可选)

    Returns:
        格式化后的元数据Markdown表格字符串
    """
    # 统一处理两种格式
    is_dict = isinstance(result, dict)

    # 提取元数据
    success = result.get('success') if is_dict else result.success
    agent_name = result.get('agent_name') if is_dict else getattr(result, 'agent_name', 'unknown')
    error = result.get('error') if is_dict else (result.error if hasattr(result, 'error') else '')
    duration = result.get('duration') if is_dict else (result.duration if hasattr(result, 'duration') else 0)
    tool = result.get('tool')

    # 获取metadata字典
    if is_dict:
        metadata = result.get('metadata', {})
        timestamp = result.get('timestamp', time.time())
    else:
        metadata = result.metadata or {}
        timestamp = metadata.get('timestamp', time.time())

    dt = datetime.fromtimestamp(timestamp)

    # 构建元数据表格
    lines = [
        "## 执行信息",
        "",
        "| 项目 | 值 |",
        "|------|-----|",
        f"| **状态** | ✅ 成功 |" if success else f"| **状态** | ❌ 失败 |",
        f"| **Agent** | `{agent_name}` |",
        f"| **模型** | `{metadata.get('model', 'N/A')}` |",
        f"| **执行时间** | {dt.strftime('%Y-%m-%d %H:%M:%S')} |",
        f"| **耗时** | {duration:.2f}s |",
    ]

    if error:
        lines.append(f"| **错误** | {error} |")

    if metadata.get('returncode') is not None:
        lines.append(f"| **返回码** | {metadata['returncode']} |")

    if tool or metadata.get('tool'):
        tool_name = tool or metadata.get('tool')
        lines.append(f"| **工具** | `{tool_name}` |")

    lines.extend(["", "---", ""])
    return "\n".join(lines)
