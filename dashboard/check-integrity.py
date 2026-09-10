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
  python check-integrity.py --quiet   # 只输出失败/警告项

退出码：0 = 无失败项，1 = 有失败项（warn 不影响退出码）

── 稳定性约定（2026-09-10 加固）──────────────────────
1. 每个检查都有稳定 id（英文小写下划线）。id 一经发布不得变更；
   category / name 中文文案同样不得改动 —— dashboard/server.py 用中文名取结果。
2. severity 三态：pass / warn / fail。
   - warn 不增加 failed 计数、不改变退出码，但终端与 JSON 均显式显示并汇总。
   - 兼容字段 passed=True 当且仅当 severity == "pass"（旧语义：未失败）。
3. run_all_checks() 对每个检查单独 try/except：任何检查内部异常都记为该检查
   fail 并写明异常类型与消息，绝不静默、绝不让整轮零输出。
   （2026-09-10 18:15 事故：根 STATUS.json 被写坏 → 脚本 traceback → 整轮无输出。）
"""
import json, os, re, sys, subprocess
from pathlib import Path
from datetime import datetime

# PyYAML 的加载必须放在模块级：任何以 import / 直接调用 run_all_checks() 方式
# 使用本模块的调用方（看板、测试、其他工具）都不会执行 main()。若只在 main() 里
# 设置该名字，read_yaml 会抛 NameError —— 而 NameError 会被误判成数据源损坏。
# 这里先做无副作用的尝试导入；pip 兜底仍留在 main() 中。
try:
    import yaml
except ImportError:  # pragma: no cover - 环境缺依赖时的降级路径
    yaml = None

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

# PyYAML 是否可用（由 main() 设置）。缺依赖时 read_yaml 逐项报错，
# 不硬崩，也不静默放行。
YAML_ERROR = None

SEVERITY_ORDER = {"fail": 0, "warn": 1, "pass": 2}


def check(category, name, passed=True, detail="", check_id="", severity=None):
    """记录一条检查结果。

    passed:  向后兼容的布尔量。True → pass，False → fail。
    severity: "pass" / "warn" / "fail"，优先于 passed。
    """
    if severity is None:
        severity = "pass" if passed else "fail"
    if severity not in SEVERITY_ORDER:
        severity = "fail"
    results.append({
        "category": category,
        "name": name,
        "passed": severity == "pass",
        "detail": detail,
        "id": check_id,
        "severity": severity,
    })


# ── 工具函数 ──────────────────────────────────────────
def read_yaml(path):
    """读 YAML。缺文件返回 {}（与历史行为一致）；解析异常直接抛出，由调用者处理。"""
    p = Path(path)
    if p.exists():
        if YAML_ERROR is not None:
            raise RuntimeError(f"PyYAML 不可用：{YAML_ERROR}")
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


def rel_to_root(p):
    """尽量给出相对项目根的路径，便于人读。"""
    try:
        return str(Path(p).relative_to(PROJECT_ROOT))
    except ValueError:
        return str(p)


def ensure_yaml_ready():
    """依赖自检：PyYAML 不可用时**不**自动安装，只登记错误。

    模块级函数，**不 import yaml、不赋值裸名 yaml**，避免把 yaml 变成调用方的
    局部变量（那会在未走到赋值分支时抛 UnboundLocalError）。

    这里刻意移除了早期的 `pip install PyYAML` 兜底：D 盘/项目外写盘与联网安装
    既违反项目「禁止写入 C 盘或用户主目录 / 禁止默认下载」的磁盘规则，也会在
    离线环境挂死。缺依赖时改为设置 YAML_ERROR，由各消费 YAML 的检查各自判 fail
    —— 数据源/依赖不可读 = fail，不静默放行，也不整轮零输出。
    返回 True 表示 yaml 可用。
    """
    global YAML_ERROR
    if yaml is not None:
        YAML_ERROR = None
        return True
    YAML_ERROR = "PyYAML 未安装（脚本不自动安装；请在工具链环境预装 PyYAML）"
    print(f"{C.R}警告: {YAML_ERROR}，依赖 YAML 的检查将判定失败{C.X}")
    return False


def data_error(path, data):
    """数据源可读性判定。

    返回 None 表示可读；否则返回中文错误描述。
    缺文件与解析失败都必须显式上报 —— 否则消费它的检查会拿空数据判定通过。
    """
    p = Path(path)
    if not p.exists():
        return f"数据源缺失：{rel_to_root(p)}"
    if data is None:
        return f"数据源不可解析（内容为空或非法）：{rel_to_root(p)}"
    if isinstance(data, (dict, list)) and len(data) == 0:
        return f"数据源为空：{rel_to_root(p)}"
    return None


def load_json_checked(path):
    """读 JSON，返回 (data, error)。error 非 None 表示不可用。"""
    p = Path(path)
    if not p.exists():
        return {}, f"数据源缺失：{rel_to_root(p)}"
    try:
        data = read_json(p)
    except Exception as e:
        return {}, f"数据源 JSON 解析失败：{rel_to_root(p)}（{type(e).__name__}: {e}）"
    err = data_error(p, data)
    return data, err


def load_yaml_checked(path):
    """读 YAML，返回 (data, error)。error 非 None 表示不可用。"""
    p = Path(path)
    if not p.exists():
        return {}, f"数据源缺失：{rel_to_root(p)}"
    try:
        data = read_yaml(p)
    except Exception as e:
        return {}, f"数据源 YAML 解析失败：{rel_to_root(p)}（{type(e).__name__}: {e}）"
    err = data_error(p, data)
    return data, err


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


# ── 五方状态归一化词表（机器可读，取代子串猜测）────────
# 顺序即优先级：终态词先判，避免描述正文里的 "blocked" 等历史字样污染终态行。
STATUS_VOCAB = [
    ("approved", ("approved", "已批准", "已验证", "已实施")),
    ("in_progress", ("in_progress", "执行中", "进行中")),
    ("ready", ("ready", "待认领", "待生成")),
    ("blocked", ("blocked", "阻塞")),
    ("awaiting_review", ("awaiting_review", "awaiting", "待审核")),
    ("draft", ("draft",)),
    ("archived", ("archived",)),
]
TERMINAL_STATES = ("approved", "archived")
STATUS_CODES = [c for c, _ in STATUS_VOCAB] + ["unknown"]


def normalize_status(raw):
    """把各源的状态原文归一化到统一词表；归一化不出来返回 'unknown'。"""
    low = (raw or "").lower()
    for canon, keywords in STATUS_VOCAB:
        for kw in keywords:
            if kw.lower() in low:
                return canon
    return "unknown"


SESSION_ID_RE = re.compile(r"^session-\d{8}-\d{3,}$")

# ── git HEAD（用于看板判断门禁结果新鲜度）─────────────
_git_head_cache = None
_git_ok = None


def _git_available():
    """git 是否可用（结果缓存，避免重复起子进程）。"""
    global _git_ok
    if _git_ok is None:
        try:
            _git_ok = subprocess.run(["git", "--version"], capture_output=True,
                                     timeout=15).returncode == 0
        except Exception:
            _git_ok = False
    return _git_ok


def git_head():
    """返回 (full_sha, short_sha)；不可用时返回 (None, None)。"""
    global _git_head_cache
    if _git_head_cache is not None:
        return _git_head_cache
    full = short = None
    if _git_available():
        try:
            full = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=str(PROJECT_ROOT),
                capture_output=True, text=True, timeout=20,
            ).stdout.strip() or None
        except Exception:
            full = None
        try:
            short = subprocess.run(
                ["git", "rev-parse", "--short=7", "HEAD"], cwd=str(PROJECT_ROOT),
                capture_output=True, text=True, timeout=20,
            ).stdout.strip() or None
        except Exception:
            short = None
    _git_head_cache = (full, short)
    return _git_head_cache


# ═══════════════════════════════════════════════════════
# 校验项
# ═══════════════════════════════════════════════════════

def check_forbidden_root():
    """1. 禁止根检查：项目父级不得存在 .trae/"""
    passed = not FORBIDDEN_ROOT.exists()
    detail = f"禁止路径 {FORBIDDEN_ROOT} {'存在（违规）' if not passed else '不存在（正常）'}"
    check("禁止根", "项目父级无 .trae/", passed, detail, check_id="forbidden_root")

def check_manifest_files():
    """2. manifest.yaml 中声明的文件全部存在"""
    manifest, err = load_yaml_checked(TRAE_ROOT / "manifest.yaml")
    if err:
        check("文件完整性", "manifest.yaml 声明文件全部存在", False,
              f"{err}，无法校验声明路径", check_id="manifest_files")
        return
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
    check("文件完整性", "manifest.yaml 声明文件全部存在", passed, detail, check_id="manifest_files")

def check_collection_counts():
    """3. 集合数量校验：实际文件数 = manifest 声明数"""
    manifest, err = load_yaml_checked(TRAE_ROOT / "manifest.yaml")
    if err:
        check("集合数量", "manifest 集合数量", False,
              f"{err}，无法校验集合数量", check_id="collection_counts")
        return
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
        check("集合数量", f"{key} 文件数", passed, detail, check_id="collection_counts")

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
          "全部使用 index.md" if all_pass else "; ".join(details),
          check_id="lowercase_indexes")

def check_skill_frontmatter():
    """5. Skill 唯一性：.trae/skills/ 下仅一个带 YAML frontmatter 的 SKILL.md"""
    skills_dir = TRAE_ROOT / "skills"
    if not skills_dir.exists():
        # 兜底分支沿用本检查的正式 name，保证 dashboard/server.py 的
        # by_name 中文名查找在任何分支下都能命中（旧版此处用了不同的 name，
        # 数据源缺失时看板会静默取不到结果）。
        check("Skill 唯一性", "仅一个带 frontmatter 的 SKILL.md", False,
              "skills/ 目录不存在", check_id="skill_frontmatter")
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
    check("Skill 唯一性", "仅一个带 frontmatter 的 SKILL.md", passed, detail, check_id="skill_frontmatter")

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
    check("链接完整性", "Markdown 本地链接无断链", passed, detail, check_id="local_markdown_links")

def check_active_gate():
    """7. active 门禁：STATUS.json 格式有效，activeTasks 数组完整"""
    status, err = load_json_checked(TRAE_ROOT / "execution/active/STATUS.json")
    if err:
        # 兜底分支沿用本检查的正式 name，保证看板 by_name 中文名查找命中
        check("active 门禁", "STATUS.json 格式与状态合法", False,
              f"{err}（原判定：STATUS.json 可读）", check_id="active_gate")
        return

    active_tasks = status.get("activeTasks", [])
    if not isinstance(active_tasks, list) or len(active_tasks) == 0:
        check("active 门禁", "activeTasks 数组非空", False, "activeTasks 为空或非数组", check_id="active_gate")
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
    check("active 门禁", "STATUS.json 格式与状态合法", passed, detail, check_id="active_gate")

def check_five_piece_set():
    """8. 五件套完整性：每个 active 任务目录包含 5 个必需文件"""
    status, err = load_json_checked(TRAE_ROOT / "execution/active/STATUS.json")
    if err:
        check("五件套", "active 任务五件套完整", False,
              f"{err}，无法校验五件套", check_id="five_piece_set")
        return
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
          "全部完整" if all_pass else "; ".join(details), check_id="five_piece_set")

def check_allowlist_conflict():
    """9. 白名单冲突检测：in_progress 任务的 ALLOWLIST 无独占路径重叠"""
    status, err = load_json_checked(TRAE_ROOT / "execution/active/STATUS.json")
    if err:
        check("白名单冲突", "in_progress 任务无独占路径重叠", False,
              f"{err}，无法校验白名单重叠", check_id="allowlist_conflict")
        return
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
    check("白名单冲突", "in_progress 任务无独占路径重叠", passed, detail, check_id="allowlist_conflict")

def check_task_register_consistency():
    """10. 任务登记册一致性：STATUS.json 中的任务状态与 07-task-register.md 一致"""
    status, err = load_json_checked(TRAE_ROOT / "execution/active/STATUS.json")
    if err:
        check("交叉引用", "STATUS.json 与任务登记册一致", False,
              f"{err}，无法校验登记册一致性", check_id="task_register_consistency")
        return
    active_tasks = status.get("activeTasks", [])

    reg_path = TRAE_ROOT / "registers/07-task-register.md"
    task_reg_text = read_text(reg_path)
    if not task_reg_text:
        check("交叉引用", "STATUS.json 与任务登记册一致", False,
              f"数据源缺失或为空：{rel_to_root(reg_path)}，无法校验登记册一致性",
              check_id="task_register_consistency")
        return
    task_reg = parse_markdown_table(task_reg_text)
    if not task_reg:
        check("交叉引用", "STATUS.json 与任务登记册一致", False,
              f"数据源不可解析（未解析出表格行）：{rel_to_root(reg_path)}",
              check_id="task_register_consistency")
        return

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

        # 归一化比对（词表见 STATUS_VOCAB），替代子串猜测
        json_norm = normalize_status(json_status)
        reg_norm = normalize_status(reg_status)
        if json_norm == "unknown":
            issues.append(f"{tid}: STATUS.json 状态 '{json_status}' 无法归一化")
            continue
        if reg_norm == "unknown":
            issues.append(f"{tid}: 登记册状态 '{reg_status}' 无法归一化（原文：{reg_status}）")
            continue
        if json_norm != reg_norm:
            issues.append(
                f"{tid}: STATUS.json='{json_status}'(归一 {json_norm}) vs "
                f"登记册='{reg_status}'(归一 {reg_norm})"
            )

    passed = len(issues) == 0
    detail = f"检查 {len(active_tasks)} 个任务" + (f"，不一致：{issues}" if issues else "，全部一致")
    check("交叉引用", "STATUS.json 与任务登记册一致", passed, detail,
          check_id="task_register_consistency")

def check_verification_evidence():
    """11. 验证证据存在性：验证登记册中引用的证据文件路径存在"""
    verif_path = TRAE_ROOT / "registers/09-verification-register.md"
    verif_text = read_text(verif_path)
    if not verif_text:
        check("交叉引用", "验证证据文件路径存在", False,
              f"数据源缺失或为空：{rel_to_root(verif_path)}，无法校验证据路径",
              check_id="verification_evidence")
        return
    verif_reg = parse_markdown_table(verif_text)
    if not verif_reg:
        check("交叉引用", "验证证据文件路径存在", False,
              f"数据源不可解析（未解析出表格行）：{rel_to_root(verif_path)}",
              check_id="verification_evidence")
        return

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
    check("交叉引用", "验证证据文件路径存在", passed, detail, check_id="verification_evidence")

def check_task_verif_consistency():
    """12b. 任务登记与验证登记交叉一致性：任务状态与验证登记状态不矛盾"""
    task_reg_path = TRAE_ROOT / "registers/07-task-register.md"
    verif_path = TRAE_ROOT / "registers/09-verification-register.md"
    task_reg_text = read_text(task_reg_path)
    verif_text = read_text(verif_path)
    if not task_reg_text:
        check("交叉引用", "任务登记与验证登记状态一致", False,
              f"数据源缺失或为空：{rel_to_root(task_reg_path)}", check_id="task_verif_consistency")
        return
    if not verif_text:
        check("交叉引用", "任务登记与验证登记状态一致", False,
              f"数据源缺失或为空：{rel_to_root(verif_path)}", check_id="task_verif_consistency")
        return
    task_reg = parse_markdown_table(task_reg_text)
    verif_reg = parse_markdown_table(verif_text)
    if not task_reg or not verif_reg:
        check("交叉引用", "任务登记与验证登记状态一致", False,
              f"数据源不可解析（未解析出表格行）：任务表 {len(task_reg)} 行 / 验证表 {len(verif_reg)} 行",
              check_id="task_verif_consistency")
        return

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
    check("交叉引用", "任务登记与验证登记状态一致", passed, detail,
          check_id="task_verif_consistency")


def check_tech_debt_status():
    """12. 技术债检查：统计 open 状态的技术债数量"""
    debt_path = TRAE_ROOT / "registers/11-tech-debt-register.md"
    debt_text = read_text(debt_path)
    if not debt_text:
        check("技术债", "open 技术债 <= 3", False,
              f"数据源缺失或为空：{rel_to_root(debt_path)}，无法统计技术债",
              check_id="tech_debt_open")
        return
    debt_reg = parse_markdown_table(debt_text)
    if not debt_reg:
        check("技术债", "open 技术债 <= 3", False,
              f"数据源不可解析（未解析出表格行）：{rel_to_root(debt_path)}",
              check_id="tech_debt_open")
        return

    open_count = 0
    for row in debt_reg:
        status = row.get("状态", "")
        if "open" in status.lower():
            open_count += 1

    # open 数量 >3 为红色，1-3 为黄色，0 为绿色
    passed = open_count <= 3
    detail = f"{len(debt_reg)} 条技术债，{open_count} 条 open"
    check("技术债", "open 技术债 <= 3", passed, detail, check_id="tech_debt_open")

def check_awaiting_review_timeout():
    """13. 待审核超时：awaiting_review 状态超过 24 小时告警"""
    status, err = load_json_checked(TRAE_ROOT / "execution/active/STATUS.json")
    if err:
        check("流程超时", "awaiting_review 不超过 24h", False,
              f"{err}，无法校验待审核超时", check_id="awaiting_review_timeout")
        return
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
    check("流程超时", "awaiting_review 不超过 24h", passed, detail,
          check_id="awaiting_review_timeout")


def check_rules_numbering():
    """14. 规则编号连续性：AGENTS.md 各节内规则编号严格递增（2026-09-04 起，实证曾发生执行纪律节内 15 号撞号未被察觉）。
    约定：必读/禁止虚构两节各自独立起号，确认门禁起 7-28 跨节连续——本检查只查节内重复与回退，不判跨节衔接。"""
    agents_path = PROJECT_ROOT / "AGENTS.md"
    text = read_text(agents_path)
    if not text:
        check("规则文本", "各节内编号严格递增", False,
              f"数据源缺失或为空：{rel_to_root(agents_path)}，无法校验规则编号",
              check_id="rules_numbering")
        return
    sections = re.split(r"^## .+$", text, flags=re.MULTILINE)[1:]
    problems = []
    total = 0
    for sec in sections:
        nums = [int(m.group(1)) for m in re.finditer(r"^(\d+)\. ", sec, re.MULTILINE)]
        if not nums:
            continue
        total += len(nums)
        for a, b in zip(nums, nums[1:]):
            if b <= a:
                problems.append(f"{a}→{b} 回退/重复")
    passed = not problems
    detail = f"共 {total} 条编号条目" + (("；" + "；".join(problems[:5])) if problems else "，各节内严格递增")
    check("规则文本", "各节内编号严格递增", passed, detail, check_id="rules_numbering")


def check_changelog_freshness():
    """15. CHANGELOG 时效性：顶部条目日期不早于 HEAD 提交日期"""
    try:
        head = subprocess.run(["git", "log", "-1", "--format=%cs"], cwd=str(PROJECT_ROOT),
                              capture_output=True, text=True, timeout=15).stdout.strip()
    except Exception:
        head = ""
    changelog_path = TRAE_ROOT / "CHANGELOG.md"
    text = read_text(changelog_path)
    if not text:
        check("变更记录", "CHANGELOG 不滞后于提交", False,
              f"数据源缺失或为空：{rel_to_root(changelog_path)}，无法校验时效性",
              check_id="changelog_freshness")
        return
    m = re.search(r"^## (\d{4}-\d{2}-\d{2})", text, re.MULTILINE)
    top = m.group(1) if m else ""
    if not head or not top:
        # 兜底分支沿用本检查的正式 name，保证看板 by_name 中文名查找命中
        check("变更记录", "CHANGELOG 不滞后于提交", False,
              f"解析失败（HEAD={head or '无'}, 顶部={top or '无'}）", check_id="changelog_freshness")
        return
    passed = top >= head
    detail = f"顶部条目 {top}，HEAD 提交 {head}"
    check("变更记录", "CHANGELOG 不滞后于提交", passed, detail, check_id="changelog_freshness")


def check_large_files():
    """16. 大文件检查：仓库可提交范围内无 >100MB 文件（规则 23 的自动化）"""
    exclude_dirs = {".git", ".vs", "Intermediate", "Binaries", "DerivedDataCache",
                    "node_modules", ".gradle", "__pycache__", "ArchivedBuilds", "StagedBuilds"}
    big = []
    for p in PROJECT_ROOT.rglob("*"):
        if not p.is_file():
            continue
        if set(p.parts) & exclude_dirs:
            continue
        try:
            size = p.stat().st_size
        except OSError:
            continue
        if size > 100 * 1024 * 1024:
            big.append(f"{p.relative_to(PROJECT_ROOT)} ({size // (1024*1024)}MB)")
    passed = not big
    detail = "未发现 >100MB 文件" if passed else "；".join(big[:5])
    check("仓库卫生", "无 >100MB 大文件", passed, detail, check_id="large_files")


def check_secret_patterns():
    """17. 密钥泄漏扫描：常见令牌模式（规则 23 的自动化，保守模式防误报）"""
    patterns = [
        ("OpenAI/Anthropic sk-", re.compile(r"sk-[A-Za-z0-9]{20,}")),
        ("AWS AKIA", re.compile(r"AKIA[0-9A-Z]{16}")),
        ("GitHub token", re.compile(r"ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{22,}")),
        ("Slack token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
        ("私钥块", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ]
    exts = {".md", ".py", ".ini", ".yaml", ".yml", ".json", ".cs", ".txt",
            ".cmd", ".ps1", ".bat", ".uproject", ".uplugin", ".html", ".js"}
    skip_dirs = {".git", ".vs", "Intermediate", "Binaries", "DerivedDataCache", "node_modules", "__pycache__"}
    hits = []
    for p in PROJECT_ROOT.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in exts:
            continue
        if set(p.parts) & skip_dirs:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for name, pat in patterns:
            if pat.search(text):
                hits.append(f"{p.name}:{name}")
                break
    passed = not hits
    detail = "未发现令牌模式" if passed else "疑似泄漏：" + "；".join(hits[:5])
    check("仓库卫生", "无密钥令牌泄漏", passed, detail, check_id="secret_patterns")


# ═══════════════════════════════════════════════════════
# 新增校验项（2026-09-10 加固）
# ═══════════════════════════════════════════════════════

def load_root_status():
    """读根 STATUS.json，返回 (tasks, error)。"""
    path = TRAE_ROOT / "execution/active/STATUS.json"
    data, err = load_json_checked(path)
    if err:
        return [], err
    tasks = data.get("activeTasks")
    if not isinstance(tasks, list):
        return [], f"根 STATUS.json 的 activeTasks 不是数组：{rel_to_root(path)}"
    return tasks, None


def iter_package_dirs():
    """列出 active/ 下全部任务包目录（跳过隐藏目录）。"""
    base = TRAE_ROOT / "execution/active"
    if not base.exists():
        return []
    return sorted([d for d in base.iterdir() if d.is_dir() and not d.name.startswith(".")],
                  key=lambda d: d.name)


def iter_package_status():
    """产出 (task_dir_name, status_dict, error)。error 非 None 表示该包 STATUS.json 不可读。"""
    for d in iter_package_dirs():
        sf = d / "STATUS.json"
        if not sf.exists():
            yield d.name, {}, f"任务包缺 STATUS.json：{rel_to_root(sf)}"
            continue
        data, err = load_json_checked(sf)
        if err:
            yield d.name, {}, err
            continue
        yield d.name, data, None


def check_package_status_mirror():
    """18. 根 ↔ 任务包 STATUS.json 镜像：分三档判定（防误报）。

    ① status 必须逐字相等 → fail
    ② 仅当 status == "in_progress" 时 claimedBy 必须逐字相等 → fail
    ③ 终态任务（approved/archived）的 claimedBy / updatedAt 漂移 → warn（不红）
    包内 `_note` 声明「本地便利副本…冲突时以根为准」，故终态漂移是历史噪声而非流程失败。
    """
    root_tasks, err = load_root_status()
    if err:
        check("五件套", "根 ↔ 任务包 STATUS.json 镜像", False,
              f"{err}，无法比对镜像", check_id="package_status_mirror")
        return

    root_map = {}
    for t in root_tasks:
        tid = t.get("taskId", "")
        if tid:
            root_map[tid] = t

    fails, warns, pkg_errors = [], [], []

    for dir_name, pkg, perr in iter_package_status():
        if perr:
            pkg_errors.append(perr)
            continue
        pkg_tid = pkg.get("taskId", "")
        if pkg_tid and pkg_tid != dir_name:
            fails.append(f"{dir_name}: 包内 taskId='{pkg_tid}' 与目录名不符")
        tid = pkg_tid or dir_name
        root = root_map.get(tid)
        if root is None:
            # 孤儿包由 five_piece_structure 判定，此处不重复计红
            continue

        pkg_status = pkg.get("status", "")
        root_status = root.get("status", "")

        # 档 1：status 必须逐字相等
        if pkg_status != root_status:
            fails.append(
                f"{tid}: status 包='{pkg_status}' vs 根='{root_status}'（必须逐字相等）"
            )
            continue

        norm = normalize_status(pkg_status)

        # 档 2：in_progress 时 claimedBy 必须逐字相等
        if norm == "in_progress":
            pkg_claim = pkg.get("claimedBy")
            root_claim = root.get("claimedBy")
            if pkg_claim != root_claim:
                fails.append(
                    f"{tid}(in_progress): claimedBy 包='{pkg_claim}' vs 根='{root_claim}'（必须逐字相等）"
                )

        # 档 3：其余漂移 → warn
        #  · 终态任务（approved/archived）的 claimedBy / updatedAt 漂移
        #  · 任何状态的 updatedAt 漂移：任务包 `_note` 明写「本地便利副本…冲突时以根为准」，
        #    包内时间戳同步滞后属正常，且终态与执行中的判定口径应一致。
        pkg_claim = pkg.get("claimedBy")
        root_claim = root.get("claimedBy")
        pkg_upd = pkg.get("updatedAt")
        root_upd = root.get("updatedAt")
        if norm in TERMINAL_STATES and pkg_claim != root_claim:
            warns.append(f"{tid}({norm}): claimedBy 包='{pkg_claim}' vs 根='{root_claim}'")
        if pkg_upd != root_upd:
            warns.append(f"{tid}({norm}): updatedAt 包='{pkg_upd}' vs 根='{root_upd}'（副本同步滞后）")

    if fails or pkg_errors:
        detail = "；".join(fails + pkg_errors)
        if warns:
            detail += f"；另有 {len(warns)} 条副本漂移(warn)：{'；'.join(warns)}"
        check("五件套", "根 ↔ 任务包 STATUS.json 镜像", False, detail,
              check_id="package_status_mirror")
    elif warns:
        check("五件套", "根 ↔ 任务包 STATUS.json 镜像", True,
              f"status 与 in_progress claimedBy 全部一致；{len(warns)} 条副本字段漂移(仅提示)："
              + "；".join(warns),
              check_id="package_status_mirror", severity="warn")
    else:
        check("五件套", "根 ↔ 任务包 STATUS.json 镜像", True,
              f"{len(root_map)} 个任务：status/claimedBy/updatedAt 全部一致",
              check_id="package_status_mirror")


def check_five_piece_structure():
    """19. 五件套结构检查：根 ↔ 目录 ↔ 包内 taskId ↔ ALLOWLIST 路径。

    防误报设计（关键）：
    · 不对文件内容做指纹/长度比对（历史任务正文常被后续补记，漂移属正常）。
    · 通配项（Source/**/X.cpp、Plugins/A/**）只校验通配符**之前**那段路径存在。
    · 与根登记无关的孤儿包才计红；根登记存在而目录缺失按任务是否终态分档。
    · 非通配路径的「引用对象不存在」按任务状态分档：in_progress → fail；
      终态任务不判（历史路径可被合法改名/删除，如 L_Prototype_1v1.umap 已被 v4/v5 取代）。
    · 绝对路径 / 含 .. 逃出项目根 → 恒 fail（这两类是结构性违规，与路径是否存在于磁盘无关）。
    """
    root_tasks, err = load_root_status()
    if err:
        check("五件套", "五件套结构（根↔目录↔taskId↔ALLOWLIST）", False,
              f"{err}，无法校验结构", check_id="five_piece_structure")
        return

    root_map = {}
    for t in root_tasks:
        tid = t.get("taskId", "")
        if tid:
            root_map[tid] = t

    dir_names = [d.name for d in iter_package_dirs()]
    dir_set = set(dir_names)

    missing_dirs, orphan_pkgs = [], []
    tid_mismatch, path_violations, path_missing_active, path_missing_terminal = [], [], [], []

    # ① 根有 taskId 但无同名目录；② 目录无根登记（孤儿包）
    for tid, t in root_map.items():
        if tid not in dir_set:
            norm = normalize_status(t.get("status", ""))
            if norm in TERMINAL_STATES:
                path_missing_terminal.append(
                    f"{tid}({norm}): 根登记存在但 active/{tid}/ 目录已不存在（历史终态）"
                )
            else:
                missing_dirs.append(f"{tid}({norm}): 根登记存在但 active/{tid}/ 目录缺失")
    for d in dir_names:
        if d not in root_map:
            orphan_pkgs.append(f"{d}: 目录存在但根 STATUS.json 无此 taskId（孤儿包）")

    # ③ 包内 taskId ≠ 目录名；④ ALLOWLIST 路径
    for dir_name, pkg, perr in iter_package_status():
        if perr:
            path_violations.append(perr)
            continue
        pkg_tid = pkg.get("taskId", "")
        if pkg_tid and pkg_tid != dir_name:
            tid_mismatch.append(f"{dir_name}: 包内 taskId='{pkg_tid}'")
        norm = normalize_status(root_map.get(dir_name, {}).get("status", ""))

        al = TRAE_ROOT / "execution/active" / dir_name / "ALLOWLIST.txt"
        if not al.exists():
            path_violations.append(f"{dir_name}: 缺 ALLOWLIST.txt")
            continue
        text = read_text(al)
        for raw in text.split("\n"):
            s = raw.strip()
            if not s or s.startswith("#"):
                continue
            # 绝对路径（含盘符）
            if re.match(r'^[A-Za-z]:[\\/]', s) or s.startswith("/") or s.startswith("\\\\"):
                path_violations.append(f"{dir_name}: 绝对路径 '{s}'")
                continue
            # 含 .. → 必须仍落在项目根内
            if ".." in s.split("/"):
                target = (PROJECT_ROOT / s).resolve()
                try:
                    target.relative_to(PROJECT_ROOT.resolve())
                except ValueError:
                    path_violations.append(f"{dir_name}: 路径逃出项目根 '{s}'")
                continue
            # 通配项：只校验通配符之前那段
            if "*" in s:
                prefix = s.split("*")[0].rstrip("/\\")
                if prefix and not (PROJECT_ROOT / prefix).exists():
                    path_violations.append(f"{dir_name}: 通配前缀不存在 '{prefix}/'（来自 '{s}'）")
                continue
            # 非通配项：引用对象不存在
            if not (PROJECT_ROOT / s).exists():
                if norm == "in_progress":
                    path_missing_active.append(f"{dir_name}: 白名单路径不存在 '{s}'")
                else:
                    path_missing_terminal.append(
                        f"{dir_name}({norm or '未知状态'}): 白名单路径不存在 '{s}'"
                    )

    fails = missing_dirs + orphan_pkgs + tid_mismatch + path_violations + path_missing_active
    has_active_ref_gap = bool(path_missing_active)
    warn_notes = []
    if path_missing_terminal:
        warn_notes.append(f"{len(path_missing_terminal)} 条历史路径引用：{'；'.join(path_missing_terminal)}")

    if fails:
        check("五件套", "五件套结构（根↔目录↔taskId↔ALLOWLIST）", False,
              "；".join(fails) + (f"；另 {len(path_missing_terminal)} 条历史提示" if path_missing_terminal else ""),
              check_id="five_piece_structure")
    elif warn_notes:
        check("五件套", "五件套结构（根↔目录↔taskId↔ALLOWLIST）", True,
              f"{len(root_map)} 个根登记 / {len(dir_names)} 个任务包目录：结构一致；"
              + "；".join(warn_notes),
              check_id="five_piece_structure", severity="warn")
    else:
        check("五件套", "五件套结构（根↔目录↔taskId↔ALLOWLIST）", True,
              f"{len(root_map)} 个根登记 / {len(dir_names)} 个任务包目录：结构一致",
              check_id="five_piece_structure")


def check_global_task_state_consistency():
    """20. 五方状态一致性：根 / 包内 / 07 登记册 / manifest / integrity。

    判定：
    ① 同步对等源（根 / 包内 / manifest / integrity）的 taskId 集合必须逐字相同。
    ② 每个任务的归一化状态必须一致（词表 STATUS_VOCAB，不用子串猜测）。
    ③ 归一化不出来的记 unknown 并 fail。
    ④ 不一致时同时打印各源原文与归一化结果。
    分档说明（防误报）：07 登记册是「项目全任务台账」，天然含未进入
    active 门禁的规划/历史任务，故只单向校验（active 源任务必须存在于登记册），
    不要求台账与 active 集合相等 —— 否则历史任务会全部误红。
    豁免：差异须命中机器可读台账 .trae/integrity-reconciliations.yaml 才降级 warn；
    台账不存在时豁免不生效（缺文件不得静默放行）。
    """
    sources = []          # (源显示名, {taskId: raw_status})
    errors = []

    # 源 1：根 STATUS.json
    root_tasks, err = load_root_status()
    if err:
        errors.append(err)
        root_map = {}
    else:
        root_map = {}
        for t in root_tasks:
            tid = t.get("taskId", "")
            if tid:
                root_map[tid] = t.get("status", "")
        sources.append(("根 STATUS.json", root_map))

    # 源 2：包内 STATUS.json
    pkg_map = {}
    for dir_name, pkg, perr in iter_package_status():
        if perr:
            errors.append(perr)
            continue
        tid = pkg.get("taskId", "") or dir_name
        pkg_map[tid] = pkg.get("status", "")
    if pkg_map:
        sources.append(("包内 STATUS.json", pkg_map))
    elif not errors:
        errors.append("包内 STATUS.json 一个都没读到")

    # 源 3：07-task-register.md
    reg_path = TRAE_ROOT / "registers/07-task-register.md"
    reg_text = read_text(reg_path)
    reg_map = {}
    if not reg_text:
        errors.append(f"数据源缺失或为空：{rel_to_root(reg_path)}")
    else:
        rows = parse_markdown_table(reg_text)
        if not rows:
            errors.append(f"数据源不可解析（未解析出表格行）：{rel_to_root(reg_path)}")
        else:
            for r in rows:
                tid = r.get("任务", "")
                if tid:
                    reg_map[tid] = r.get("状态", "")
            sources.append(("registers/07-task-register.md", reg_map))

    # 源 4：.trae/manifest.yaml active_gate.task_packages
    man_path = TRAE_ROOT / "manifest.yaml"
    man, man_err = load_yaml_checked(man_path)
    if man_err:
        errors.append(man_err)
    else:
        pkgs = man.get("active_gate", {}).get("task_packages")
        if not isinstance(pkgs, list) or not pkgs:
            errors.append(f"manifest.yaml 的 active_gate.task_packages 缺失或非数组：{rel_to_root(man_path)}")
        else:
            m = {}
            for e in pkgs:
                if isinstance(e, dict) and e.get("task_id"):
                    m[e["task_id"]] = e.get("status", "")
            sources.append(("manifest.yaml", m))

    # 源 5：.trae/integrity.yaml verification.checks.active_gate.active_tasks
    int_path = TRAE_ROOT / "integrity.yaml"
    integ, int_err = load_yaml_checked(int_path)
    if int_err:
        errors.append(int_err)
    else:
        ats = (integ.get("verification", {}).get("checks", {})
                   .get("active_gate", {}).get("active_tasks"))
        if not isinstance(ats, list) or not ats:
            errors.append(f"integrity.yaml 的 verification.checks.active_gate.active_tasks 缺失或非数组："
                          f"{rel_to_root(int_path)}")
        else:
            m = {}
            for e in ats:
                if isinstance(e, dict) and e.get("task_id"):
                    m[e["task_id"]] = e.get("status", "")
            sources.append(("integrity.yaml", m))

    if errors:
        check("交叉引用", "五方任务状态一致", False,
              "；".join(errors), check_id="global_task_state_consistency")
        return

    src_names = [n for n, _ in sources]
    # 对等源 = 除 07 登记册以外的四方（登记册是全量台账，不算对等集）
    peer_sources = [(n, m) for n, m in sources if "07-task-register" not in n]
    peer_sets = {n: set(m.keys()) for n, m in peer_sources}

    issues = []

    # ① 对等源 taskId 集合逐字相同
    if len(set(frozenset(s) for s in peer_sets.values())) > 1:
        union = set()
        for s in peer_sets.values():
            union |= s
        for name, s in peer_sets.items():
            extra = sorted(s - set.intersection(*peer_sets.values())) if len(peer_sets) > 1 else []
            missing = sorted(set.intersection(*(set(v) for k, v in peer_sets.items() if k != name)) - s) \
                if len(peer_sets) > 1 else []
            if missing:
                issues.append(f"{name} 缺少任务 {missing}")
            # 某一方多出来的也报（不得拿某一方当全集）
            others = set()
            for k, v in peer_sets.items():
                if k != name:
                    others |= v
            extra_only = sorted(s - others)
            if extra_only:
                issues.append(f"{name} 多出任务 {extra_only}（其他源无此任务）")

    # ② + ④ 逐任务归一化比对，并打印各源原文
    all_ids = set()
    for name, m in sources:
        all_ids |= set(m.keys())

    for tid in sorted(all_ids):
        raws = {}
        norms = {}
        for name, m in sources:
            if tid in m:
                raws[name] = m[tid]
                norms[name] = normalize_status(m[tid])
        if not raws:
            continue
        if "unknown" in norms.values():
            bad = [f"{n}='{raws[n]}'" for n, v in norms.items() if v == "unknown"]
            issues.append(f"{tid}: 状态无法归一化 → " + "，".join(bad))
            continue
        if len(set(norms.values())) > 1:
            parts = [f"{n}='{raws[n]}'(归一 {norms[n]})" for n in raws]
            issues.append(f"{tid}: 各源状态不一致 → " + "，".join(parts))

    # ③ active 对等源的任务必须存在于 07 登记册
    peer_ids = set()
    for s in peer_sets.values():
        peer_ids |= s
    reg_only_extra = sorted(set(reg_map.keys()) - peer_ids)
    not_in_reg = sorted(peer_ids - set(reg_map.keys()))
    for tid in not_in_reg:
        norm = None
        for name, m in peer_sources:
            if tid in m:
                norm = normalize_status(m[tid])
                break
        if norm in TERMINAL_STATES:
            # 终态历史任务未收录台账：记账提示，不计红（各源自身已一致）
            pass
        issues.append(f"{tid}: 不在 registers/07-task-register.md 中（active 源有、台账无）")

    # 豁免台账
    recon_path = TRAE_ROOT / "integrity-reconciliations.yaml"
    exemptions = []
    recon_note = "无豁免台账（.trae/integrity-reconciliations.yaml 不存在）"
    if recon_path.exists():
        recon, recon_err = load_yaml_checked(recon_path)
        if recon_err:
            recon_note = f"豁免台账不可读：{recon_err}"
        else:
            entries = recon.get("reconciliations") if isinstance(recon, dict) else None
            if not isinstance(entries, list):
                entries = recon if isinstance(recon, list) else []
            today = datetime.now().strftime("%Y-%m-%d")
            for e in entries:
                if not isinstance(e, dict):
                    continue
                trigger = str(e.get("reviewTrigger", ""))
                expired = bool(trigger) and trigger < today
                exemptions.append((e, expired))
            recon_note = f"豁免台账 {len(entries)} 条"
    else:
        recon_note = "无豁免台账（.trae/integrity-reconciliations.yaml 不存在，豁免不生效）"

    def _exempt(tid):
        """返回 (命中未过期豁免, 命中已过期豁免)。"""
        hit, expired = False, False
        for e, is_exp in exemptions:
            if e.get("taskId") == tid:
                if is_exp:
                    expired = True
                else:
                    hit = True
        return hit, expired

    # 把 issues 按 taskId 分档；豁免命中的降级 warn，过期的保持 fail
    fail_issues, warn_issues = [], []
    for msg in issues:
        tid = msg.split(":", 1)[0].strip()
        hit, expired = _exempt(tid)
        if hit:
            warn_issues.append(f"[已豁免] {msg}")
        else:
            if expired:
                msg = f"[豁免已过期] {msg}"
            fail_issues.append(msg)

    detail_bits = []
    if fail_issues:
        detail_bits.append("；".join(fail_issues))
    if not fail_issues:
        detail_bits.append(
            f"{len(peer_ids)} 个任务跨 {len(sources)} 方一致（{', '.join(src_names)}）"
        )
    if reg_only_extra:
        detail_bits.append(
            f"台账另有 {len(reg_only_extra)} 条未进入 active 门禁的规划/历史任务（不计红）："
            + ", ".join(reg_only_extra[:8])
            + ("…" if len(reg_only_extra) > 8 else "")
        )
    if warn_issues:
        detail_bits.append("；".join(warn_issues))
    detail_bits.append(recon_note)

    detail = "；".join(detail_bits)
    if fail_issues:
        check("交叉引用", "五方任务状态一致", False, detail,
              check_id="global_task_state_consistency")
    elif warn_issues:
        check("交叉引用", "五方任务状态一致", True, detail,
              check_id="global_task_state_consistency", severity="warn")
    else:
        check("交叉引用", "五方任务状态一致", True, detail,
              check_id="global_task_state_consistency")


def check_session_records():
    """21. 会话记录检查（兑现 AGENTS.md 规则 26 / governance/policy.md 的承诺）。

    只对 status == "in_progress" 的任务强制：
      ① claimedBy 非空
      ② claimedBy 命名符合 ^session-\\d{8}-\\d{3,}$
      ③ .trae/execution/sessions/{claimedBy}.md 存在
      ④ 该文件 >= 200 字节，且含一行以 # 开头的标题，标题内含 sessionId
    任一项不满足 → fail。
    终态任务（approved/archived）残留的 claimedBy 只做 warn：治理正文从未要求
    批准时清空 claimedBy，硬判会造假红。
    不要求「每次会话都有记录」：sessions/ 现存 9 份而历史登记过的会话标识更多，
    按会话判定会立刻打红，而该欠账已作为已知事项挂起。
    """
    root_tasks, err = load_root_status()
    if err:
        check("流程规范", "in_progress 任务会话记录完整", False,
              f"{err}，无法校验会话记录", check_id="session_records")
        return

    sessions_dir = TRAE_ROOT / "execution/sessions"
    fails, warns = [], []

    for t in root_tasks:
        tid = t.get("taskId", "")
        norm = normalize_status(t.get("status", ""))
        claimed = t.get("claimedBy")

        if norm == "in_progress":
            if not claimed or not isinstance(claimed, str) or not claimed.strip():
                fails.append(f"{tid}: in_progress 但 claimedBy 为空")
                continue
            if not SESSION_ID_RE.match(claimed):
                fails.append(f"{tid}: claimedBy='{claimed}' 不符合 ^session-\\d{{8}}-\\d{{3,}}$")
                continue
            sf = sessions_dir / f"{claimed}.md"
            if not sf.exists():
                fails.append(f"{tid}: 会话记录不存在 {rel_to_root(sf)}")
                continue
            try:
                text = sf.read_text(encoding="utf-8", errors="ignore")
            except OSError as e:
                fails.append(f"{tid}: 会话记录不可读 {rel_to_root(sf)}（{type(e).__name__}: {e}）")
                continue
            size = len(text.encode("utf-8"))
            if size < 200:
                fails.append(f"{tid}: 会话记录仅 {size} 字节（<200）{rel_to_root(sf)}")
                continue
            heads = [ln for ln in text.split("\n") if ln.lstrip().startswith("#")]
            if not any(claimed in ln for ln in heads):
                fails.append(f"{tid}: 会话记录无含 sessionId 的 '#' 标题 {rel_to_root(sf)}")
        elif norm in TERMINAL_STATES and claimed:
            reason = []
            if not SESSION_ID_RE.match(str(claimed)):
                reason.append("命名不符 ^session-\\d{8}-\\d{3,}$")
            if not (sessions_dir / f"{claimed}.md").exists():
                reason.append("无对应会话记录文件")
            if reason:
                warns.append(f"{tid}({norm}): claimedBy='{claimed}' 残留（{'、'.join(reason)}）")

    if fails:
        detail = "；".join(fails)
        if warns:
            detail += f"；另 {len(warns)} 条终态残留(仅提示)：{'；'.join(warns)}"
        check("流程规范", "in_progress 任务会话记录完整", False, detail,
              check_id="session_records")
    elif warns:
        check("流程规范", "in_progress 任务会话记录完整", True,
              f"in_progress 任务会话记录齐全；{len(warns)} 条终态残留 claimedBy(仅提示)："
              + "；".join(warns),
              check_id="session_records", severity="warn")
    else:
        check("流程规范", "in_progress 任务会话记录完整", True,
              "in_progress 任务 claimedBy 与会话记录均完整", check_id="session_records")


def check_integrity_yaml_consistency():
    """22. integrity.yaml 计数一致性：local_markdown_links 计数 vs 脚本实测。

    分档：
      ① 两侧都有值且不等 → fail
      ② 缺失或非法 → fail（不得靠缺失静默通过）
      ③ 两侧都为空 → warn
    防误报关键：为 checked 引入机器可读作用域字段 scope。脚本只统计
    local_markdown_links.scope 所列文件/glob 内的链接；若 scope 缺失，本项一律
    降级 warn 并写明「缺 scope，无法判定」——任何一次合规的文档新增/删除都会
    改变全量链接数，没有 scope 就必然假红。broken 永远 0 容忍。
    """
    int_path = TRAE_ROOT / "integrity.yaml"
    integ, err = load_yaml_checked(int_path)
    if err:
        check("链接完整性", "integrity.yaml 链接计数一致", False,
              f"{err}，无法校验计数", check_id="integrity_yaml_consistency")
        return

    node = (integ.get("verification", {}).get("checks", {})
                 .get("local_markdown_links"))
    if not isinstance(node, dict):
        check("链接完整性", "integrity.yaml 链接计数一致", False,
              f"{rel_to_root(int_path)} 的 verification.checks.local_markdown_links 缺失或非映射，"
              f"无法校验计数", check_id="integrity_yaml_consistency")
        return

    declared_checked = node.get("checked")
    declared_broken = node.get("broken")
    scope = node.get("scope")

    # ── 脚本侧实测 ──────────────────────────────────
    if scope is not None and not isinstance(scope, list):
        check("链接完整性", "integrity.yaml 链接计数一致", False,
              f"local_markdown_links.scope 非法（应为列表，实际 {type(scope).__name__}），无法判定",
              check_id="integrity_yaml_consistency")
        return

    if scope:
        md_files = []
        for item in scope:
            if not isinstance(item, str) or not item.strip():
                continue
            item = item.strip()
            if any(ch in item for ch in "*?["):
                md_files.extend(sorted(PROJECT_ROOT.glob(item)))
            else:
                p = PROJECT_ROOT / item
                if p.is_dir():
                    md_files.extend(sorted(p.rglob("*.md")))
                elif p.exists():
                    md_files.append(p)
            if len(md_files) > 20000:
                md_files = md_files[:20000]
                break
        scope_desc = f"scope {len(scope)} 项 → {len(md_files)} 个文件"
    else:
        md_files = find_md_files(TRAE_ROOT)
        scope_desc = "无 scope（当前按全量 .trae/**/*.md 实测，仅供参考）"

    total_links = 0
    broken_links = 0
    for md_file in md_files:
        for _t, link_path, _tg in extract_md_links(md_file):
            total_links += 1
            if not resolve_link(md_file, link_path).exists():
                broken_links += 1

    actual_checked = total_links
    actual_broken = broken_links

    def _as_int(v):
        if isinstance(v, bool):
            return None
        if isinstance(v, int):
            return v
        if isinstance(v, str) and v.strip().lstrip("-").isdigit():
            return int(v.strip())
        return None

    d_checked, d_broken = _as_int(declared_checked), _as_int(declared_broken)

    problems = []
    if declared_checked is not None and d_checked is None:
        problems.append(f"checked 非法值 '{declared_checked}'")
    if declared_broken is not None and d_broken is None:
        problems.append(f"broken 非法值 '{declared_broken}'")

    # broken 永远 0 容忍
    if d_broken is not None and d_broken != actual_broken:
        problems.append(f"broken 声明 {d_broken} ≠ 实测 {actual_broken}")
    if declared_broken is None:
        problems.append("broken 缺失，无法判定")

    no_scope = not scope
    if no_scope:
        # 缺 scope：不判 checked 相等，只降级 warn
        if problems:
            detail = f"{rel_to_root(int_path)}: " + "；".join(problems)
            if not scope:
                detail += f"；缺 scope，无法判定 checked（实测全量 {actual_checked} / 断链 {actual_broken}）"
            check("链接完整性", "integrity.yaml 链接计数一致", False, detail,
                  check_id="integrity_yaml_consistency")
        else:
            check("链接完整性", "integrity.yaml 链接计数一致", True,
                  f"broken 声明 {d_broken} = 实测 {actual_broken}（0 容忍，一致）；"
                  f"缺 scope，无法判定 checked：声明 {declared_checked}，"
                  f"脚本全量实测 {actual_checked}（{scope_desc}）",
                  check_id="integrity_yaml_consistency", severity="warn")
        return

    # 有 scope：checked 必须相等
    if declared_checked is None or d_checked is None:
        problems.append("checked 缺失或非法，无法判定（有 scope 时不允许缺值）")
    elif d_checked != actual_checked:
        problems.append(f"checked 声明 {d_checked} ≠ 作用域内实测 {actual_checked}")

    if problems:
        check("链接完整性", "integrity.yaml 链接计数一致", False,
              f"{rel_to_root(int_path)}: " + "；".join(problems) + f"（{scope_desc}）",
              check_id="integrity_yaml_consistency")
    else:
        check("链接完整性", "integrity.yaml 链接计数一致", True,
              f"checked {d_checked} / broken {d_broken} 与实测一致（{scope_desc}）",
              check_id="integrity_yaml_consistency")


# ═══════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════

ALL_CHECKS = [
    ("forbidden_root", check_forbidden_root),
    ("manifest_files", check_manifest_files),
    ("collection_counts", check_collection_counts),
    ("lowercase_indexes", check_lowercase_indexes),
    ("skill_frontmatter", check_skill_frontmatter),
    ("local_markdown_links", check_markdown_links),
    ("active_gate", check_active_gate),
    ("five_piece_set", check_five_piece_set),
    ("allowlist_conflict", check_allowlist_conflict),
    ("task_register_consistency", check_task_register_consistency),
    ("verification_evidence", check_verification_evidence),
    ("task_verif_consistency", check_task_verif_consistency),
    ("tech_debt_open", check_tech_debt_status),
    ("awaiting_review_timeout", check_awaiting_review_timeout),
    ("rules_numbering", check_rules_numbering),
    ("changelog_freshness", check_changelog_freshness),
    ("large_files", check_large_files),
    ("secret_patterns", check_secret_patterns),
    # 2026-09-10 新增
    ("five_piece_structure", check_five_piece_structure),
    ("package_status_mirror", check_package_status_mirror),
    ("global_task_state_consistency", check_global_task_state_consistency),
    ("session_records", check_session_records),
    ("integrity_yaml_consistency", check_integrity_yaml_consistency),
]

# 每个检查的 category / name 文案（用于异常兜底时也能给出可读条目）
CHECK_LABELS = {
    "five_piece_structure": ("五件套", "五件套结构（根↔目录↔taskId↔ALLOWLIST）"),
    "package_status_mirror": ("五件套", "根 ↔ 任务包 STATUS.json 镜像"),
    "global_task_state_consistency": ("交叉引用", "五方任务状态一致"),
    "session_records": ("流程规范", "in_progress 任务会话记录完整"),
    "integrity_yaml_consistency": ("链接完整性", "integrity.yaml 链接计数一致"),
}


def run_all_checks():
    """执行全部校验。

    每个检查单独 try/except：异常记为该检查 fail，绝不静默、绝不整轮零输出。
    同时校验每个检查确实产生了结果（防空跑）。
    """
    results.clear()
    git_head()  # 预热缓存，避免网络/子进程异常影响输出阶段

    for check_id, fn in ALL_CHECKS:
        before = len(results)
        try:
            fn()
        except Exception as e:
            category, name = CHECK_LABELS.get(check_id, ("校验脚本", check_id))
            check(category, name, False,
                  f"检查内部错误: {type(e).__name__}: {e}", check_id=check_id)
        after = len(results)

        if after == before:
            category, name = CHECK_LABELS.get(check_id, ("校验脚本", check_id))
            check(category, name, False,
                  f"检查内部错误: NoResultError: 检查 {check_id} 未产生任何结果（空跑）",
                  check_id=check_id)
        else:
            for r in results[before:after]:
                if not r.get("id"):
                    r["id"] = check_id
                if r.get("severity") not in SEVERITY_ORDER:
                    r["severity"] = "pass" if r.get("passed") else "fail"

    return results


def _counts(results):
    total = len(results)
    failed = sum(1 for r in results if r.get("severity") == "fail")
    warned = sum(1 for r in results if r.get("severity") == "warn")
    passed = total - failed - warned
    return total, passed, warned, failed


def print_terminal(results, quiet=False):
    """终端彩色输出"""
    total, passed, warned, failed = _counts(results)

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
            # 旧行为：只显示失败项。warn 同样需要可见，故一并保留。
            items = [r for r in items if r.get("severity") != "pass"]
            if not items:
                continue
        print(f"  {C.B}{cat}{C.X}")
        for r in items:
            sev = r.get("severity", "pass")
            if sev == "fail":
                status = f"{C.R}✗{C.X}"
            elif sev == "warn":
                status = f"{C.Y}!{C.X}"
            else:
                status = f"{C.G}✓{C.X}"
            name = r["name"]
            detail = r["detail"]
            if sev == "pass":
                print(f"    {status} {name} {C.D}— {detail}{C.X}")
            elif sev == "warn":
                print(f"    {status} {name}")
                print(f"      {C.Y}{detail}{C.X}")
            else:
                print(f"    {status} {name}")
                print(f"      {C.R}{detail}{C.X}")

    print(f"\n  {'─' * 50}")
    color = C.G if failed == 0 else C.R
    warn_part = f"  {C.Y}警告:{C.X} {warned}  " if warned else ""
    print(f"  {C.B}总计:{C.X} {total} 项  {C.G}通过:{C.X} {passed}  "
          f"{warn_part}{color}失败:{C.X} {failed}")

    if failed == 0 and warned == 0:
        print(f"  {C.G}✓ 全部校验通过{C.X}\n")
    elif failed == 0:
        print(f"  {C.Y}! 全部校验通过，有 {warned} 项警告（不阻断）{C.X}\n")
    else:
        print(f"  {C.R}✗ 有 {failed} 项校验失败，请检查{C.X}\n")

    return failed

def print_json(results):
    """JSON 输出（供看板调用）

    向后兼容：timestamp / trae_root / total / passed / failed / overall / checks[]
    字段一律保留且语义不变；新增字段只追加。
    checks[] 每项追加 id 与 severity；passed 兼容字段语义为「未失败」
    （severity != fail）。
    """
    total, passed, warned, failed = _counts(results)
    head_full, head_short = git_head()

    output = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "trae_root": str(TRAE_ROOT),
        "total": total,
        "passed": passed,
        "failed": failed,
        "overall": "pass" if failed == 0 else "fail",
        "checks": results,
        # ── 以下为新增（追加，不改变既有字段）──
        "warned": warned,
        "passed_strict": sum(1 for r in results if r.get("severity") == "pass"),
        "git_head": head_full,
        "git_head_short": head_short,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return failed

def main():
    global YAML_ERROR

    # 检查 .trae/ 是否存在
    if not TRAE_ROOT.exists():
        print(f"{C.R}错误: .trae/ 目录不存在于 {TRAE_ROOT}{C.X}")
        sys.exit(1)

    # 依赖自检。注意：本函数内**不得**再出现 `import yaml` 或对裸名 yaml 的赋值——
    # 那会把 yaml 变成 main() 的局部变量、遮蔽模块级导入，并在未走到赋值分支时
    # 抛 UnboundLocalError（2026-09-11 实发事故）。回退逻辑一律走模块级 helper。
    ensure_yaml_ready()

    args = sys.argv[1:]
    all_results = run_all_checks()

    if "--json" in args:
        failed = print_json(all_results)
    elif "--quiet" in args:
        failed = print_terminal(all_results, quiet=True)
    else:
        failed = print_terminal(all_results)

    sys.exit(1 if failed > 0 else 0)

if __name__ == "__main__":
    main()
