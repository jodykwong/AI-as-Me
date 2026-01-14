"""多工具智能选择模块 - Epic 5"""
from enum import Enum
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import yaml
import sqlite3
import logging

logger = logging.getLogger(__name__)


# Story 5.1: 任务类型识别
class TaskType(Enum):
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    DOCUMENTATION = "documentation"
    ARCHITECTURE = "architecture"
    DEBUG = "debug"
    UNKNOWN = "unknown"


class TaskAnalyzer:
    """基于关键词匹配的任务类型识别器"""
    
    # Story 8.3: 预处理为小写的关键词
    KEYWORDS: dict[TaskType, list[str]] = {
        TaskType.CODE_GENERATION: [
            "创建", "实现", "生成", "开发", "编写", "函数", "类", "模块",
            "create", "implement", "generate", "develop", "function", "class"
        ],
        TaskType.CODE_REVIEW: [
            "审查", "检查", "review", "check", "分析代码", "代码质量", "inspect"
        ],
        TaskType.DOCUMENTATION: [
            "文档", "说明", "readme", "doc", "注释", "document", "文档化", "写文档", "api文档"
        ],
        TaskType.ARCHITECTURE: [
            "架构", "设计", "architecture", "design", "系统设计", "模块", "structure"
        ],
        TaskType.DEBUG: [
            "修复", "bug", "fix", "调试", "debug", "错误", "问题", "issue"
        ],
    }
    
    def __init__(self) -> None:
        # Story 8.3: 初始化时预处理关键词为小写
        self._keywords_lower: dict[TaskType, list[str]] = {
            task_type: [kw.lower() for kw in keywords]
            for task_type, keywords in self.KEYWORDS.items()
        }
    
    def analyze(self, description: str) -> TaskType:
        """分析任务描述，返回任务类型"""
        desc_lower = description.lower()
        scores = {t: 0 for t in TaskType if t != TaskType.UNKNOWN}
        
        # Story 8.3: 使用预处理的小写关键词
        for task_type, keywords in self._keywords_lower.items():
            for kw in keywords:
                if kw in desc_lower:  # 不再需要 kw.lower()
                    scores[task_type] += 1
        
        if max(scores.values()) == 0:
            return TaskType.UNKNOWN
        
        return max(scores, key=scores.get)


# Story 5.2: 工具能力注册
@dataclass
class ToolCapability:
    tool_name: str
    capabilities: dict[TaskType, float]  # Story 8.4: 完整类型注解


class ToolRegistry:
    """工具能力注册表"""
    
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.tools = {}
        if config_path.exists():
            self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        with open(self.config_path) as f:
            config = yaml.safe_load(f)
        
        for name, data in config.get('agents', {}).items():
            caps = {}
            for k, v in data.get('capabilities', {}).items():
                try:
                    task_type = TaskType[k.upper()]
                    caps[task_type] = float(v)
                except (KeyError, ValueError):
                    continue
            self.tools[name] = ToolCapability(name, caps)
    
    def get_capability(self, tool_name: str, task_type: TaskType) -> float:
        """获取工具对特定任务类型的能力评分"""
        tool = self.tools.get(tool_name)
        if not tool:
            return 0.0
        return tool.capabilities.get(task_type, 0.0)
    
    def get_available(self) -> list[str]:
        """获取所有可用工具名称"""
        return list(self.tools.keys())


# Story 5.3: 历史成功率追踪
class HistoryTracker:
    """工具执行历史追踪器"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_db_dir()
        self._ensure_table()
    
    def _ensure_db_dir(self):
        """确保数据库目录存在"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
    
    def _ensure_table(self):
        """确保数据库表存在"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tool_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    tool_name TEXT NOT NULL,
                    task_type TEXT NOT NULL,
                    success BOOLEAN NOT NULL,
                    execution_time REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_tool_history_tool 
                ON tool_history(tool_name)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_tool_history_type 
                ON tool_history(task_type)
            """)
    
    def record(self, task_id: str, tool_name: str, 
               task_type: TaskType, success: bool, 
               execution_time: float = None) -> None:
        """记录工具执行历史"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO tool_history 
                (task_id, tool_name, task_type, success, execution_time)
                VALUES (?, ?, ?, ?, ?)
            """, (task_id, tool_name, task_type.value, success, execution_time))
    
    def get_success_rate(self, tool_name: str, task_type: TaskType) -> float:
        """获取工具在特定任务类型的成功率"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT 
                    SUM(CASE WHEN success THEN 1 ELSE 0 END) as successes,
                    COUNT(*) as total
                FROM tool_history
                WHERE tool_name = ? AND task_type = ?
            """, (tool_name, task_type.value))
            
            row = cursor.fetchone()
            if not row or row[1] == 0:
                return 0.5  # 默认 50% (无历史数据)
            
            return row[0] / row[1]


# Story 5.4: 智能工具选择算法
class SkillMatcher:
    """智能工具选择器"""
    
    def __init__(self, config_path: Path, db_path: str):
        self.analyzer = TaskAnalyzer()
        self.registry = ToolRegistry(config_path)
        self.history = HistoryTracker(db_path)
        # Story 10.4: BMAD 扩展接口
        self.bmad_extension = None
    
    def set_bmad_extension(self, extension):
        """设置 BMAD 技能扩展（预留接口）"""
        self.bmad_extension = extension
    
    def detect_capability_gap(self, task_description: str) -> bool:
        """检测能力缺口"""
        task_type = self.analyzer.analyze(task_description)
        
        # 如果任务类型未知，可能需要 BMAD 扩展
        if task_type == TaskType.UNKNOWN:
            return True
        
        # 检查所有工具的能力评分
        scores = self._calculate_scores(task_type)
        max_score = max(scores.values()) if scores else 0
        
        # 如果最高分 <0.5，认为存在能力缺口
        return max_score < 0.5
    
    def match(self, task_description: str) -> str:
        """返回最匹配的工具名称"""
        # 1. 分析任务类型
        task_type = self.analyzer.analyze(task_description)
        
        # 2. 计算所有工具的评分
        scores = self._calculate_scores(task_type)
        
        if not scores:
            logger.warning("No tools available for matching")
            return None
        
        # 3. 选择最高分工具
        best_tool = max(scores, key=scores.get)
        
        # 4. 记录决策 (Story 11.3: DEBUG级别用于详细信息)
        logger.debug(
            f"Tool selection: task_type={task_type.value}, "
            f"selected={best_tool}, scores={scores}"
        )
        
        return best_tool
    
    def _calculate_scores(self, task_type: TaskType) -> dict[str, float]:
        """
        计算所有工具的评分
        
        Story 11.4: 评分算法说明
        综合评分 = 能力评分(50%) + 历史成功率(30%) + 可用性(20%)
        - 能力评分: 工具对特定任务类型的能力 (0.0-1.0)
        - 历史成功率: 基于历史执行记录计算 (0.0-1.0)
        - 可用性: 工具当前是否可用 (简化为1.0)
        """
        scores = {}
        
        for tool in self.registry.get_available():
            # 能力评分 (50%)
            cap_score = self.registry.get_capability(tool, task_type)
            
            # 历史成功率 (30%)
            hist_score = self.history.get_success_rate(tool, task_type)
            
            # 可用性 (20%) - 简化为 1.0
            avail_score = 1.0
            
            # 综合评分
            scores[tool] = (
                cap_score * 0.5 + 
                hist_score * 0.3 + 
                avail_score * 0.2
            )
        
        return scores
    
    def rank(self, task_description: str) -> list[tuple[str, float]]:
        """返回工具排名和分数"""
        task_type = self.analyzer.analyze(task_description)
        scores = self._calculate_scores(task_type)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)
