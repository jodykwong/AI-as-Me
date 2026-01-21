# Test Architecture

**Version**: 1.0 | **Date**: 2026-01-22

## Testing Pyramid
```
     /E2E\      10%
    /Integr\    20%
   /  Unit  \   70%
```

## Test Levels

### Unit Tests (70%)
- Location: `tests/unit/`
- Coverage: 80%+
- Framework: pytest

### Integration Tests (20%)
- Location: `tests/integration/`
- Test component interactions

### E2E Tests (10%)
- Location: `tests/e2e/`
- Test complete workflows

## TDD with Ralph
1. Red: Write failing test
2. Green: Implement minimal code
3. Refactor: Improve quality

Run: `ralph run -c ralph-test.yml`

## Coverage Requirements
- soul/: 80% (current: 85%) ✅
- kanban/: 80% (current: 75%) ⚠️
- agents/: 80% (current: 70%) ⚠️
- evolution/: 80% (current: 65%) ❌
- Overall: 75% (current: 70%) ⚠️

## Best Practices
- Test one thing per test
- Use descriptive names
- Keep tests fast (< 1s)
- Mock external dependencies
- Clean up after tests
