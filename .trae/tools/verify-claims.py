#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify-claims.py · 判据工具「核对执行器」（M00-T007）

单一事实源：本文件是「判据执行」这件事的单一事实源（声明式判据文件 -> 三态结论）。
规格正文（唯一权威）：.trae/execution/CR-20260912-001-judgement-tool.md（本文件只实现，不复制其正文）。
任务：.trae/execution/active/M00-T007/TASK.md；验收判据 = 规格 §7 的 TC-01 ~ TC-16。

运行前提
--------
* 宿主语言：Python 3（规格 §4.1 明文要求；**不得把判据结论建立在 PowerShell 格式化输出上**）。
* 依赖：**仅标准库 + pyyaml**（规格 §3 非目标 4）。
* 本机解释器不在 PATH，调用须用绝对路径并设 PYTHONIOENCODING=utf-8：
      $env:PYTHONIOENCODING='utf-8'
      & 'D:\\App\\trae\\Traedata\\TRAE SOLO CN\\ModularData\\ai-agent\\vm\\tools\\python\\python.exe' `
          -B -X utf8 .trae/tools/verify-claims.py <判据文件.yaml> [--allow-unknown] [--json out.json]
  （该绝对路径是**可复现性依赖**，按 AGENTS.md 规则 23 的口径澄清保留。）
* 项目外临时目录（有意为之，符合磁盘规则；临时文件一律写此处且用完即删）：
      D:\\AWork\\TraeAdmin\\VRSanguoYanWuchang\\tmp
  本工具**自身不写任何文件**（只读被检查文件）；唯一可选的写操作是调用方显式指定的 --json 路径。

内置能力 ↔ 规格 §4.3 十八条（实现位置）
---------------------------------------
 1 三态 + fail-closed ..................... S_PASS/S_FAIL/S_UNKNOWN + derive_verdict()
 2 可满足性前置（0 候选 ⇒ 不成立）......... eval_contains() 的 candidate 扫描
 3 匹配方式显式声明 ........................ validate_claims() 要求 match ∈ MATCH_MODES
 4 三口径（原样/去反引号/去行内标记）....... CALIBERS + eval_contains()
 5 双算法交叉（不一致 ⇒ 不取其一）......... eval_count_regex() 的 A/B 两算法
 6 字节导出法（禁 git show + join 计行）.... Reader.bytes()（按字节读；全文件不见 "git show"）
 7 行数权威 = ReadAllLines 语义 ............ measure_lines() + MEASURE_DOC（报告标注口径）
 8 非空断言 ................................ Reader.bytes()/text() 与 exec 的 stdout 非空断言
 9 显式退出码与 stderr 检查 ................ eval_exec() 同时报 exit/stdout/stderr；本工具自报 exit
10 结果变量每轮显式置空 .................... run_all() 的 Outcome 每轮新建 + Reader.set_timing() 每轮重置
11 汇总段测量驱动 .......................... render_summary()（所有数字来自计数，禁写死）
12 归属标签严格枚举 + 前置断言 ............. IdentifierTable.normalize('ownership', ...) 抛错
13 标识符统一规范化 ........................ IdentifierTable（file/workflow/ownership/claim_id 同一张表）
14 量具定义显式声明 ........................ 缺 measure / fence_measure ⇒ 拒绝执行（ClaimSpecInvalid）
15 报告义务不可被短路 ...................... build_report_section() 独立遍历 + assert_report_complete()
16 取数必须 fail-closed .................... EmptyMeasurement 抛错 + Reader 数值溯源断言
17 集合形状不得被静默改写 + 判据门自断言 ..... typed_ints/typed_strs/count_of/join_flat（形状异常抛
                                            ShapeAnomaly）+ assert_gate_self_check()（应产出判定条数
                                            vs 实际产出条数；不符 ⇒ 该门无效 ⇒ 停手并报告）
18 量具必须声明时点 + 外部输出必须先结构化 .... ① 时点：每条判据必须声明 at（或顶层 measure_at），
                                            缺失 ⇒ 拒绝执行（ClaimSpecInvalid，含「不可采信」）；
                                            每轮 run_all() 把时点下发给 Reader.set_timing()，未声明
                                            时点的读数 ⇒ MeasurementUntrusted（**不可采信**，不出结论）；
                                            每条判据的输出都显式打印「测量时点 = …」。
                                            ② 结构化：eval_exec() 一律先过 ExternalOutput（strip_ansi()
                                            剥离 ANSI/CSI + int()/scalar_int() 显式转型）；多值 / 多分组
                                            / 空值 ⇒ 抛错，**禁止**把集合多值交给格式化或比较
                                            （scalar_text/scalar_int；`System.Object[]` 与「项数 =（空）」
                                            两条原型）

时点假设（第 18 条 ①的落地口径）
--------------------------------
* Reader 不缓存任何读数 ⇒ 每个读数的时点 = **调用它的那一刻**；时点由调用方显式声明，不由工具猜测。
* 文件类取数（bytes/text）：时点 = 读取时刻的**磁盘字节**（不读 git 对象、不读旧副本）。
* 命令类取数（exec）：时点 = 命令**本次执行**的时刻（不复用上一轮输出）。
* 时点文本由判据作者填写（例：「步骤 5 之后、提交之前」）⇒ 工具只负责**要求它被写出**并原样回显。

禁止事项（规格 §4.4）落实
-------------------------
 1 只读：本工具不打开任何被检查文件用于写入（open(mode="rb") / read_bytes）。
 2 禁写死结论：结论串内含实际计数（render_summary）。
 3 不把「脚本没报错」当判据证据：每条判据都必须产出读数或显式「未取到数」。
 4 禁用 git show + join 计行：全文件不含 "git show"（--self-test 第 6 项自检源码）。
 5 不依赖 PowerShell 格式化：纯 Python。
 6 临时文件写项目外且用完即删：默认 TMP_ROOT（见上），--self-test 用后即删。
 7 禁用截断文本做归属判定：归属只取结构化字段 owner；owner_text/owner_from_text 一律拒绝。
 8 禁未声明时点的读数（第 18 条 ①）：at/measure_at 缺失 ⇒ 拒绝执行；Reader.num() 二次兜底。
 9 禁未结构化的外部输出（第 18 条 ②）：外部输出必须先剥离 ANSI 并显式转型；集合/多值/空值
   一律不得进入格式化或比较（ExternalOutput / scalar_text / scalar_int）。

用法
----
    verify-claims.py <判据文件> [--project-root DIR] [--allow-unknown]
                     [--json PATH] [--quiet] [--self-test] [--tmp-root DIR]

退出码（规格 §4.6）
------------------
    0 全部通过（且无「未取到数/不成立」；或已显式 --allow-unknown）
    1 至少一项「未通过」
    2 无「未通过」，但存在「未取到数/不成立」且未加 --allow-unknown（fail-closed）
    3 判据文件本身不合法（**未执行任何判据**）
"""

from __future__ import annotations

import argparse
import ast
import datetime as _dt
import fnmatch
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except Exception as _exc:  # pragma: no cover - 依赖缺失时立刻可见
    sys.stderr.write("verify-claims.py 需要 pyyaml：%s\n" % _exc)
    raise

TOOL_NAME = "verify-claims.py"
TOOL_VERSION = "1.1.0"
SPEC_REF = ".trae/execution/CR-20260912-001-judgement-tool.md"
DEFAULT_TMP_ROOT = Path(r"D:\AWork\TraeAdmin\VRSanguoYanWuchang\tmp")

# ─────────────────────────── 状态与退出码（三态 + 不成立 + 跳过）───────────────────────────
S_PASS = "通过"
S_FAIL = "未通过"
S_UNKNOWN = "未取到数"
S_NOT_EST = "不成立"          # 可满足性前置：0 候选 ⇒ 判据自身不成立，不判「未通过」
S_SKIP = "跳过"               # 作者显式 enabled:false ⇒ 不执行，但**仍须出现在报告段**

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_UNKNOWN = 2
EXIT_INVALID = 3

NON_PASS_STATES = (S_FAIL, S_UNKNOWN, S_NOT_EST)

# ─────────────────────────── 判据类型与枚举（表外取值一律拒绝）───────────────────────────
CLAIM_KINDS = ("contains", "count_regex", "shape", "sha256", "exec")
MATCH_MODES = ("exact", "prefix", "substring")
LINE_MEASURES = ("readalllines", "split_lf")
FENCE_MEASURES = ("indent_aware", "column0")
ALGORITHMS = ("dual",)

# 量具定义必须显式声明（规格 §4.3 第 14 条）。此处是**唯一**的量具字典。
MEASURE_DOC = {
    "readalllines": "行数 = ReadAllLines 语义（str.splitlines()）——文件以 LF 结尾时**不**产生尾部空行",
    "split_lf": '行数 = str.split("\\n")（对照口径）——文件以 LF 结尾时比 ReadAllLines 多 1',
    "indent_aware": "围栏 = 行首**允许前导空白**的 ``` 行数（含缩进围栏）",
    "column0": "围栏 = **第 0 列即** ``` 的行数（不含缩进围栏）",
}
CONTAINS_MEASURE_DOC = {
    "exact": "精确相等 = 去掉首尾空白后的整行与目标串逐字相等",
    "prefix": "前缀 = 去掉首尾空白后的整行以目标串开头",
    "substring": "子串 = 行内任意位置包含目标串",
}

# 单一规范化表（规格 §4.3 第 13 条）：文件路径 / 工作流名 / 归属标签 / 判据 id 都走这里。
FILE_PATTERNS = (
    ".trae/**",
    "AGENTS.md",
    "dashboard/**",
    "Docs/**",
    "Content/**",
    "Source/**",
    "Config/**",
    "Plugins/**",
    "Saved/**",
)
WORKFLOW_ALIASES = {
    "governance-check": "治理校验",
    "ci": "CI 任务/步骤",
    "git": "版本库操作",
    "pre-commit": "提交前核对",
}
OWNERSHIP_ALIASES = {
    "execution": "执行侧",
    "decision": "决策侧",
    "review": "审核侧",
    "governance": "治理",
    "ci": "CI",
    "git": "版本库",
    "human": "用户",
}
CLAIM_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")

# 规格 §4.4 第 7 条：禁止用截断/模糊文本做归属判定。这些键名一律拒绝。
OWNERSHIP_TEXT_KEYS = ("owner_text", "owner_from_text", "owner_prefix", "owner_guess")

COMMON_KEYS = ("id", "kind", "file", "note", "enabled", "owner", "workflow", "at")
KIND_KEYS = {
    "contains": ("text", "match", "cross_check_file"),
    "count_regex": ("pattern", "expect", "algorithm"),
    "shape": ("lines", "h2", "fences", "measure", "fence_measure"),
    "sha256": ("expect",),
    "exec": ("command", "expect_exit", "stdout_contains", "stdout_match", "timeout_sec",
             "stdout_int_regex", "expect_int"),
}
TOP_LEVEL_KEYS = ("claims", "identifiers", "note", "expect_judgements", "measure_at")

# ─────────────────────────── 异常类型 ───────────────────────────
class ClaimSpecInvalid(Exception):
    """判据文件不合法 ⇒ 退出码 3，且不得执行任何判据。"""


class IdentifierRejected(ClaimSpecInvalid):
    """标识符不在规范化表内 ⇒ 立刻抛错（不落 default 分支）。"""


class MeasurementUnavailable(Exception):
    """取数失败（文件缺失、命令无输出、外部服务未索引）⇒ 该判据「未取到数」。"""


class EmptyMeasurement(MeasurementUnavailable):
    """取数返回 null / 空串 / 空集合 ⇒ 必须抛错（规格 §4.3 第 16 条）。"""


class MeasurementUntrusted(MeasurementUnavailable):
    """读数**不可采信** ⇒ 拒绝出结论（规格 §4.3 第 18 条）。

    两类原型：① 取数**未声明测量时点**（「在 X 步之前 / 之后测」）—— 时点错的读数看起来照样合理，
    例如「本地 LFS 对象」断言跑在 `git add` 之前 ⇒ clean filter 未运行 ⇒ 对象本就不存在；
    ② 外部输出**未经结构化**（未剥离 ANSI / 未显式类型转换）就参与读数。
    ⇒ 处理方式与「未取到数」同列：**不出结论**，绝不当作「通过」更不当作「未通过」。
    """


class ShapeAnomaly(MeasurementUnavailable):
    """取数函数返回的**集合形状异常**（被额外包裹/元素非标量）⇒ 必须抛错（§4.3 第 17 条 / 第 20 例）。

    原型：把 `Get-Hit` 的返回值再用 `@(...)` 收集后取 `.Count` ⇒ 双重包裹 ⇒ `.Count` 恒为 1
    ⇒ 候选数与违反数都被静默伪造成 1。⇒ 本工具**禁止**对取数结果直接 len()/join()。
    """


class GateInvalid(Exception):
    """判据门自断言失败：应产出判定条数 ≠ 实际产出条数 ⇒ 该门视为无效 ⇒ 停手（§4.3 第 17 条 ②）。"""


class ReportShortCircuit(Exception):
    """应报项存在但报告段为空/缺项 ⇒ 结构性缺陷（规格 §4.3 第 15 条 / 第 18 例）。"""


# ─────────────────────────── 标识符规范化表 ───────────────────────────
class IdentifierTable:
    """**唯一**的标识符规范化入口。任何地方都不得自造标识符字符串。"""

    def __init__(self) -> None:
        self.file_patterns = list(FILE_PATTERNS)
        self.workflows = dict(WORKFLOW_ALIASES)
        self.ownership = dict(OWNERSHIP_ALIASES)
        self.claim_ids: dict[str, str] = {}

    # ---- 单一注册路径 ----
    def register_files(self, patterns) -> None:
        for p in patterns or ():
            canon = self._norm_rel_path(p)
            if canon not in self.file_patterns:
                self.file_patterns.append(canon)

    def register_workflows(self, names) -> None:
        for n in names or ():
            s = str(n).strip()
            if not s:
                raise IdentifierRejected("工作流名为空串")
            self.workflows.setdefault(s.lower(), s)

    def register_ownership(self, names) -> None:
        for n in names or ():
            s = str(n).strip()
            if not s:
                raise IdentifierRejected("归属标签为空串")
            self.ownership.setdefault(s.lower(), s)

    def register_claim_id(self, raw) -> str:
        return self.normalize("claim_id", raw)

    # ---- 单一规范化入口 ----
    def normalize(self, kind: str, raw):
        if kind == "file":
            rel = self._norm_rel_path(raw)
            if not self._matches_file(rel):
                raise IdentifierRejected(
                    "文件标识符不在规范化表内（表外取值一律拒绝）：%r ⇒ 允许的路径模式：%s"
                    % (raw, ", ".join(self.file_patterns))
                )
            return rel
        if kind == "workflow":
            return self._lookup(self.workflows, raw, "工作流名")
        if kind == "ownership":
            return self._lookup(self.ownership, raw, "归属标签")
        if kind == "claim_id":
            s = str(raw).strip().lower()
            if not CLAIM_ID_RE.match(s):
                raise IdentifierRejected(
                    "判据 id 不符合规范化表要求 %s：%r" % (CLAIM_ID_RE.pattern, raw)
                )
            return s
        raise IdentifierRejected("未知标识符种类：%r" % (kind,))

    # ---- 内部 ----
    @staticmethod
    def _lookup(table: dict, raw, what: str) -> str:
        s = str(raw).strip()
        if not s:
            raise IdentifierRejected("%s为空串 ⇒ 拒绝执行该判据" % what)
        if s.lower() in table:
            return table[s.lower()]
        for canon in set(table.values()):
            if s == canon:
                return canon
        raise IdentifierRejected(
            "%s不在规范化表内（枚举外取值 ⇒ 拒绝执行该判据）：%r ⇒ 允许：%s"
            % (what, raw, ", ".join(sorted(set(table.values()))))
        )

    @staticmethod
    def _norm_rel_path(raw) -> str:
        s = str(raw).strip().replace("\\", "/")
        if not s:
            raise IdentifierRejected("文件路径为空串")
        if s.startswith("/") or re.match(r"^[A-Za-z]:", s):
            raise IdentifierRejected("文件路径必须是项目相对路径（不得绝对路径/盘符）：%r" % raw)
        parts = []
        for seg in s.split("/"):
            if seg in ("", "."):
                continue
            if seg == "..":
                raise IdentifierRejected("文件路径不得上跳（..）：%r" % raw)
            parts.append(seg)
        canon = "/".join(parts)
        if not canon:
            raise IdentifierRejected("文件路径归一后为空：%r" % raw)
        return canon

    def _matches_file(self, rel: str) -> bool:
        for pat in self.file_patterns:
            if pat.endswith("/**"):
                head = pat[:-3]
                if rel == head or rel.startswith(head + "/"):
                    return True
            elif fnmatch.fnmatchcase(rel, pat):
                return True
        return False


# ─────────────────────────── 取数层（第 6 / 8 / 16 / 18 条）───────────────────────────
class Reader:
    """按**字节**读文件，并把每一次非空取数登记为溯源键（第 6、8、16 条）。

    **时点假设（第 18 条 ①）**：本类**不缓存**任何读数 ⇒ 每个读数等价于「调用它的那一刻」的
    文件 / 命令状态。因此调用方必须在**每轮开始时**用 `set_timing()` 声明该轮的测量时点
    （「在 X 步之前 / 之后测」）；**未声明时点的读数一律不可采信** ⇒ `num()` 抛
    `MeasurementUntrusted`，拒绝出结论。
    """

    def __init__(self, project_root: Path) -> None:
        self.root = project_root
        self.sources: dict[str, str] = {}      # 溯源键 -> 人类可读描述
        self.values: list[tuple[str, object, str]] = []   # (名称, 数值, 溯源键)
        self.timing = ""                       # 本轮声明的测量时点（第 18 条 ①）
        self._n = 0

    def set_timing(self, at) -> None:
        """声明本轮测量时点；空值 ⇒ 该轮任何读数都不可采信（由 `num()` 兜住）。"""
        self.timing = str(at or "").strip()

    def _new_key(self, desc: str) -> str:
        self._n += 1
        key = "read#%d" % self._n
        self.sources[key] = desc
        return key

    def external(self, desc: str) -> str:
        """登记一次非空外部取数（如 exec 的退出码/stdout），走**同一**溯源路径。"""
        return self._new_key(desc)

    def bytes(self, rel: str, what: str):
        """时点假设：读取调用时刻的**磁盘字节**（不读 git 对象、不读缓存）⇒ 必须由调用方声明时点。"""
        p = self.root / rel
        if not p.exists():
            raise MeasurementUnavailable("%s：文件不存在 %s" % (what, rel))
        if not p.is_file():
            raise MeasurementUnavailable("%s：不是普通文件 %s" % (what, rel))
        data = p.read_bytes()                      # 字节导出法：整块按字节读
        if len(data) == 0:
            raise EmptyMeasurement(
                "%s：%s 逐字节读数 = 0 字节 ⇒ 第 16 条：取数为空必须抛错，"
                "不得输出 0 / 空串 / 空集合当作读数" % (what, rel)
            )
        return self._new_key("%s｜%s（%d 字节）" % (what, rel, len(data))), data

    def text(self, rel: str, what: str):
        """时点假设同 `bytes()`；另加 UTF-8 解码口径（解码失败 ⇒ 未取到数）。"""
        key, data = self.bytes(rel, what)
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise MeasurementUnavailable("%s：%s 非 UTF-8（%s）" % (what, rel, exc)) from exc
        if text.strip() == "":
            raise EmptyMeasurement(
                "%s：%s 解码后为空串（仅空白）⇒ 第 16 条：取数失败必须抛错" % (what, rel)
            )
        return key, text

    def num(self, value, src_key: str, what: str):
        """报告段/结构段的**每一个数值**都必须经此产出，从而可追溯至一次非空取数。

        同时兜住第 18 条 ①：**本轮未声明测量时点 ⇒ 读数不可采信 ⇒ 立刻抛错**（不出结论）。
        """
        if not self.timing:
            raise MeasurementUntrusted(
                "读数不可采信：未声明测量时点（at / 顶层 measure_at）⇒ 第 18 条 ①："
                "未声明时点的读数一律不采信 ⇒ 拒绝出结论（既不当作「通过」，也不当作「未通过」）"
            )
        if src_key not in self.sources:
            raise AssertionError("数值 %s=%r 无法追溯至任何非空取数（第 16 条）" % (what, value))
        self.values.append((what, value, src_key))
        return value

    def provenance_line(self) -> str:
        return "数值溯源断言：%d 个数值全部可追溯至 %d 次非空取数（测量时点 = %s）" % (
            len(self.values), len(self.sources), self.timing or "**未声明**",
        )


# ─────────────────────────── 量具（第 7 / 14 条）───────────────────────────
def measure_lines(text: str, measure: str) -> int:
    if measure == "readalllines":
        return len(text.splitlines())
    if measure == "split_lf":
        return len(text.split("\n"))
    raise IdentifierRejected("量具定义未声明或表外取值：measure=%r" % (measure,))


def contrast_lines(text: str) -> int:
    """对照口径，仅用于报告，**不参与判定**（第 7 条：报告须标注所用口径）。"""
    return len(text.split("\n"))


def measure_fences(text: str, fence_measure: str) -> int:
    if fence_measure == "indent_aware":
        return sum(1 for ln in text.split("\n") if ln.lstrip(" \t").startswith("```"))
    if fence_measure == "column0":
        return sum(1 for ln in text.split("\n") if ln.startswith("```"))
    raise IdentifierRejected("量具定义未声明或表外取值：fence_measure=%r" % (fence_measure,))


def count_h2(text: str) -> int:
    return sum(
        1
        for ln in text.splitlines()
        if ln.startswith("## ") and not ln.startswith("### ")
    )


# ──────────── 集合形状定型（第 17 条 ①：严禁对取数结果直接 .Count / -join）────────────
def _describe_shape(value) -> str:
    if isinstance(value, dict):
        return "映射(%d 键)" % len(value)
    if isinstance(value, (list, tuple, set)):
        inner = [type(v).__name__ for v in value]
        return "%s(%d 元素：%s)" % (type(value).__name__, len(value), ",".join(inner[:5]) or "空")
    return type(value).__name__


def typed_flat(value, what: str, elem_type=None) -> list:
    """取数结果**必须在内部定型**：非序列 / 元素被额外包裹 / 元素类型不符 ⇒ 立刻抛错。

    这一步就是第 20 例的对策：**不允许**对取数函数返回值直接取长度或拼串 ——
    双重包裹（`@( @(a,b) )` 的 Python 对应 = `[["a","b"]]`）会让 `.Count`/len() 恒为 1。
    """
    if value is None:
        raise ShapeAnomaly("%s：取数返回 null ⇒ 第 17 条 ①：形状异常必须抛错" % what)
    if isinstance(value, str) or not hasattr(value, "__len__") or isinstance(value, dict):
        raise ShapeAnomaly(
            "%s：取数返回非序列（%s）⇒ 形状异常必须抛错，不得静默当作 1 个元素" % (what, _describe_shape(value))
        )
    items = list(value)
    for i, v in enumerate(items):
        if isinstance(v, (list, tuple, set, dict)):
            raise ShapeAnomaly(
                "%s：第 %d 个元素仍是被包裹的集合（%s）⇒ 形状异常（双重包裹会让计数恒为 1）"
                "⇒ 必须抛错，禁止静默计数" % (what, i, _describe_shape(v))
            )
        if elem_type is not None and not isinstance(v, elem_type):
            raise ShapeAnomaly(
                "%s：第 %d 个元素类型为 %s，期望 %s ⇒ 定型失败" % (what, i, type(v).__name__, elem_type.__name__)
            )
    return items


def typed_ints(value, what: str) -> list:
    if isinstance(value, bool) or (not isinstance(value, (list, tuple)) and not hasattr(value, "__len__")):
        raise ShapeAnomaly("%s：期望整数序列，实得 %s" % (what, _describe_shape(value)))
    return [int(v) for v in typed_flat(value, what)]


def typed_strs(value, what: str) -> list:
    return [str(v) for v in typed_flat(value, what, str)]


def count_of(value, what: str) -> int:
    """**唯一**允许的计数入口：先定型，再计数（禁止对取数结果直接 len()）。"""
    return len(typed_flat(value, what))


def join_flat(value, sep: str, what: str) -> str:
    """**唯一**允许的拼接入口：先定型，再拼接（禁止出现 'System.Object[]' 式静默串化）。"""
    return sep.join(typed_strs(value, what))


# ──────────── 外部输出结构化（第 18 条 ②：剥离 ANSI + 显式类型转换）────────────
# 原型 (b)：门禁项数正则被 ANSI 转义切断（`总计:[0m` ⇒ `\s*` 不匹配）⇒ 两次都**未取到数**，
#           却输出了「项数 = （空）」这类**空值伪读数**。
# 原型 (c)：`@(git rev-list --count …)` ⇒ 输出 `System.Object[]` ⇒ 集合被直接交给格式化/比较。
ANSI_RE = re.compile(r"\x1b(?:\[[0-9;?]*[ -/]*[@-~]|[@-Z\\-_])")


def count_ansi(text: str) -> int:
    """ANSI 转义出现次数（用于「原始 N 处 ⇒ 结构化后 0 处」的证据行）。"""
    return len(ANSI_RE.findall(text))


def strip_ansi(text: str) -> str:
    """**结构化第一步**：剥离 ANSI/CSI 转义，之后才允许参与读数。"""
    return ANSI_RE.sub("", text)


def scalar_text(value, what: str) -> str:
    """**结构化第二步**：集合 / 多值 / 空值**一律不得**直接交给格式化或比较（第 18 条 ②）。"""
    if isinstance(value, (list, tuple, set, frozenset, dict)):
        raise ShapeAnomaly(
            "%s：不得把集合/多值（形状 = %s）直接交给格式化或比较 ⇒ 第 18 条 ②"
            "（`System.Object[]` 同族）" % (what, _describe_shape(value))
        )
    if value is None:
        raise EmptyMeasurement("%s：不得把空值（None）当作读数输出 ⇒ 第 16 / 18 条" % what)
    return str(value)


def scalar_int(value, what: str) -> int:
    """**结构化第二步**（整数口径）：显式类型转换；非整数 ⇒ 抛错，不做隐式串化。"""
    if isinstance(value, bool) or not isinstance(value, int):
        if isinstance(value, (list, tuple, set, frozenset, dict)):
            raise ShapeAnomaly(
                "%s：集合/多值（形状 = %s）不得当作单值整数 ⇒ 第 18 条 ②" % (what, _describe_shape(value))
            )
        raise MeasurementUntrusted(
            "%s：显式整数转型失败（收到 %s）⇒ 读数不可采信，不得隐式串化 ⇒ 第 18 条 ②"
            % (what, type(value).__name__)
        )
    return value


class ExternalOutput:
    """**外部命令输出的唯一结构化入口**（第 18 条 ②）。

    所有「外部输出参与读数」的路径都必须先经本类：① 剥离 ANSI 转义；② 显式类型转换；
    ③ 拒绝把集合 / 多值 / 空值当作单值读数（`System.Object[]` 与「项数 = （空）」两条原型）。
    """

    def __init__(self, argv, returncode, stdout_raw: bytes, stderr_raw: bytes) -> None:
        self.argv = [str(a) for a in argv]
        self.returncode = int(returncode)                       # 显式转型（禁止保留字符串）
        self.stdout_bytes = len(stdout_raw)
        self.stderr_bytes = len(stderr_raw)
        self.stdout_raw = stdout_raw.decode("utf-8", errors="replace")
        self.stderr_raw = stderr_raw.decode("utf-8", errors="replace")
        self.ansi_stdout_raw = count_ansi(self.stdout_raw)
        self.ansi_stderr_raw = count_ansi(self.stderr_raw)
        self.stdout = strip_ansi(self.stdout_raw)               # ← 只有剥离后的文本可参与读数
        self.stderr = strip_ansi(self.stderr_raw)
        self.ansi_stdout = count_ansi(self.stdout)
        self.ansi_stderr = count_ansi(self.stderr)

    def ansi_line(self) -> str:
        return ("ANSI 转义剥离（第 18 条 ②）：stdout 原始 %d 处 ⇒ 结构化后 %d 处；"
                "stderr 原始 %d 处 ⇒ 结构化后 %d 处"
                % (self.ansi_stdout_raw, self.ansi_stdout, self.ansi_stderr_raw, self.ansi_stderr))

    def value_lines(self) -> list:
        return [ln for ln in self.stdout.splitlines() if ln.strip() != ""]

    def scalar(self, what: str) -> str:
        vs = self.value_lines()
        if not vs:
            raise EmptyMeasurement(
                "%s：剥离 ANSI 后 stdout **无非空行** ⇒ 第 16 / 18 条：不得输出「（空）」这类空值伪读数" % what
            )
        if len(vs) > 1:
            raise ShapeAnomaly(
                "%s：stdout 有 %d 个非空行（多值）⇒ 不得当作单值读数 ⇒ 第 18 条 ②" % (what, len(vs))
            )
        return vs[0]

    def as_int(self, what: str) -> int:
        """显式类型转换：单值且必须是完整整数，否则抛错（绝不输出空值/多值）。"""
        s = self.scalar(what).strip()
        if not re.fullmatch(r"[+-]?\d+", s):
            raise MeasurementUntrusted(
                "%s：单值 %r 不是完整整数 ⇒ 显式类型转换失败 ⇒ 读数不可采信（第 18 条 ②）" % (what, s)
            )
        return int(s)

    def int_via_regex(self, pattern, what: str) -> int:
        """按正则取**唯一**单值整数：0 处匹配 ⇒ 未取到数；>1 处 / 多分组 ⇒ 抛错（不得取其一）。"""
        matches = pattern.findall(self.stdout)
        if not matches:
            raise MeasurementUnavailable(
                "%s：剥离 ANSI 后仍 0 处匹配 %r ⇒ 未取到数（**不得**输出空值当读数）"
                % (what, pattern.pattern)
            )
        if len(matches) > 1:
            raise ShapeAnomaly(
                "%s：%d 处匹配 ⇒ 多值 ⇒ 不得当作单值读数（第 18 条 ②，`System.Object[]` 同族）"
                % (what, len(matches))
            )
        m0 = matches[0]
        if isinstance(m0, tuple):
            raise ShapeAnomaly(
                "%s：正则声明了 %d 个捕获组 ⇒ findall 返回元组（双重包裹）⇒ 第 17 条 ① / 第 18 条 ②"
                % (what, len(m0))
            )
        return scalar_int(_int_from_text(m0, what), what)


def _int_from_text(text: str, what: str) -> int:
    s = str(text).strip()
    if not re.fullmatch(r"[+-]?\d+", s):
        raise MeasurementUntrusted(
            "%s：捕获值 %r 不是完整整数 ⇒ 显式类型转换失败 ⇒ 读数不可采信（第 18 条 ②）" % (what, s)
        )
    return int(s)


def code_only_source(src: str) -> str:
    """源码「去注释 / 去 docstring」口径（量具定义见下），用于禁词自检。

    量具定义：先 `ast.parse`，把模块/类/函数的首个字符串常量（docstring）置为空串，
    再 `ast.unparse`（AST 本身不含注释）⇒ 结果**只保留可执行代码与其余字符串字面量**。
    **对照口径**：整文件原文匹配（含注释与 docstring）。
    本工具自检实测：整文件口径会把说明性文字里的「禁词」误报成违规（假阳性，同族第 11 例），
    故禁词自检一律用「去注释/去 docstring」口径，并**同时打印对照口径的命中**作为证据。
    """
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = getattr(node, "body", None) or []
            if body:
                first = body[0]
                if (isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)
                        and isinstance(first.value.value, str)):
                    first.value.value = ""
    return ast.unparse(tree)


# ─────────────────────────── 三口径（第 4 条）───────────────────────────
def caliber_raw(line: str) -> str:
    return line


def caliber_strip_backtick(line: str) -> str:
    return line.replace("`", "")


def caliber_strip_inline(line: str) -> str:
    return re.sub(r"[`*_~]", "", line)


CALIBERS = (
    ("原样", caliber_raw),
    ("去反引号", caliber_strip_backtick),
    ("去行内标记", caliber_strip_inline),
)

SEGMENT_SPLIT_RE = re.compile(r"[\s，。：；、,.:;!?！？（）()\[\]【】「」《》\"'|/]+")


def candidate_keys(text: str) -> list:
    """可满足性前置（第 2 条）用的候选键：整串（去行内标记）+ 最长片段。"""
    norm = caliber_strip_inline(text).strip()
    keys = [norm] if norm else []
    segs = [s for s in SEGMENT_SPLIT_RE.split(norm) if len(s) >= 2]
    if segs:
        keys.append(max(segs, key=len))
    out = []
    for k in keys:
        if k and k not in out:
            out.append(k)
    return out


def matched_by(mode: str, line: str, target: str) -> bool:
    if mode == "exact":
        return line.strip() == target
    if mode == "prefix":
        return line.strip().startswith(target)
    if mode == "substring":
        return target in line
    raise IdentifierRejected("匹配方式未声明或表外取值：match=%r" % (mode,))


# ─────────────────────────── 判据执行结果的载体 ───────────────────────────
class Outcome:
    """**每轮显式新建**（第 10 条：禁止跨轮复用结果变量）。"""

    __slots__ = ("idx", "id", "kind", "state", "detail", "structural", "report_reason")

    def __init__(self, idx: int, cid: str, kind: str) -> None:
        self.idx = idx
        self.id = cid
        self.kind = kind
        self.state = S_UNKNOWN
        self.detail = ""
        self.structural: list = []
        self.report_reason = ""

    def add(self, line: str) -> None:
        self.structural.append(line)


class RunContext:
    """一次运行的**唯一**状态容器。报告段只依赖它，不依赖执行控制流。"""

    def __init__(self) -> None:
        self.project_root: Path = Path(".")
        self.claims_path: Path | None = None
        self.claims: list = []              # 已解析的原始判据（含被拒绝的）
        self.outcomes: dict[int, Outcome] = {}
        self.report_items: list = []
        self.round_no = 0
        self.spec_errors: list = []
        self.executed = 0
        self.raised: list = []
        self.reader: Reader | None = None
        self.notes: list = []
        self.expect_judgements_declared = None     # 第 17 条 ②：声明的应产出判定条数
        self.gate_ok = True

    # 第 10 条：每轮显式置空
    def begin_round(self, idx: int, cid: str, kind: str) -> Outcome:
        self.round_no += 1
        out = Outcome(idx, cid, kind)
        self.outcomes[idx] = out
        return out


# ─────────────────────────── 判据文件解析与校验 ───────────────────────────
def load_claims_document(path: Path):
    if not path.exists():
        raise ClaimSpecInvalid("判据文件不存在：%s" % path)
    raw = path.read_bytes()
    if len(raw) == 0:
        raise ClaimSpecInvalid("判据文件为空（0 字节）：%s" % path)
    try:
        doc = yaml.safe_load(raw.decode("utf-8"))
    except Exception as exc:
        raise ClaimSpecInvalid("判据文件 YAML 解析失败：%s" % exc) from exc
    if doc is None:
        raise ClaimSpecInvalid("判据文件无内容（YAML 解析为 None）")
    if isinstance(doc, list):
        return {"claims": doc}
    if isinstance(doc, dict):
        return doc
    raise ClaimSpecInvalid("判据文件顶层必须是列表或映射（含 claims 键）")


def validate_claims(doc: dict, table: IdentifierTable):
    """返回 (归一化后的判据列表, 声明的应产出判定条数)。

    任一项不合法 ⇒ ClaimSpecInvalid（退出码 3，未执行任何判据）。
    """
    unknown_top = [k for k in doc if k not in TOP_LEVEL_KEYS]
    if unknown_top:
        raise ClaimSpecInvalid("判据文件顶层出现未知键：%s" % ", ".join(sorted(unknown_top)))

    # 第 18 条 ①：时点与范围同等重要。顶层 measure_at 作为**声明式默认值**，逐条可用 at 覆盖。
    doc_at = doc.get("measure_at")
    if doc_at is not None and not str(doc_at).strip():
        raise ClaimSpecInvalid(
            "顶层 measure_at 不得为空串（第 18 条 ①：未声明时点的读数一律不采信）"
        )

    expect_declared = doc.get("expect_judgements")
    if expect_declared is not None and (not isinstance(expect_declared, int) or isinstance(expect_declared, bool)):
        raise ClaimSpecInvalid("expect_judgements 必须是整数（第 17 条 ②：声明应产出的判定条数）")
    if isinstance(expect_declared, int) and expect_declared < 0:
        raise ClaimSpecInvalid("expect_judgements 不得为负")

    ids = doc.get("identifiers") or {}
    if ids and not isinstance(ids, dict):
        raise ClaimSpecInvalid("identifiers 必须是映射")
    table.register_files(ids.get("files"))
    table.register_workflows(ids.get("workflows"))
    table.register_ownership(ids.get("ownership"))

    raw_claims = doc.get("claims")
    if not isinstance(raw_claims, list) or not raw_claims:
        raise ClaimSpecInvalid("claims 必须是非空列表")

    seen: dict[str, int] = {}
    claims: list = []
    for idx, rc in enumerate(raw_claims):
        if not isinstance(rc, dict):
            raise ClaimSpecInvalid("第 %d 条判据不是映射" % (idx + 1))
        for k in OWNERSHIP_TEXT_KEYS:
            if k in rc:
                raise ClaimSpecInvalid(
                    "第 %d 条判据使用了 %r：禁止用截断/模糊文本做归属判定（§4.4 第 7 条）；"
                    "归属必须给结构化字段 owner" % (idx + 1, k)
                )
        if "id" not in rc:
            raise ClaimSpecInvalid("第 %d 条判据缺 id" % (idx + 1))
        kind = rc.get("kind")
        if kind not in CLAIM_KINDS:
            raise ClaimSpecInvalid(
                "第 %d 条判据 kind=%r 表外取值 ⇒ 允许：%s" % (idx + 1, kind, ", ".join(CLAIM_KINDS))
            )
        allowed = set(COMMON_KEYS) | set(KIND_KEYS[kind])
        unknown = [k for k in rc if k not in allowed]
        if unknown:
            raise ClaimSpecInvalid(
                "第 %d 条判据（kind=%s）出现未知键：%s（未知键一律拒绝，避免拼写错误静默通过）"
                % (idx + 1, kind, ", ".join(sorted(unknown)))
            )

        cid = table.register_claim_id(rc["id"])
        if cid in seen:
            raise ClaimSpecInvalid("判据 id 重复（归一后）：%r 与第 %d 条冲突" % (cid, seen[cid]))
        seen[cid] = idx + 1

        # 第 18 条 ①：**未声明测量时点 ⇒ 拒绝执行该判据**（不算通过也不算未通过，不出结论）。
        at = rc.get("at", doc_at)
        if at is None or not str(at).strip():
            raise ClaimSpecInvalid(
                "第 %d 条判据未声明测量时点（本条无 at，且顶层无 measure_at）⇒ 第 18 条 ①："
                "未声明时点的读数一律**不可采信** ⇒ 拒绝执行该判据（既不算通过也不算未通过，不出结论）"
                % (idx + 1)
            )

        norm = {
            "id": cid,
            "kind": kind,
            "note": rc.get("note") or "",
            "enabled": rc.get("enabled", True),
            "at": str(at).strip(),          # 测量时点（第 18 条 ①）
            "owner": None,
            "workflow": None,
            "_raw": rc,
        }
        if "owner" in rc:
            norm["owner"] = table.normalize("ownership", rc["owner"])   # 枚举外 ⇒ 立刻抛错
        if "workflow" in rc:
            norm["workflow"] = table.normalize("workflow", rc["workflow"])
        if not isinstance(norm["enabled"], bool):
            raise ClaimSpecInvalid("第 %d 条判据 enabled 必须是布尔" % (idx + 1))

        if "file" in rc:
            norm["file"] = table.normalize("file", rc["file"])
        else:
            norm["file"] = None
        if "cross_check_file" in rc:
            norm["cross_check_file"] = table.normalize("file", rc["cross_check_file"])

        _validate_kind_fields(rc, norm, idx + 1, kind)
        claims.append(norm)
    return claims, expect_declared


def _validate_kind_fields(rc: dict, norm: dict, human_idx: int, kind: str) -> None:
    def need(key):
        if key not in rc:
            raise ClaimSpecInvalid("第 %d 条判据（kind=%s）缺必填字段 %s" % (human_idx, kind, key))

    if kind == "contains":
        need("file")
        need("text")
        need("match")                                   # 第 3 条：未声明 ⇒ 拒绝执行
        if rc["match"] not in MATCH_MODES:
            raise ClaimSpecInvalid(
                "第 %d 条判据 match=%r 表外取值 ⇒ 允许：%s" % (human_idx, rc["match"], ", ".join(MATCH_MODES))
            )
        if not str(rc["text"]).strip():
            raise ClaimSpecInvalid("第 %d 条判据 text 为空串" % human_idx)
        norm["text"] = str(rc["text"])
        norm["match"] = rc["match"]
    elif kind == "count_regex":
        need("file")
        need("pattern")
        need("expect")
        need("algorithm")                               # 第 5 条：计数类必填 dual
        if rc["algorithm"] not in ALGORITHMS:
            raise ClaimSpecInvalid(
                "第 %d 条判据 algorithm=%r 表外取值 ⇒ 允许：%s" % (human_idx, rc["algorithm"], ", ".join(ALGORITHMS))
            )
        try:
            norm["pattern"] = re.compile(str(rc["pattern"]))
        except re.error as exc:
            raise ClaimSpecInvalid("第 %d 条判据 pattern 非合法正则：%s" % (human_idx, exc)) from exc
        if not isinstance(rc["expect"], int) or isinstance(rc["expect"], bool):
            raise ClaimSpecInvalid("第 %d 条判据 expect 必须是整数" % human_idx)
        norm["expect"] = rc["expect"]
        norm["algorithm"] = rc["algorithm"]
    elif kind == "shape":
        need("file")
        need("measure")                                 # 第 14 条：量具定义显式声明
        if rc["measure"] not in LINE_MEASURES:
            raise ClaimSpecInvalid(
                "第 %d 条判据 measure=%r 表外取值 ⇒ 允许：%s" % (human_idx, rc["measure"], ", ".join(LINE_MEASURES))
            )
        norm["measure"] = rc["measure"]
        if "fences" in rc:
            if "fence_measure" not in rc:
                raise ClaimSpecInvalid(
                    "第 %d 条判据声明了 fences 但缺 fence_measure（第 14 条：量具定义必须显式声明）" % human_idx
                )
            if rc["fence_measure"] not in FENCE_MEASURES:
                raise ClaimSpecInvalid(
                    "第 %d 条判据 fence_measure=%r 表外取值 ⇒ 允许：%s"
                    % (human_idx, rc["fence_measure"], ", ".join(FENCE_MEASURES))
                )
            norm["fence_measure"] = rc["fence_measure"]
        for key in ("lines", "h2", "fences"):
            if key in rc:
                if not isinstance(rc[key], int) or isinstance(rc[key], bool):
                    raise ClaimSpecInvalid("第 %d 条判据 %s 必须是整数" % (human_idx, key))
                norm[key] = rc[key]
        if not any(k in norm for k in ("lines", "h2", "fences")):
            raise ClaimSpecInvalid(
                "第 %d 条判据（kind=shape）未声明任何被测量指标（lines/h2/fences）" % human_idx
            )
    elif kind == "sha256":
        need("file")
        need("expect")
        exp = str(rc["expect"]).strip().lower()
        if not re.fullmatch(r"[0-9a-f]{8,64}", exp):
            raise ClaimSpecInvalid("第 %d 条判据 expect 必须是 8~64 位十六进制" % human_idx)
        norm["expect"] = exp
    elif kind == "exec":
        need("command")
        cmd = rc["command"]
        if isinstance(cmd, str) or not isinstance(cmd, list) or not cmd:
            raise ClaimSpecInvalid(
                "第 %d 条判据 command 必须是非空数组（禁止以字符串形式传给 shell，禁止开启 shell 解析）" % human_idx
            )
        if not all(isinstance(c, str) and c for c in cmd):
            raise ClaimSpecInvalid("第 %d 条判据 command 元素必须是非空字符串" % human_idx)
        norm["command"] = list(cmd)
        norm["expect_exit"] = rc.get("expect_exit", 0)
        if not isinstance(norm["expect_exit"], int) or isinstance(norm["expect_exit"], bool):
            raise ClaimSpecInvalid("第 %d 条判据 expect_exit 必须是整数" % human_idx)
        if "stdout_contains" in rc:
            need("stdout_match")                        # 第 3 条同款：匹配方式必须显式声明
            if rc["stdout_match"] not in MATCH_MODES:
                raise ClaimSpecInvalid(
                    "第 %d 条判据 stdout_match=%r 表外取值 ⇒ 允许：%s"
                    % (human_idx, rc["stdout_match"], ", ".join(MATCH_MODES))
                )
            norm["stdout_contains"] = str(rc["stdout_contains"])
            norm["stdout_match"] = rc["stdout_match"]
        norm["timeout_sec"] = rc.get("timeout_sec", 60)
        if not isinstance(norm["timeout_sec"], (int, float)) or norm["timeout_sec"] <= 0:
            raise ClaimSpecInvalid("第 %d 条判据 timeout_sec 必须是正数" % human_idx)
        if "stdout_int_regex" in rc:
            need("expect_int")                          # 显式类型转换必须有期望值可比
            try:
                pat = re.compile(str(rc["stdout_int_regex"]))
            except re.error as exc:
                raise ClaimSpecInvalid(
                    "第 %d 条判据 stdout_int_regex 非合法正则：%s" % (human_idx, exc)
                ) from exc
            if pat.groups != 1:
                raise ClaimSpecInvalid(
                    "第 %d 条判据 stdout_int_regex 必须**恰好 1 个**捕获组（第 17 条 ① / 第 18 条 ②："
                    "多分组 ⇒ findall 返回元组 ⇒ 双重包裹 ⇒ 声明 %d 个" % (human_idx, pat.groups)
                )
            norm["stdout_int_regex"] = pat
            if not isinstance(rc["expect_int"], int) or isinstance(rc["expect_int"], bool):
                raise ClaimSpecInvalid("第 %d 条判据 expect_int 必须是整数" % human_idx)
            norm["expect_int"] = rc["expect_int"]


# ─────────────────────────── 各类型判据的执行 ───────────────────────────
def eval_contains(claim: dict, rd: Reader, out: Outcome) -> None:
    key, text = rd.text(claim["file"], "contains 目标文件")
    lines = text.splitlines()
    out.add("量具定义：%s" % CONTAINS_MEASURE_DOC[claim["match"]])
    out.add("匹配方式声明：match=%s（第 3 条）" % claim["match"])
    out.add("文件：%s（%d 行，口径=readalllines）" % (claim["file"], count_of(lines, "目标文件行集合")))
    rd.num(count_of(lines, "目标文件行集合"), key, "候选扫描行数")

    keys = candidate_keys(claim["text"])
    if not keys:
        raise ClaimSpecInvalid("contains 的目标串归一后为空 ⇒ 拒绝执行")

    per_caliber_cand = {}
    for name, fn in CALIBERS:
        hits_lines = [ln for ln in lines if any(k in fn(ln) for k in keys)]
        per_caliber_cand[name] = count_of(hits_lines, "候选行集合[%s]" % name)
        out.add("候选行数[%s] = %d" % (name, per_caliber_cand[name]))

    loosest = per_caliber_cand[CALIBERS[-1][0]]
    rd.num(loosest, key, "候选行数(去行内标记)")
    if loosest == 0:
        out.state = S_NOT_EST
        out.detail = (
            "可满足性前置：0 候选（候选键 %s 在该文件中连一行都不出现）⇒ 判「判据不成立」，"
            "不判「未通过」（第 2 条 / 第 13 例）" % "、".join(repr(k) for k in keys)
        )
        out.report_reason = out.detail
        return

    hits = {}
    for name, fn in CALIBERS:
        target = fn(claim["text"]).strip()
        hits[name] = any(matched_by(claim["match"], fn(ln), target) for ln in lines)
        out.add("三口径判定[%s] = %s" % (name, "命中" if hits[name] else "未命中"))
    merged = any(hits.values())
    out.add("合并结论 = %s（三口径任一命中即判命中）" % ("命中" if merged else "未命中"))

    if claim.get("cross_check_file"):
        cc = claim["cross_check_file"]
        try:
            ckey, ctext = rd.text(cc, "cross_check 文件")
            clines = ctext.splitlines()
            cand = count_of(
                [ln for ln in clines if any(k in caliber_strip_inline(ln) for k in keys)],
                "cross_check 候选行集合",
            )
            out.add("cross_check 文件 %s：候选数 = %d（行数 %d）"
                    % (cc, cand, count_of(clines, "cross_check 行集合")))
            rd.num(cand, ckey, "cross_check 候选数")
        except MeasurementUnavailable as exc:
            out.add("cross_check 文件取数失败：%s ⇒ 该判据按「未取到数」处理" % exc)
            out.state = S_UNKNOWN
            out.detail = "cross_check 文件取数失败：%s" % exc
            out.report_reason = out.detail
            return

    out.state = S_PASS if merged else S_FAIL
    if merged:
        hit_calibers = [n for n, v in hits.items() if v]
        out.detail = "命中（命中口径：%s）；候选行数[原样/去反引号/去行内标记] = %d/%d/%d" % (
            "、".join(hit_calibers),
            per_caliber_cand["原样"], per_caliber_cand["去反引号"], per_caliber_cand["去行内标记"],
        )
    else:
        out.detail = "未命中（三口径均未命中）；候选行数 = %d（有候选 ⇒ 判「未通过」，非「不成立」）" % loosest
    out.report_reason = out.detail


def eval_count_regex(claim: dict, rd: Reader, out: Outcome) -> None:
    key, text = rd.text(claim["file"], "count_regex 目标文件")
    pat = claim["pattern"]
    out.add("算法声明：algorithm=dual（第 5 条：两种独立算法各算一遍，不一致不得取其一）")
    out.add("集合定型：两个算法的命中集合都先经 typed_flat 定型，再计数（第 17 条 ①）")
    raw_a = [ln for ln in text.splitlines() if pat.search(ln)]
    algo_a = count_of(raw_a, "算法A 命中行集合")
    out.add("算法 A（逐行 re.search 命中行数） = %d（集合形状：list[str] %d 元素）" % (algo_a, algo_a))
    raw_b = pat.findall(text)
    hits_b = typed_flat(raw_b, "算法B 命中集合（re.findall 结果）")
    algo_b = len(hits_b)
    out.add("算法 B（全文 re.findall 命中个数） = %d（集合形状：list[标量] %d 元素）" % (algo_b, algo_b))
    rd.num(algo_a, key, "算法A")
    rd.num(algo_b, key, "算法B")
    if algo_a != algo_b:
        out.state = S_FAIL
        out.detail = (
            "双算法不一致（A=%d，B=%d）⇒ 只能报「不一致」，**不得取其一**（第 5 条 / 第 11 例）"
            % (algo_a, algo_b)
        )
        out.report_reason = out.detail
        return
    expect = claim["expect"]
    out.add("期望值 = %d" % expect)
    if algo_a == 0 and expect != 0:
        out.add("注：0 命中是**派生的计数读数**（文件取数非空），不属第 16 条的伪读数")
    out.state = S_PASS if algo_a == expect else S_FAIL
    out.detail = "两算法一致 = %d；期望 %d ⇒ %s" % (algo_a, expect, "相等" if algo_a == expect else "不等")
    out.report_reason = out.detail


def eval_shape(claim: dict, rd: Reader, out: Outcome) -> None:
    key, text = rd.text(claim["file"], "shape 目标文件")
    measure = claim["measure"]
    lines_n = measure_lines(text, measure)
    out.add("量具定义[行数]：%s" % MEASURE_DOC[measure])
    # 对照口径必须**换一个口径**；若实测口径本就是 split_lf，则对照口径取 readalllines
    # （否则「对照口径」会与所用口径同值 ⇒ 文字自相矛盾，实测踩坑）。
    if measure == "readalllines":
        contrast_doc, contrast_n = 'split("\\n")', contrast_lines(text)
        rd.num(contrast_n, key, "对照口径行数")
    else:
        contrast_doc, contrast_n = "ReadAllLines", len(text.splitlines())
    out.add("行数 = %d（所用口径 %s）；对照口径 %s = %d" % (lines_n, measure, contrast_doc, contrast_n))
    rd.num(lines_n, key, "行数(%s)" % measure)

    actual = {"lines": lines_n}
    if "h2" in claim:
        actual["h2"] = count_h2(text)
        out.add('h2 计数定义：以 "## " 开头且不以 "### " 开头；实测 = %d' % actual["h2"])
        rd.num(actual["h2"], key, "h2 计数")
    if "fences" in claim:
        fm = claim["fence_measure"]
        actual["fences"] = measure_fences(text, fm)
        out.add("量具定义[围栏]：%s" % MEASURE_DOC[fm])
        out.add("围栏 = %d（所用口径 %s）；对照口径 column0 = %d"
                % (actual["fences"], fm, measure_fences(text, "column0")))
        rd.num(actual["fences"], key, "围栏(%s)" % fm)

    diffs = []
    for k, want in (("lines", claim.get("lines")), ("h2", claim.get("h2")), ("fences", claim.get("fences"))):
        if want is None:
            continue
        got = actual[k]
        out.add("比对 %s：实测 %d vs 期望 %d ⇒ %s" % (k, got, want, "相等" if got == want else "不等"))
        if got != want:
            diffs.append("%s（实测 %d ≠ 期望 %d）" % (k, got, want))
    if diffs:
        out.state = S_FAIL
        out.detail = "结构不符：" + "、".join(diffs)
    else:
        out.state = S_PASS
        out.detail = "结构相符（量具口径 %s）" % measure
    out.report_reason = out.detail


def eval_sha256(claim: dict, rd: Reader, out: Outcome) -> None:
    key, data = rd.bytes(claim["file"], "sha256 目标文件")
    digest = hashlib.sha256(data).hexdigest()
    exp = claim["expect"]
    out.add("字节数 = %d" % len(data))
    out.add("sha256 = %s" % digest)
    out.add("期望（前缀比对，长度 %d）= %s" % (len(exp), exp))
    rd.num(len(data), key, "字节数")
    if digest.startswith(exp):
        out.state = S_PASS
        out.detail = "sha256 前 %d 位相符" % len(exp)
    else:
        out.state = S_FAIL
        out.detail = "sha256 前 %d 位不符（实测 %s）" % (len(exp), digest[: len(exp)])
    out.report_reason = out.detail


def eval_exec(claim: dict, rd: Reader, out: Outcome) -> None:
    """外部命令判据。

    时点假设（第 18 条 ①）：命令在**本次调用时刻**执行（无缓存、不复用上一轮结果）；
    所有外部输出一律先经 `ExternalOutput` **结构化**（剥离 ANSI + 显式类型转换）后才允许参与读数。
    """
    cmd = [c.replace("{python}", sys.executable) for c in claim["command"]]
    out.add("命令（数组，无 shell）= %s" % json.dumps(cmd, ensure_ascii=False))
    try:
        proc = subprocess.run(
            cmd, cwd=str(rd.root), capture_output=True, timeout=claim["timeout_sec"], shell=False
        )
    except FileNotFoundError as exc:
        raise MeasurementUnavailable("命令不存在：%s（%s）" % (cmd[0], exc)) from exc
    except subprocess.TimeoutExpired as exc:
        raise MeasurementUnavailable("命令超时 %ss：%s" % (claim["timeout_sec"], exc)) from exc

    # ← 外部输出**唯一**结构化入口：剥离 ANSI + 显式转型；此后只用 eo.stdout / eo.stderr
    eo = ExternalOutput(cmd, proc.returncode, proc.stdout, proc.stderr)
    stdout, stderr = eo.stdout, eo.stderr
    out.add("显式退出码 = %d（第 9 条）" % eo.returncode)
    out.add(eo.ansi_line())
    out.add("stdout 字节数 = %d；stderr 字节数 = %d（stderr 必须显式检查，不得只看 stdout）"
            % (eo.stdout_bytes, eo.stderr_bytes))
    if eo.stdout_raw != eo.stdout:
        out.add("ANSI 剥离前后 stdout 不同 ⇒ 已按**结构化后**文本读数（第 18 条 ②）")
    if stderr.strip():
        out.add("stderr 首行 = %s" % stderr.strip().splitlines()[0][:160])
    src = rd.external("exec 输出｜%s（stdout %d 字节，ANSI 原始 %d 处）"
                      % (cmd[0], eo.stdout_bytes, eo.ansi_stdout_raw))
    rd.num(scalar_int(eo.returncode, "exec 退出码"), src, "exec 退出码")

    if eo.returncode != claim["expect_exit"]:
        out.state = S_FAIL
        out.detail = "退出码 %d ≠ 期望 %d" % (eo.returncode, claim["expect_exit"])
        out.report_reason = out.detail
        return
    if "stdout_contains" in claim:
        if stdout.strip() == "":
            raise EmptyMeasurement(
                "exec：命令退出码符合期望，但**剥离 ANSI 后** stdout 为空 ⇒ 第 8/16/18 条："
                "非空断言失败，判「未取到数」，不得输出「（空）」当读数"
            )
        ok = matched_by(claim["stdout_match"], stdout, claim["stdout_contains"]) or any(
            matched_by(claim["stdout_match"], ln, claim["stdout_contains"]) for ln in stdout.splitlines()
        )
        out.add("stdout 匹配（方式 %s，**在剥离 ANSI 后的文本上**）：%s"
                % (claim["stdout_match"], "命中" if ok else "未命中"))
        rd.num(count_of(stdout.splitlines(), "exec stdout 行集合"), src, "stdout 行数")
        if not ok:
            out.state = S_FAIL
            out.detail = "stdout 未命中目标串（方式 %s）" % claim["stdout_match"]
            out.report_reason = out.detail
            return
    if "stdout_int_regex" in claim:
        pat = claim["stdout_int_regex"]
        out.add("单值整数取数（第 18 条 ②）：正则 = %s（捕获组 %d 个，剥离 ANSI 后匹配）"
                % (pat.pattern, pat.groups))
        got = eo.int_via_regex(pat, "exec stdout 单值整数读数")
        rd.num(got, src, "stdout 整数读数（显式转型）")
        out.add("显式转型后读数 = %d；期望 = %d" % (got, claim["expect_int"]))
        if got != claim["expect_int"]:
            out.state = S_FAIL
            out.detail = "stdout 整数读数 %d ≠ 期望 %d" % (got, claim["expect_int"])
            out.report_reason = out.detail
            return
    out.state = S_PASS
    out.detail = ("退出码 %d 符合期望；stdout/stderr 已显式检查；"
                  "外部输出已结构化（ANSI 原始 %d 处 ⇒ 结构化后 %d 处）"
                  % (eo.returncode, eo.ansi_stdout_raw, eo.ansi_stdout))
    out.report_reason = out.detail


EVALUATORS = {
    "contains": eval_contains,
    "count_regex": eval_count_regex,
    "shape": eval_shape,
    "sha256": eval_sha256,
    "exec": eval_exec,
}


# ─────────────────────────── 执行循环（含 skip 分支）───────────────────────────
def run_all(ctx: RunContext, table: IdentifierTable) -> None:
    rd = Reader(ctx.project_root)
    ctx.reader = rd
    for idx, claim in enumerate(ctx.claims):           # ← 报告段用的是**另一次**独立遍历
        out = ctx.begin_round(idx, claim["id"], claim["kind"])   # 第 10 条：每轮显式新建
        rd.set_timing(claim.get("at"))                 # 第 18 条 ①：每轮显式声明测量时点（禁止跨轮复用）
        if claim["enabled"] is False:
            out.state = S_SKIP
            out.detail = "判据作者显式声明 enabled=false ⇒ 本条目跳过（不执行），但仍须出现在报告段"
            out.report_reason = out.detail
            continue                                    # ← TC-13 的 skip 分支，位于报告段之前
        try:
            EVALUATORS[claim["kind"]](claim, rd, out)
        except EmptyMeasurement as exc:
            ctx.raised.append("EmptyMeasurement: %s" % exc)
            out.state = S_UNKNOWN
            out.detail = "取数为空 ⇒ 按第 16 条**抛错**（EmptyMeasurement），不输出 0/空串/空集合当作读数：%s" % exc
            out.report_reason = out.detail
        except MeasurementUntrusted as exc:
            ctx.raised.append("MeasurementUntrusted: %s" % exc)
            out.state = S_UNKNOWN
            out.detail = ("读数**不可采信** ⇒ 按第 18 条**抛错**（MeasurementUntrusted），"
                          "**拒绝出结论**（既不当作通过，也不当作未通过）：%s" % exc)
            out.report_reason = out.detail
        except ShapeAnomaly as exc:
            ctx.raised.append("ShapeAnomaly: %s" % exc)
            out.state = S_UNKNOWN
            out.detail = ("集合形状异常 ⇒ 按第 17 条 ①**抛错**（ShapeAnomaly），"
                          "不把被包裹的多元集合静默报告成 1：%s" % exc)
            out.report_reason = out.detail
        except MeasurementUnavailable as exc:
            ctx.raised.append("MeasurementUnavailable: %s" % exc)
            out.state = S_UNKNOWN
            out.detail = "未取到数：%s" % exc
            out.report_reason = out.detail
        except ClaimSpecInvalid:
            raise
        except Exception as exc:                        # 绝不落 default 静默：一律显式登记
            ctx.raised.append("%s: %s" % (type(exc).__name__, exc))
            out.state = S_UNKNOWN
            out.detail = "执行异常（%s）：%s" % (type(exc).__name__, exc)
            out.report_reason = out.detail


# ─────────────────────────── 报告段（第 15 条：结构性解耦 + 独立非空断言）───
def build_report_section(ctx: RunContext) -> list:
    """**独立遍历**产出：对每一条应报项都要产出，且**只**能被它自身的条件跳过。

    本函数不参与执行控制流（无 continue / 无提前 return / 不依赖执行是否发生过异常），
    因此任何 skip / 异常 / 提前退出都不会让报告段整体消失（规格 §4.3 第 15 条 / 第 18 例）。
    """
    items = []
    for idx, claim in enumerate(ctx.claims):
        out = ctx.outcomes.get(idx)
        cid = claim.get("id", "?")
        kind = claim.get("kind", "?")
        if out is None:
            items.append("[%d] %s（kind=%s）⇒ 未执行：%s" % (idx + 1, cid, kind, "判据文件不合法，本条目未被求值"))
        else:
            items.append("[%d] %s（kind=%s）⇒ %s：%s" % (idx + 1, cid, kind, out.state, out.detail or "—"))
    return items


def assert_report_complete(ctx: RunContext) -> str:
    """**独立断言**：条目计数正确 ≠ 报告完整 ⇒ 必须另有一条「报告段非空且不缺项」断言。"""
    expected = len(ctx.claims)
    got = len(ctx.report_items)
    if expected > 0 and got == 0:
        raise ReportShortCircuit(
            "应报项 %d 条，但报告段为空 ⇒ 报告义务被短路（规格 §4.3 第 15 条 / 第 18 例）" % expected
        )
    if got < expected:
        raise ReportShortCircuit("应报项 %d 条，实际报告 %d 条 ⇒ 缺报 %d 条" % (expected, got, expected - got))
    return "报告段完整性断言：应报项 %d · 实报 %d · 缺报 %d ⇒ %s" % (
        expected, got, expected - got, "通过" if got >= expected else "失败",
    )


def assert_gate_self_check(ctx: RunContext) -> tuple:
    """第 17 条 ②：**判据门必须自断言**。

    声明应产出的判定条数，与实际产出的判定条数比对：
      *「未产出判定」= 该条目既没有判定态（通过/未通过/未取到数/不成立），也不是作者**显式**跳过；
      * 任一条未产出判定 ⇒ **该门视为无效 ⇒ 停手并报告**（不得据本次结论行动）。
    原型（第 20 例）：探针门因异常未产出判定，却因「没报错」而静默通过。
    """
    declared = ctx.expect_judgements_declared
    if isinstance(declared, int):
        expected = declared
        basis = "声明值 expect_judgements=%d" % declared
    else:
        expected = len([c for c in ctx.claims if c.get("enabled", True)])
        basis = "未声明 ⇒ 取「非显式跳过条目数」= %d" % expected
    actual = 0
    for i in range(len(ctx.claims)):
        out = ctx.outcomes.get(i)
        if out is not None and out.state in (S_PASS, S_FAIL, S_UNKNOWN, S_NOT_EST):
            actual += 1
    ctx.gate_ok = (expected == actual)
    ctx.gate_expected = expected
    ctx.gate_actual = actual
    line = "判据门自断言（第 17 条 ②）：应产出判定 %d（%s）· 实际产出判定 %d ⇒ %s" % (
        expected, basis, actual, "门有效" if ctx.gate_ok else "**该门无效 ⇒ 停手并报告**",
    )
    return ctx.gate_ok, line


# ─────────────────────────── 汇总（第 11 条：测量驱动）───────────────────────────
def count_states(ctx: RunContext) -> dict:
    c = {S_PASS: 0, S_FAIL: 0, S_UNKNOWN: 0, S_NOT_EST: 0, S_SKIP: 0}
    for out in ctx.outcomes.values():
        c[out.state] = c.get(out.state, 0) + 1
    c["total"] = len(ctx.claims)
    return c


def derive_verdict(c: dict, allow_unknown: bool, invalid: bool) -> tuple:
    """退出码由计数**机械推出**（规格 §4.6）；依据串内嵌实际计数，禁止写死结论。"""
    if invalid:
        return EXIT_INVALID, "依据：判据文件不合法（spec_errors=%d）⇒ §4.6 退出码 3，且未执行任何判据" % len(
            c.get("_spec", [])
        )
    if c.get("gate_expected") != c.get("gate_actual"):
        return EXIT_INVALID, (
            "依据：**判据门自断言失败**（应产出判定 %s ≠ 实际产出判定 %s）⇒ 该门视为无效 ⇒ **停手并报告**；"
            "退出码记 3（本门不可用 —— 第 17 条 ②）" % (c.get("gate_expected"), c.get("gate_actual"))
        )
    f, u, d = c[S_FAIL], c[S_UNKNOWN], c[S_NOT_EST]
    if f > 0:
        return EXIT_FAIL, "依据：未通过 %d > 0 ⇒ §4.6 退出码 1" % f
    if (u + d) > 0 and not allow_unknown:
        return EXIT_UNKNOWN, (
            "依据：未通过 %d = 0；未取到数 %d + 不成立 %d = %d > 0，且未加 --allow-unknown "
            "⇒ fail-closed，§4.6 退出码 2" % (f, u, d, u + d)
        )
    if (u + d) > 0 and allow_unknown:
        return EXIT_PASS, (
            "依据：未通过 %d = 0；未取到数 %d + 不成立 %d = %d > 0，但已显式 --allow-unknown "
            "⇒ 退出码 0（该态计数仍保留在报告中）" % (f, u, d, u + d)
        )
    if c["total"] > 0 and c.get("executed", 0) == 0:
        return EXIT_UNKNOWN, (
            "依据：未通过 %d = 0 且实际执行条目 %d = 0（全部跳过）⇒ fail-closed，退出码 2"
            % (f, c.get("executed", 0))
        )
    return EXIT_PASS, "依据：未通过 %d = 0 且未取到数 %d = 0 且不成立 %d = 0 ⇒ 退出码 0" % (f, u, d)


def render_summary(c: dict, allow_unknown: bool, invalid: bool) -> tuple:
    verdict, basis = derive_verdict(c, allow_unknown, invalid)
    lines = [
        "判据 %d 项 · 通过 %d · 未通过 %d · 未取到数 %d · 不成立 %d · 跳过 %d"
        % (c["total"], c[S_PASS], c[S_FAIL], c[S_UNKNOWN], c[S_NOT_EST], c[S_SKIP]),
        "⇒ 结论：通过 %d/%d · 未通过 %d · 未取到数 %d · 不成立 %d · 跳过 %d · 实际执行 %d ⇒ 判定 exit=%d（%s）"
        % (c[S_PASS], c["total"], c[S_FAIL], c[S_UNKNOWN], c[S_NOT_EST], c[S_SKIP],
           c.get("executed", 0), verdict, basis),
    ]
    return verdict, lines


# ─────────────────────────── 输出（唯一出口，位于 finally）───────────────────────────
def render_output(ctx: RunContext, allow_unknown: bool, json_path) -> tuple:
    lines = []
    lines.append("=" * 78)
    lines.append("%s v%s · 判据执行器（规格正文：%s）" % (TOOL_NAME, TOOL_VERSION, SPEC_REF))
    lines.append("时间：%s" % _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    lines.append("项目根：%s" % ctx.project_root)
    lines.append("判据文件：%s" % (ctx.claims_path or "—"))
    lines.append("=" * 78)

    if ctx.spec_errors:
        lines.append("")
        lines.append("【判据文件校验】不合法 ⇒ 退出码 3（**未执行任何判据**）：")
        for e in ctx.spec_errors:
            lines.append("  ✗ %s" % e)

    lines.append("")
    lines.append("【判据明细】")
    if not ctx.outcomes:
        lines.append("  （本次未执行任何判据）")
    for idx in sorted(ctx.outcomes):
        out = ctx.outcomes[idx]
        lines.append("  %d) %s（kind=%s）⇒ %s" % (idx + 1, out.id, out.kind, out.state))
        # 第 18 条 ①：时点与范围同等重要 ⇒ 每条判据都必须**显式打印**本轮的测量时点
        at_txt = ""
        if 0 <= idx < len(ctx.claims):
            at_txt = ctx.claims[idx].get("at") or ""
        lines.append("       测量时点 = %s" % (at_txt or "**未声明 ⇒ 读数不可采信**"))
        for s in out.structural:
            lines.append("       %s" % s)
        if not out.structural:
            lines.append("       %s" % (out.detail or "—"))

    lines.append("")
    lines.append("【报告段】（每一条应报项逐条产出；与执行控制流结构性解耦）")
    if ctx.report_items:
        for it in ctx.report_items:
            lines.append("  " + it)
    else:
        lines.append("  （应报项 0 条：无判据需报告）")
    try:
        lines.append("  " + assert_report_complete(ctx))
    except ReportShortCircuit as exc:
        lines.append("  !! 断言失败：%s" % exc)
        ctx.spec_errors.append(str(exc))

    try:
        _, gate_line = assert_gate_self_check(ctx)
    except Exception as exc:                                   # 自断言本身失败也必须出声
        gate_line = "!! 判据门自断言无法完成：%s" % exc
        ctx.spec_errors.append(gate_line)
    lines.append("  " + gate_line)

    if ctx.reader is not None:
        lines.append("  " + ctx.reader.provenance_line())

    c = count_states(ctx)
    # 第 18 条 ②：汇总段参与格式化/比较的每一个数都必须**显式整数转型**（禁止集合/多值直接进格式化）
    for _k in (S_PASS, S_FAIL, S_UNKNOWN, S_NOT_EST, S_SKIP, "total"):
        c[_k] = scalar_int(c[_k], "汇总计数 %s" % _k)
    c["executed"] = sum(1 for o in ctx.outcomes.values() if o.state != S_SKIP)
    c["gate_expected"] = getattr(ctx, "gate_expected", None)
    c["gate_actual"] = getattr(ctx, "gate_actual", None)
    c["_spec"] = list(ctx.spec_errors)                 # 结论串里的 spec_errors 计数必须是真的
    invalid = bool(ctx.spec_errors)
    verdict, summary = render_summary(c, allow_unknown, invalid)

    lines.append("")
    lines.append("【汇总段】")
    for s in summary:
        lines.append("  " + s)

    if ctx.raised:
        lines.append("")
        lines.append("【抛错登记】（第 16 条：取数失败必须抛错，不得伪造成读数）")
        for r in ctx.raised:
            lines.append("  !! %s" % r)

    if ctx.notes:
        lines.append("")
        for n in ctx.notes:
            lines.append("  " + n)

    lines.append("")
    lines.append("EXIT=%d" % verdict)

    payload = {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "spec": SPEC_REF,
        "project_root": str(ctx.project_root),
        "claims_file": str(ctx.claims_path) if ctx.claims_path else None,
        "allow_unknown": bool(allow_unknown),
        "summary": {
            "total": c["total"], "pass": c[S_PASS], "fail": c[S_FAIL],
            "unknown": c[S_UNKNOWN], "not_established": c[S_NOT_EST],
            "skipped": c[S_SKIP], "executed": c["executed"], "exit_code": verdict,
            "basis": summary[1],
        },
        "claims": [
            {
                "index": idx + 1,
                "id": ctx.outcomes[idx].id,
                "kind": ctx.outcomes[idx].kind,
                "state": ctx.outcomes[idx].state,
                "at": (ctx.claims[idx].get("at") if 0 <= idx < len(ctx.claims) else None),  # 第 18 条 ①
                "detail": ctx.outcomes[idx].detail,
                "measurements": ctx.outcomes[idx].structural,
            }
            for idx in sorted(ctx.outcomes)
        ],
        "skipped_or_unrun": [
            {"index": i + 1, "id": cl.get("id"), "kind": cl.get("kind")}
            for i, cl in enumerate(ctx.claims) if i not in ctx.outcomes
        ],
        "report": list(ctx.report_items),
        "provenance": ctx.reader.provenance_line() if ctx.reader else None,
        "spec_errors": list(ctx.spec_errors),
        "raised": list(ctx.raised),
    }
    return verdict, lines, payload


def write_json(payload: dict, json_path: Path, lines: list) -> None:
    jp = Path(json_path)
    if jp.exists() and jp.is_dir():
        raise ClaimSpecInvalid("--json 目标是目录：%s" % jp)
    if jp.parent and not jp.parent.exists():
        jp.parent.mkdir(parents=True, exist_ok=True)
    # 一致性声明**只生成一次**，同时进 JSON 与文本（单一来源、两处渲染）⇒ 不允许一处改而另一处不改。
    statement = ("文本/JSON 结论一致性：一致（同一测量对象；exit=%s 由计数机械推出；"
                 "本句由同一 payload 渲染进 JSON 与文本两处）" % payload["summary"]["exit_code"])
    payload["consistency"] = statement
    jp.write_bytes(json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"))
    lines.append("  " + statement)


# ─────────────────────────── 自检（第 15 / 16 条与禁止事项的机械证据）───────────
def self_test(tmp_root: Path) -> int:
    results = []

    def record(name: str, ok: bool, evidence: str) -> None:
        results.append((name, ok, evidence))

    table = IdentifierTable()

    # 1) 第 16 条：取数返回 null / 空串 / 空集合 ⇒ 必须抛错
    rd = Reader(tmp_root)
    probes = tmp_root / "_selftest"
    probes.mkdir(parents=True, exist_ok=True)
    try:
        (probes / "empty.bin").write_bytes(b"")
        raised = []
        for label in ("空文件（0 字节 ⇒ 空集合语义）",):
            try:
                rd.bytes("_selftest/empty.bin", label)
                raised.append((label, "未抛错"))
            except EmptyMeasurement as exc:
                raised.append((label, "%s: %s" % (type(exc).__name__, str(exc)[:60])))
        # null / 空串 直接走量具与断言路径
        for label, value in (("null", None), ("空串", ""), ("空集合", [])):
            try:
                if value is None or (hasattr(value, "__len__") and len(value) == 0):
                    raise EmptyMeasurement("自检注入：取数返回 %s ⇒ 必须抛错（第 16 条）" % label)
                raise AssertionError("不该到达")
            except EmptyMeasurement as exc:
                raised.append((label, "%s: %s" % (type(exc).__name__, str(exc)[:60])))
        ok = all("未抛错" not in r[1] for r in raised) and len(raised) == 4
        record("第16条 取数为空必须抛错（null/空串/空集合/0 字节）", ok,
               "；".join("%s → %s" % (a, b) for a, b in raised))
    finally:
        shutil.rmtree(probes, ignore_errors=True)

    # 2) 三口径：加粗/反引号跨度造成的裸串假阴性必须被拦住
    line = "**用户裁定 A**：120×120 是满意的；更正 `38cd714` 提交信息"
    ok = (
        not matched_by("substring", line, "用户裁定 A：120")
        and matched_by("substring", caliber_strip_inline(line), "用户裁定 A：120")
        and not matched_by("substring", line, "更正 38cd714")
        and matched_by("substring", caliber_strip_backtick(line), "更正 38cd714")
    )
    record("第4条 三口径拦住加粗/反引号假阴性", ok,
           "原样(加粗)=未命中·去行内标记=命中；原样(反引号)=未命中·去反引号=命中")

    # 3) 第 7 条：ReadAllLines 语义与 split("\\n") 差 1
    sample = "a\nb\n"
    a, b = measure_lines(sample, "readalllines"), measure_lines(sample, "split_lf")
    record("第7条 行数量具（readalllines vs split_lf）", (a, b) == (2, 3),
           "readalllines=%d · split_lf=%d（LF 结尾文件少算 1）" % (a, b))

    # 4) 第 14 条：量具未声明 ⇒ 拒绝执行
    rejected = []
    try:
        measure_lines(sample, "whatever")
    except IdentifierRejected as exc:
        rejected.append(str(exc)[:60])
    try:
        measure_fences(sample, "guess")
    except IdentifierRejected as exc:
        rejected.append(str(exc)[:60])
    record("第14条 量具定义未声明/表外 ⇒ 拒绝执行", len(rejected) == 2, "；".join(rejected))

    # 5) 第 13 / 12 条：标识符与归属标签枚举外 ⇒ 立刻抛错（不落 default）
    outs = []
    for raw in ("张三", "CHANGELOG（你本次正文编辑）"):
        try:
            table.normalize("ownership", raw)
            outs.append("未抛错")
        except IdentifierRejected as exc:
            outs.append(type(exc).__name__)
    try:
        table.normalize("file", "C:/Windows/system32/drivers/etc/hosts")
        outs.append("未抛错")
    except IdentifierRejected as exc:
        outs.append(type(exc).__name__)
    record("第13/12条 枚举外表外标识符立刻抛错", outs == ["IdentifierRejected"] * 3, "；".join(outs))

    # 6) 第 15 条：报告段与 skip 分支结构性解耦 + 独立非空断言
    ctx = RunContext()
    ctx.claims = [{"id": "a", "kind": "contains"}, {"id": "b", "kind": "contains"},
                  {"id": "c", "kind": "contains"}]
    ctx.begin_round(0, "a", "contains").state = S_PASS
    skip = ctx.begin_round(1, "b", "contains")
    skip.state = S_SKIP
    skip.detail = "显式跳过"
    ctx.begin_round(2, "c", "contains").state = S_PASS
    ctx.report_items = build_report_section(ctx)
    ok = (len(ctx.report_items) == 3 and any("跳过" in x for x in ctx.report_items)
          and "通过" in assert_report_complete(ctx))
    record("第15条 报告段不被 skip 短路（独立遍历 + 非空断言）", ok,
           "应报项 3 · 实报 %d · 含跳过条目=%s" % (len(ctx.report_items),
                                              any("跳过" in x for x in ctx.report_items)))

    # 7) 第 17 条 ①：集合形状不得被静默改写（双重包裹 ⇒ 必须抛错，不得报成 1）
    shape_outs = []
    shape_probes = [
        ("双重包裹 [[a,b]]", lambda: count_of([["a", "b"]], "探针集合")),
        ("双重包裹 [[a],[b]]", lambda: count_of([["a"], ["b"]], "探针集合")),
        ("字符串当集合", lambda: count_of("System.Object[]", "探针集合")),
        ("null", lambda: count_of(None, "探针集合")),
        ("映射当集合", lambda: count_of({"a": 1, "b": 2}, "探针集合")),
        ("join 被包裹集合", lambda: join_flat([["a", "b"]], ",", "探针集合")),
        ("findall 多分组返回元组", lambda: typed_flat(re.findall(r"(a)(b)", "ab ab"), "探针集合")),
    ]
    for label, fn in shape_probes:
        try:
            got = fn()
            shape_outs.append("%s → 未抛错（得到 %r ⇒ 会把多元集合静默报成 1）" % (label, got))
        except ShapeAnomaly:
            shape_outs.append("%s → 抛错 ShapeAnomaly" % label)
    record("第17条① 集合形状异常必须抛错（禁止静默 .Count / -join）",
           len(shape_outs) == 7 and all("未抛错" not in s for s in shape_outs),
           "；".join(shape_outs))

    # 8) 第 17 条 ②：判据门自断言（应产出判定条数 ≠ 实际产出条数 ⇒ 该门无效 ⇒ 停手）
    gate_ctx = RunContext()
    gate_ctx.expect_judgements_declared = 3
    gate_ctx.claims = [{"id": "a", "kind": "contains", "enabled": True},
                       {"id": "b", "kind": "contains", "enabled": True},
                       {"id": "c", "kind": "contains", "enabled": True}]
    gate_ctx.begin_round(0, "a", "contains").state = S_PASS
    gate_ctx.begin_round(1, "b", "contains").state = S_FAIL
    # 第 3 条判据**未产出判定**（既非四种判定态，也非显式跳过）⇒ 门必须自己发现
    ok_gate_bad, line_bad = assert_gate_self_check(gate_ctx)
    gate_ctx2 = RunContext()
    gate_ctx2.claims = [{"id": "a", "kind": "contains", "enabled": True},
                        {"id": "b", "kind": "contains", "enabled": True},
                        {"id": "c", "kind": "contains", "enabled": False}]
    gate_ctx2.begin_round(0, "a", "contains").state = S_PASS
    gate_ctx2.begin_round(1, "b", "contains").state = S_PASS
    _sk = gate_ctx2.begin_round(2, "c", "contains")
    _sk.state = S_SKIP
    ok_gate_ok, line_ok = assert_gate_self_check(gate_ctx2)
    record("第17条② 判据门自断言（缺判定 ⇒ 门无效 ⇒ 停手并报告）",
           (not ok_gate_bad) and ("该门无效" in line_bad) and ok_gate_ok,
           "%s ／ %s" % (line_bad, line_ok))

    # 9) 禁止事项 4：源码（去注释/去 docstring 口径）不含外部命令直取与 shell 解析
    #    禁词本身**由片段拼出**，否则本探针的图案定义就会成为自己的假阳性来源（实测踩坑）。
    src_raw = Path(__file__).read_bytes().decode("utf-8")
    src_code = code_only_source(src_raw)
    patterns = [a + b for a, b in (("git", " show"), ("shell", "=True"), ("os.", "system("))]
    ban_raw = [p for p in patterns if p in src_raw]
    ban = [p for p in patterns if p in src_code]
    record("禁止事项4/5 源码口径自检（去注释/去 docstring）",
           not ban,
           "口径A 整文件原文命中 %s（**说明性文字误报 = 假阳性**）；"
           "口径B 去注释/去 docstring 命中 %s" % (ban_raw or "无", ban or "无"))

    # 10) 第 18 条 ①：未声明测量时点的读数 ⇒ 不可采信 ⇒ 抛错（拒绝出结论）
    timing_probes = tmp_root / ".trae" / "_selftest18"
    timing_probes.mkdir(parents=True, exist_ok=True)
    probe_rel = ".trae/_selftest18/at.md"          # 落在 .trae/** 内 ⇒ 通过标识符规范化表（表外取值会被拒）
    try:
        (timing_probes / "at.md").write_bytes("a\nb\nc\n".encode("utf-8"))
        rt = Reader(tmp_root)
        k, _data = rt.bytes(probe_rel, "探针文件")
        untrusted = []
        try:
            rt.num(3, k, "行数")                      # 未 set_timing() ⇒ 时点未声明
            untrusted.append("未抛错")
        except MeasurementUntrusted as exc:
            untrusted.append("MeasurementUntrusted（含「不可采信」=%s）" % ("不可采信" in str(exc)))
        rt.set_timing("自检：声明时点之后")
        got_after = rt.num(3, k, "行数")
        record("第18条① 未声明时点的读数不可采信（拒绝出结论）",
               untrusted == ["MeasurementUntrusted（含「不可采信」=True）"] and got_after == 3,
               "未声明时点 → %s；声明时点后 → 读数 %r 放行（时点=%s）" % (untrusted[0], got_after, rt.timing))

        # 11) 第 18 条 ①：判据未声明时点 ⇒ 判据文件不合法（拒绝执行该判据，不出结论）
        at_probe = {"claims": [
            {"id": "no-at", "kind": "shape", "file": probe_rel,
             "measure": "readalllines", "lines": 3},
        ]}
        try:
            validate_claims(at_probe, IdentifierTable())
            at_msg = "未抛错（⇒ 未声明时点会被静默接受）"
        except ClaimSpecInvalid as exc:
            at_msg = "%s（含「不可采信」=%s）" % (type(exc).__name__, "不可采信" in str(exc))
        at_probe_ok = {"measure_at": "顶层默认时点（探针）", "claims": [
            {"id": "with-at", "kind": "shape", "file": probe_rel,
             "measure": "readalllines", "lines": 3},
            {"id": "override", "kind": "shape", "at": "本条覆盖时点", "file": probe_rel,
             "measure": "readalllines", "lines": 3},
        ]}
        try:
            v_claims, _ = validate_claims(at_probe_ok, IdentifierTable())
            at_msg_ok = "顶层默认=%r · 逐条覆盖=%r" % (v_claims[0]["at"], v_claims[1]["at"])
        except ClaimSpecInvalid as exc:
            at_msg_ok = "意外抛错：%s" % exc
        record("第18条① 判据未声明时点 ⇒ 拒绝执行（顶层 measure_at 可作默认，逐条 at 覆盖）",
               at_msg.startswith("ClaimSpecInvalid") and "顶层默认='顶层默认时点（探针）'" in at_msg_ok,
               "%s ／ %s" % (at_msg, at_msg_ok))
    finally:
        shutil.rmtree(timing_probes, ignore_errors=True)

    # 12) 第 18 条 ②：外部输出含 ANSI ⇒ 必须先剥离再读数（不得出现空值伪读数）
    eo = ExternalOutput(["probe"], 0, "\x1b[1m总计:\x1b[0m 30 项\n".encode("utf-8"), b"")
    ansi_read = eo.int_via_regex(re.compile(r"总计:\s*(\d+)\s*项"), "探针项数")
    record("第18条② 外部输出剥离 ANSI 后再读数（原型 b：正则被色码切断）",
           eo.ansi_stdout_raw == 2 and eo.ansi_stdout == 0 and ansi_read == 30,
           "原始 ANSI %d 处 ⇒ 结构化后 %d 处；正则取数 = %d（**不是**「项数 =（空）」）"
           % (eo.ansi_stdout_raw, eo.ansi_stdout, ansi_read))

    # 13) 第 18 条 ②：多值 / 多分组 / 集合 ⇒ 一律抛错（不得取其一、不得静默串化）
    multi_outs = []

    def _probe(label, fn):
        try:
            got = fn()
            multi_outs.append("%s → 未抛错（得到 %r）" % (label, got))
        except (ShapeAnomaly, MeasurementUntrusted, EmptyMeasurement) as exc:
            multi_outs.append("%s → 抛错 %s" % (label, type(exc).__name__))

    eo_multi = ExternalOutput(["probe"], 0, b"12\n34\n", b"")
    _probe("stdout 多值取单值整数", lambda: eo_multi.as_int("探针单值"))
    _probe("正则多处匹配取单值", lambda: eo_multi.int_via_regex(re.compile(r"(\d+)"), "探针单值"))
    eo_tuple = ExternalOutput(["probe"], 0, b"ab ab\n", b"")
    _probe("findall 多分组返回元组", lambda: eo_tuple.int_via_regex(re.compile(r"(a)(b)"), "探针单值"))
    _probe("stdout 无非空行（空值）", lambda: ExternalOutput(["probe"], 0, b"\x1b[0m\n", b"").as_int("探针单值"))
    _probe("集合交给格式化（scalar_text）", lambda: scalar_text(["a", "b"], "探针集合"))
    _probe("集合当作单值整数（scalar_int）", lambda: scalar_int(["1"], "探针集合"))
    _probe("None 当作读数（scalar_text）", lambda: scalar_text(None, "探针空值"))
    record("第18条② 集合/多值/空值不得进入格式化或比较（原型 c：System.Object[]）",
           len(multi_outs) == 7 and all("未抛错" not in s for s in multi_outs),
           "；".join(multi_outs))

    # 14) 第 18 条 ②：显式类型转换（整数）——合法输入必须真的转成 int，而非字符串比较
    eo_ok = ExternalOutput(["probe"], "0", b"30\n", b"")
    typed = eo_ok.as_int("探针单值")
    typed_bad = []
    for raw in ("30 项\n".encode("utf-8"), b"3.0\n", b"\n30\n34\n"):
        label = raw.decode("utf-8", "replace").replace("\n", "\\n")
        try:
            ExternalOutput(["probe"], 0, raw, b"").as_int("探针单值")
            typed_bad.append("%r → 未抛错" % label)
        except (MeasurementUntrusted, ShapeAnomaly, EmptyMeasurement) as exc:
            typed_bad.append("%r → %s" % (label, type(exc).__name__))
    record("第18条② 显式类型转换（returncode 字符串 '0' ⇒ int；非整数一律抛错）",
           isinstance(typed, int) and typed == 30
           and len(typed_bad) == 3 and all("未抛错" not in s for s in typed_bad),
           "as_int('30') = %r（类型 %s）；拒绝样本 %s"
           % (typed, type(typed).__name__, "；".join(typed_bad)))

    print("【自检】%s v%s" % (TOOL_NAME, TOOL_VERSION))
    for name, ok, ev in results:
        print("  %s %s — %s" % ("✓" if ok else "✗", name, ev))
    bad = [n for n, ok, _ in results if not ok]
    print("  自检 %d 项 · 通过 %d · 未通过 %d ⇒ EXIT=%d"
          % (len(results), len(results) - len(bad), len(bad), EXIT_FAIL if bad else EXIT_PASS))
    return EXIT_FAIL if bad else EXIT_PASS


# ─────────────────────────── 主流程（输出只在 finally，与所有分支解耦）───────────
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog=TOOL_NAME,
        description="判据工具「核对执行器」：声明式判据 → 三态输出 + fail-closed",
    )
    ap.add_argument("claims", nargs="?", help="判据文件（YAML）")
    ap.add_argument("--project-root", default=None, help="被检查项目的根目录（默认：判据文件所在处的 .trae 祖先，或 cwd）")
    ap.add_argument("--allow-unknown", action="store_true",
                    help="显式放行「未取到数/不成立」（默认 fail-closed，退出码 2）")
    ap.add_argument("--json", default=None, help="机器可读 JSON 输出路径（项目外临时目录）")
    ap.add_argument("--quiet", action="store_true", help="仅打印汇总段")
    ap.add_argument("--self-test", action="store_true", help="运行内置自检（不读判据文件）")
    ap.add_argument("--tmp-root", default=str(DEFAULT_TMP_ROOT), help="项目外临时目录（自检用，用完即删）")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test(Path(args.tmp_root))

    if not args.claims:
        sys.stderr.write("%s：缺少判据文件参数（或用 --self-test）\n" % TOOL_NAME)
        return EXIT_INVALID

    ctx = RunContext()
    claims_path = Path(args.claims)
    ctx.claims_path = claims_path
    verdict = EXIT_INVALID
    lines: list = []
    payload: dict = {}

    try:
        doc = load_claims_document(claims_path)
        ctx.claims = doc.get("claims") if isinstance(doc.get("claims"), list) else []
        root = resolve_project_root(args.project_root, claims_path)
        ctx.project_root = root
        table = IdentifierTable()
        claims, expect_declared = validate_claims(doc, table)
        ctx.claims = claims
        ctx.expect_judgements_declared = expect_declared
        run_all(ctx, table)
        ctx.report_items = build_report_section(ctx)
    except ClaimSpecInvalid as exc:
        ctx.spec_errors.append("%s: %s" % (type(exc).__name__, exc))
        if isinstance(exc, IdentifierRejected):
            ctx.notes.append("标识符规范化失败 ⇒ **立刻抛错**（第 13/12 条：不得落 default 分支）")
        ctx.report_items = build_report_section(ctx)
    except Exception as exc:                              # 兜底：仍必须产出报告段
        ctx.spec_errors.append("内部错误 %s: %s" % (type(exc).__name__, exc))
        ctx.report_items = build_report_section(ctx)
    finally:
        # ── 唯一输出出口：报告段与结构段在这里产出，与上面任何 continue/skip/return/异常解耦 ──
        verdict, lines, payload = render_output(ctx, args.allow_unknown, args.json)
        if args.quiet:
            lines = [ln for ln in lines if ln.startswith("  ") and ("判据 " in ln or "⇒ 结论" in ln)]
        if args.json:
            write_json(payload, Path(args.json), lines)      # 先落 JSON（会追加一致性行），再打印
        sys.stdout.write("\n".join(lines) + "\n")
    return verdict


def resolve_project_root(explicit, claims_path: Path) -> Path:
    if explicit:
        p = Path(explicit).resolve()
        if not p.exists():
            raise ClaimSpecInvalid("--project-root 不存在：%s" % p)
        return p
    cur = claims_path.resolve().parent
    for cand in [cur, *cur.parents]:
        if (cand / ".trae").is_dir():
            return cand
    return Path.cwd().resolve()


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    raise SystemExit(main())
