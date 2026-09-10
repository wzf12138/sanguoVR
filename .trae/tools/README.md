# 项目工具脚本（`.trae/tools/`）

> 本目录是**项目工具脚本**的授权落点。规则依据：`AGENTS.md` §文件边界「项目工具脚本：仅 `.trae/tools/`」（2026-09-10 修订）；变更依据：`execution/CR-20260910-001-project-tooling-home.md`。

## 与「临时脚本」的区分

`AGENTS.md` 仍禁止临时脚本进入项目。本次修订只把**长期复用的工具脚本**从禁令中单列出来，判据如下：

| | 允许入库 | 落点 | 判据 |
|---|---|---|---|
| **项目工具脚本** | ✅ | `.trae/tools/<域>/` | 会被**重复使用**；产出物属于项目（关卡 / 文档 / 证据）；且是某产物的**单一事实源** |
| **一次性临时脚本** | ❌ | 项目外临时目录，用完即删 | 为一次排障、一次迁移临时写的；事后无复用价值 |

被单列出来，是因为这类脚本**是项目资产的一部分**：丢了它，对应产物就无法复现。此前它们无授权落点，只能留在项目外，**因而从未进入任何备份**——这是本次修订要修的实际风险，不是形式问题。

## scene/ — 竞技场关卡生成

`Content/VRSanguo/Dev/L_Prototype_1v1_v5.umap` 及 `Docs/Scene/` 四件套的**单一事实源**。任何改动 = 改脚本参数重跑，禁止在编辑器里手补单件。

| 脚本 | 字节 | SHA256[:16] | mtime | 作用 |
|---|---|---|---|---|
| `rebuild_v5.py` | 50,614 | `D3F562935DC9A841` | 2026-09-10 19:14:34 | **现行单源**：v5 校场全要素生成；`MODULES` 登记表自动产出 `Docs/Scene/` 四件套 |
| `rebuild_v4.py` | 18,018 | `59D7A6FB45BC3A85` | 2026-09-10 14:53:40 | v4（120m 场地口径）历史版本，供回溯 |
| `rebuild_v3.py` | 15,027 | `23187469D0872087` | 2026-09-09 23:37:54 | v3（70m 场地口径）历史版本，供回溯 |
| `flip_topdown.ps1` | 935 | `FC68C2D0C0887EA4` | 2026-09-10 17:52:41 | `rebuild_v5.py` 俯视图后处理（去 SceneCapture 水平镜像） |

**运行前提**（v5）：编辑器已切到空关卡 `/Game/VRSanguo/Dev/L_Prototype_1v1_v5` 后执行本脚本。

**脚本内的项目外路径**（有意为之，符合磁盘与临时文件规则，非缺陷）：

- `TMP_DIR = D:\AWork\TraeAdmin\VRSanguoYanWuchang\tmp` —— 俯拍 raw 中间产物，不入项目。
- `DOCS_DIR = D:\AWork\Unreal\Project\VRSanguoYanWuchang\Docs\Scene` —— 文档产物落点。

四个脚本均**不依赖自身所在目录**（无 `__file__`、无相对路径解析），因此入库不改行为。

## 不在此目录的脚本

- **NTFS 权限脚本**（`Set-TraeGovernanceAcl.ps1`、`Unlock-TraeAssets.ps1`、`Unlock-GripPolish.ps1`）：按 `AGENTS.md` 文件边界留在项目外 `D:/AWork/TraeAdmin/VRSanguoYanWuchang/`，**不搬入**。
- **一次性排障脚本**（`repair_status_json5.js`、`verify2.js`、`verify3.js`）：2026-09-10 根 STATUS.json 事故用的一次性工具，不属项目工具脚本。

## 新增脚本的准入

1. 先判断它属于上表哪一类；判"一次性"的不得入库。
2. 入 `.trae/tools/<域>/`，并在本文件登记：字节、SHA256[:16]、mtime、作用、运行前提。
3. 脚本内的项目外路径必须在本文件说明，并注明"有意为之"。
4. 涉及产物的脚本，须在脚本头部注释里写明"单一事实源"与运行前提。
