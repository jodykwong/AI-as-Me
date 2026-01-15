# AI-as-Me v3.3 PRD - 规则版本管理

**创建日期**: 2026-01-15  
**状态**: Draft

---

## 1. 目标
为 Soul 规则提供完整的版本控制能力，支持变更追踪、回滚和差异对比。

---

## 2. 功能需求

### 2.1 版本记录
- 每次规则修改自动创建版本
- 版本号：v1, v2, v3...
- 记录：时间戳、变更原因、变更内容

### 2.2 版本查询
- 查看规则历史版本列表
- 查看特定版本内容
- 对比两个版本差异

### 2.3 版本回滚
- 一键回滚到任意历史版本
- 回滚后创建新版本记录

---

## 3. CLI 命令

```bash
ai-as-me rule history <rule_path>     # 查看版本历史
ai-as-me rule show <rule_path> --version 2  # 查看特定版本
ai-as-me rule diff <rule_path> --v1 1 --v2 3  # 对比版本
ai-as-me rule rollback <rule_path> --to 2     # 回滚
```

---

## 4. 存储设计

```
soul/rules/
├── learned/
│   └── rule_001.md           # 当前版本
└── .versions/
    └── rule_001/
        ├── v1.md
        ├── v2.md
        └── history.json      # 版本元数据
```
