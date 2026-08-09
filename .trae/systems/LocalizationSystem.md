# LocalizationSystem

## 职责

管理文化设置、文本资源、术语、字体、字幕、语言切换和本地化资源状态。

## 边界

- 遵循 `LocalizationStandard`；业务系统传递稳定文本 Key、参数或内容 ID，不传递已拼接显示字符串。
- UISystem 负责布局刷新，AudioSystem 负责语音播放；LocalizationSystem 解析对应语言内容。
- 玩家语言偏好交给 SaveSystem 持久化。

## 运行规则

- 启动时按用户设置、平台语言和项目默认值依次选择文化。
- 语言切换发布统一事件，所有缓存 FText 的界面与字幕订阅刷新。
- 缺失翻译在开发构建中记录 Key、命名空间和调用上下文；Shipping 使用源语言回退。
- 字体回退链按语言配置并受内存预算约束。

## 验收

- `zh-Hans` 与 `en` 的 Gather、Compile、Cook 和真机显示通过。
- 无硬编码玩家可见字符串、缺字方框、格式参数错误或切换后混合语言。
