---
title: AI-as-Me Product Requirements Document
version: 3.5.0
status: Active
last_updated: 2026-01-22
---

# AI-as-Me PRD

## Executive Summary
Self-evolving AI digital twin that learns from interactions and manages tasks intelligently.

## Core Features

### 1. Soul System
- Profile, Mission, Rules (Core/Learned/Archived)
- FR-1.1: Require approval before modifying soul
- FR-1.2: Log all changes
- FR-1.3: Rules have metadata
- FR-1.4: Enforce file permissions (700/600)

### 2. Kanban System
- States: Inbox → Todo → Doing → Done
- FR-2.1: Tasks as markdown files
- FR-2.2: Support metadata (ID, status, tags)
- FR-2.3: Unique task IDs
- FR-2.4: Track task history

### 3. Agent System
- OpenCode (primary), Claude Code (optional)
- FR-3.1: Multiple agent backends
- FR-3.2: Isolated execution
- FR-3.3: Log all calls
- FR-3.4: Graceful failure handling

### 4. Evolution System
- Pattern detection → Rule generation → Validation → Approval
- FR-4.1: Detect recurring patterns
- FR-4.2: Generate rules automatically
- FR-4.3: Safety validation
- FR-4.4: User approval required

### 5. Dashboard
- Home, Kanban, Soul, Agents, Logs
- FR-5.1: Responsive design
- FR-5.2: Real-time updates
- FR-5.3: Drag-and-drop
- FR-5.4: < 1s page load

## Non-Functional Requirements
- NFR-1: Dashboard < 1s response
- NFR-2: API < 200ms (p95)
- NFR-3: Memory < 500MB
- NFR-5: Validate all inputs
- NFR-6: No SQL injection
- NFR-15: Code coverage > 70%

## Success Metrics
- 1,000 users in 6 months
- 70%+ rule effectiveness
- 90%+ task completion
