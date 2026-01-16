#!/usr/bin/env python3
"""v3.4.3 E2E 验证测试"""
import requests
import sys

BASE_URL = "http://localhost:8000"
results = []

def test(name, url, expect_json=True):
    try:
        r = requests.get(f"{BASE_URL}{url}", timeout=5)
        if r.status_code == 200:
            if expect_json:
                r.json()
            results.append((name, True, "OK"))
            print(f"✅ {name}")
        else:
            results.append((name, False, f"Status {r.status_code}"))
            print(f"❌ {name} - Status {r.status_code}")
    except Exception as e:
        results.append((name, False, str(e)))
        print(f"❌ {name} - {e}")

print("=" * 60)
print("🧪 v3.4.3 E2E 验证测试")
print("=" * 60)

# API Tests
test("健康检查", "/health")
test("Kanban 看板", "/api/kanban/board")
test("Soul 状态", "/api/soul/status")

# Page Tests
test("首页", "/", expect_json=False)
test("Kanban 页面", "/kanban.html", expect_json=False)
test("Soul 页面", "/soul.html", expect_json=False)
test("灵感池页面", "/inspirations.html", expect_json=False)
test("规则管理页面", "/rules.html", expect_json=False)
test("统计页面", "/stats.html", expect_json=False)
test("日志页面", "/logs.html", expect_json=False)

# Summary
print("\n" + "=" * 60)
print("📊 验证结果汇总")
print("=" * 60)
passed = sum(1 for _, ok, _ in results if ok)
total = len(results)
for name, ok, msg in results:
    status = "✅ PASS" if ok else f"❌ FAIL - {msg}"
    print(f"{status} - {name}")

print(f"\n总计: {passed}/{total} 通过 ({passed*100//total}%)")
sys.exit(0 if passed == total else 1)
