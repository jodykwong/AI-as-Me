# AI-as-Me v3.3 Architecture - 规则版本管理

**创建日期**: 2026-01-15

---

## 1. 架构概览

```
┌─────────────────────────────────────────┐
│              CLI Layer                   │
│  ai-as-me rule [history|show|diff|rollback]
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│         RuleVersionManager               │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │save_ver │ │get_ver  │ │rollback │   │
│  └─────────┘ └─────────┘ └─────────┘   │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│           Storage Layer                  │
│  soul/rules/.versions/{rule}/           │
│    ├── v1.md, v2.md, ...                │
│    └── history.json                     │
└─────────────────────────────────────────┘
```

## 2. 数据模型

```python
@dataclass
class RuleVersion:
    version: int      # 版本号
    timestamp: str    # ISO8601
    reason: str       # 变更原因
    checksum: str     # MD5 前8位
```

## 3. 存储结构

```
soul/rules/
├── learned/
│   └── rule_001.md        # 当前版本
└── .versions/
    └── rule_001/
        ├── v1.md          # 历史版本
        ├── v2.md
        └── history.json   # 版本元数据
```

## 4. 核心方法

| 方法 | 功能 |
|------|------|
| save_version() | 保存当前版本 |
| get_history() | 获取版本历史 |
| get_version() | 获取特定版本内容 |
| diff() | 对比两个版本 (difflib) |
| rollback() | 回滚到指定版本 |
