# Git 标准

## 当前状态

Git for Windows 与 Git LFS 已安装，仓库已初始化并推送远程（2026-08-09 用户确认，详见 `../registers/09-verification-register.md` V-002 与 `../knowledge/EnvironmentSetup.md`）。实际主分支为 `master`，与远程 `origin/master` 同步。

## 分支与提交

- 主分支为 `master`（与远程 `origin/master` 同步；不创建 `main`），功能分支格式 `type/MNN-TNNN-short-name`。
- 提交格式：`type(scope): summary [MNN-TNNN]`，类型包括 `feat`、`fix`、`docs`、`refactor`、`test`、`build`、`chore`。
- 提交原子化并关联任务编号；每个可回滚单元独立提交，混合格式化和功能变更应拆分。

## 提交前检查

- 无生成目录、无密钥、无本机配置。
- 文本规则文件可读，任务和登记册已同步。
- 合并前通过完整性检查并附任务报告。

## 禁止提交

- `.uasset`、`.umap` 使用 Git LFS；大型二进制禁止直接进入普通 Git 对象库。
- **「大型」的可判定阈值（2026-09-11 固化）**：同一事实曾因无阈值而出现两种口径，故明确如下——受索引**非 LFS** 文件：**> 5 MB = 违规**（必须 LFS；当前实测 **0 个**）；**1–5 MB = 预警区间**，须在资产登记册登记并写明保留理由（当前实测 **18 个**，全部为 `Content/VRSanguo/Art/References/` 下武器参考图 PNG，1.06–4.59 MB、合计约 43 MB，`git cat-file -s` 证实为真实二进制，最大者 `REF_Weapon_Shield_02.png` blob = 4,590,192 B）。
- **已备案例外（用户 2026-09-10 明示裁定）**：`Content/VRSanguo/Art/References/` 参考图**留在仓库不动**，作为磁盘规则的一处已知例外。故上述 18 个预警区间对象为**已备案例外，不是待修违规**；登记为 `deferred`，**不得**为此改写历史或强制推送。
- **禁止为修复 LFS 覆盖而改写历史**：新增 `.gitattributes` 规则**不回溯**已入库对象；把既有对象迁入 LFS 需 `git lfs migrate` + 强制推送，与本标准「禁止改写已推送历史」及项目红线冲突——须另立任务并由用户单独放行。
- 禁止强推共享主分支。
- 禁止提交 `Binaries/`、`Intermediate/`、`Saved/`、`DerivedDataCache/`、缓存与派生数据。
