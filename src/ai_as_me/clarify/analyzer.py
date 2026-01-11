"""Task clarification analyzer."""
from typing import List, Optional


class ClarificationAnalyzer:
    """Analyze tasks and generate clarification questions."""
    
    def __init__(self, llm_client):
        """Initialize analyzer.
        
        Args:
            llm_client: LLMClient instance
        """
        self.llm_client = llm_client
    
    def analyze_complexity(self, task) -> str:
        """Analyze task complexity.
        
        Args:
            task: Task object
            
        Returns:
            Complexity level: 'low', 'medium', or 'high'
        """
        # Simple heuristic-based analysis
        context_length = len(task.context)
        has_expected_output = bool(task.expected_output)
        
        # Low complexity: short, clear tasks with expected output
        if context_length < 200 and has_expected_output:
            return "low"
        
        # High complexity: long tasks without expected output
        if context_length > 500 or not has_expected_output:
            return "high"
        
        return "medium"
    
    def generate_questions(self, task) -> Optional[List[str]]:
        """Generate clarification questions for a task.
        
        Args:
            task: Task object
            
        Returns:
            List of clarification questions, or None if not needed
        """
        complexity = self.analyze_complexity(task)
        
        # Skip clarification for low complexity tasks
        if complexity == "low":
            return None
        
        # Use LLM to generate questions
        prompt = f"""Analyze this task and generate 1-3 clarification questions to ensure clear understanding.

Task: {task.title}
Context: {task.context}

Generate specific, actionable questions that would help execute this task better.
Return only the questions, one per line, starting with "- "."""

        messages = [
            {"role": "system", "content": "You are a helpful assistant that generates clarification questions."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm_client.chat(messages, max_retries=2)
        
        if response:
            # Parse questions from response
            questions = [
                line.strip()[2:].strip()  # Remove "- " prefix
                for line in response.split('\n')
                if line.strip().startswith('-')
            ]
            return questions[:3]  # Max 3 questions
        
        return None
    
    def should_clarify(self, task, skip_clarification: bool = False) -> bool:
        """Determine if task needs clarification.
        
        Args:
            task: Task object
            skip_clarification: Global skip flag
            
        Returns:
            True if clarification needed
        """
        if skip_clarification:
            return False
        
        complexity = self.analyze_complexity(task)
        return complexity in ["medium", "high"]
