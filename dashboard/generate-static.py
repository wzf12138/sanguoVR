#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VR 三国演武场 · 静态看板生成器
================================
从 .trae/ 治理文件生成静态 JSON 数据和 HTML 页面，用于 GitHub Pages 托管。
本地无需运行任何进程，所有数据在 push 时由 GitHub Actions 自动生成。

生成文件：
  - status.json    : 全部看板数据（任务/风险/决策/资产/健康度等）
  - integrity.json : check-integrity.py 校验结果
  - index.html     : 静态看板页面（fetch 相对路径 JSON）

用法：
  python generate-static.py
"""
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
TRAE_ROOT = PROJECT_ROOT / ".trae"

# 导入 server.py 的数据构建函数
sys.path.insert(0, str(SCRIPT_DIR))
import server
import asset_scanner


def generate_status_json():
    """生成 status.json — 包含所有看板数据"""
    data = server.build_api_data()
    output_path = SCRIPT_DIR / "status.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    size_kb = round(output_path.stat().st_size / 1024, 1)
    print(f"  ✓ status.json ({size_kb}KB)")
    return data


def generate_integrity_json():
    """生成 integrity.json — 校验脚本结果"""
    output_path = SCRIPT_DIR / "integrity.json"
    try:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "check-integrity.py"), "--json"],
            capture_output=True, text=True, timeout=30
        )
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.stdout)
        data = json.loads(result.stdout)
        print(f"  ✓ integrity.json (通过 {data.get('passed', 0)}/{data.get('total', 0)})")
    except Exception as e:
        error = {
            "error": str(e), "overall": "fail", "checks": [],
            "passed": 0, "failed": 0, "total": 0,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(error, f, ensure_ascii=False, indent=2)
        print(f"  ✗ integrity.json (错误: {e})")


def generate_index_html(generated_at):
    """生成静态 index.html — 修改 fetch 路径为相对路径，移除自动刷新"""
    html = server.DASHBOARD_HTML

    # 1. 替换 API 调用为静态 JSON 文件
    html = html.replace("fetch('/api/status')", "fetch('status.json')")
    html = html.replace("fetch('/api/integrity')", "fetch('integrity.json')")

    # 2. 移除自动刷新（静态页面数据在 push 时更新）
    html = html.replace(
        "setInterval(load, 300000);",
        "// 静态模式：数据在 GitHub push 时更新，无需自动刷新"
    )

    # 3. 修改"下次刷新"为"最后更新"
    html = html.replace(
        "const next = new Date(Date.now() + REFRESH_MIN * 60000);\n"
        "  document.getElementById('nextRefresh').textContent =\n"
        "    String(next.getHours()).padStart(2,'0') + ':' + String(next.getMinutes()).padStart(2,'0');",
        "document.getElementById('nextRefresh').textContent = 'push 时更新';"
    )

    # 4. 修改"立即刷新"按钮为 GitHub 仓库链接
    html = html.replace(
        '<button onclick="location.reload()">立即刷新</button>',
        '<a href="https://github.com/AWork-Unreal/VRSanguoYanWuchang" target="_blank" '
        'style="color:var(--gold);text-decoration:none;font-size:0.75rem;">'
        '查看仓库 →</a>'
    )

    # 5. 更新页脚说明
    html = html.replace(
        "VR 三国演武场 · 治理驱动开发 · 数据源 .trae/ · 零虚构数据",
        f"VR 三国演武场 · 治理驱动开发 · GitHub Pages 静态看板 · 生成于 {generated_at}"
    )

    output_path = SCRIPT_DIR / "index.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    size_kb = round(output_path.stat().st_size / 1024, 1)
    print(f"  ✓ index.html ({size_kb}KB)")


def main():
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n  ⚔  VR 三国演武场 - 静态看板生成器")
    print(f"  ──────────────────────────────────────")
    print(f"  数据源: {TRAE_ROOT}")
    print(f"  输出:   {SCRIPT_DIR}")
    print(f"  时间:   {generated_at}")
    print()

    generate_status_json()
    generate_integrity_json()
    generate_index_html(generated_at)

    print(f"\n  ✅ 静态看板已生成")
    print(f"  部署到 GitHub Pages 后访问:")
    print(f"  https://<username>.github.io/VRSanguoYanWuchang/")


if __name__ == "__main__":
    main()
