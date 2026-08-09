# M00-T004 检查

## 始终禁止
- 修改治理锁定文件、Skill、总纲或 Design 产品详规
- 修改白名单外文件
- 创建第二 Skill 或平行知识库
- 执行 Git 命令
- 把未执行的真机验证写成通过
- 修改 `VRSanguoYanWuchang.uproject` 或 `Source/`、`Content/`、`Config/`、`Plugins/` 文件
- 用配置存在替代运行验证，用 PC VR 替代 PICO Neo3 结论

## 执行前
- 结构完整性复核已通过，用户已确认解除冻结；执行模型可按 `TASK.md` 继续任务。
- 执行前仍须确认 Android SDK 组件、UE Android 配置和 PICO 设备条件，不得跳过环境检查。
- 若发现新的路径冲突、权限问题或证据不足，立即停止并将状态改为 `blocked`。

## 执行后
- Phase 3 核验结果写入 V-004
- Phase 5+6 真机结果写入 V-005
- 三份知识文档已同步（PicoNeo3BuildGuide / EnvironmentSetup / TechnicalDecisions）
- 任务报告写入 `.trae/execution/reports/tasks/M00-T004.md`
- `STATUS.json` 更新为 `awaiting_review` 或 `blocked`

## 阻塞处理
- SDK 下载失败：记录 sdkmanager 错误，提示用户检查网络
- UE Configure Now 报错：记录错误截图，检查路径拼写
- `adb devices` 无设备：检查 USB 线/开发者模式/USB 调试授权
- 构建失败：记录完整 UAT 输出
- 部署后黑屏：记录设备型号、系统版本，检查插件加载日志
