"""Stats Visualizer - 统计可视化."""
from typing import Dict, List


class StatsVisualizer:
    """统计可视化生成器."""
    
    def render_ascii_bar(self, data: Dict[str, float], max_width: int = 40) -> str:
        """渲染 ASCII 条形图."""
        if not data:
            return "无数据"
        
        max_val = max(data.values())
        lines = []
        
        for key, val in sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]:
            bar_len = int((val / max_val) * max_width) if max_val > 0 else 0
            bar = "█" * bar_len
            lines.append(f"{key[:20]:20} {bar} {val:.2f}")
        
        return "\n".join(lines)
    
    def render_ascii_trend(self, scores: Dict[str, float]) -> str:
        """渲染有效性评分."""
        if not scores:
            return "无数据"
        
        lines = []
        for rule, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]:
            stars = "★" * int(score * 5)
            lines.append(f"{rule[:20]:20} {stars} {score:.2f}")
        
        return "\n".join(lines)
    
    def generate_heatmap(self, frequency_data: Dict[str, float]) -> dict:
        """生成应用热力图数据."""
        return {
            "type": "heatmap",
            "data": [
                {"rule": rule, "frequency": freq, "percentage": freq * 100}
                for rule, freq in sorted(
                    frequency_data.items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )
            ]
        }
    
    def generate_trend_chart(self, effectiveness_data: Dict[str, float]) -> dict:
        """生成有效性趋势图数据."""
        return {
            "type": "line",
            "data": [
                {"rule": rule, "effectiveness": score}
                for rule, score in effectiveness_data.items()
            ]
        }
    
    def generate_timeline(self, log_entries: List[dict]) -> dict:
        """生成进化时间线数据."""
        return {
            "type": "timeline",
            "events": [
                {
                    "timestamp": entry.get("timestamp"),
                    "event": entry.get("event"),
                    "rule_id": entry.get("rule_id")
                }
                for entry in log_entries
            ]
        }
