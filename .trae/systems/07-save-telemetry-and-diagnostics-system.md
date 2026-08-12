# 保存、遥测与诊断系统工程实现指引

设置、进度、统计与持久化范围以 [`../knowledge/Design/GameModesAndProgression.md`](../knowledge/Design/GameModesAndProgression.md) 为权威产品详规。本文件只描述本地保存、事件采集和诊断的工程边界。

## 工程职责

- 提供版本化保存结构、迁移入口和安全默认值。
- 从规则事件汇总单局统计与验证所需诊断数据。
- 统一日志分类、上下文标识、节流和构建配置。
- 管理开发调试面板与匿名导出，不阻塞核心流程。

## 实现边界

UI 文本不是统计事实源；保存与遥测不反向驱动战斗规则。采集字段遵循最小化原则，敏感或现实空间数据必须有明确批准。开发诊断与 Shipping 输出通过构建配置隔离。

## 日志分类与最小诊断能力

日志分类统一使用以下类别：`LogVRSanguoCore`、`LogVRSanguoVR`、`LogVRSanguoCombat`、`LogVRSanguoWeapon`、`LogVRSanguoMovement`、`LogVRSanguoAI`、`LogVRSanguoFlow`、`LogVRSanguoPerf`。

最小诊断能力：

- 显示追踪状态、输入动作、抓取对象和移动模式。
- 绘制武器连续轨迹、命中点、格挡结果与去重窗口。
- 显示角色生命、护甲、硬直、目标、AI 决策与小队角色。
- 采样 Game/Render/GPU 帧时间、Draw Call、三角形、内存和活跃 Actor。
- 一键重置玩家、武器、AI、比赛流程和测试场景。

调试功能必须由开发配置或控制台开关控制，发布构建默认关闭。

## 接口契约（规划级）

以下为 M00 规划阶段的接口契约框架，具体签名在 M00-T005 C++ 骨架中实现并以此为准。

**保存服务**：
- `SaveGame(const FSaveData& Data)` → `FSaveResult`
- `LoadGame(int32 SlotIndex)` → `FSaveResult`
- `GetSaveVersion()` → `int32`

**遥测服务**：
- `RecordEvent(const FTelemetryEvent& Event)`
- `GetMatchStatistics()` → `FMatchStatistics`

**诊断服务**：
- `Log(ELogCategory Category, ELogVerbosity Verbosity, const FString& Message, const FLogContext& Context)`
- `StartDebugSession()` / `EndDebugSession()`
- `DrawDebugOverlay(EDebugOverlayFlags Flags)`

**数据结构**：
- `FSaveData`：`int32 Version; FMatchProgress Progress; TMap<FString, FString> Settings; TArray<FAchievementRecord> Achievements;`
- `FSaveResult`：`bool bSuccess; ESaveFailReason FailReason; int32 MigratedVersion;`
- `FTelemetryEvent`：`FName EventType; int32 MatchId; float Timestamp; FString ContextJson;`
- `FLogContext`：`int32 MatchId; int32 AttackId; AActor* Source; AActor* Target;`

**依赖接口**：
- GameModeFlow: 接收 `OnMatchEnded` 事件触发保存
- Combat: 接收 `OnHitDealt`, `OnHitBlocked` 事件采集遥测
- 所有系统: 接收日志写入请求

## 接口与验证

保存接口返回版本、迁移和失败结果；日志与事件包含战局、攻击或对象上下文。验证覆盖字段缺失、版本升级、损坏恢复、写入失败、日志节流、导出失败和构建裁剪；保存范围与字段定义从权威详规读取。
