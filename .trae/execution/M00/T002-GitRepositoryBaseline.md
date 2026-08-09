# M00-T002 Git 与仓库基线

- 状态：已实施（Git for Windows + Git LFS 已安装，仓库已初始化并推送远程，2026-08-09 用户确认）
- 优先级：P0
- 目标：建立适用于 UE5.8 与大二进制资产的版本控制边界。

## 交付

- `.gitignore`：排除 UE、IDE、平台生成物和本机敏感配置。
- `.gitattributes`：文本归一化与 UE/媒体资产 Git LFS 规则。
- `.editorconfig`：编码、换行和基础格式。
- `.lfsconfig`：允许锁定验证。
- `.trae/standards/10-git-standard.md`。

## 实施记录（2026-08-09）

- Git for Windows 与 Git LFS 已安装（用户执行）。
- 仓库已初始化，`master` 分支已推送远程 `origin`（用户确认）。
- `.gitignore`、`.gitattributes`、`.editorconfig`、`.lfsconfig` 已落盘并被 git 跟踪。

## 验收

- Git 安装、仓库初始化与远程推送已完成（用户确认）。
- LFS 跟踪规则与文本归一化以真实 `.gitattributes` 为准，命中率待后续提交复核。
