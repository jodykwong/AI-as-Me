"""Tests for inspiration module."""
import pytest
from pathlib import Path
from ai_as_me.inspiration import (
    Inspiration,
    InspirationPool,
    InspirationCapturer,
    InspirationIncubator,
)


@pytest.fixture
def temp_pool(tmp_path):
    """创建临时灵感池."""
    return InspirationPool(tmp_path / "inspiration")


def test_inspiration_model():
    """测试灵感数据模型."""
    insp = Inspiration(content="测试灵感", priority="high")
    
    assert insp.content == "测试灵感"
    assert insp.priority == "high"
    assert insp.status == "incubating"
    assert insp.maturity == 0.0


def test_inspiration_serialization():
    """测试序列化."""
    insp = Inspiration(content="测试", tags=["tag1"])
    json_str = insp.to_json()
    
    assert "测试" in json_str
    assert "tag1" in json_str


def test_pool_add_and_get(temp_pool):
    """测试灵感池添加和获取."""
    insp = Inspiration(content="池测试")
    insp_id = temp_pool.add(insp)
    
    retrieved = temp_pool.get(insp_id)
    assert retrieved is not None
    assert retrieved.content == "池测试"


def test_pool_list(temp_pool):
    """测试灵感池列表."""
    temp_pool.add(Inspiration(content="灵感1"))
    temp_pool.add(Inspiration(content="灵感2"))
    
    all_insp = temp_pool.list()
    assert len(all_insp) == 2


def test_capturer_from_text():
    """测试文本捕获."""
    capturer = InspirationCapturer()
    
    # 应该捕获
    insp = capturer.capture_from_text("以后可以添加语音支持")
    assert insp is not None
    assert "语音" in insp.content
    
    # 不应该捕获
    insp2 = capturer.capture_from_text("今天天气不错")
    assert insp2 is None


def test_capturer_priority():
    """测试优先级推断."""
    capturer = InspirationCapturer()
    
    high = capturer.capture_from_text("紧急：以后要修复这个bug")
    assert high.priority == "high"
    
    low = capturer.capture_from_text("有空以后可以优化一下")
    assert low.priority == "low"


def test_incubator_maturity(temp_pool):
    """测试成熟度计算."""
    insp = Inspiration(content="测试", priority="high", mentions=3)
    temp_pool.add(insp)
    
    incubator = InspirationIncubator(temp_pool)
    maturity = incubator.calculate_maturity(insp)
    
    # high priority (0.3) + 3 mentions (0.3) = 0.6
    assert maturity >= 0.5
