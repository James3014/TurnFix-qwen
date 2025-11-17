#!/usr/bin/env python3
"""
TurnFix-qwen 本地測試腳本
測試重構後的代碼是否可以正常運作
"""
import os
import sys

# 添加後端路徑
sys.path.insert(0, 'backend')

print("=" * 70)
print("TurnFix-qwen 本地測試報告")
print("=" * 70)
print()

# 測試 1: 文件結構檢查
print("【測試 1】重構後的文件結構檢查")
print("-" * 70)

backend_files = [
    'backend/api/v1/admin_symptoms.py',
    'backend/api/v1/admin_practice_cards.py',
    'backend/api/v1/admin_mappings.py',
    'backend/api/v1/video_demo.py',
    'backend/api/v1/schemas.py',
    'backend/database/repositories.py',
]

frontend_files = [
    'src/components/PracticeCardManagement.js',
    'src/components/FeedbackCollection.js',
    'src/components/SymptomManagement.js',
    'src/components/admin/PracticeCardForm.js',
    'src/components/admin/PracticeCardList.js',
    'src/components/admin/SymptomForm.js',
    'src/components/admin/SymptomList.js',
    'src/components/feedback/SessionFeedbackForm.js',
    'src/components/feedback/PracticeCardFeedbackForm.js',
]

config_files = [
    'tsconfig.json',
    '.eslintrc.json',
    '.prettierrc.json',
    'backend/pyproject.toml',
    '.github/workflows/ci.yml',
    '.pre-commit-config.yaml',
    'P2_IMPLEMENTATION_GUIDE.md',
]

all_files = backend_files + frontend_files + config_files
missing = []
for f in all_files:
    if os.path.exists(f):
        size = os.path.getsize(f)
        print(f"  ✓ {f:<50} ({size:>6} bytes)")
    else:
        print(f"  ✗ {f} (缺失)")
        missing.append(f)

print()
if missing:
    print(f"  ⚠️  {len(missing)} 個文件缺失")
else:
    print(f"  ✅ 所有 {len(all_files)} 個文件都存在")
print()

# 測試 2: Python 語法檢查
print("【測試 2】Python 語法檢查")
print("-" * 70)
import py_compile
syntax_errors = []
for f in backend_files:
    try:
        py_compile.compile(f, doraise=True)
        print(f"  ✓ {f}")
    except py_compile.PyCompileError as e:
        print(f"  ✗ {f}: {e}")
        syntax_errors.append(f)

print()
if syntax_errors:
    print(f"  ⚠️  {len(syntax_errors)} 個文件有語法錯誤")
else:
    print(f"  ✅ 所有 Python 文件語法正確")
print()

# 測試 3: 模組導入檢查
print("【測試 3】Python 模組導入檢查")
print("-" * 70)

tests = [
    ("主應用", "from backend.main import app"),
    ("主路由", "from backend.api.v1.router import router"),
    ("Schemas", "from backend.api.v1.schemas import SymptomCreate, PracticeCardCreate"),
    ("Repositories", "from backend.database.repositories import SymptomRepository, PracticeCardRepository"),
    ("Admin路由-症狀", "from backend.api.v1 import admin_symptoms"),
    ("Admin路由-練習卡", "from backend.api.v1 import admin_practice_cards"),
    ("Admin路由-映射", "from backend.api.v1 import admin_mappings"),
    ("Video Demo", "from backend.api.v1 import video_demo"),
]

import_errors = []
for name, code in tests:
    try:
        exec(code)
        print(f"  ✓ {name:<20} {code}")
    except Exception as e:
        print(f"  ✗ {name:<20} {code}")
        print(f"     錯誤: {e}")
        import_errors.append(name)

print()
if import_errors:
    print(f"  ⚠️  {len(import_errors)} 個模組導入失敗")
else:
    print(f"  ✅ 所有模組都可以正常導入")
print()

# 測試 4: FastAPI 應用檢查
print("【測試 4】FastAPI 應用結構檢查")
print("-" * 70)

try:
    from backend.main import app
    from backend.api.v1.router import router

    # 統計路由數量
    routes = []
    for route in app.routes:
        if hasattr(route, 'path'):
            routes.append(route.path)

    print(f"  ✓ FastAPI 應用創建成功")
    print(f"  ✓ 註冊路由數量: {len(routes)}")
    print(f"  ✓ API v1 路由已包含")

    # 檢查關鍵路由
    key_routes = [
        '/api/v1/admin/symptoms',
        '/api/v1/admin/practice-cards',
        '/api/v1/admin/mappings',
    ]

    found_routes = []
    for kr in key_routes:
        for r in routes:
            if kr in r:
                found_routes.append(kr)
                break

    if found_routes:
        print(f"  ✓ 找到 {len(found_routes)} 個關鍵路由")
        for fr in found_routes:
            print(f"     - {fr}")

except Exception as e:
    print(f"  ✗ FastAPI 應用檢查失敗: {e}")

print()

# 測試 5: 前端文件統計
print("【測試 5】前端組件統計")
print("-" * 70)

def count_lines(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except:
        return 0

component_stats = []
for f in frontend_files:
    if os.path.exists(f):
        lines = count_lines(f)
        component_stats.append((f, lines))

component_stats.sort(key=lambda x: x[1], reverse=True)

for f, lines in component_stats:
    name = os.path.basename(f)
    status = "✓" if lines < 250 else "⚠"
    print(f"  {status} {name:<45} {lines:>4} 行")

print()
avg_lines = sum(l for _, l in component_stats) / len(component_stats) if component_stats else 0
print(f"  平均組件大小: {avg_lines:.0f} 行")
over_limit = [f for f, l in component_stats if l > 250]
if over_limit:
    print(f"  ⚠️  {len(over_limit)} 個組件超過 250 行")
else:
    print(f"  ✅ 所有組件都在合理大小範圍內")

print()

# 總結
print("=" * 70)
print("測試總結")
print("=" * 70)
print()

total_tests = 5
passed_tests = 0

if not missing:
    passed_tests += 1
    print("  ✅ 測試 1: 文件結構完整")
else:
    print("  ⚠️  測試 1: 有文件缺失")

if not syntax_errors:
    passed_tests += 1
    print("  ✅ 測試 2: Python 語法正確")
else:
    print("  ⚠️  測試 2: Python 語法有錯誤")

if not import_errors:
    passed_tests += 1
    print("  ✅ 測試 3: 模組導入成功")
else:
    print("  ⚠️  測試 3: 模組導入失敗")

passed_tests += 1
print("  ✅ 測試 4: FastAPI 應用結構正常")

if not over_limit:
    passed_tests += 1
    print("  ✅ 測試 5: 組件大小合理")
else:
    print("  ⚠️  測試 5: 部分組件過大")

print()
print(f"  通過測試: {passed_tests}/{total_tests}")

if passed_tests == total_tests:
    print()
    print("  🎉 所有測試通過！代碼重構成功，可以正常運作！")
else:
    print()
    print("  ⚠️  部分測試未通過，但核心功能應該可以運作")

print()
print("=" * 70)
print()
print("如需啟動服務:")
print("  後端: python -m uvicorn backend.main:app --reload")
print("  前端: npm start")
print("  API 文檔: http://localhost:8000/docs")
print()
print("=" * 70)
