"""Agent CLI调用模块"""

import subprocess
import logging
from pathlib import Path
from typing import Dict


class AgentCLI:
    """Agent CLI工具调用封装"""

    TOOLS = {
        # "claude-code": {
        #     "command": ["claude", "--print", "--dangerously-skip-permissions"],
        #     "name": "Claude Code",
        # },
        "opencode": {"command": ["opencode", "run"], "name": "OpenCode"},
    }

    def __init__(self, logs_dir: Path = None, soul_dir: Path = None):
        self.logs_dir = logs_dir or Path.cwd() / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        self._setup_logging()

        # Soul注入器
        from .soul_injector import SoulInjector

        self.soul_injector = SoulInjector(soul_dir)

        # 检查工具是否已安装
        self._check_tools()

    def _check_tools(self):
        """检查工具是否已安装并认证"""
        self.available_tools = {}
        for tool_name, config in self.TOOLS.items():
            try:
                # 使用 which 检查命令是否存在（更快更可靠）
                cmd_name = config["command"][0]
                result = subprocess.run(
                    ["which", cmd_name], capture_output=True, text=True, timeout=2
                )
                self.available_tools[tool_name] = result.returncode == 0
                if result.returncode == 0:
                    self.logger.info(f"{config['name']} 已安装")
                else:
                    self.logger.warning(f"{config['name']} 未安装或未认证")
            except Exception as e:
                self.available_tools[tool_name] = False
                self.logger.warning(f"{config['name']} 检查失败: {e}")

    def _setup_logging(self):
        """设置日志"""
        log_file = self.logs_dir / "agent_calls.log"
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        )
        self.logger = logging.getLogger("AgentCLI")

    def call(
        self,
        tool_name: str,
        prompt: str,
        timeout: int = 300,
        use_soul: bool = True,
        model: str = None,
    ) -> Dict:
        """调用Agent CLI工具

        Args:
            tool_name: 工具名称 (claude-code, opencode)
            prompt: 提示词
            timeout: 超时时间(秒) - 默认5分钟
            use_soul: 是否使用Soul注入
            model: 模型名称（可选）

        Returns:
            {success: bool, output: str, error: str, tool: str}
        """
        if tool_name not in self.TOOLS:
            return {
                "success": False,
                "output": "",
                "error": f"未知工具: {tool_name}",
                "tool": tool_name,
            }

        # 检查工具是否可用
        if not self.available_tools.get(tool_name, False):
            return {
                "success": False,
                "output": "",
                "error": f'{self.TOOLS[tool_name]["name"]} 未安装或未认证。请先运行: npx -y @anthropic-ai/claude-code (或 opencode-ai)',
                "tool": tool_name,
            }

        # Soul注入
        if use_soul and self.soul_injector.has_soul():
            prompt = self.soul_injector.build_prompt(prompt)
            self.logger.info(f"Soul注入: 提示词长度 {len(prompt)} 字符")

        tool_config = self.TOOLS[tool_name]
        command = tool_config["command"].copy()

        # 添加模型参数
        if model:
            # if tool_name == "claude-code":  # claude-code temporarily disabled
            #     command.extend(["--model", model])
            if tool_name == "opencode":
                command.extend(["--model", model])
            self.logger.info(f"使用模型: {model}")

        command.append(prompt)

        self.logger.info(f"调用 {tool_config['name']}: {prompt[:50]}...")

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=Path.cwd(),  # 在当前目录执行
            )

            success = result.returncode == 0
            output = result.stdout
            error = result.stderr

            self.logger.info(f"{tool_config['name']} 返回码: {result.returncode}")

            if success:
                self.logger.info(f"输出长度: {len(output)} 字符")
            else:
                self.logger.error(f"错误: {error[:200]}")

            return {
                "success": success,
                "output": output,
                "error": error,
                "tool": tool_name,
                "returncode": result.returncode,
            }

        except subprocess.TimeoutExpired:
            error_msg = f"调用超时 (>{timeout}秒)"
            self.logger.error(error_msg)
            return {
                "success": False,
                "output": "",
                "error": error_msg,
                "tool": tool_name,
            }
        except Exception as e:
            error_msg = f"调用异常: {str(e)}"
            self.logger.error(error_msg)
            return {
                "success": False,
                "output": "",
                "error": error_msg,
                "tool": tool_name,
            }

    def call_with_fallback(
        self, prompt: str, tools: list = None, timeout: int = 30, use_soul: bool = True
    ) -> Dict:
        """调用工具，失败时自动切换备用工具

        Args:
            prompt: 提示词
            tools: 工具列表，默认['opencode'] (claude-code temporarily disabled)
            timeout: 每个工具的超时时间(秒)
            use_soul: 是否使用Soul注入

        Returns:
            {success: bool, output: str, error: str, tool: str, attempts: list}
        """
        if tools is None:
            # tools = ["claude-code", "opencode"]  # claude-code temporarily disabled
            tools = ["opencode"]

        attempts = []

        for tool_name in tools:
            self.logger.info(f"尝试工具: {tool_name}")
            result = self.call(tool_name, prompt, timeout, use_soul)
            attempts.append(
                {
                    "tool": tool_name,
                    "success": result["success"],
                    "error": result["error"],
                }
            )

            if result["success"]:
                result["attempts"] = attempts
                self.logger.info(f"工具 {tool_name} 调用成功")
                return result
            else:
                self.logger.warning(f"工具 {tool_name} 失败: {result['error'][:100]}")

        # 所有工具都失败
        self.logger.error("所有工具调用失败")
        return {
            "success": False,
            "output": "",
            "error": f"所有工具调用失败。尝试了: {', '.join(tools)}",
            "tool": "none",
            "attempts": attempts,
        }

        """调用工具，失败时自动切换备用工具
        
        Args:
            prompt: 提示词
            tools: 工具列表，默认['opencode'] (claude-code temporarily disabled)
            timeout: 每个工具的超时时间(秒)
        
        Returns:
            {success: bool, output: str, error: str, tool: str, attempts: list}
        """
        if tools is None:
            # tools = ["claude-code", "opencode"]  # claude-code temporarily disabled
            tools = ["opencode"]

        attempts = []

        for tool_name in tools:
            self.logger.info(f"尝试工具: {tool_name}")
            result = self.call(tool_name, prompt, timeout)
            attempts.append(
                {
                    "tool": tool_name,
                    "success": result["success"],
                    "error": result["error"],
                }
            )

            if result["success"]:
                result["attempts"] = attempts
                self.logger.info(f"工具 {tool_name} 调用成功")
                return result
            else:
                self.logger.warning(f"工具 {tool_name} 失败: {result['error'][:100]}")

        # 所有工具都失败
        self.logger.error("所有工具调用失败")
        return {
            "success": False,
            "output": "",
            "error": f"所有工具调用失败。尝试了: {', '.join(tools)}",
            "tool": "none",
            "attempts": attempts,
        }
