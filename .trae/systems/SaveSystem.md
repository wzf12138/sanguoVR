# SaveSystem

## 职责

提供槽位枚举、快照采集、异步写入、读取、版本迁移、备份恢复、自动存档和设置持久化。

## 边界

- 遵循 `SaveSystemStandard`；SaveSystem 编排数据，不拥有各玩法域的业务真值。
- 各系统通过稳定 Save Fragment 接口导出和恢复数据，禁止 SaveSystem 遍历任意 Actor 猜测状态。
- UI 只提交保存/读取请求并显示状态，不直接访问文件。

## 状态机

`Idle -> Capturing -> Writing -> Verifying -> Completed/Failed`；读取使用 `Reading -> Migrating -> Applying`。同一槽位写操作串行，多余自动存档请求合并。

## 失败处理

- 写入失败保留原文件和错误码；验证失败尝试读取备份但不自动覆盖源文件。
- 应用存档前完成兼容校验；部分系统恢复失败时中止进入世界并报告失败域。
- Android 生命周期触发的紧急存档只保存允许的最小快照。

## 验收

- 往返、损坏、旧版本、磁盘不足、强退和并发请求测试通过。
- 游戏线程无同步大文件 IO，失败日志不包含敏感数据。
