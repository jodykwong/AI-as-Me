"""Tests for First Evolution Demo."""
import pytest
from ai_as_me.demo import FirstEvolutionDemo


@pytest.mark.asyncio
async def test_demo_run():
    """测试 Demo 完整流程."""
    demo = FirstEvolutionDemo()
    result = await demo.run()
    
    assert result["success"] is True
    assert "rule_path" in result
    assert "rule_name" in result


@pytest.mark.asyncio
async def test_sample_task():
    """测试示例任务."""
    from ai_as_me.demo.sample_task import SampleTask
    
    task = SampleTask()
    result = await task.execute()
    
    assert result["task"] == "check_python_dependencies"
    assert result["success"] is True


def test_progress_tracker():
    """测试进度追踪器."""
    from ai_as_me.demo.progress_tracker import ProgressTracker
    
    tracker = ProgressTracker(total_steps=5)
    tracker.update(1, "测试步骤 1")
    tracker.complete(1)
    
    assert tracker.current_step == 1
