# Git 标准

## 当前状态

Git for Windows 与 Git LFS 已安装，仓库已初始化并推送远程（2026-08-09 用户确认，详见 `../registers/09-verification-register.md` V-002 与 `../knowledge/EnvironmentSetup.md`）。实际主分支为 `master`，与远程 `origin/master` 同步。

## 分支与提交

- 主分支建议 `main`，功能分支格式 `type/MNN-TNNN-short-name`。
- 提交格式：`type(scope): summary [MNN-TNNN]`，类型包括 `feat`、`fix`、`docs`、`refactor`、`test`、`build`、`chore`。
- 提交原子化并关联任务编号；每个可回滚单元独立提交，混合格式化和功能变更应拆分。

## 提交前检查

- 无生成目录、无密钥、无本机配置。
- 文本规则文件可读，任务和登记册已同步。
- 合并前通过完整性检查并附任务报告。

## 禁止提交

- `.uasset`、`.umap` 使用 Git LFS；大型二进制禁止直接进入普通 Git 对象库。
- 禁止强推共享主分支。
- 禁止提交 `Binaries/`、`Intermediate/`、`Saved/`、`DerivedDataCache/`、缓存与派生数据。
