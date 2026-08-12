#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资产仓库扫描模块 - 零虚构数据
扫描 Content/ 目录获取真实资产文件，读取 .trae/ 登记册获取规划信息。
"""
import os
import re
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
TRAE_ROOT = PROJECT_ROOT / ".trae"
CONTENT_ROOT = PROJECT_ROOT / "Content"


def read_text(path):
    p = TRAE_ROOT / path
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def parse_markdown_table(text):
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


# ── 资产类型分类 ──────────────────────────────────────────

ASSET_TYPE_MAP = {
    "SK_": "SkeletalMesh",
    "SKM_": "SkeletalMesh",
    "SM_": "StaticMesh",
    "A_": "Animation",
    "ABP_": "AnimBlueprint",
    "MDT_": "AnimBlueprint",
    "B_": "Blueprint",
    "BP_": "Blueprint",
    "WBP_": "WidgetBlueprint",
    "MI_": "MaterialInstance",
    "M_": "Material",
    "MF_": "MaterialFunction",
    "T_": "Texture",
    "CA_": "CurveAsset",
    "IA_": "InputAction",
    "IMC_": "InputMappingContext",
    "RT_": "RenderTarget",
    "NS_": "NiagaraSystem",
    "NPC_": "NiagaraSystem",
    "DA_": "DataAsset",
    "L_": "Level",
    "EV": "Enum",
    "PA_": "PhysicsAsset",
}

SOURCE_MAP = {
    "VRTemplate": "UE VR 模板",
    "Characters/MannequinsXR": "UE MannequinsXR",
    "LevelPrototyping": "UE 关卡原型",
    "VRSpectator": "UE VR 观战",
    "Weapons/Pistol": "UE 模板武器",
    "Weapons/Rifle": "UE 模板武器",
    "Weapons/GrenadeLauncher": "UE 模板武器",
    "VRSanguo": "项目资产",
}


def classify_asset(filename):
    """根据文件名前缀分类资产类型"""
    name = filename.rsplit(".", 1)[0]
    for prefix, atype in sorted(ASSET_TYPE_MAP.items(), key=lambda x: -len(x[0])):
        if name.startswith(prefix):
            return atype
    return "Other"


def classify_source(rel_path):
    """根据路径分类资产来源"""
    for key, label in SOURCE_MAP.items():
        if key in rel_path:
            return label
    return "其他"


def scan_content_assets():
    """扫描 Content/ 目录，返回真实资产列表"""
    assets = []
    if not CONTENT_ROOT.exists():
        return assets

    for root, dirs, files in os.walk(CONTENT_ROOT):
        for f in files:
            if f.endswith((".uasset", ".umap")):
                full = Path(root) / f
                rel = str(full.relative_to(CONTENT_ROOT)).replace("\\", "/")
                stat = full.stat()
                assets.append({
                    "name": f.rsplit(".", 1)[0],
                    "filename": f,
                    "path": f"Content/{rel}",
                    "type": classify_asset(f),
                    "source": classify_source(rel),
                    "size_kb": round(stat.st_size / 1024, 1),
                    "mtime": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                    "category": _categorize_path(rel),
                })
    return assets


def _categorize_path(rel_path):
    """将资产路径映射到业务分类"""
    if "Characters" in rel_path or "Mannequins" in rel_path:
        return "角色"
    if "Weapons" in rel_path:
        return "武器"
    if "LevelPrototyping" in rel_path or "Maps" in rel_path:
        return "关卡/场景"
    if "Materials" in rel_path or "Textures" in rel_path:
        return "材质/贴图"
    if "Input" in rel_path:
        return "输入系统"
    if "VFX" in rel_path or "FX" in rel_path:
        return "特效"
    if "Audio" in rel_path:
        return "音效"
    if "Haptics" in rel_path:
        return "触觉反馈"
    if "Blueprints" in rel_path:
        return "蓝图"
    if "VRSpectator" in rel_path:
        return "VR 观战"
    if "VRSanguo" in rel_path:
        return "项目目录"
    return "其他"


# ── 规划资产（来自 GameMasterPlan 和 ArtStyleGuide） ──

PLANNED_ASSETS = [
    # 武器
    {"id": "PLN-W01", "category": "武器", "name": "单手刀剑（环首刀）", "type": "SkeletalMesh",
     "planned_path": "Content/VRSanguo/Weapons/Sword/SK_Sword", "milestone": "M01", "status": "planned",
     "deps": "角色骨架", "desc": "环首刀，约 100cm，玩家版+AI版+灰盒版"},
    {"id": "PLN-W02", "category": "武器", "name": "盾牌（钩镶/长方盾）", "type": "StaticMesh",
     "planned_path": "Content/VRSanguo/Weapons/Shield/SM_Shield", "milestone": "M02", "status": "planned",
     "deps": "角色骨架（挂载点）", "desc": "钩镶或长方盾，约 60x40cm"},
    {"id": "PLN-W03", "category": "武器", "name": "长柄重兵（戟/长刀）", "type": "SkeletalMesh",
     "planned_path": "Content/VRSanguo/Weapons/Halberd/SK_Halberd", "milestone": "M02", "status": "planned",
     "deps": "角色骨架（挂载点）", "desc": "戟或长刀，约 250cm"},
    {"id": "PLN-W04", "category": "武器", "name": "长矛（矟/槊）", "type": "SkeletalMesh",
     "planned_path": "Content/VRSanguo/Weapons/Spear/SK_Spear", "milestone": "M02", "status": "planned",
     "deps": "角色骨架（挂载点）", "desc": "矟或槊，约 300cm"},
    {"id": "PLN-W05", "category": "武器", "name": "弓箭（汉弓）", "type": "SkeletalMesh",
     "planned_path": "Content/VRSanguo/Weapons/Bow/SK_Bow", "milestone": "M02", "status": "planned",
     "deps": "角色骨架（挂载点）", "desc": "汉弓，约 120cm"},
    # 角色
    {"id": "PLN-C01", "category": "角色", "name": "刀盾兵", "type": "SkeletalMesh",
     "planned_path": "Content/VRSanguo/Characters/SK_Militia_SwordShield", "milestone": "M03", "status": "planned",
     "deps": "统一骨架", "desc": "中甲札甲，刀盾组合"},
    {"id": "PLN-C02", "category": "角色", "name": "长矛兵", "type": "SkeletalMesh",
     "planned_path": "Content/VRSanguo/Characters/SK_Militia_Spearman", "milestone": "M03", "status": "planned",
     "deps": "统一骨架", "desc": "中甲札甲，长矛"},
    {"id": "PLN-C03", "category": "角色", "name": "长柄重兵", "type": "SkeletalMesh",
     "planned_path": "Content/VRSanguo/Characters/SK_Militia_Halberdier", "milestone": "M03", "status": "planned",
     "deps": "统一骨架", "desc": "重甲两当铠，长柄武器"},
    {"id": "PLN-C04", "category": "角色", "name": "弓兵", "type": "SkeletalMesh",
     "planned_path": "Content/VRSanguo/Characters/SK_Militia_Archer", "milestone": "M03", "status": "planned",
     "deps": "统一骨架", "desc": "轻甲皮甲，弓箭"},
    {"id": "PLN-C05", "category": "角色", "name": "精锐近战", "type": "SkeletalMesh",
     "planned_path": "Content/VRSanguo/Characters/SK_Elite_Melee", "milestone": "M03", "status": "planned",
     "deps": "统一骨架", "desc": "重甲筒袖铠，精锐近战"},
    {"id": "PLN-C06", "category": "角色", "name": "武将", "type": "SkeletalMesh",
     "planned_path": "Content/VRSanguo/Characters/SK_General", "milestone": "M05", "status": "planned",
     "deps": "统一骨架", "desc": "略高大 180cm，重甲，三国武将"},
    # 场景
    {"id": "PLN-L01", "category": "场景", "name": "校场（灰盒）", "type": "Level",
     "planned_path": "Content/VRSanguo/Maps/L_Prototype_Symmetric", "milestone": "M01", "status": "planned",
     "deps": "—", "desc": "对称灰盒竞技场，约 50x50m"},
    {"id": "PLN-L02", "category": "场景", "name": "校场（正式）", "type": "Level",
     "planned_path": "Content/VRSanguo/Maps/L_Arena_Camp", "milestone": "M05", "status": "planned",
     "deps": "M01 灰盒验证通过", "desc": "夯土地面，木栅围栏，观武台"},
    {"id": "PLN-L03", "category": "场景", "name": "关隘", "type": "Level",
     "planned_path": "Content/VRSanguo/Maps/L_Arena_Pass", "milestone": "M05", "status": "planned",
     "deps": "—", "desc": "石墙，城楼，狭窄通道"},
    {"id": "PLN-L04", "category": "场景", "name": "水寨", "type": "Level",
     "planned_path": "Content/VRSanguo/Maps/L_Arena_Water", "milestone": "M05", "status": "planned",
     "deps": "—", "desc": "木质栈道，水面，船只"},
    {"id": "PLN-L05", "category": "场景", "name": "山地", "type": "Level",
     "planned_path": "Content/VRSanguo/Maps/L_Arena_Mountain", "milestone": "M05", "status": "planned",
     "deps": "—", "desc": "斜坡，岩石，树木"},
    # 骨骼与动画
    {"id": "PLN-A01", "category": "骨骼/动画", "name": "统一角色骨架", "type": "SkeletalMesh",
     "planned_path": "Content/VRSanguo/Characters/SK_Militia", "milestone": "M01", "status": "planned",
     "deps": "—", "desc": "所有兵种复用的统一骨架，约 170cm"},
    {"id": "PLN-A02", "category": "骨骼/动画", "name": "角色动画集（战斗）", "type": "Animation",
     "planned_path": "Content/VRSanguo/Characters/Animations/", "milestone": "M01", "status": "planned",
     "deps": "统一角色骨架", "desc": "挥砍、格挡、受击、死亡等战斗动画"},
]


def get_asset_summary(existing_assets):
    """生成资产汇总统计"""
    categories = {}
    for a in existing_assets:
        cat = a["category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "by_type": {}}
        categories[cat]["total"] += 1
        atype = a["type"]
        categories[cat]["by_type"][atype] = categories[cat]["by_type"].get(atype, 0) + 1

    planned_by_ms = {}
    for p in PLANNED_ASSETS:
        ms = p["milestone"]
        if ms not in planned_by_ms:
            planned_by_ms[ms] = 0
        planned_by_ms[ms] += 1

    return {
        "existing_total": len(existing_assets),
        "planned_total": len(PLANNED_ASSETS),
        "categories": categories,
        "planned_by_milestone": planned_by_ms,
        "project_assets_count": sum(1 for a in existing_assets if a["source"] == "项目资产"),
        "template_assets_count": sum(1 for a in existing_assets if a["source"] != "项目资产"),
    }


def get_tech_debt():
    """读取技术债登记册"""
    text = read_text("registers/11-tech-debt-register.md")
    rows = parse_markdown_table(text)
    return [{"id": r.get("ID", ""), "desc": r.get("描述", ""), "location": r.get("位置", ""),
             "reason": r.get("引入原因", ""), "impact": r.get("影响", ""),
             "plan": r.get("偿还计划", ""), "priority": r.get("优先级", ""),
             "status": r.get("状态", "")} for r in rows]


def get_pattern_progress():
    """读取模式库进度"""
    patterns_dir = TRAE_ROOT / "knowledge" / "Patterns"
    if not patterns_dir.exists():
        return {"total_categories": 0, "filled": 0, "categories": []}

    categories = []
    for f in sorted(patterns_dir.iterdir()):
        if f.is_file() and f.suffix == ".md" and f.name != "README.md":
            content = f.read_text(encoding="utf-8")
            # 检查是否有实际模式内容（不只是标题和骨架）
            pattern_count = content.count("### ") + content.count("## ")
            has_content = len(content) > 500
            categories.append({
                "name": f.stem,
                "patterns": pattern_count,
                "has_content": has_content,
            })

    filled = sum(1 for c in categories if c["has_content"])
    return {"total_categories": len(categories), "filled": filled, "categories": categories}


def get_interface_contract_status():
    """检查系统指引的接口契约状态"""
    systems_dir = TRAE_ROOT / "systems"
    if not systems_dir.exists():
        return []

    results = []
    source_interfaces = PROJECT_ROOT / "Source" / "VRSanguoYanWuchang" / "Public" / "Interfaces"

    for f in sorted(systems_dir.iterdir()):
        if f.is_file() and f.suffix == ".md" and f.name != "index.md":
            content = f.read_text(encoding="utf-8")
            has_contract = "接口契约" in content or "interface contract" in content.lower()
            # 检查 Source/ 下是否有对应 C++ 头文件
            has_implementation = False
            if source_interfaces.exists():
                for h in source_interfaces.iterdir():
                    if h.suffix == ".h":
                        has_implementation = True
                        break

            results.append({
                "file": f.name,
                "has_contract": has_contract,
                "has_implementation": has_implementation,
                "status": "已定义" if has_contract else "缺失",
                "impl_status": "已有C++实现" if has_implementation else "未实现（M01+）",
            })
    return results


def check_cross_references(task_reg, verif_reg):
    """检查任务登记与验证登记的交叉一致性"""
    issues = []
    task_status = {t.get("任务", ""): t.get("状态", "") for t in task_reg}
    for v in verif_reg:
        vid = v.get("ID", "")
        v_status = v.get("状态", "")
        v_task = v.get("关联任务", "")
        if v_task and v_task in task_status:
            t_status = task_status[v_task]
            # 如果任务已验证但验证登记未通过，或反之
            if "已验证" in t_status and "已验证" not in v_status and "通过" not in v_status:
                issues.append(f"{v_task} 任务标记已验证，但验证登记 {vid} 状态为 {v_status}")
            elif "已验证" not in t_status and "已验证" in v_status:
                issues.append(f"{v_task} 验证登记 {vid} 标记已验证，但任务状态为 {t_status}")
    return issues


def build_asset_repository_data():
    """构建完整的资产仓库数据"""
    existing = scan_content_assets()
    summary = get_asset_summary(existing)

    # 读取资产登记册
    asset_reg_text = read_text("registers/10-asset-register.md")
    registered = parse_markdown_table(asset_reg_text)

    # 读取依赖链
    dep_text = read_text("registers/03-dependency-register.md")
    dep_rows = parse_markdown_table(dep_text)

    # 提取资产级依赖链
    dep_chain_text = ""
    in_chain = False
    for line in dep_text.split("\n"):
        if "资产级依赖链" in line:
            in_chain = True
        elif in_chain and line.startswith("## "):
            break
        elif in_chain:
            dep_chain_text += line + "\n"

    return {
        "existing_assets": existing,
        "planned_assets": PLANNED_ASSETS,
        "registered_assets": registered,
        "dependency_chain": dep_chain_text.strip(),
        "summary": summary,
    }


def get_governance_file_mtimes(governance_tree):
    """为治理资产树添加文件修改时间"""
    for d in governance_tree:
        for f in d.get("files", []):
            fpath = TRAE_ROOT / d["dir"] / f["name"]
            if fpath.exists():
                stat = fpath.stat()
                f["mtime"] = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d")
                f["size"] = f"{round(stat.st_size / 1024, 1)}KB"
            else:
                f["mtime"] = "—"
                f["size"] = "—"
    return governance_tree
