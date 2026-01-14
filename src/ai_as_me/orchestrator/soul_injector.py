"""Soul注入模块 - 提示词模板构建"""
from pathlib import Path
from typing import Optional


class SoulInjector:
    """Soul注入器 - 构建个性化提示词"""
    
    def __init__(self, soul_dir: Path = None, rag_retriever=None):
        self.soul_dir = soul_dir or Path.cwd() / "soul"
        self.profile_file = self.soul_dir / "profile.md"
        self.rules_file = self.soul_dir / "rules.md"
        self.rag_retriever = rag_retriever  # Story 7.4: RAG 集成
        self._cache = {}
    
    def _read_soul_file(self, file_path: Path) -> str:
        """读取Soul文件，带缓存"""
        if file_path in self._cache:
            return self._cache[file_path]
        
        if not file_path.exists():
            return ""
        
        content = file_path.read_text()
        self._cache[file_path] = content
        return content
    
    def build_prompt(self, user_task: str, max_length: int = 4000) -> str:
        """构建包含Soul上下文的提示词
        
        Args:
            user_task: 用户任务描述
            max_length: 最大长度限制
        
        Returns:
            完整的提示词
        """
        # 读取Soul文件
        profile = self._read_soul_file(self.profile_file)
        rules = self._read_soul_file(self.rules_file)
        
        # Story 7.4: 检索历史经验
        rag_context = ""
        if self.rag_retriever:
            try:
                experiences = self.rag_retriever.retrieve(user_task, top_k=3)
                rag_context = self.rag_retriever.build_context(experiences, max_tokens=500)
            except:
                pass  # RAG 失败不影响主流程
        
        # 如果没有任何上下文，直接返回用户任务
        if not profile and not rules and not rag_context:
            return user_task
        
        # 构建提示词模板
        prompt_parts = []
        
        if profile:
            prompt_parts.append("# 个人档案\n" + profile)
        
        if rules:
            prompt_parts.append("# 工作规则\n" + rules)
        
        if rag_context:
            prompt_parts.append("# 相关历史经验\n" + rag_context)
        
        prompt_parts.append("# 任务\n" + user_task)
        
        full_prompt = "\n\n".join(prompt_parts)
        
        # 长度控制
        if len(full_prompt) > max_length:
            # 简单截断策略：优先保留任务和规则
            task_section = "# 任务\n" + user_task
            rules_section = "# 工作规则\n" + rules if rules else ""
            
            available_length = max_length - len(task_section) - 100
            
            if rules_section and len(rules_section) < available_length:
                full_prompt = rules_section + "\n\n" + task_section
            else:
                full_prompt = task_section
        
        return full_prompt
    
    def has_soul(self) -> bool:
        """检查是否存在Soul文件"""
        return self.profile_file.exists() or self.rules_file.exists()
    
    def clear_cache(self):
        """清除缓存"""
        self._cache.clear()
