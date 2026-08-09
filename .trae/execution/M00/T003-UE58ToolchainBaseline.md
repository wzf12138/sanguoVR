# M00-T003 UE5.8 工程与工具链基线

- 状态：已批准
- 优先级：P0
- 目标：证明工程可生成、编译、启动并形成可重复环境记录。

## 步骤

1. 核对 UE5.8 安装、UBT、Visual Studio/MSVC、Windows SDK 与 Android SDK/NDK/JDK；Git 已由 M00-T002 安装启用，本任务不含 Git 操作。
2. 读取 `.uproject`，确认模块、插件与目标平台。
3. 生成项目文件。
4. 清理编译 `VRSanguoYanWuchangEditor Win64 Development`。
5. 启动编辑器，检查缺失模块、插件、重定向和资源错误。
6. 将版本、路径策略、命令和结果写入 `knowledge/EnvironmentSetup.md` 与验证登记册。

## 验收

- Editor 目标成功编译并启动。
- 不依赖未记录的用户级手工修改。
- Android 工具链能被 UE 识别；若失败，保留完整错误与阻塞项。
