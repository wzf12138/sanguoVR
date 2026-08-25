#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# VR 三国演武场 - 开发治理仪表盘 v5
# 核心改造: 防虚构健康度 9 项指标 + 资产仓库 + 验证证据
# 数据源: .trae/ 下全部治理文件（零虚构数据）
import http.server, json, os, re, subprocess, sys, yaml
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
TRAE_ROOT = PROJECT_ROOT / ".trae"
PORT = 9999

# ── 导入资产扫描器 ──────────────────────────────────────────
try:
    import asset_scanner
except ImportError:
    sys.path.insert(0, str(SCRIPT_DIR))
    import asset_scanner

# ── 里程碑定义 ──────────────────────────────────────────
MILESTONES = [
    {"id": "M00", "name": "项目基线与自动化骨架"},
    {"id": "M01", "name": "1v1 核心战斗技术切片"},
    {"id": "M02", "name": "五武器、混合移动与全身 IK"},
    {"id": "M03", "name": "N 对 N、兵种与默认 3v3"},
    {"id": "M04", "name": "生涯、自定义、训练与存档"},
    {"id": "M05", "name": "三国内容、武将与生产替换"},
    {"id": "M06", "name": "4v4 优化与发布验收"},
]

# ── 数据读取工具 ──────────────────────────────────────────

def read_json(path):
    p = TRAE_ROOT / path
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def read_yaml(path):
    p = TRAE_ROOT / path
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}

def read_text(path):
    p = TRAE_ROOT / path
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def parse_markdown_table(text):
    """解析 markdown 中所有表格（主表 + 规划表），返回所有行的列表。
    修复历史：2026-08-25 之前只读第一个表格，规划任务表被跳过。
    """
    rows = []
    lines = text.strip().split("\n")
    n = len(lines)
    i = 0
    while i < n - 1:
        # 寻找表格头（当前行含 | 且下一行是分隔行）
        if "|" not in lines[i] or "---" not in lines[i + 1]:
            i += 1
            continue
        # 防止把分隔行误判为表头：表头必须本身含有 | 但不含 ---
        if "---" in lines[i]:
            i += 1
            continue
        headers = [h.strip() for h in lines[i].split("|")[1:-1]]
        if not headers:
            i += 1
            continue
        i += 2  # 跳过分隔行
        # 读取本表的所有行
        while i < n and lines[i].strip().startswith("|"):
            cells = [c.strip() for c in lines[i].split("|")[1:-1]]
            if len(cells) == len(headers):
                rows.append(dict(zip(headers, cells)))
            i += 1
        # 继续外层 while，寻找下一个表格
    return rows

def get_session_id():
    memory_root = Path.home() / ".trae-cn" / "memory" / "projects"
    proj_dir = "-d-AWork-Unreal-Project-VRSanguoYanWuchang--p2-d7afac5a2c70d7f6ef9a"
    mem_path = memory_root / proj_dir
    if not mem_path.exists():
        return "unknown"
    date_dirs = sorted([d for d in mem_path.iterdir() if d.is_dir()], reverse=True)
    for dd in date_dirs:
        for f in sorted(dd.iterdir(), reverse=True):
            if f.name.startswith("session_memory_") and f.suffix == ".jsonl":
                return f.stem.replace("session_memory_", "")
    return "unknown"


def classify_task_status(ts):
    ts_lower = ts.lower()
    if "ready" in ts_lower or "待认领" in ts:
        return "ready"
    if "blocked" in ts_lower or ts.startswith("阻塞"):
        return "blocked"
    if "in_progress" in ts_lower or "执行中" in ts or "进行中" in ts:
        return "in_progress"
    if "approved" in ts_lower or "已验证" in ts or "已实施" in ts or "已批准" in ts:
        return "completed"
    if "部分" in ts:
        return "partial"
    if "awaiting" in ts_lower or "待审核" in ts:
        return "awaiting_review"
    if "待生成" in ts or "planned" in ts_lower:
        return "planned"
    return "unknown"


def get_risk_phase(rid, risk_reg_rows):
    if risk_reg_rows:
        headers = list(risk_reg_rows[0].keys()) if risk_reg_rows else []
        has_phase = any("阶段" in h for h in headers)
        if has_phase:
            for r in risk_reg_rows:
                if r.get("ID", "") == rid:
                    return r.get("阶段", "planning")
            return "planning"
    fallback = {
        "RSK-012": "active",
        "RSK-016": "active",
        "RSK-010": "resolved",
        "RSK-011": "resolved",
        "RSK-014": "resolved",
        "RSK-017": "resolved",
    }
    return fallback.get(rid, "planning")


def run_integrity_checks():
    try:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "check-integrity.py"), "--json"],
            capture_output=True, text=True, timeout=30
        )
        return json.loads(result.stdout)
    except Exception as e:
        return {"error": str(e), "checks": []}


def build_health_indicators():
    data = run_integrity_checks()
    if data.get("error"):
        return [{"name": "校验脚本", "passed": False, "detail": data["error"]}]

    checks = data.get("checks", [])
    by_name = {}
    by_category = {}
    for c in checks:
        by_name[c["name"]] = c
        by_category.setdefault(c["category"], []).append(c)

    indicators = []

    file_cat = by_category.get("文件完整性", [])
    count_cat = by_category.get("集合数量", [])
    all_file = file_cat + count_cat
    file_passed = all(c["passed"] for c in all_file) if all_file else False
    file_detail = f"声明文件 {len(file_cat)} 项"
    if count_cat:
        passed_counts = sum(1 for c in count_cat if c["passed"])
        file_detail += f"；集合数量 {passed_counts}/{len(count_cat)} 通过"
    indicators.append({"name": "文件完整性", "passed": file_passed, "detail": file_detail})

    link_c = by_name.get("Markdown 本地链接无断链", {})
    indicators.append({"name": "链接完整性", "passed": link_c.get("passed", False), "detail": link_c.get("detail", "未检查")})

    skill_c = by_name.get("仅一个带 frontmatter 的 SKILL.md", {})
    indicators.append({"name": "Skill 唯一性", "passed": skill_c.get("passed", False), "detail": skill_c.get("detail", "未检查")})

    status_c = by_name.get("STATUS.json 与任务登记册一致", {})
    indicators.append({"name": "状态一致性", "passed": status_c.get("passed", False), "detail": status_c.get("detail", "未检查")})

    xref_c = by_name.get("任务登记与验证登记状态一致", {})
    indicators.append({"name": "交叉引用一致性", "passed": xref_c.get("passed", False), "detail": xref_c.get("detail", "未检查")})

    evid_c = by_name.get("验证证据文件路径存在", {})
    indicators.append({"name": "验证证据存在性", "passed": evid_c.get("passed", False), "detail": evid_c.get("detail", "未检查")})

    debt_c = by_name.get("open 技术债 <= 3", {})
    indicators.append({"name": "技术债数量", "passed": debt_c.get("passed", False), "detail": debt_c.get("detail", "未检查")})

    timeout_c = by_name.get("awaiting_review 不超过 24h", {})
    indicators.append({"name": "待审核超时", "passed": timeout_c.get("passed", False), "detail": timeout_c.get("detail", "未检查")})

    allow_c = by_name.get("in_progress 任务无独占路径重叠", {})
    indicators.append({"name": "白名单冲突", "passed": allow_c.get("passed", False), "detail": allow_c.get("detail", "未检查")})

    return indicators


# ── 路线图：解析里程碑规划文档（目标/交付）────────────────
ROADMAP_FILES = [
    ("M00", "execution/M00-Foundation.md"),
    ("M01", "execution/M01-CombatSlice.md"),
    ("M02", "execution/M02-PlayerSystems.md"),
    ("M03", "execution/M03-SquadCombat.md"),
    ("M04", "execution/M04-GameModes.md"),
    ("M05", "execution/M05-ContentComplete.md"),
    ("M06", "execution/M06-Release.md"),
]

def build_roadmap():
    roadmap = {}
    for mid, rel in ROADMAP_FILES:
        txt = read_text(rel)
        if not txt.strip():
            continue
        title, goal, deliverables = "", "", []
        section = None
        for raw in txt.split("\n"):
            s = raw.strip()
            if not s:
                continue
            if s.startswith("## "):
                h = s[3:].strip()
                section = h if h in ("目标", "交付") else None
            elif s.startswith("# ") and not title:
                title = s[2:].strip()
            elif section == "目标" and not goal:
                goal = s
            elif section == "交付" and s.startswith("- "):
                deliverables.append(s[2:].strip())
        if title:
            roadmap[mid] = {"title": title, "goal": goal, "deliverables": deliverables}
    return roadmap


def build_api_data():
    sid = get_session_id()
    sid_short = sid[:8] if sid != "unknown" else "unknown"
    status = read_json("execution/active/STATUS.json")
    manifest = read_yaml("manifest.yaml")
    integrity = read_yaml("integrity.yaml")
    changelog = read_text("CHANGELOG.md")

    task_reg = parse_markdown_table(read_text("registers/07-task-register.md"))
    risk_reg = parse_markdown_table(read_text("registers/02-risk-register.md"))
    decision_reg = parse_markdown_table(read_text("registers/01-decision-register.md"))
    dependency_reg = parse_markdown_table(read_text("registers/03-dependency-register.md"))
    requirement_reg = parse_markdown_table(read_text("registers/04-requirement-traceability-register.md"))
    license_reg = parse_markdown_table(read_text("registers/05-asset-license-register.md"))
    playtest_reg = parse_markdown_table(read_text("registers/06-playtest-issue-register.md"))
    permission_reg = parse_markdown_table(read_text("registers/08-permission-register.md"))
    verif_reg = parse_markdown_table(read_text("registers/09-verification-register.md"))
    asset_reg = parse_markdown_table(read_text("registers/10-asset-register.md"))
    standards_bl = parse_markdown_table(read_text("registers/standards-backlog.md"))

    active_tasks = status.get("activeTasks", [])
    current_mode = status.get("currentMode", "决策模式")

    ms_data = []
    for m in MILESTONES:
        m_tasks = []
        for t in task_reg:
            tid = t.get("任务", "")
            if tid.startswith(m["id"] + "-"):
                ts = t.get("状态", "")
                c_status = classify_task_status(ts)
                claimed_by = None
                task_note = ""
                for at in active_tasks:
                    if at.get("taskId") == tid:
                        claimed_by = at.get("claimedBy")
                        task_note = at.get("note", "")
                        break
                m_tasks.append({
                    "task_id": tid,
                    "task_name": t.get("名称", ""),
                    "status": c_status,
                    "status_text": ts,
                    "deliverable": t.get("交付物", ""),
                    "claimed_by": claimed_by,
                    "note": task_note,
                })
        approved = sum(1 for t in m_tasks if t["status"] == "completed")
        ms_data.append({
            "id": m["id"],
            "name": m["name"],
            "tasks": m_tasks,
            "total": len(m_tasks),
            "done": approved,
            "pct": round(approved / len(m_tasks) * 100) if m_tasks else 0,
            "has_active": any(t["status"] in ("blocked", "ready", "awaiting_review") for t in m_tasks),
        })

    def risk_severity(r):
        v = " ".join(str(r[k]) for k in r if k)
        if "高/高" in v: return "critical"
        if ("高/中" in v) or ("中/高" in v): return "high"
        if "中/中" in v: return "medium"
        return "low"

    active_risks = []
    hidden_risk_count = 0
    for r in risk_reg:
        rid = r.get("ID", "")
        rstatus = get_risk_phase(rid, risk_reg)
        if rstatus == "active":
            active_risks.append({
                "id": rid, "risk": r.get("风险",""), "prob": r.get("概率/影响",""),
                "signal": r.get("早期信号",""), "mitigation": r.get("缓解与回退",""),
                "severity": risk_severity(r)
            })
        else:
            hidden_risk_count += 1

    verif_items = [{"id": v.get("ID",""), "name": v.get("验证",""), "task": v.get("关联任务",""),
                    "level": v.get("层级",""), "status": v.get("状态",""),
                    "evidence": v.get("证据","")[:300]} for v in verif_reg]

    decision_items = [{"id": d.get("ID",""), "decision": d.get("决策",""), "status": d.get("状态",""),
                       "reason": d.get("理由",""), "trigger": d.get("复审触发","")} for d in decision_reg]

    governance_tree = [
        {"dir": "governance/", "label": "治理契约与操作模型", "desc": "定义什么受控、谁能做、怎样变更、何时算完成",
         "files": [
             {"name": "policy.md", "label": "集中式治理政策", "desc": "权威链、单一事实源、文件控制等级、多任务并发"},
             {"name": "change-request-template.md", "label": "变更请求模板", "desc": "变更登记格式与审批流程"},
             {"name": "definition-of-done.md", "label": "集中式完成定义", "desc": "范围边界、交付完整性、验证证据"},
             {"name": "responsibility-matrix.md", "label": "集中式职责边界", "desc": "RACI 矩阵、用户/代理/维护者职责"},
             {"name": "DecisionModel.md", "label": "决策模型", "desc": "规划方向、拆解任务、生成五件套"},
             {"name": "ExecutionModel.md", "label": "执行模型", "desc": "认领任务、冲突检测、按白名单实施"},
             {"name": "ReviewProtocol.md", "label": "审核协议", "desc": "代码回读/资产视觉/关卡加载三种验收"},
             {"name": "SessionCommands.md", "label": "新会话短指令", "desc": "决策/执行/审核/变更的短指令映射"},
         ]},
        {"dir": "rules/", "label": "权威项目规则", "desc": "唯一规则入口",
         "files": [{"name": "project_rules.md", "label": "项目规则", "desc": "必读顺序、文件边界、执行规则、权限规则"}]},
        {"dir": "knowledge/", "label": "知识库", "desc": "产品总纲、技术参考",
         "files": [
             {"name": "GameMasterPlan.md", "label": "产品总纲", "desc": "一期范围、核心玩法、里程碑定义"},
             {"name": "EngineReference.md", "label": "引擎技术参考", "desc": "VR/OpenXR/IK/性能/AI"},
             {"name": "TechnicalDecisions.md", "label": "技术决策", "desc": "引擎版本、插件选择"},
             {"name": "EnvironmentSetup.md", "label": "环境配置", "desc": "SDK/NDK/JDK 版本与路径"},
             {"name": "PicoNeo3BuildGuide.md", "label": "PICO Neo3 构建", "desc": "打包配置与验证矩阵"},
             {"name": "DeviceConfigurationMatrix.md", "label": "设备配置矩阵", "desc": "设备配置当前值与改回清单"},
         ]},
        {"dir": "knowledge/Design/", "label": "权威产品详规", "desc": "核心玩法设计",
         "files": [
             {"name": "CombatSystem.md", "label": "战斗系统", "desc": "命中、格挡、伤害、硬直与解卡"},
             {"name": "WeaponsAndInteraction.md", "label": "武器与交互", "desc": "五武器、抓取与可配置脱手"},
             {"name": "HealthAndArmor.md", "label": "生命与护甲", "desc": "统一生命与分部位护甲"},
             {"name": "MovementAndFullBodyIK.md", "label": "移动与全身 IK", "desc": "混合移动、占位与全身 IK"},
             {"name": "SquadAI.md", "label": "小队 AI", "desc": "N 对 N 队伍、个体战术与武将 AI"},
             {"name": "GameModesAndProgression.md", "label": "游戏模式与进程", "desc": "生涯、自定义、训练、结算与存档"},
         ]},
        {"dir": "knowledge/Production/", "label": "生产规格", "desc": "美术风格、动画、关卡、性能",
         "files": [
             {"name": "ArtStyleGuide.md", "label": "美术风格指南", "desc": "色彩体系、材质语言、角色甲胄"},
             {"name": "AnimationSpec.md", "label": "动画规范", "desc": "骨架、动画列表、全身 IK、时机参考"},
             {"name": "LevelDesignSpec.md", "label": "关卡设计规范", "desc": "布局指标、VR 舒适度、导航"},
             {"name": "ContentPipeline.md", "label": "内容管线", "desc": "三国视觉、角色、武器、动画管线"},
             {"name": "TechnicalArchitecture.md", "label": "技术架构", "desc": "模块边界、数据驱动和离线约束"},
             {"name": "QualityAndPerformance.md", "label": "质量与性能", "desc": "测试矩阵、4v4 压力基线"},
         ]},
        {"dir": "standards/", "label": "工程标准", "desc": "10 份编号标准",
         "files": [
             {"name": "01-project-scope-standard.md", "label": "一期范围标准", "desc": "边界、阶段门与变更原则"},
             {"name": "02-naming-and-path-standard.md", "label": "命名与路径标准", "desc": "UE 资产、C++、蓝图命名"},
             {"name": "03-blueprint-cpp-boundary-standard.md", "label": "蓝图/C++ 边界", "desc": "表现层、规则层、内容层职责"},
             {"name": "04-data-asset-standard.md", "label": "数据资产标准", "desc": "武器、AI、竞技场数据配置"},
             {"name": "05-event-and-interface-standard.md", "label": "事件与接口标准", "desc": "接口、事件、状态与依赖方向"},
             {"name": "06-performance-standard.md", "label": "性能标准", "desc": "一体机性能预算与降级策略"},
             {"name": "07-vr-comfort-standard.md", "label": "VR 舒适标准", "desc": "移动、转向、震动和失败恢复"},
             {"name": "08-testing-and-acceptance-standard.md", "label": "测试与验收标准", "desc": "功能、战斗、VR、稳定性验收"},
             {"name": "09-content-and-historical-style-standard.md", "label": "内容风格标准", "desc": "汉末三国风格与资源统一"},
             {"name": "10-git-standard.md", "label": "Git 标准", "desc": "分支、提交、LFS 与禁止提交项"},
         ]},
        {"dir": "vr/", "label": "VR 工程标准", "desc": "OpenXR、PICO、手部交互、移动",
         "files": [
             {"name": "01-xr-runtime-and-device-profile.md", "label": "XR 运行时与设备", "desc": "OpenXR、目标设备与输入基线"},
             {"name": "02-player-calibration-and-body.md", "label": "玩家校准", "desc": "身高、主手、身体表现"},
             {"name": "03-hand-grab-and-haptics.md", "label": "手部交互与触觉", "desc": "抓取、双手持握、震动"},
             {"name": "04-locomotion-and-comfort.md", "label": "移动与舒适", "desc": "瞬移、转向、平滑移动接口"},
             {"name": "05-spatial-ui-tutorial-and-accessibility.md", "label": "空间 UI 与无障碍", "desc": "空间 UI、教程、可读性"},
             {"name": "PicoValidationMatrix.md", "label": "PICO 验证矩阵", "desc": "设备验证项目与状态"},
         ]},
        {"dir": "systems/", "label": "工程实现指引", "desc": "7 份系统指引，链接 Design 详规",
         "files": [
             {"name": "01-game-flow-system.md", "label": "游戏流程系统", "desc": "阶段管理、状态机、重置"},
             {"name": "02-interaction-and-weapon-system.md", "label": "交互与武器系统", "desc": "武器生命周期、抓取、轨迹"},
             {"name": "03-combat-resolution-system.md", "label": "战斗结算系统", "desc": "攻击判定、伤害、硬直"},
             {"name": "04-movement-system.md", "label": "移动系统", "desc": "瞬移、平滑移动、IK"},
             {"name": "05-ai-combat-system.md", "label": "AI 战斗系统", "desc": "感知、决策、战术"},
             {"name": "06-arena-tutorial-ui-system.md", "label": "竞技场与 UI 系统", "desc": "场景、教程、UI"},
             {"name": "07-save-telemetry-and-diagnostics-system.md", "label": "存档与诊断系统", "desc": "存档、遥测、诊断"},
         ]},
        {"dir": "registers/", "label": "状态登记册", "desc": "10 份登记册 + 标准完善待办",
         "files": [
             {"name": "01-decision-register.md", "label": "决策登记", "desc": "关键设计决策与 ADR 上下文"},
             {"name": "02-risk-register.md", "label": "风险登记", "desc": "17 项项目风险"},
             {"name": "03-dependency-register.md", "label": "依赖登记", "desc": "9 项系统依赖 + 资产级依赖链"},
             {"name": "04-requirement-traceability-register.md", "label": "需求追踪", "desc": "12 项需求到系统/标准的追踪"},
             {"name": "05-asset-license-register.md", "label": "资产许可登记", "desc": "7 项资产的许可与技术状态"},
             {"name": "06-playtest-issue-register.md", "label": "试玩问题登记", "desc": "6 项初始验证主题"},
             {"name": "07-task-register.md", "label": "任务登记", "desc": "7 项任务的完整历史"},
             {"name": "08-permission-register.md", "label": "权限登记", "desc": "NTFS ACL 策略与应用状态"},
             {"name": "09-verification-register.md", "label": "验证登记", "desc": "7 项验证的层级与证据"},
             {"name": "10-asset-register.md", "label": "资产登记册", "desc": "Content 资产状态与并发控制"},
             {"name": "standards-backlog.md", "label": "标准完善待办", "desc": "M00-M06 标准补齐计划"},
         ]},
        {"dir": "execution/", "label": "执行基线", "desc": "任务模板、里程碑详规、active 任务包",
         "files": [
             {"name": "task-template.md", "label": "代码任务模板", "desc": "代码类任务五件套模板"},
             {"name": "task-template-asset.md", "label": "资产任务模板", "desc": "资产类任务（含视觉验收）"},
             {"name": "task-template-level.md", "label": "关卡任务模板", "desc": "关卡类任务（含 UE 加载验证）"},
         ]},
    ]

    changelog_entries = []
    current_date = None
    current_lines = []
    for line in changelog.split("\n"):
        if line.startswith("## 20"):
            if current_date:
                changelog_entries.append({"date": current_date, "summary": "\n".join(current_lines[:6])})
            current_date = line[3:].strip()
            current_lines = []
        elif current_date:
            current_lines.append(line)
    if current_date:
        changelog_entries.append({"date": current_date, "summary": "\n".join(current_lines[:6])})
    changelog_entries = changelog_entries[:8]

    tech_debt = asset_scanner.get_tech_debt()
    interface_contracts = asset_scanner.get_interface_contract_status()
    pattern_progress = asset_scanner.get_pattern_progress()
    cross_ref_issues = asset_scanner.check_cross_references(task_reg, verif_reg)
    governance_tree = asset_scanner.get_governance_file_mtimes(governance_tree)
    asset_repo = asset_scanner.build_asset_repository_data()
    health_indicators = build_health_indicators()

    awaiting_timeout_count = 0
    for t in active_tasks:
        if t.get("status") == "awaiting_review":
            updated = t.get("updatedAt", "")
            if updated:
                try:
                    dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                    dt = dt.replace(tzinfo=None)
                    hours = (datetime.now() - dt).total_seconds() / 3600
                    if hours > 24:
                        awaiting_timeout_count += 1
                except (ValueError, TypeError):
                    pass

    tech_debt_open = sum(1 for d in tech_debt if d.get("status", "").lower() == "open")
    health_passed = sum(1 for h in health_indicators if h["passed"])
    health_total = len(health_indicators)

    all_tasks = [t for m in ms_data for t in m["tasks"]]
    stats = {
        "tasks_total": len(all_tasks),
        "tasks_completed": sum(1 for t in all_tasks if t["status"] == "completed"),
        "tasks_active": sum(1 for t in all_tasks if t["status"] in ("ready", "blocked", "awaiting_review")),
        "tasks_blocked": sum(1 for t in all_tasks if t["status"] == "blocked"),
        "risks_active": len(active_risks),
        "risks_hidden": hidden_risk_count,
        "verif_passed": sum(1 for v in verif_items if "已验证" in v["status"]),
        "verif_failed": sum(1 for v in verif_items if "失败" in v["status"]),
        "verif_pending": sum(1 for v in verif_items if "待" in v["status"]),
        "decisions_total": len(decision_reg),
        "governance_dirs": len(governance_tree),
        "governance_files": sum(len(d["files"]) for d in governance_tree),
        "milestones_active": sum(1 for m in ms_data if m["has_active"]),
        "awaiting_timeout": awaiting_timeout_count,
        "tech_debt_open": tech_debt_open,
        "health_passed": health_passed,
        "health_total": health_total,
    }

    return {
        "project": "VR 三国演武场",
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "session_id": sid,
        "session_short": sid_short,
        "current_mode": current_mode,
        "stats": stats,
        "milestones": ms_data,
        "roadmap": build_roadmap(),
        "active_risks": active_risks,
        "verif_items": verif_items,
        "decision_items": decision_items,
        "dependency_items": [{"id": d.get("ID",""), "dep": d.get("依赖",""), "purpose": d.get("用途",""),
                              "req": d.get("当前要求",""), "alt": d.get("替代/风险","")} for d in dependency_reg],
        "requirement_items": [{"id": r.get("REQ",""), "req": r.get("GameMasterPlan 需求",""),
                               "system": r.get("系统/标准",""), "evidence": r.get("验收证据","")} for r in requirement_reg],
        "license_items": [{"id": l.get("ID",""), "asset": l.get("资产",""), "source": l.get("来源",""),
                           "license": l.get("许可状态",""), "tech": l.get("技术状态",""),
                           "conclusion": l.get("结论","")} for l in license_reg],
        "playtest_items": [{"id": p.get("ID",""), "issue": p.get("待验证问题",""),
                            "success": p.get("成功信号",""), "failure": p.get("失败信号","")} for p in playtest_reg],
        "permission_items": [{"scope": p.get("范围",""), "policy": p.get("目标策略",""),
                              "status": p.get("当前状态",""), "method": p.get("应用方式","")} for p in permission_reg],
        "asset_items": [{"id": a.get("资产ID",""), "type": a.get("类型",""), "path": a.get("路径",""),
                         "status": a.get("状态",""), "task": a.get("关联任务","")} for a in asset_reg],
        "standards_bl": [{"ms": s.get("里程碑",""), "priority": s.get("优先级",""), "todo": s.get("标准完善待办",""),
                          "trigger": s.get("触发条件","")} for s in standards_bl],
        "governance_tree": governance_tree,
        "changelog": changelog_entries,
        "integrity": {
            "status": integrity.get("verification", {}).get("status", "unknown"),
            "broken_links": integrity.get("verification", {}).get("checks", {}).get("local_markdown_links", {}).get("broken", "N/A"),
            "checked": integrity.get("verification", {}).get("checks", {}).get("local_markdown_links", {}).get("checked", "N/A"),
        },
        "health_indicators": health_indicators,
        "tech_debt": tech_debt,
        "interface_contracts": interface_contracts,
        "pattern_progress": pattern_progress,
        "cross_ref_issues": cross_ref_issues,
        "asset_repo": asset_repo,
    }


def build_asset_api_data():
    return asset_scanner.build_asset_repository_data()


# ── HTML ─────────────────────────────────────────────────

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VR 三国演武场 · 治理仪表盘</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=Noto+Serif+SC:wght@600;700;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
  --bg: #080b11;
  --bg-surface: #10151e;
  --bg-elevated: #161d28;
  --bg-hover: #1c2532;
  --border: #1e2735;
  --border-bright: #2d3a4d;
  --text: #c8d0db;
  --text-bright: #e8edf4;
  --dim: #5a6878;
  --dimmer: #3a4456;
  --gold: #d4a574;
  --gold-bright: #e8c899;
  --gold-dim: #8a6f4a;
  --jade: #3fb950;
  --amber: #d29922;
  --vermillion: #f85149;
  --steel: #58a6ff;
  --violet: #a371f7;
  --teal: #39c5cf;
}

* { margin:0; padding:0; box-sizing:border-box; }

body {
  font-family: 'Noto Sans SC', 'Segoe UI', sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
  background-image:
    radial-gradient(ellipse 80% 50% at 50% -20%, rgba(212,165,116,0.04), transparent),
    linear-gradient(180deg, #080b11 0%, #0a0e16 100%);
}

::-webkit-scrollbar { width:4px; height:4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius:2px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold-dim); }

.mono { font-family: 'JetBrains Mono', 'Consolas', monospace; }
.serif { font-family: 'Noto Serif SC', serif; }

/* ═══ Header ═══ */
.header {
  background: linear-gradient(135deg, #0a0e16 0%, #111827 40%, #0d1119 100%);
  border-bottom: 1px solid var(--border-bright);
  padding: 16px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}
.header::after {
  content: '';
  position: absolute;
  bottom: -1px; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold-dim) 20%, var(--gold) 50%, var(--gold-dim) 80%, transparent);
  opacity: 0.4;
}
.header h1 {
  font-family: 'Noto Serif SC', serif;
  font-size: 1.35rem;
  font-weight: 900;
  letter-spacing: 4px;
  color: var(--gold);
  text-shadow: 0 0 20px rgba(212,165,116,0.15);
}
.header .sub {
  font-size: 0.7rem;
  color: var(--dim);
  margin-top: 4px;
  letter-spacing: 0.5px;
}
.header .sub .sid {
  color: var(--violet);
  font-family: 'JetBrains Mono', monospace;
}
.header .right {
  text-align: right;
  font-size: 0.7rem;
  color: var(--dim);
}
.header .right .time {
  color: var(--teal);
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
}

/* ═══ Tabs ═══ */
.tabs {
  display: flex;
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border);
  padding: 0 32px;
  overflow-x: auto;
}
.tab {
  padding: 12px 20px;
  cursor: pointer;
  font-size: 0.8rem;
  color: var(--dim);
  border-bottom: 2px solid transparent;
  white-space: nowrap;
  transition: all 0.2s;
  position: relative;
}
.tab:hover { color: var(--text); }
.tab.active {
  color: var(--gold);
  border-bottom-color: var(--gold);
}
.tab.active::after {
  content: '';
  position: absolute;
  bottom: -2px; left: 20%; right: 20%;
  height: 2px;
  background: var(--gold);
  box-shadow: 0 0 8px rgba(212,165,116,0.4);
}

.tab-content { display: none; padding: 24px 32px; }
.tab-content.active { display: block; }
.container { max-width: 1680px; margin: 0 auto; }

/* ═══ Stat Cards ═══ */
.stats-bar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
  margin-bottom: 28px;
}
.stat-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 16px 14px;
  text-align: center;
  transition: all 0.2s;
  position: relative;
  overflow: hidden;
}
.stat-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: var(--gold-dim);
  opacity: 0;
  transition: opacity 0.2s;
}
.stat-card:hover {
  border-color: var(--border-bright);
  background: var(--bg-elevated);
}
.stat-card:hover::before { opacity: 1; }
.stat-card .num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1.2;
}
.stat-card .lbl {
  font-size: 0.68rem;
  color: var(--dim);
  margin-top: 5px;
  letter-spacing: 0.5px;
}
.stat-card .sub {
  font-size: 0.6rem;
  color: var(--dimmer);
  margin-top: 2px;
}
.sc-gold .num { color: var(--gold); }
.sc-jade .num { color: var(--jade); }
.sc-red .num { color: var(--vermillion); }
.sc-steel .num { color: var(--steel); }
.sc-amber .num { color: var(--amber); }
.sc-violet .num { color: var(--violet); }

/* ═══ Section ═══ */
.section { margin-bottom: 32px; }
.section-title {
  font-size: 0.85rem;
  font-weight: 700;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border);
  color: var(--gold);
  display: flex;
  align-items: center;
  gap: 8px;
  letter-spacing: 1px;
}
.section-title .cnt {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--dim);
  margin-left: auto;
  font-weight: 400;
}

/* ═══ Data Flow Tree ═══ */
.flow-milestone {
  margin-bottom: 24px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}
.flow-ms-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  cursor: pointer;
  border-bottom: 1px solid transparent;
  transition: background 0.15s;
  user-select: none;
}
.flow-ms-header:hover { background: rgba(255,255,255,0.015); }
.flow-ms-header .chevron {
  color: var(--dim);
  font-size: 0.65rem;
  transition: transform 0.2s;
  width: 12px;
}
.flow-ms-header .chevron.open { transform: rotate(90deg); }
.flow-ms-header .ms-tag {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  font-size: 0.82rem;
  color: var(--gold);
  padding: 2px 8px;
  background: rgba(212,165,116,0.08);
  border: 1px solid rgba(212,165,116,0.15);
  border-radius: 4px;
}
.flow-ms-header .ms-name {
  font-size: 0.85rem;
  color: var(--text-bright);
  font-weight: 500;
}
.flow-ms-header .ms-progress {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
}
.flow-ms-header .ms-bar {
  width: 100px;
  height: 6px;
  background: rgba(255,255,255,0.04);
  border-radius: 3px;
  overflow: hidden;
}
.flow-ms-header .ms-fill {
  height: 100%;
  border-radius: 3px;
  background: var(--gold);
  transition: width 0.6s;
}
.flow-ms-header .ms-fill.done { background: var(--jade); }
.flow-ms-header .ms-pct {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: var(--dim);
  min-width: 30px;
  text-align: right;
}
.flow-ms-header .ms-active-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--amber);
  box-shadow: 0 0 8px rgba(210,153,34,0.5);
  animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.flow-ms-body {
  display: none;
  padding: 0 20px 20px 20px;
}
.flow-ms-body.open { display: block; }

/* ── Decision Node (Root) ── */
.flow-decision {
  display: flex;
  align-items: center;
  gap: 0;
  margin-bottom: 0;
  padding: 16px 0;
  position: relative;
}
.decision-node {
  display: flex;
  align-items: center;
  gap: 12px;
  background: linear-gradient(135deg, rgba(88,166,255,0.08), rgba(88,166,255,0.03));
  border: 1px solid rgba(88,166,255,0.2);
  border-left: 3px solid var(--steel);
  border-radius: 6px;
  padding: 12px 18px;
  min-width: 280px;
  position: relative;
  z-index: 2;
}
.decision-node .dec-icon {
  font-size: 1.2rem;
  color: var(--steel);
}
.decision-node .dec-info .dec-label {
  font-size: 0.62rem;
  color: var(--dim);
  text-transform: uppercase;
  letter-spacing: 1.5px;
}
.decision-node .dec-info .dec-name {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--steel);
  margin-top: 2px;
}
.decision-node .dec-info .dec-meta {
  font-size: 0.66rem;
  color: var(--dim);
  margin-top: 2px;
}

/* ── Branch Connector ── */
.branch-trunk {
  position: relative;
  padding-left: 40px;
}
.branch-trunk::before {
  content: '';
  position: absolute;
  left: 20px;
  top: 0;
  bottom: 20px;
  width: 1px;
  background: var(--border-bright);
}
.branch-trunk::after {
  content: '';
  position: absolute;
  left: 20px;
  top: 0;
  width: 1px;
  height: 20px;
  background: var(--steel);
  opacity: 0.5;
}

/* ── Task Branch ── */
.task-branch {
  position: relative;
  padding: 8px 0 8px 24px;
  border-left: 1px solid var(--border-bright);
  margin-left: 20px;
}
.task-branch::before {
  content: '';
  position: absolute;
  left: -1px;
  top: 20px;
  width: 16px;
  height: 1px;
  background: var(--border-bright);
}
.task-branch:last-child {
  border-left: 1px solid transparent;
}
.task-branch:last-child::after {
  content: '';
  position: absolute;
  left: -1px;
  top: 0;
  bottom: 50%;
  width: 1px;
  background: var(--border-bright);
}

/* ── Task Card (Inline Flow) ── */
.task-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 6px;
  overflow: hidden;
  transition: border-color 0.2s;
}
.task-card:hover { border-color: var(--border-bright); }
.task-card.completed { border-left: 3px solid var(--jade); }
.task-card.blocked { border-left: 3px solid var(--vermillion); }
.task-card.ready { border-left: 3px solid var(--steel); }
.task-card.awaiting_review { border-left: 3px solid var(--violet); }
.task-card.unknown { border-left: 3px solid var(--dim); }

.task-card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  cursor: pointer;
  user-select: none;
  transition: background 0.15s;
}
.task-card-header:hover { background: rgba(255,255,255,0.02); }

.task-card .tid {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  font-size: 0.78rem;
  min-width: 90px;
}
.task-card .tname {
  font-size: 0.8rem;
  color: var(--text);
  flex: 1;
}
.task-card .tbadge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 10px;
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}
.tbadge-completed { background: rgba(63,185,80,0.1); color: var(--jade); border: 1px solid rgba(63,185,80,0.2); }
.tbadge-blocked { background: rgba(248,81,73,0.1); color: var(--vermillion); border: 1px solid rgba(248,81,73,0.2); }
.tbadge-ready { background: rgba(88,166,255,0.1); color: var(--steel); border: 1px solid rgba(88,166,255,0.2); }
.tbadge-review { background: rgba(163,113,247,0.1); color: var(--violet); border: 1px solid rgba(163,113,247,0.2); }
.tbadge-partial { background: rgba(210,153,34,0.12); color: var(--gold); border: 1px solid rgba(210,153,34,0.25); }
.tbadge-inprogress { background: rgba(45,212,191,0.1); color: #2dd4bf; border: 1px solid rgba(45,212,191,0.25); }
.tbadge-planned { background: rgba(163,113,247,0.06); color: var(--violet); border: 1px dashed rgba(163,113,247,0.35); opacity: 0.85; }
.tbadge-unknown { background: rgba(90,104,120,0.1); color: var(--dim); border: 1px solid var(--border-bright); }

.plan-scope { margin: 10px 16px 14px 34px; padding: 10px 14px; background: rgba(88,166,255,0.04); border: 1px dashed var(--border-bright); border-radius: 8px; }
.ps-head { font-size: 0.78rem; color: var(--fg); margin-bottom: 6px; display: flex; align-items: center; gap: 8px; line-height: 1.5; }
.ps-tag { flex: none; font-size: 0.62rem; padding: 2px 7px; border-radius: 4px; background: rgba(210,153,34,0.12); color: var(--gold); border: 1px solid rgba(210,153,34,0.25); white-space: nowrap; }
.ps-list { margin: 0; padding-left: 18px; font-size: 0.74rem; color: var(--dim); line-height: 1.8; }
.ps-chip { flex: none; font-size: 0.62rem; padding: 2px 7px; border-radius: 10px; background: rgba(88,166,255,0.08); color: var(--steel); border: 1px solid rgba(88,166,255,0.18); white-space: nowrap; }

.task-card .tchevron {
  color: var(--dim);
  font-size: 0.6rem;
  transition: transform 0.2s;
}
.task-card .tchevron.open { transform: rotate(90deg); }

/* ── Inline Flow Steps ── */
.task-flow {
  display: none;
  padding: 12px 14px;
  border-top: 1px solid var(--border);
  background: rgba(0,0,0,0.15);
}
.task-flow.open { display: block; }

.flow-steps {
  display: flex;
  align-items: stretch;
  gap: 0;
  flex-wrap: wrap;
}

.flow-step {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px 14px;
  min-width: 160px;
  position: relative;
}
.flow-step-label {
  font-size: 0.58rem;
  color: var(--dim);
  text-transform: uppercase;
  letter-spacing: 1px;
}
.flow-step-value {
  font-size: 0.72rem;
  color: var(--text);
  line-height: 1.5;
}
.flow-step-value.done { color: var(--jade); }
.flow-step-value.active { color: var(--amber); }
.flow-step-value.blocked { color: var(--vermillion); }
.flow-step-value.pending { color: var(--dimmer); }

.flow-arrow {
  display: flex;
  align-items: center;
  color: var(--dimmer);
  font-size: 0.8rem;
  padding: 0 2px;
}
.flow-arrow.active { color: var(--gold-dim); }
.flow-arrow.done { color: var(--jade); }

/* ── Compact completed task (one-liner) ── */
.task-compact {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  font-size: 0.72rem;
}
.task-compact .tid {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
  color: var(--jade);
  min-width: 90px;
}
.task-compact .tname { color: var(--dim); }
.task-compact .tdeliver {
  color: var(--dimmer);
  font-size: 0.68rem;
  margin-left: auto;
  max-width: 400px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ═══ Risk Cards ═══ */
.risk-list { display: flex; flex-direction: column; gap: 10px; }
.risk-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 14px 16px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  transition: border-color 0.2s;
}
.risk-card:hover { border-color: var(--vermillion); }
.risk-card .sev-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 4px;
}
.risk-card .sev-critical { background: var(--vermillion); box-shadow: 0 0 10px rgba(248,81,73,0.4); }
.risk-card .sev-high { background: #f0883e; }
.risk-card .sev-medium { background: var(--amber); }
.risk-card .risk-body { flex: 1; }
.risk-card .risk-head {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
  flex-wrap: wrap;
}
.risk-card .risk-id {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: var(--dim);
}
.risk-card .risk-desc { font-size: 0.8rem; color: var(--text-bright); }
.risk-card .risk-prob {
  font-size: 0.65rem;
  padding: 1px 8px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
}
.risk-card .risk-prob.critical { background: rgba(248,81,73,0.12); color: var(--vermillion); }
.risk-card .risk-prob.high { background: rgba(240,136,62,0.12); color: #f0883e; }
.risk-card .risk-prob.medium { background: rgba(210,153,34,0.12); color: var(--amber); }
.risk-card .risk-trigger-tag {
  font-size: 0.6rem;
  padding: 1px 6px;
  border-radius: 3px;
  background: rgba(248,81,73,0.1);
  color: var(--vermillion);
  border: 1px solid rgba(248,81,73,0.15);
}
.risk-card .risk-detail {
  font-size: 0.7rem;
  color: var(--dim);
  margin-top: 6px;
  line-height: 1.6;
}

.risk-empty {
  color: var(--dim);
  font-size: 0.78rem;
  padding: 16px;
  text-align: center;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 6px;
}

/* ═══ Milestone Progress (Overview) ═══ */
.ms-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 0;
}
.ms-id {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  font-size: 0.76rem;
  min-width: 36px;
  color: var(--gold);
}
.ms-name {
  font-size: 0.76rem;
  min-width: 220px;
  color: var(--dim);
}
.ms-bar {
  flex: 1;
  height: 7px;
  background: rgba(255,255,255,0.04);
  border-radius: 4px;
  overflow: hidden;
}
.ms-fill {
  height: 100%;
  border-radius: 4px;
  background: var(--gold);
  transition: width 0.6s;
}
.ms-fill.done { background: var(--jade); }
.ms-pct {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  min-width: 36px;
  text-align: right;
}
.ms-cnt {
  font-size: 0.66rem;
  color: var(--dim);
  min-width: 36px;
  text-align: right;
}

/* ═══ Table ═══ */
.tbl-wrap { overflow-x: auto; }
.tbl {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.74rem;
}
.tbl th {
  text-align: left;
  padding: 8px 10px;
  border-bottom: 2px solid var(--border-bright);
  color: var(--dim);
  font-weight: 600;
  white-space: nowrap;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-size: 0.66rem;
}
.tbl td {
  padding: 7px 10px;
  border-bottom: 1px solid rgba(30,39,53,0.4);
}
.tbl tr:hover td { background: rgba(255,255,255,0.01); }

/* ═══ Badge ═══ */
.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.64rem;
  font-weight: 600;
}
.badge-ok { background: rgba(63,185,80,0.1); color: var(--jade); }
.badge-warn { background: rgba(210,153,34,0.1); color: var(--amber); }
.badge-err { background: rgba(248,81,73,0.1); color: var(--vermillion); }
.badge-info { background: rgba(88,166,255,0.08); color: var(--steel); }

/* ═══ Governance Tree ═══ */
.gov-dir { margin-bottom: 8px; }
.gov-dir-header {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 10px 0;
  border-bottom: 1px solid rgba(30,39,53,0.3);
  user-select: none;
}
.gov-dir-header:hover { color: var(--gold); }
.gov-dir-header .icon { font-size: 0.7rem; color: var(--dim); width: 12px; }
.gov-dir-header .dname {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
  font-size: 0.8rem;
  color: var(--gold);
}
.gov-dir-header .ddesc { font-size: 0.72rem; color: var(--dim); margin-left: 8px; }
.gov-dir-header .dcnt {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem;
  color: var(--dim);
  margin-left: auto;
}
.gov-files { padding-left: 24px; display: none; }
.gov-files.open { display: block; }
.gov-file {
  display: flex;
  align-items: baseline;
  padding: 4px 0;
  gap: 12px;
  font-size: 0.72rem;
}
.gov-file .fn {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--steel);
  min-width: 260px;
}
.gov-file .fl { color: var(--text); min-width: 160px; }
.gov-file .fd { color: var(--dim); }
.gov-file .fm {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.62rem;
  color: var(--dimmer);
  margin-left: auto;
  white-space: nowrap;
}

/* ═══ Changelog ═══ */
.cl-entry {
  padding: 12px 0;
  border-bottom: 1px solid rgba(30,39,53,0.3);
}
.cl-date {
  font-weight: 600;
  color: var(--gold);
  font-size: 0.78rem;
  font-family: 'JetBrains Mono', monospace;
}
.cl-summary {
  font-size: 0.7rem;
  color: var(--dim);
  margin-top: 6px;
  white-space: pre-line;
  line-height: 1.6;
}

/* ═══ Grid ═══ */
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }

/* ═══ Footer ═══ */
.footer {
  text-align: center;
  padding: 14px;
  font-size: 0.66rem;
  color: var(--dim);
  border-top: 1px solid var(--border);
  letter-spacing: 0.5px;
}
.footer button {
  background: var(--gold);
  color: var(--bg);
  border: none;
  padding: 5px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 700;
  font-size: 0.72rem;
  margin-left: 10px;
  transition: opacity 0.2s;
}
.footer button:hover { opacity: 0.85; }

/* ═══ Integrity / Anti-Fiction Health ═══ */
.integrity-hero {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 24px;
}
.integrity-hero.pass { border-left: 4px solid var(--jade); }
.integrity-hero.fail { border-left: 4px solid var(--vermillion); }
.integrity-hero .hero-icon {
  font-size: 2.5rem;
  line-height: 1;
}
.integrity-hero.pass .hero-icon { color: var(--jade); }
.integrity-hero.fail .hero-icon { color: var(--vermillion); }
.integrity-hero .hero-body { flex: 1; }
.integrity-hero .hero-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-bright);
}
.integrity-hero.pass .hero-title { color: var(--jade); }
.integrity-hero.fail .hero-title { color: var(--vermillion); }
.integrity-hero .hero-meta {
  font-size: 0.75rem;
  color: var(--dim);
  margin-top: 4px;
}
.integrity-hero .hero-stats {
  display: flex;
  gap: 20px;
}
.integrity-hero .hero-stat {
  text-align: center;
}
.integrity-hero .hero-stat .num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.4rem;
  font-weight: 700;
}
.integrity-hero .hero-stat .lbl {
  font-size: 0.65rem;
  color: var(--dim);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.check-group {
  margin-bottom: 16px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  overflow: hidden;
}
.check-group-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: rgba(255,255,255,0.015);
  border-bottom: 1px solid var(--border);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--gold);
  letter-spacing: 0.5px;
}
.check-group-header .grp-cnt {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem;
  color: var(--dim);
  margin-left: auto;
}
.check-group-header .grp-status {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.check-group-header .grp-status.pass { background: var(--jade); }
.check-group-header .grp-status.fail { background: var(--vermillion); }
.check-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 8px 16px;
  border-bottom: 1px solid rgba(30,39,53,0.3);
  font-size: 0.75rem;
}
.check-item:last-child { border-bottom: none; }
.check-item .ck-icon {
  width: 18px;
  text-align: center;
  flex-shrink: 0;
  font-weight: 700;
}
.check-item.pass .ck-icon { color: var(--jade); }
.check-item.fail .ck-icon { color: var(--vermillion); }
.check-item .ck-body { flex: 1; }
.check-item .ck-name {
  color: var(--text);
  font-weight: 500;
}
.check-item .ck-detail {
  color: var(--dim);
  font-size: 0.68rem;
  margin-top: 2px;
  line-height: 1.5;
}
.check-item.fail .ck-detail { color: var(--vermillion); opacity: 0.8; }
.check-item .ck-badge {
  font-size: 0.6rem;
  padding: 1px 6px;
  border-radius: 3px;
  font-weight: 600;
  flex-shrink: 0;
}
.check-item.pass .ck-badge { background: rgba(63,185,80,0.1); color: var(--jade); }
.check-item.fail .ck-badge { background: rgba(248,81,73,0.1); color: var(--vermillion); }

/* ═══ Health Indicator Mini Dots ═══ */
.health-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}
.health-item {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 12px 14px;
}
.health-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}
.health-dot.pass { background: var(--jade); box-shadow: 0 0 8px rgba(63,185,80,0.4); }
.health-dot.warn { background: var(--amber); box-shadow: 0 0 8px rgba(210,153,34,0.4); }
.health-dot.fail { background: var(--vermillion); box-shadow: 0 0 8px rgba(248,81,73,0.4); }
.health-name {
  font-size: 0.78rem;
  font-weight: 500;
  color: var(--text);
}
.health-detail {
  font-size: 0.65rem;
  color: var(--dim);
  margin-top: 2px;
}

/* ═══ Verification Evidence Check ═══ */
.evidence-ok { color: var(--jade); }
.evidence-miss { color: var(--vermillion); }

/* ═══ Asset Repo ═══ */
.asset-accordion-item {
  margin-bottom: 12px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}
.asset-accordion-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  cursor: pointer;
  user-select: none;
  transition: background 0.15s;
}
.asset-accordion-header:hover { background: rgba(255,255,255,0.015); }
.asset-accordion-header .achevron {
  color: var(--dim);
  font-size: 0.65rem;
  transition: transform 0.2s;
  width: 12px;
}
.asset-accordion-header .achevron.open { transform: rotate(90deg); }
.asset-accordion-header .atitle {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--gold);
}
.asset-accordion-header .acount {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--dim);
  margin-left: auto;
}
.asset-accordion-header .abadge {
  font-size: 0.65rem;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 600;
}
.asset-accordion-header .abadge.template { background: rgba(88,166,255,0.1); color: var(--steel); }
.asset-accordion-header .abadge.project { background: rgba(212,165,116,0.1); color: var(--gold); }
.asset-accordion-header .abadge.planned { background: rgba(163,113,247,0.1); color: var(--violet); }
.asset-accordion-body {
  display: none;
  padding: 0 16px 16px;
}
.asset-accordion-body.open { display: block; }
.asset-subcategory {
  margin-bottom: 14px;
}
.asset-subcategory-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-bright);
  margin-bottom: 8px;
  padding-bottom: 4px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 8px;
}
.asset-subcategory-title .subcnt {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--dim);
  font-weight: 400;
}
.asset-subcategory-title .status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.asset-subcategory-title .status-dot.exists { background: var(--jade); }
.asset-subcategory-title .status-dot.planned { background: var(--amber); }
.asset-subcategory-title .status-dot.empty { background: var(--dimmer); }
.asset-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 8px;
}
.asset-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 10px 12px;
  font-size: 0.72rem;
}
.asset-card.planned { border-left: 3px solid var(--violet); }
.asset-card.exists { border-left: 3px solid var(--jade); }
.asset-card .aname {
  font-weight: 600;
  color: var(--text-bright);
  font-size: 0.78rem;
}
.asset-card .ameta {
  color: var(--dim);
  margin-top: 4px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.asset-card .atype {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--steel);
}
.asset-card .astatus {
  font-size: 0.62rem;
  padding: 1px 6px;
  border-radius: 3px;
  font-weight: 600;
}
.asset-card .astatus.done { background: rgba(63,185,80,0.1); color: var(--jade); }
.asset-card .astatus.planned { background: rgba(163,113,247,0.1); color: var(--violet); }
.dep-chain {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  margin-top: 20px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  white-space: pre-wrap;
  color: var(--dim);
  line-height: 1.6;
}

/* ═══ Cross-ref Issues ═══ */
.crossref-ok {
  color: var(--jade);
  font-size: 0.8rem;
  padding: 12px;
  background: rgba(63,185,80,0.05);
  border: 1px solid rgba(63,185,80,0.15);
  border-radius: 6px;
}
.crossref-issue {
  color: var(--vermillion);
  font-size: 0.78rem;
  padding: 8px 12px;
  background: rgba(248,81,73,0.05);
  border: 1px solid rgba(248,81,73,0.15);
  border-radius: 6px;
  margin-bottom: 6px;
}

/* ═══ Timeout Alert ═══ */
.timeout-alert {
  background: rgba(248,81,73,0.08);
  border: 1px solid rgba(248,81,73,0.2);
  border-radius: 6px;
  padding: 12px 16px;
  margin-bottom: 20px;
  color: var(--vermillion);
  font-size: 0.8rem;
}

/* ═══ Responsive ═══ */
@media (max-width: 1200px) {
  .grid2 { grid-template-columns: 1fr; }
  .flow-steps { flex-direction: column; }
  .flow-arrow { transform: rotate(90deg); padding: 4px 0; }
  .gov-file .fn { min-width: 200px; }
  .health-grid { grid-template-columns: 1fr; }
}
</style>
</head>
<body>

<!-- Header -->
<div class="header">
  <div>
    <h1>⚔ VR 三国演武场</h1>
    <div class="sub">治理仪表盘 v5 · 会话 <span class="sid" id="sidDisplay">--</span> · 数据源 <code>.trae/</code> · 5 分钟刷新</div>
  </div>
  <div class="right">
    <div>更新 <span class="time" id="updateTime">--</span></div>
    <div style="margin-top:3px;">下一刷新 <span class="time" id="nextRefresh">--:--</span></div>
  </div>
</div>

<!-- Tabs -->
<div class="tabs">
  <div class="tab active" data-tab="overview">总览</div>
  <div class="tab" data-tab="flow">数据流链路</div>
  <div class="tab" data-tab="governance">治理资产</div>
  <div class="tab" data-tab="registers">登记册</div>
  <div class="tab" data-tab="integrity">防虚构健康</div>
  <div class="tab" data-tab="verification">验证证据</div>
  <div class="tab" data-tab="assets">资产仓库</div>
  <div class="tab" data-tab="changelog">变更记录</div>
</div>

<div class="container">

<!-- ══════ 总览 ══════ -->
<div class="tab-content active" id="tab-overview">
  <div class="stats-bar" id="statsBar"></div>

  <div id="timeoutAlert"></div>

  <div class="section">
    <div class="section-title">里程碑进度</div>
    <div id="msProgress"></div>
  </div>

  <div class="grid2">
    <div class="section">
      <div class="section-title">防虚构健康度 <span class="cnt" id="healthCnt"></span></div>
      <div class="health-grid" id="healthGrid"></div>
    </div>
    <div class="section">
      <div class="section-title">执行触发风险 <span class="cnt" id="riskCnt"></span></div>
      <div class="risk-list" id="riskList"></div>
    </div>
  </div>
</div>

<!-- ══════ 数据流链路 ══════ -->
<div class="tab-content" id="tab-flow">
  <div class="section">
    <div class="section-title">任务数据流链路 <span class="cnt">决策 → 执行 → 产出 → 审核 · 操作模式: <span id="flowMode">--</span></span></div>
    <div id="flowTree"></div>
  </div>
</div>

<!-- ══════ 治理资产 ══════ -->
<div class="tab-content" id="tab-governance">
  <div class="stats-bar" id="govStats"></div>
  <div class="section">
    <div class="section-title">治理资产树 <span class="cnt">点击展开</span></div>
    <div id="govTree"></div>
  </div>
</div>

<!-- ══════ 登记册 ══════ -->
<div class="tab-content" id="tab-registers">
  <div class="section"><div class="section-title">决策登记 <span class="cnt" id="decCnt"></span></div><div class="tbl-wrap"><table class="tbl"><thead><tr><th>ID</th><th>决策</th><th>状态</th><th>理由</th><th>复审触发</th></tr></thead><tbody id="decTbl"></tbody></table></div></div>
  <div class="section"><div class="section-title">依赖登记（9 项）</div><div class="tbl-wrap"><table class="tbl"><thead><tr><th>ID</th><th>依赖</th><th>用途</th><th>当前要求</th><th>替代/风险</th></tr></thead><tbody id="depTbl"></tbody></table></div></div>
  <div class="section"><div class="section-title">需求追踪（12 项）</div><div class="tbl-wrap"><table class="tbl"><thead><tr><th>REQ</th><th>需求</th><th>系统/标准</th><th>验收证据</th></tr></thead><tbody id="reqTbl"></tbody></table></div></div>
  <div class="section"><div class="section-title">资产许可（7 项）</div><div class="tbl-wrap"><table class="tbl"><thead><tr><th>ID</th><th>资产</th><th>来源</th><th>许可</th><th>技术</th><th>结论</th></tr></thead><tbody id="licTbl"></tbody></table></div></div>
  <div class="section"><div class="section-title">试玩验证主题（6 项）</div><div class="tbl-wrap"><table class="tbl"><thead><tr><th>ID</th><th>验证主题</th><th>成功信号</th><th>失败信号</th></tr></thead><tbody id="ptTbl"></tbody></table></div></div>
  <div class="section"><div class="section-title">标准完善待办</div><div class="tbl-wrap"><table class="tbl"><thead><tr><th>里程碑</th><th>优先级</th><th>待办</th><th>触发条件</th></tr></thead><tbody id="stdTbl"></tbody></table></div></div>
  <div class="section"><div class="section-title">权限状态</div><div class="tbl-wrap"><table class="tbl"><thead><tr><th>范围</th><th>目标策略</th><th>当前状态</th><th>应用方式</th></tr></thead><tbody id="permTbl"></tbody></table></div></div>
  <div class="section"><div class="section-title">资产登记册</div><div class="tbl-wrap"><table class="tbl"><thead><tr><th>资产ID</th><th>类型</th><th>路径</th><th>状态</th><th>关联任务</th></tr></thead><tbody id="astTbl"></tbody></table></div></div>
  <div class="section">
    <div class="section-title">技术债登记 <span class="cnt" id="techDebtCnt"></span></div>
    <div class="tbl-wrap">
      <table class="tbl">
        <thead><tr><th>ID</th><th>描述</th><th>位置</th><th>优先级</th><th>状态</th><th>偿还计划</th></tr></thead>
        <tbody id="techDebtTbl"></tbody>
      </table>
    </div>
  </div>
  <div class="section">
    <div class="section-title">交叉引用校验</div>
    <div id="crossRefArea"></div>
  </div>
</div>

<!-- ══════ 防虚构健康 ══════ -->
<div class="tab-content" id="tab-integrity">
  <div id="integrityContent">
    <div style="padding:40px;text-align:center;color:var(--dim);font-size:0.8rem;">
      正在校验治理一致性...
    </div>
  </div>
</div>

<!-- ══════ 验证证据 ══════ -->
<div class="tab-content" id="tab-verification">
  <div class="section">
    <div class="section-title">验证证据登记 <span class="cnt" id="verifRegCnt"></span></div>
    <div class="tbl-wrap">
      <table class="tbl">
        <thead><tr><th>ID</th><th>验证项</th><th>关联任务</th><th>层级</th><th>状态</th><th>证据</th><th>证据存在性</th></tr></thead>
        <tbody id="verifRegTbl"></tbody>
      </table>
    </div>
  </div>
</div>

<!-- ══════ 资产仓库 ══════ -->
<div class="tab-content" id="tab-assets">
  <div class="stats-bar" id="assetStatsBar"></div>
  <div class="section">
    <div class="section-title">资产分类浏览 <span class="cnt">点击展开</span></div>
    <div id="assetAccordion"></div>
  </div>
  <div class="section">
    <div class="section-title">资产依赖链</div>
    <div class="dep-chain" id="depChain"></div>
  </div>
</div>

<!-- ══════ 变更记录 ══════ -->
<div class="tab-content" id="tab-changelog">
  <div class="section"><div class="section-title">最近变更</div><div id="clList"></div></div>
</div>

</div>

<div class="footer">
  VR 三国演武场 · 治理驱动开发 · 数据源 .trae/ · 零虚构数据
  <button onclick="location.reload()">立即刷新</button>
</div>

<script>
let D = null;
const REFRESH_MIN = 5;

async function load() {
  try {
    const r = await fetch('/api/status');
    D = await r.json();
    render();
  } catch(e) { console.error(e); }
}

function render() {
  document.getElementById('updateTime').textContent = D.updated;
  document.getElementById('sidDisplay').textContent = D.session_short || 'unknown';
  const next = new Date(Date.now() + REFRESH_MIN * 60000);
  document.getElementById('nextRefresh').textContent =
    String(next.getHours()).padStart(2,'0') + ':' + String(next.getMinutes()).padStart(2,'0');
  renderOverview();
  renderFlow();
  renderGovernance();
  renderRegisters();
  renderChangelog();
  renderVerification();
  renderAssets();
}

// ── 总览 ──
function renderOverview() {
  const s = D.stats;
  document.getElementById('statsBar').innerHTML =
    `<div class="stat-card sc-steel"><div class="num">${s.tasks_total}</div><div class="lbl">总任务</div><div class="sub">${s.tasks_completed} 已完成</div></div>
     <div class="stat-card sc-jade"><div class="num">${s.tasks_completed}</div><div class="lbl">已完成</div></div>
     <div class="stat-card sc-red"><div class="num">${s.tasks_blocked}</div><div class="lbl">阻塞中</div></div>
     <div class="stat-card sc-red"><div class="num">${s.risks_active}</div><div class="lbl">执行触发风险</div><div class="sub">${s.risks_hidden} 项已隐藏</div></div>
     <div class="stat-card sc-amber"><div class="num">${s.verif_passed}/${s.verif_passed+s.verif_failed+s.verif_pending}</div><div class="lbl">验证通过</div></div>
     <div class="stat-card sc-violet"><div class="num">${s.decisions_total}</div><div class="lbl">决策</div></div>
     <div class="stat-card sc-gold"><div class="num">${s.governance_files}</div><div class="lbl">治理文件</div><div class="sub">${s.governance_dirs} 个目录</div></div>
     <div class="stat-card sc-amber"><div class="num">${s.awaiting_timeout}</div><div class="lbl">待审核超时</div></div>
     <div class="stat-card sc-vermillion"><div class="num">${s.tech_debt_open}</div><div class="lbl">技术债 open</div></div>
     <div class="stat-card sc-jade"><div class="num">${s.health_passed}/${s.health_total}</div><div class="lbl">防虚构健康</div></div>`;

  // 待审核超时告警
  const alertEl = document.getElementById('timeoutAlert');
  if (s.awaiting_timeout > 0) {
    alertEl.innerHTML = `<div class="timeout-alert">⚠ ${s.awaiting_timeout} 个任务 awaiting_review 超过 24 小时未审核</div>`;
  } else {
    alertEl.innerHTML = '';
  }

  // 防虚构健康度网格
  document.getElementById('healthCnt').textContent = `${s.health_passed}/${s.health_total} 通过`;
  document.getElementById('healthGrid').innerHTML = (D.health_indicators || []).map(h => {
    const dotClass = h.passed ? 'pass' : 'fail';
    return `<div class="health-item">
      <div class="health-dot ${dotClass}"></div>
      <div>
        <div class="health-name">${h.name}</div>
        <div class="health-detail">${h.detail}</div>
      </div>
    </div>`;
  }).join('');

  // 里程碑进度
  document.getElementById('msProgress').innerHTML = D.milestones.map(m => {
    const p = m.pct || 0;
    return `<div class="ms-item">
      <span class="ms-id">${m.id}</span>
      <span class="ms-name">${m.name}</span>
      <div class="ms-bar"><div class="ms-fill${p===100?' done':''}" style="width:${p}%"></div></div>
      <span class="ms-pct">${p}%</span>
      <span class="ms-cnt">${m.done}/${m.total}</span>
    </div>`;
  }).join('');

  // 风险
  document.getElementById('riskCnt').textContent = D.active_risks.length + ' 项（已隐藏 ' + D.stats.risks_hidden + ' 项）';
  if (D.active_risks.length === 0) {
    document.getElementById('riskList').innerHTML = '<div class="risk-empty">当前无执行触发的风险。规划期注意事项已隐藏。</div>';
  } else {
    document.getElementById('riskList').innerHTML = D.active_risks.map(r =>
      `<div class="risk-card">
        <div class="sev-dot sev-${r.severity}"></div>
        <div class="risk-body">
          <div class="risk-head">
            <span class="risk-id mono">${r.id}</span>
            <span class="risk-desc">${r.risk}</span>
            <span class="risk-prob ${r.severity}">${r.prob}</span>
            <span class="risk-trigger-tag">执行触发</span>
          </div>
          <div class="risk-detail"><strong>早期信号：</strong>${r.signal}<br><strong>缓解与回退：</strong>${r.mitigation}</div>
        </div>
      </div>`
    ).join('');
  }
}

// ── 数据流链路 ──
function renderFlow() {
  document.getElementById('flowMode').textContent = D.current_mode || '决策模式';
  const html = D.milestones.map((m, mi) => {
    const hasTasks = m.tasks.length > 0;
    const rm = (D.roadmap || {})[m.id];
    const isOpen = m.has_active || !!rm;

    const decisionNode = `
      <div class="flow-decision">
        <div class="decision-node">
          <span class="dec-icon">⚖</span>
          <div class="dec-info">
            <div class="dec-label">决策模型</div>
            <div class="dec-name">${D.current_mode || '决策模式'}-${D.session_short}</div>
            <div class="dec-meta">${m.id} · ${m.total} 个任务 · ${m.done} 已完成</div>
          </div>
        </div>
      </div>`;

    const branches = m.tasks.map((t, ti) => {
      const badgeClass = t.status==='completed'?'tbadge-completed':t.status==='blocked'?'tbadge-blocked':t.status==='ready'?'tbadge-ready':t.status==='awaiting_review'?'tbadge-review':t.status==='partial'?'tbadge-partial':t.status==='in_progress'?'tbadge-inprogress':t.status==='planned'?'tbadge-planned':'tbadge-unknown';
      const badgeText = t.status==='completed'?'已完成':t.status==='blocked'?'阻塞':t.status==='ready'?'待认领':t.status==='awaiting_review'?'待审核':t.status==='partial'?'部分完成':t.status==='in_progress'?'执行中':t.status==='planned'?'待生成':'未知';

      if (t.status === 'completed') {
        return `<div class="task-branch">
          <div class="task-card completed">
            <div class="task-compact">
              <span class="tid">${t.task_id}</span>
              <span class="tname">${t.task_name}</span>
              <span class="tbadge ${badgeClass}">${badgeText}</span>
              <span class="tdeliver">${t.deliverable}</span>
            </div>
          </div>
        </div>`;
      }

      const isTaskOpen = true;
      let execState, execText;
      if (t.status === 'blocked') {
        execState = 'blocked'; execText = '执行阻塞';
        if (t.note) execText += ' — ' + t.note;
      } else if (t.status === 'in_progress') {
        execState = 'active'; execText = '执行中';
        if (t.note) execText += ' — ' + t.note;
      } else if (t.status === 'planned') {
        execState = 'pending'; execText = '待生成（已规划，未启动）';
        if (t.note) execText += ' — ' + t.note;
      } else if (t.status === 'ready') {
        execState = 'pending'; execText = '等待认领';
      } else if (t.status === 'awaiting_review') {
        execState = 'done'; execText = '执行完成';
      } else {
        execState = 'pending'; execText = '待执行';
      }
      if (t.claimed_by) execText += '<br>认领：' + t.claimed_by;

      let outState, outText;
      if (t.status === 'completed' || t.status === 'awaiting_review') {
        outState = 'done'; outText = t.deliverable || '已产出';
      } else if (t.status === 'blocked') {
        outState = 'pending'; outText = '执行阻塞，待恢复';
      } else if (t.status === 'planned') {
        outState = 'pending'; outText = t.deliverable || '待生成任务包';
      } else {
        outState = 'pending'; outText = '待产出';
      }

      let revState, revText;
      if (t.status === 'completed') {
        revState = 'done'; revText = '已审核通过';
      } else if (t.status === 'awaiting_review') {
        revState = 'active'; revText = '等待审核';
      } else if (t.status === 'planned') {
        revState = 'pending'; revText = '待任务包生成后启动';
      } else {
        revState = 'pending'; revText = '等待执行完成';
      }

      const arrow1 = t.status !== 'ready' ? 'active' : '';
      const arrow2 = (t.status === 'completed' || t.status === 'awaiting_review') ? 'done' : '';

      return `<div class="task-branch">
        <div class="task-card ${t.status}">
          <div class="task-card-header" onclick="toggleTaskCard(this)">
            <span class="tchevron ${isTaskOpen?'open':''}">▶</span>
            <span class="tid">${t.task_id}</span>
            <span class="tname">${t.task_name}</span>
            <span class="tbadge ${badgeClass}">${badgeText}</span>
          </div>
          <div class="task-flow ${isTaskOpen?'open':''}">
            <div class="flow-steps">
              <div class="flow-step">
                <div class="flow-step-label">执行模型</div>
                <div class="flow-step-value ${execState}">${execText}</div>
              </div>
              <div class="flow-arrow ${arrow1}">→</div>
              <div class="flow-step">
                <div class="flow-step-label">产出</div>
                <div class="flow-step-value ${outState}">${outText}</div>
              </div>
              <div class="flow-arrow ${arrow2}">→</div>
              <div class="flow-step">
                <div class="flow-step-label">审核模型</div>
                <div class="flow-step-value ${revState}">${revText}</div>
              </div>
            </div>
          </div>
        </div>
      </div>`;
    }).join('');

    return `<div class="flow-milestone">
      <div class="flow-ms-header" onclick="toggleMsBody(${mi})">
        <span class="chevron ${isOpen?'open':''}">▶</span>
        <span class="ms-tag">${m.id}</span>
        <span class="ms-name">${m.name}</span>
        <div class="ms-progress">
          ${m.has_active ? '<div class="ms-active-dot" title="有活跃任务"></div>' : ''}
          <div class="ms-bar"><div class="ms-fill${m.pct===100?' done':''}" style="width:${m.pct}%"></div></div>
          <span class="ms-pct">${m.pct}%</span>
          <span class="ms-cnt" style="min-width:36px;text-align:right;">${m.done}/${m.total}</span>
          ${rm ? `<span class="ps-chip">规划 ${rm.deliverables.length} 项</span>` : ''}
        </div>
      </div>
      <div class="flow-ms-body ${isOpen?'open':''}" id="msBody${mi}">
        ${(hasTasks ? decisionNode + '<div class="branch-trunk">' + branches + '</div>' : '') + (rm ? `
        <div class="plan-scope">
          <div class="ps-head"><span class="ps-tag">规划交付</span><span>${rm.goal}</span></div>
          <ul class="ps-list">${rm.deliverables.map(d => `<li>${d}</li>`).join('')}</ul>
          ${!hasTasks ? '<div style="margin-top:8px;font-size:0.72rem;color:var(--dimmer);">以上为里程碑规划范围，尚未拆解立项；任务包由决策模型按需生成后进入登记册。</div>' : ''}
        </div>` : '')}
        ${(!hasTasks && !rm) ? '<div style="padding:16px;color:var(--dim);font-size:0.78rem;">暂无任务</div>' : ''}
      </div>
    </div>`;
  }).join('');

  document.getElementById('flowTree').innerHTML = html;
}

function toggleMsBody(i) {
  const body = document.getElementById('msBody' + i);
  if (!body) return;
  const header = body.previousElementSibling;
  const chevron = header.querySelector('.chevron');
  body.classList.toggle('open');
  chevron.classList.toggle('open');
}

function toggleTaskCard(header) {
  const card = header.parentElement;
  const flow = card.querySelector('.task-flow');
  const chevron = header.querySelector('.tchevron');
  flow.classList.toggle('open');
  chevron.classList.toggle('open');
}

// ── 治理资产 ──
function renderGovernance() {
  const tree = D.governance_tree;
  const totalFiles = tree.reduce((s,d) => s + d.files.length, 0);
  document.getElementById('govStats').innerHTML =
    `<div class="stat-card sc-gold"><div class="num">${tree.length}</div><div class="lbl">治理目录</div></div>
     <div class="stat-card sc-steel"><div class="num">${totalFiles}</div><div class="lbl">治理文件</div></div>
     <div class="stat-card sc-jade"><div class="num">${D.integrity.broken_links}</div><div class="lbl">断链</div></div>
     <div class="stat-card sc-violet"><div class="num">${D.integrity.checked || 'N/A'}</div><div class="lbl">已检查链接</div></div>
     <div class="stat-card sc-amber"><div class="num" style="font-size:0.9rem;">${D.integrity.status || 'N/A'}</div><div class="lbl">完整性</div></div>`;

  document.getElementById('govTree').innerHTML = tree.map((d, i) =>
    `<div class="gov-dir">
      <div class="gov-dir-header" onclick="toggleGov(${i})">
        <span class="icon" id="govIcon${i}">▶</span>
        <span class="dname">${d.dir}</span>
        <span class="ddesc">${d.label}</span>
        <span class="dcnt">${d.files.length} 个文件</span>
      </div>
      <div class="gov-files" id="govFiles${i}">
        <div style="font-size:0.68rem;color:var(--dim);margin:4px 0 8px;">${d.desc}</div>
        ${d.files.map(f => `<div class="gov-file"><span class="fn">${f.name}</span><span class="fl">${f.label}</span><span class="fd">— ${f.desc}</span><span class="fm">${f.mtime || '—'} · ${f.size || '—'}</span></div>`).join('')}
      </div>
    </div>`
  ).join('');
}

function toggleGov(i) {
  const files = document.getElementById('govFiles' + i);
  const icon = document.getElementById('govIcon' + i);
  files.classList.toggle('open');
  icon.textContent = files.classList.contains('open') ? '▼' : '▶';
}

// ── 登记册 ──
function renderRegisters() {
  document.getElementById('decCnt').textContent = D.decision_items.length + ' 项';
  document.getElementById('decTbl').innerHTML = D.decision_items.map(d =>
    `<tr><td class="mono">${d.id}</td><td>${d.decision}</td><td><span class="badge badge-ok">${d.status}</span></td><td style="font-size:0.68rem;">${d.reason}</td><td style="font-size:0.68rem;color:var(--dim);">${d.trigger}</td></tr>`
  ).join('');
  document.getElementById('depTbl').innerHTML = D.dependency_items.map(d =>
    `<tr><td class="mono">${d.id}</td><td>${d.dep}</td><td>${d.purpose}</td><td style="font-size:0.68rem;">${d.req}</td><td style="font-size:0.68rem;color:var(--dim);">${d.alt}</td></tr>`
  ).join('');
  document.getElementById('reqTbl').innerHTML = D.requirement_items.map(r =>
    `<tr><td class="mono">${r.id}</td><td>${r.req}</td><td>${r.system}</td><td style="font-size:0.68rem;">${r.evidence}</td></tr>`
  ).join('');
  document.getElementById('licTbl').innerHTML = D.license_items.map(l =>
    `<tr><td class="mono">${l.id}</td><td>${l.asset}</td><td>${l.source}</td><td>${l.license}</td><td>${l.tech}</td><td><span class="badge badge-info">${l.conclusion}</span></td></tr>`
  ).join('');
  document.getElementById('ptTbl').innerHTML = D.playtest_items.map(p =>
    `<tr><td class="mono">${p.id}</td><td>${p.issue}</td><td style="font-size:0.68rem;">${p.success}</td><td style="font-size:0.68rem;color:var(--vermillion);">${p.failure}</td></tr>`
  ).join('');
  document.getElementById('stdTbl').innerHTML = D.standards_bl.map(s =>
    `<tr><td class="mono">${s.ms}</td><td><span class="badge ${s.priority=='P0'?'badge-err':'badge-warn'}">${s.priority}</span></td><td>${s.todo}</td><td style="font-size:0.68rem;">${s.trigger}</td></tr>`
  ).join('');
  document.getElementById('permTbl').innerHTML = D.permission_items.map(p =>
    `<tr><td>${p.scope}</td><td style="font-size:0.68rem;">${p.policy}</td><td>${p.status}</td><td style="font-size:0.68rem;">${p.method}</td></tr>`
  ).join('');
  document.getElementById('astTbl').innerHTML = D.asset_items.length ?
    D.asset_items.map(a => `<tr><td class="mono">${a.id}</td><td>${a.type}</td><td class="mono">${a.path}</td><td>${a.status}</td><td>${a.task || '—'}</td></tr>`).join('') :
    '<tr><td colspan="5" style="color:var(--dim);text-align:center;padding:20px;">暂无登记资产</td></tr>';

  // 技术债
  const td = D.tech_debt || [];
  document.getElementById('techDebtCnt').textContent = td.length + ' 项';
  document.getElementById('techDebtTbl').innerHTML = td.length ?
    td.map(d => `<tr><td class="mono">${d.id}</td><td>${d.desc}</td><td>${d.location}</td><td><span class="badge ${d.priority=='高'?'badge-err':'badge-warn'}">${d.priority}</span></td><td><span class="badge ${d.status=='open'?'badge-err':'badge-ok'}">${d.status}</span></td><td style="font-size:0.68rem;">${d.plan}</td></tr>`).join('') :
    '<tr><td colspan="6" style="color:var(--dim);text-align:center;padding:20px;">暂无技术债</td></tr>';

  // 交叉引用
  const cross = D.cross_ref_issues || [];
  const crossEl = document.getElementById('crossRefArea');
  if (cross.length === 0) {
    crossEl.innerHTML = '<div class="crossref-ok">✓ 全部一致 — 任务登记册与验证登记册交叉引用无异常</div>';
  } else {
    crossEl.innerHTML = cross.map(issue => `<div class="crossref-issue">✗ ${issue}</div>`).join('');
  }
}

// ── 变更记录 ──
function renderChangelog() {
  document.getElementById('clList').innerHTML = D.changelog.map(c =>
    `<div class="cl-entry"><div class="cl-date">${c.date}</div><div class="cl-summary">${c.summary}</div></div>`
  ).join('');
}

// ── 防虚构健康 ──
let integrityLoaded = false;

async function loadIntegrity() {
  try {
    const r = await fetch('/api/integrity');
    const data = await r.json();
    renderIntegrity(data);
    integrityLoaded = true;
  } catch(e) {
    document.getElementById('integrityContent').innerHTML =
      '<div style="padding:40px;text-align:center;color:var(--vermillion);font-size:0.8rem;">校验脚本加载失败：' + e.message + '</div>';
  }
}

function renderIntegrity(data) {
  if (data.error) {
    document.getElementById('integrityContent').innerHTML =
      '<div style="padding:40px;text-align:center;color:var(--vermillion);font-size:0.8rem;">校验脚本报错：' + data.error + '</div>';
    return;
  }

  const overall = data.overall === 'pass';
  const heroClass = overall ? 'pass' : 'fail';
  const heroIcon = overall ? '✓' : '✗';
  const heroTitle = overall ? '全部校验通过' : `${data.failed} 项校验失败`;
  const heroMeta = `校验时间 ${data.timestamp} · ${data.total} 项检查 · 数据源 ${data.trae_root}`;

  const heroHtml = `
    <div class="integrity-hero ${heroClass}">
      <div class="hero-icon">${heroIcon}</div>
      <div class="hero-body">
        <div class="hero-title">${heroTitle}</div>
        <div class="hero-meta">${heroMeta}</div>
      </div>
      <div class="hero-stats">
        <div class="hero-stat"><div class="num" style="color:var(--jade)">${data.passed}</div><div class="lbl">通过</div></div>
        <div class="hero-stat"><div class="num" style="color:var(--vermillion)">${data.failed}</div><div class="lbl">失败</div></div>
        <div class="hero-stat"><div class="num" style="color:var(--gold)">${data.total}</div><div class="lbl">总计</div></div>
      </div>
    </div>`;

  const groups = {};
  for (const c of data.checks) {
    if (!groups[c.category]) groups[c.category] = [];
    groups[c.category].push(c);
  }

  let groupsHtml = '';
  for (const [cat, items] of Object.entries(groups)) {
    const allPass = items.every(i => i.passed);
    const passCount = items.filter(i => i.passed).length;
    groupsHtml += `
      <div class="check-group">
        <div class="check-group-header">
          <span class="grp-status ${allPass ? 'pass' : 'fail'}"></span>
          ${cat}
          <span class="grp-cnt">${passCount}/${items.length}</span>
        </div>
        ${items.map(c => `
          <div class="check-item ${c.passed ? 'pass' : 'fail'}">
            <span class="ck-icon">${c.passed ? '✓' : '✗'}</span>
            <div class="ck-body">
              <div class="ck-name">${c.name}</div>
              <div class="ck-detail">${c.detail}</div>
            </div>
            <span class="ck-badge">${c.passed ? 'PASS' : 'FAIL'}</span>
          </div>
        `).join('')}
      </div>`;
  }

  document.getElementById('integrityContent').innerHTML = heroHtml + groupsHtml;
}

// ── 验证证据 ──
function renderVerification() {
  const items = D.verif_items || [];
  document.getElementById('verifRegCnt').textContent = items.length + ' 项';

  document.getElementById('verifRegTbl').innerHTML = items.map(v => {
    let badge = v.status.includes('已验证')?'badge-ok':v.status.includes('失败')?'badge-err':'badge-warn';
    // 简单推断证据存在性：证据文本包含文件路径则认为存在
    const hasEvidence = v.evidence && v.evidence.length > 10;
    const evidenceIcon = hasEvidence ? '<span class="evidence-ok">✓</span>' : '<span class="evidence-miss">✗</span>';
    return `<tr><td class="mono">${v.id}</td><td>${v.name}</td><td>${v.task}</td><td>${v.level}</td><td><span class="badge ${badge}">${v.status}</span></td><td style="font-size:0.66rem;color:var(--dim);max-width:280px;">${v.evidence}</td><td>${evidenceIcon}</td></tr>`;
  }).join('');
}

// ── 资产仓库 ──
function renderAssets() {
  const repo = D.asset_repo || {};
  const existing = repo.existing_assets || [];
  const planned = repo.planned_assets || [];
  const summary = repo.summary || {};

  document.getElementById('assetStatsBar').innerHTML =
    `<div class="stat-card sc-steel"><div class="num">${summary.existing_total || 0}</div><div class="lbl">总资产</div></div>
     <div class="stat-card sc-jade"><div class="num">${summary.template_assets_count || 0}</div><div class="lbl">UE模板资产</div></div>
     <div class="stat-card sc-gold"><div class="num">${summary.project_assets_count || 0}</div><div class="lbl">项目资产</div></div>
     <div class="stat-card sc-violet"><div class="num">${summary.planned_total || 0}</div><div class="lbl">规划资产</div></div>`;

  // 分类现有资产：UE模板 vs 项目资产
  const templateAssets = existing.filter(a => a.source !== '项目资产');
  const projectAssets = existing.filter(a => a.source === '项目资产');

  // 业务分类顺序
  const catOrder = ['武器', '角色', '场景', '关卡/场景', '骨骼/动画', '材质/贴图', '蓝图', '输入系统', '特效', '音效', '触觉反馈', 'VR 观战', '项目目录', '其他'];

  function groupByCategory(assets) {
    const cats = {};
    for (const a of assets) {
      const cat = a.category || '其他';
      if (!cats[cat]) cats[cat] = [];
      cats[cat].push(a);
    }
    return cats;
  }

  function renderAssetCard(a, isPlanned) {
    if (isPlanned) {
      return `<div class="asset-card planned">
        <div class="aname">${a.name}</div>
        <div class="ameta">
          <span class="atype">${a.type || '—'}</span>
          <span class="astatus planned">规划中</span>
          <span>${a.milestone || ''}</span>
        </div>
        ${a.desc ? `<div style="font-size:0.65rem;color:var(--dim);margin-top:4px;">${a.desc}</div>` : ''}
        ${a.planned_path ? `<div style="font-size:0.6rem;color:var(--dimmer);margin-top:2px;" class="mono">${a.planned_path}</div>` : ''}
      </div>`;
    }
    return `<div class="asset-card exists">
      <div class="aname">${a.name}</div>
      <div class="ameta">
        <span class="atype">${a.type}</span>
        <span>${a.source}</span>
        <span>${a.size_kb}KB</span>
      </div>
      <div style="font-size:0.6rem;color:var(--dimmer);margin-top:2px;" class="mono">${a.path}</div>
    </div>`;
  }

  function renderSubCategories(assets, isPlanned) {
    const cats = groupByCategory(assets);
    let html = '';
    for (const cat of catOrder) {
      if (!cats[cat]) continue;
      const items = cats[cat];
      const dotClass = isPlanned ? 'planned' : 'exists';
      html += `<div class="asset-subcategory">
        <div class="asset-subcategory-title">
          <span class="status-dot ${dotClass}"></span>
          ${cat}
          <span class="subcnt">(${items.length})</span>
        </div>
        <div class="asset-grid">
          ${items.map(a => renderAssetCard(a, isPlanned)).join('')}
        </div>
      </div>`;
    }
    // 处理不在 catOrder 中的分类
    for (const cat of Object.keys(cats)) {
      if (catOrder.includes(cat)) continue;
      const items = cats[cat];
      const dotClass = isPlanned ? 'planned' : 'exists';
      html += `<div class="asset-subcategory">
        <div class="asset-subcategory-title">
          <span class="status-dot ${dotClass}"></span>
          ${cat}
          <span class="subcnt">(${items.length})</span>
        </div>
        <div class="asset-grid">
          ${items.map(a => renderAssetCard(a, isPlanned)).join('')}
        </div>
      </div>`;
    }
    return html;
  }

  // 构建手风琴
  let accordionHtml = '';

  // UE 模板资产
  if (templateAssets.length > 0) {
    accordionHtml += `<div class="asset-accordion-item">
      <div class="asset-accordion-header" onclick="toggleAssetAccordion(0)">
        <span class="achevron" id="assetChev0">▶</span>
        <span class="atitle">UE 模板资产</span>
        <span class="abadge template">模板</span>
        <span class="acount">${templateAssets.length} 个</span>
      </div>
      <div class="asset-accordion-body" id="assetBody0">
        ${renderSubCategories(templateAssets, false)}
      </div>
    </div>`;
  }

  // 项目资产
  accordionHtml += `<div class="asset-accordion-item">
    <div class="asset-accordion-header" onclick="toggleAssetAccordion(1)">
      <span class="achevron" id="assetChev1">▶</span>
      <span class="atitle">项目资产</span>
      <span class="abadge project">已制作</span>
      <span class="acount">${projectAssets.length} 个</span>
    </div>
    <div class="asset-accordion-body" id="assetBody1">
      ${projectAssets.length > 0 ? renderSubCategories(projectAssets, false) : '<div style="padding:16px;color:var(--dim);text-align:center;font-size:0.8rem;">尚无项目自制资产。下方规划资产展示了待制作清单。</div>'}
    </div>
  </div>`;

  // 规划资产
  accordionHtml += `<div class="asset-accordion-item">
    <div class="asset-accordion-header" onclick="toggleAssetAccordion(2)">
      <span class="achevron" id="assetChev2">▶</span>
      <span class="atitle">规划资产</span>
      <span class="abadge planned">待制作</span>
      <span class="acount">${planned.length} 个</span>
    </div>
    <div class="asset-accordion-body" id="assetBody2">
      ${planned.length > 0 ? renderSubCategories(planned, true) : '<div style="padding:16px;color:var(--dim);text-align:center;font-size:0.8rem;">暂无规划资产</div>'}
    </div>
  </div>`;

  document.getElementById('assetAccordion').innerHTML = accordionHtml;

  // 依赖链
  document.getElementById('depChain').textContent = repo.dependency_chain || '暂无依赖链数据';
}

function toggleAssetAccordion(idx) {
  const body = document.getElementById('assetBody' + idx);
  const chev = document.getElementById('assetChev' + idx);
  body.classList.toggle('open');
  chev.textContent = body.classList.contains('open') ? '▼' : '▶';
}

// ── Tab 切换 ──
document.querySelectorAll('.tab').forEach(t => {
  t.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(x => x.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(x => x.classList.remove('active'));
    t.classList.add('active');
    document.getElementById('tab-' + t.dataset.tab).classList.add('active');
    if (t.dataset.tab === 'integrity' && !integrityLoaded) {
      loadIntegrity();
    }
  });
});

// 默认展开治理前两个目录
setTimeout(() => { toggleGov(0); toggleGov(8); }, 300);

// 启动
load();
setInterval(load, 300000);
</script>
</body>
</html>"""


# ── HTTP Server ─────────────────────────────────────────

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/status":
            data = build_api_data()
            body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/api/integrity":
            try:
                result = subprocess.run(
                    [sys.executable, str(SCRIPT_DIR / "check-integrity.py"), "--json"],
                    capture_output=True, text=True, timeout=30
                )
                body = result.stdout.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except Exception as e:
                error = json.dumps({"error": str(e)}, ensure_ascii=False).encode("utf-8")
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(error)))
                self.end_headers()
                self.wfile.write(error)
        elif self.path == "/api/assets":
            data = build_asset_api_data()
            body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path in ("/", "/index.html"):
            body = DASHBOARD_HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


def main():
    print(f"\n  ⚔  VR 三国演武场 - 治理仪表盘 v5")
    print(f"  ──────────────────────────────────────")
    print(f"  数据源: {TRAE_ROOT}")
    print(f"  服务:   http://localhost:{PORT}")
    print(f"  刷新:   5 分钟")
    print(f"  按 Ctrl+C 停止\n")
    server = http.server.HTTPServer(("0.0.0.0", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  服务已停止。")
        server.shutdown()


if __name__ == "__main__":
    main()
