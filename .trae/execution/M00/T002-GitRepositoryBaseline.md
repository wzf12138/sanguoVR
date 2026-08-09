# M00-T002 Git 与仓库基线

- 状态：规范文件已建档；Git 未安装、未执行
- 优先级：P0
- 目标：建立适用于 UE5.8 与大二进制资产的版本控制边界。
- 当前约束：本轮不得安装 Git、不得执行任何 Git 或 Git LFS 命令。

## 交付

- `.gitignore`：排除 UE、IDE、平台生成物和本机敏感配置。
- `.gitattributes`：文本归一化与 UE/媒体资产 Git LFS 规则。
- `.editorconfig`：编码、换行和基础格式。
- `.lfsconfig`：允许锁定验证。
- `.trae/standards/GitStandard.md`。

## 后续执行（本轮禁止）

以下步骤仅保留为未来获批后的计划，本轮不执行：确认 Git/Git LFS、初始化仓库、安装本地 LFS、检查属性匹配及提交前复查。

## 验收

当前仅验证规范文件可读取；Git 状态、LFS 命中和仓库初始化均未执行、未验证。
