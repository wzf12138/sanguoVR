#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VR 三国演武场 · 治理一致性校验脚本
=====================================
自动扫描 .trae/ 目录，校验文件完整性、链接有效性、Skill 唯一性、
active 门禁、五件套完整性、登记册交叉引用一致性。

用法：
  python check-integrity.py           # 终端彩色输出
  python check-integrity.py --json    # JSON 输出（供看板调用）
  python check-integrity.py --quiet   # 只输出失败项

退出码：0 = 全部通过，1 = 有失败项
"""
import json, os, re, sys, yaml
from pathlib import Path
from datetime import datetime

# ── 路径 ──────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
TRAE_ROOT = PROJECT_ROOT / ".trae"
FORBIDDEN_ROOT = PROJECT_ROOT.parent / ".trae"

# ── 颜色 ──────────────────────────────────────────────
class C:
    G = '\033[92m'  # green
    R = '\033[91m'  # red
    Y = '\033[93m'  # yellow
    D = '\033[90m'  # dim
    B = '\033[1m'   # bold
    X = '\033[0m'   # reset

# ── 结果收集 ──────────────────────────────────────────
results = []

def check(category, name, passed, detail=""):
    results.append({
        "category": category,
        "name": name,
        "passed": passed,
        "detail": detail,
    })

# ── 工具函数 ──────────────────────────────────────────
def read_yaml(path):
    p = Path(path)
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}

def read_json(path):
    p = Path(path)
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def read_text(path):
    p = Path(path)
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def find_md_files(root):
    """递归查找所有 .md 文件"""
    md_files = []
    for p in Path(root).rglob("*.md"):
        md_files.append(p)
    return md_files

def extract_md_links(filepath):
    """从 Markdown 文件中提取本地链接（排除 http/https）"""
    text = read_text(filepath)
    # 匹配 [text](path) 格式，排除 http、https、mailto
    pattern = r'\[([^\]]*)\]\(([^)]+)\)'
    links = []
    for match in re.finditer(pattern, text):
        link_text = match.group(1)
        link_target = match.group(2)
        if link_target.startswith(('http://', 'https://', 'mailto:', '#')):
            continue
        # 去掉锚点
        link_path = link_target.split('#')[0]
        if link_path:
            links.append((link_text, link_path, link_target))
    return links

def resolve_link(filepath, link_path):
    """解析相对链接，返回绝对路径"""
    base = Path(filepath).parent
    target = (base / link_path).resolve()
    return target

def parse_markdown_table(text):
    """解析 Markdown 表格，返回字典列表"""
    rows = []
    lines = text.strip().split("\n")
    if len(lines) < 2:
        return rows
    header_line = None
    for i, line in enumerate(lines):
        if i + 1 < len(lines) and "|" in line and "---" in lines[i + 1]:
            header_line = i
            break
    if header_line is None:
        return rows
    headers = [h.strip() for h in lines[header_line].split("|")[1:-1]]
    for line in lines[header_line + 2:]:
        if not line.strip().startswith("|"):
            break
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
    return rows


# ═══════════════════════════════════════════════════════
# 校验项
# ═══════════════════════════════════════════════════════

def check_forbidden_root():
    """1. 禁止根检查：项目父级不得存在 .trae/"""
    passed = not FORBIDDEN_ROOT.exists()
    detail = f"禁止路径 {FORBIDDEN_ROOT} {'存在（违规）' if not passed else '不存在（正常）'}"
    check("禁止根", "项目父级无 .trae/", passed, detail)

def check_manifest_files():
    """2. manifest.yaml 中声明的文件全部存在"""
    manifest = read_yaml(TRAE_ROOT / "manifest.yaml")
    all_paths = []
    all_paths.extend(manifest.get("indexes", {}).values())
    all_paths.extend(manifest.get("governance_contracts", []))
    all_paths.extend(manifest.get("operation_models", []))
    all_paths.append(manifest.get("rules", {}).get("authoritative", ""))
    all_paths.append(manifest.get("source_of_truth", ""))
    all_paths.append(manifest.get("active_gate", {}).get("status_file", ""))

    missing = []
    for p in all_paths:
        if not p:
            continue
        full = PROJECT_ROOT / p
        if not full.exists():
            missing.append(p)

    passed = len(missing) == 0
    detail = f"检查 {len(all_paths)} 个声明路径，缺失 {len(missing)} 个" + (f"：{missing}" if missing else "")
    check("文件完整性", "manifest.yaml 声明文件全部存在", passed, detail)

def check_collection_counts():
    """3. 集合数量校验：实际文件数 = manifest 声明数"""
    manifest = read_yaml(TRAE_ROOT / "manifest.yaml")
    collections = manifest.get("collections", {})

    checks = [
        ("task_templates", "execution/task-template*.md", 3, []),
        ("standards_indexed", "standards/[01]*-*.md", 10, ["index.md"]),
        ("vr_indexed", "vr/0*.md", 5, ["index.md"]),
        ("systems_guides", "systems/0*.md", 7, ["index.md"]),
        ("registers_core", "registers/[01]*-*.md", 11, ["index.md"]),
        ("production_specs", "knowledge/Production/*.md", 6, ["README.md"]),
        ("pattern_library", "knowledge/Patterns/README.md", 1, []),
        ("standards_backlog", "registers/standards-backlog.md", 1, []),
    ]

    for key, glob_pattern, expected, exclude_names in checks:
        expected_count = collections.get(key, expected)
        actual_files = list(TRAE_ROOT.glob(glob_pattern))
        # 排除指定的文件名（如 index.md）
        actual_files = [f for f in actual_files if f.name not in exclude_names]
        actual_count = len(actual_files)
        passed = actual_count == expected_count
        detail = f"期望 {expected_count}，实际 {actual_count}" + (f"：{[f.name for f in actual_files]}" if not passed else "")
        check("集合数量", f"{key} 文件数", passed, detail)

def check_lowercase_indexes():
    """4. 小写索引检查：必需目录使用 index.md 而非 README.md"""
    required_dirs = [
        "standards", "vr", "systems", "registers", "knowledge/Design"
    ]
    all_pass = True
    details = []
    for d in required_dirs:
        dir_path = TRAE_ROOT / d
        has_index = (dir_path / "index.md").exists()
        has_readme = (dir_path / "README.md").exists()
        if not has_index or has_readme:
            all_pass = False
            details.append(f"{d}: index.md={'有' if has_index else '无'}, README.md={'有' if has_readme else '无'}")

    # 特殊：.trae/README.md 是允许的（根入口）
    check("索引规范", "必需目录使用 index.md", all_pass,
          "全部使用 index.md" if all_pass else "; ".join(details))

def check_skill_frontmatter():
    """5. Skill 唯一性：.trae/skills/ 下仅一个带 YAML frontmatter 的 SKILL.md"""
    skills_dir = TRAE_ROOT / "skills"
    if not skills_dir.exists():
        check("Skill 唯一性", "skills 目录存在", False, "skills/ 目录不存在")
        return

    frontmatter_files = []
    for md_file in skills_dir.rglob("*.md"):
        text = read_text(md_file)
        if text.startswith("---"):
            # 检查是否有 YAML frontmatter
            end = text.find("\n---", 3)
            if end > 0:
                frontmatter = text[3:end]
                if "name:" in frontmatter or "description:" in frontmatter:
                    frontmatter_files.append(str(md_file.relative_to(TRAE_ROOT)))

    passed = len(frontmatter_files) == 1
    detail = f"找到 {len(frontmatter_files)} 个带 frontmatter 的 Skill 文件" + (f"：{frontmatter_files}" if frontmatter_files else "")
    check("Skill 唯一性", "仅一个带 frontmatter 的 SKILL.md", passed, detail)

def check_markdown_links():
    """6. Markdown 本地链接检查：所有 .md 文件中的本地链接可解析"""
    md_files = find_md_files(TRAE_ROOT)
    total_links = 0
    broken_links = []

    for md_file in md_files:
        links = extract_md_links(md_file)
        for link_text, link_path, link_target in links:
            total_links += 1
            resolved = resolve_link(md_file, link_path)
            if not resolved.exists():
                rel_md = md_file.relative_to(TRAE_ROOT)
                broken_links.append(f"{rel_md} → {link_target}")

    passed = len(broken_links) == 0
    detail = f"检查 {total_links} 个链接，断链 {len(broken_links)} 个"
    if broken_links:
        # 只显示前 10 个断链
        show = broken_links[:10]
        if len(broken_links) > 10:
            show.append(f"... 还有 {len(broken_links) - 10} 个")
        detail += "：" + "; ".join(show)
    check("链接完整性", "Markdown 本地链接无断链", passed, detail)

def check_active_gate():
    """7. active 门禁：STATUS.json 格式有效，activeTasks 数组完整"""
    status = read_json(TRAE_ROOT / "execution/active/STATUS.json")
    if not status:
        check("active 门禁", "STATUS.json 可读", False, "文件不存在或为空")
        return

    active_tasks = status.get("activeTasks", [])
    if not isinstance(active_tasks, list) or len(active_tasks) == 0:
        check("active 门禁", "activeTasks 数组非空", False, "activeTasks 为空或非数组")
        return

    issues = []
    for t in active_tasks:
        tid = t.get("taskId", "")
        tstatus = t.get("status", "")
        if not tid:
            issues.append(f"任务缺少 taskId")
        if tstatus not in ("draft", "ready", "in_progress", "blocked", "awaiting_review", "approved", "archived"):
            issues.append(f"{tid}: 非法状态 '{tstatus}'")

    passed = len(issues) == 0
    detail = f"{len(active_tasks)} 个 active 任务" + (f"，问题：{issues}" if issues else "，全部状态合法")
    check("active 门禁", "STATUS.json 格式与状态合法", passed, detail)

def check_five_piece_set():
    """8. 五件套完整性：每个 active 任务目录包含 5 个必需文件"""
    status = read_json(TRAE_ROOT / "execution/active/STATUS.json")
    active_tasks = status.get("activeTasks", [])
    required_files = ["TASK.md", "ALLOWLIST.txt", "INPUTS.md", "CHECKS.md", "STATUS.json"]

    all_pass = True
    details = []
    for t in active_tasks:
        tid = t.get("taskId", "")
        task_dir = TRAE_ROOT / "execution/active" / tid
        if not task_dir.exists():
            all_pass = False
            details.append(f"{tid}: 任务目录不存在")
            continue
        missing = [f for f in required_files if not (task_dir / f).exists()]
        if missing:
            all_pass = False
            details.append(f"{tid}: 缺失 {missing}")
        else:
            # 检查 ALLOWLIST.txt 至少有一行非空非注释
            allowlist = read_text(task_dir / "ALLOWLIST.txt")
            has_valid = any(
                line.strip() and not line.strip().startswith("#")
                for line in allowlist.split("\n")
            )
            if not has_valid:
                all_pass = False
                details.append(f"{tid}: ALLOWLIST.txt 无有效路径")

    check("五件套", "active 任务五件套完整", all_pass,
          "全部完整" if all_pass else "; ".join(details))

def check_allowlist_conflict():
    """9. 白名单冲突检测：in_progress 任务的 ALLOWLIST 无独占路径重叠"""
    status = read_json(TRAE_ROOT / "execution/active/STATUS.json")
    active_tasks = status.get("activeTasks", [])

    # 收集 in_progress 任务的白名单
    task_paths = {}
    for t in active_tasks:
        if t.get("status") != "in_progress":
            continue
        tid = t.get("taskId", "")
        allowlist_path = TRAE_ROOT / "execution/active" / tid / "ALLOWLIST.txt"
        if not allowlist_path.exists():
            continue
        text = read_text(allowlist_path)
        paths = set()
        for line in text.split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                paths.add(line)
        task_paths[tid] = paths

    # 共享文件（不算冲突）
    shared = {
        ".trae/CHANGELOG.md",
        ".trae/integrity.yaml",
        ".trae/manifest.yaml",
        ".trae/execution/active/STATUS.json",
        "Intermediate/**",
        "Binaries/**",
    }
    # 登记册也是共享的
    for reg in (TRAE_ROOT / "registers").glob("*.md"):
        shared.add(f".trae/registers/{reg.name}")

    conflicts = []
    task_ids = list(task_paths.keys())
    for i, t1 in enumerate(task_ids):
        for t2 in task_ids[i+1:]:
            overlap = (task_paths[t1] - shared) & (task_paths[t2] - shared)
            if overlap:
                conflicts.append(f"{t1} ∩ {t2}: {overlap}")

    passed = len(conflicts) == 0
    detail = f"{len(task_paths)} 个 in_progress 任务" + (f"，冲突：{conflicts}" if conflicts else "，无路径冲突")
    check("白名单冲突", "in_progress 任务无独占路径重叠", passed, detail)

def check_task_register_consistency():
    """10. 任务登记册一致性：STATUS.json 中的任务状态与 07-task-register.md 一致"""
    status = read_json(TRAE_ROOT / "execution/active/STATUS.json")
    active_tasks = status.get("activeTasks", [])

    task_reg_text = read_text(TRAE_ROOT / "registers/07-task-register.md")
    task_reg = parse_markdown_table(task_reg_text)

    # 构建 任务登记册 的任务 ID → 状态文本 映射
    reg_map = {}
    for row in task_reg:
        tid = row.get("任务", "")
        tstatus = row.get("状态", "")
        reg_map[tid] = tstatus

    issues = []
    for t in active_tasks:
        tid = t.get("taskId", "")
        json_status = t.get("status", "")
        reg_status = reg_map.get(tid, "")

        if not reg_status:
            issues.append(f"{tid}: 任务登记册中无此任务")
            continue

        # 宽松匹配：登记册状态文本中包含 STATUS.json 的状态关键字
        status_keywords = {
            "blocked": ["blocked", "阻塞"],
            "ready": ["ready", "待认领"],
            "in_progress": ["in_progress", "执行中"],
            "awaiting_review": ["awaiting", "待审核"],
            "approved": ["approved", "已验证", "已批准", "已实施"],
        }
        keywords = status_keywords.get(json_status, [json_status])
        matched = any(kw.lower() in reg_status.lower() for kw in keywords)

        if not matched:
            issues.append(f"{tid}: STATUS.json='{json_status}' vs 登记册='{reg_status}'")

    passed = len(issues) == 0
    detail = f"检查 {len(active_tasks)} 个任务" + (f"，不一致：{issues}" if issues else "，全部一致")
    check("交叉引用", "STATUS.json 与任务登记册一致", passed, detail)

def check_verification_evidence():
    """11. 验证证据存在性：验证登记册中引用的证据文件路径存在"""
    verif_text = read_text(TRAE_ROOT / "registers/09-verification-register.md")
    verif_reg = parse_markdown_table(verif_text)

    issues = []
    checked = 0
    for row in verif_reg:
        vid = row.get("ID", "")
        evidence = row.get("证据", "")
        if not evidence:
            continue
        checked += 1
        # 从证据文本中提取 .trae/ 路径
        paths = re.findall(r'\.trae/[^\s,;，；）)]+', evidence)
        for p in paths:
            full = PROJECT_ROOT / p
            if not full.exists():
                issues.append(f"{vid}: 证据路径不存在 {p}")

    passed = len(issues) == 0
    detail = f"检查 {checked} 项验证证据" + (f"，缺失：{issues}" if issues else "，全部存在")
    check("交叉引用", "验证证据文件路径存在", passed, detail)

def check_task_verif_consistency():
    """12b. 任务登记与验证登记交叉一致性：任务状态与验证登记状态不矛盾"""
    task_reg_text = read_text(TRAE_ROOT / "registers/07-task-register.md")
    task_reg = parse_markdown_table(task_reg_text)
    verif_text = read_text(TRAE_ROOT / "registers/09-verification-register.md")
    verif_reg = parse_markdown_table(verif_text)

    task_status = {t.get("任务", ""): t.get("状态", "") for t in task_reg}
    issues = []
    for v in verif_reg:
        vid = v.get("ID", "")
        v_status = v.get("状态", "")
        v_task = v.get("关联任务", "")
        if v_task and v_task in task_status:
            t_status = task_status[v_task]
            if "已验证" in t_status and "已验证" not in v_status and "通过" not in v_status:
                issues.append(f"{v_task} 任务标记已验证，但验证登记 {vid} 状态为 {v_status}")
            elif "已验证" not in t_status and "approved" not in t_status.lower() and ("已验证" in v_status or "通过" in v_status):
                issues.append(f"{v_task} 验证登记 {vid} 标记已验证，但任务状态为 {t_status}")

    passed = len(issues) == 0
    detail = f"检查 {len(verif_reg)} 项验证登记" + (f"，不一致：{issues}" if issues else "，全部一致")
    check("交叉引用", "任务登记与验证登记状态一致", passed, detail)


def check_tech_debt_status():
    """12. 技术债检查：统计 open 状态的技术债数量"""
    debt_text = read_text(TRAE_ROOT / "registers/11-tech-debt-register.md")
    debt_reg = parse_markdown_table(debt_text)

    open_count = 0
    for row in debt_reg:
        status = row.get("状态", "")
        if "open" in status.lower():
            open_count += 1

    # open 数量 >3 为红色，1-3 为黄色，0 为绿色
    passed = open_count <= 3
    detail = f"{len(debt_reg)} 条技术债，{open_count} 条 open"
    check("技术债", "open 技术债 <= 3", passed, detail)

def check_awaiting_review_timeout():
    """13. 待审核超时：awaiting_review 状态超过 24 小时告警"""
    status = read_json(TRAE_ROOT / "execution/active/STATUS.json")
    active_tasks = status.get("activeTasks", [])

    now = datetime.now()
    timeouts = []
    for t in active_tasks:
        if t.get("status") != "awaiting_review":
            continue
        updated = t.get("updatedAt", "")
        if not updated:
            continue
        try:
            dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
            # 去掉时区信息用于比较
            dt = dt.replace(tzinfo=None)
            hours = (now - dt).total_seconds() / 3600
            if hours > 24:
                timeouts.append(f"{t.get('taskId', '')}: {hours:.1f}h")
        except (ValueError, TypeError):
            pass

    passed = len(timeouts) == 0
    detail = f"检查 awaiting_review 任务" + (f"，超时：{timeouts}" if timeouts else "，无超时")
    check("流程超时", "awaiting_review 不超过 24h", passed, detail)


# ═══════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════

def run_all_checks():
    """执行全部校验"""
    results.clear()

    # 1. 禁止根
    check_forbidden_root()
    # 2. manifest 文件存在性
    check_manifest_files()
    # 3. 集合数量
    check_collection_counts()
    # 4. 小写索引
    check_lowercase_indexes()
    # 5. Skill 唯一性
    check_skill_frontmatter()
    # 6. Markdown 链接
    check_markdown_links()
    # 7. active 门禁
    check_active_gate()
    # 8. 五件套
    check_five_piece_set()
    # 9. 白名单冲突
    check_allowlist_conflict()
    # 10. 任务登记册一致性
    check_task_register_consistency()
    # 11. 验证证据存在性
    check_verification_evidence()
    # 11b. 任务登记与验证登记交叉一致性
    check_task_verif_consistency()
    # 12. 技术债
    check_tech_debt_status()
    # 13. 待审核超时
    check_awaiting_review_timeout()

    return results

def print_terminal(results, quiet=False):
    """终端彩色输出"""
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed

    if not quiet:
        print(f"\n  {C.B}⚔ VR 三国演武场 · 治理一致性校验{C.X}")
        print(f"  {'─' * 50}")
        print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  路径: {TRAE_ROOT}\n")

    # 按类别分组
    categories = {}
    for r in results:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r)

    for cat, items in categories.items():
        if quiet:
            items = [r for r in items if not r["passed"]]
            if not items:
                continue
        print(f"  {C.B}{cat}{C.X}")
        for r in items:
            status = f"{C.G}✓{C.X}" if r["passed"] else f"{C.R}✗{C.X}"
            name = r["name"]
            detail = r["detail"]
            if r["passed"]:
                print(f"    {status} {name} {C.D}— {detail}{C.X}")
            else:
                print(f"    {status} {name}")
                print(f"      {C.R}{detail}{C.X}")

    print(f"\n  {'─' * 50}")
    color = C.G if failed == 0 else C.R
    print(f"  {C.B}总计:{C.X} {total} 项  {C.G}通过:{C.X} {passed}  {color}失败:{C.X} {failed}")

    if failed == 0:
        print(f"  {C.G}✓ 全部校验通过{C.X}\n")
    else:
        print(f"  {C.R}✗ 有 {failed} 项校验失败，请检查{C.X}\n")

    return failed

def print_json(results):
    """JSON 输出（供看板调用）"""
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed

    output = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "trae_root": str(TRAE_ROOT),
        "total": total,
        "passed": passed,
        "failed": failed,
        "overall": "pass" if failed == 0 else "fail",
        "checks": results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return failed

def main():
    # 检查 .trae/ 是否存在
    if not TRAE_ROOT.exists():
        print(f"{C.R}错误: .trae/ 目录不存在于 {TRAE_ROOT}{C.X}")
        sys.exit(1)

    # 检查依赖
    try:
        import yaml
    except ImportError:
        print(f"{C.Y}提示: 正在安装 PyYAML 依赖...{C.X}")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyYAML", "-q"])
        import yaml

    args = sys.argv[1:]
    results = run_all_checks()

    if "--json" in args:
        failed = print_json(results)
    elif "--quiet" in args:
        failed = print_terminal(results, quiet=True)
    else:
        failed = print_terminal(results)

    sys.exit(1 if failed > 0 else 0)

if __name__ == "__main__":
    main()
