# M00-T004 VR/OpenXR/PICO 基线

- 任务编号：M00-T004
- 状态：blocked（2026-08-10 更新：V-005 PICO Neo3 真机验证失败，设备不兼容，待用户决策换设备或降级引擎）
- 负责人：执行模型 + 用户（分工见下）
- 里程碑：M00
- 优先级：P0
- 预估耗时：SDK 下载 15 分钟 + UE 配置 5 分钟 + PICO 验证 15 分钟

---

## 这个任务在完整游戏开发中的位置

```
已完成：
  T001 治理基线 ✅ → 项目怎么管，定了
  T002 Git 基线 ✅   → 代码怎么存，定了
  T003 编译基线 ✅   → 代码能编译、编辑器能跑、MCP 通了

本任务 T004：
  让游戏第一次在你的 PICO Neo3 上跑起来
  ── 这是"游戏能上真机"的第 0 步证明，不是优化、不是调手感

之后：
  T005 系统骨架 → 搭 C++ 战斗/武器/移动模块
  T006 自动化门禁 → 测试框架
  M01 1v1 战斗切片 → 开始做真正的战斗玩法
```

---

## Phase 1：安装 Android SDK（用户操作，~15 分钟）

### 为什么需要这一步
UE5.8 编译 Android/ARM64 程序需要 Android SDK（基础库）、NDK（C++ 编译器）和 build-tools。你的 SDK 是 UE4 时期的旧版本（platforms 只到 33、NDK 21.4），必须升级。

### 当前状态
- SDK 目录：`D:\AWork\Android_SDK\SDK` ✅ 已存在
- sdkmanager：可用 ✅
- JDK：OpenJDK 21.0.10 ✅ UE5.8 官方要求就是 JDK 21

### 需要安装的

| 组件 | 当前 | 需要 | 用途 |
|------|------|------|------|
| SDK 平台 | 最高 android-33 | android-34（最低）+ android-35（推荐） | 编译目标 API |
| NDK | 21.4.7075529（UE4 时代） | r27c（27.2.12479018） | C++ 交叉编译到 ARM64 |
| Build-tools | 待查 | 35.0.1 | APK 打包工具链 |

### 操作（你在终端执行）

```powershell
# 一条命令安装全部
$env:ANDROID_HOME = "D:\AWork\Android_SDK\SDK"
& "D:\AWork\Android_SDK\SDK\cmdline-tools\latest\bin\sdkmanager.bat" "platforms;android-34" "platforms;android-35" "build-tools;35.0.1" "ndk;27.2.12479018"
```

### 如何确认成功
下载完成后，检查以下目录存在：
```
D:\AWork\Android_SDK\SDK\platforms\android-35\
D:\AWork\Android_SDK\SDK\ndk\27.2.12479018\
D:\AWork\Android_SDK\SDK\build-tools\35.0.1\
```

---

## Phase 2：在 UE 编辑器中配置 Android 路径（用户操作，~5 分钟）

### 为什么需要这一步
UE 编辑器需要知道 SDK/NDK/JDK 在硬盘上的位置，才能调用它们编译 APK。这一步是把 Phase 1 装好的工具链"注册"到 UE。

### 操作（你在 UE 编辑器中执行）

1. 打开 UE5.8 编辑器，加载 `VRSanguoYanWuchang` 项目
2. 菜单：**Edit → Project Settings → Platforms → Android**
3. 配置以下路径：

| 设置项 | 填入的值 |
|--------|---------|
| Android SDK Location | `D:\AWork\Android_SDK\SDK` |
| Android NDK Location | `D:\AWork\Android_SDK\SDK\ndk\27.2.12479018` |
| Java JDK Location | 留空（UE 会自动探测 PATH 上的 JDK 21） |

4. 点击 **"Accept SDK License"** 按钮（接受 Android SDK 许可协议）
5. 点击 **"Configure Now"** 按钮，UE 会验证路径并下载缺失项

### 如何确认成功
- Configure Now 后无红色报错
- 下面状态栏显示 SDK/NDK 版本号（不是 "Not Found"）

---

## Phase 3：AI 核验（执行模型在新会话中执行）

### 3.1 核验 SDK 安装
执行模型通过终端检查：
```powershell
# 检查各组件是否存在
Test-Path "D:\AWork\Android_SDK\SDK\platforms\android-35"
Test-Path "D:\AWork\Android_SDK\SDK\ndk\27.2.12479018"
Test-Path "D:\AWork\Android_SDK\SDK\build-tools\35.0.1"
```

### 3.2 核验 VR 模板资产完整性
通过 MCP 或文件读取确认 `Content/` 下存在以下 VR 模板核心资产，没有因为之前操作被误删：
- VRPawn（玩家 VR 角色蓝图）
- 手部 SkeletalMesh（Left Hand / Right Hand）
- 抓取组件
- 瞬移组件
- Enhanced Input Actions / Mapping Context

### 3.3 核验插件加载状态
通过 MCP `GetLogEntries` 检查 `LogLoad` 分类，确认以下插件无加载错误：
- OpenXR
- OpenXREyeTracker
- OpenXRHandTracking
- PICOController

### 结果记录
将 3.1-3.3 结果写入验证登记册 V-004（编辑器 VR 验证）。

---

## Phase 4：开启 PICO Neo3 开发者模式（用户操作，~2 分钟）

### 为什么需要
PICO Neo3 出厂默认不允许 adb 调试和安装非商店应用。必须开启开发者模式才能部署你自己的游戏。

### 操作

1. PICO 开机，进入 **设置 → 通用 → 关于**
2. 连续点击 **"软件版本号"** 7 次，直到提示"已进入开发者模式"
3. 返回 **设置 → 通用 → 开发者选项**
4. 开启 **"USB 调试"**

### 如何确认
用 USB 线连接 PICO 到电脑，PICO 头显内会弹出"是否允许 USB 调试"对话框，勾选"始终允许"，点确定。

然后运行：
```powershell
& "D:\AWork\Android_SDK\SDK\platform-tools\adb.exe" devices
```
应显示类似 `A8X0119523000639  device`（具体 ID 不同）。

---

## Phase 5：方式 A — Launch on Device（快速验证，用户操作，~10 分钟）

### 这是什么
UE 编辑器通过 adb 直接把整个项目部署到 USB 连接的 PICO 上运行。不生成独立 APK。

### 为什么先做这个
这是最快确认"游戏能在 PICO 上渲染 VR 画面"的方法。如果这步失败（黑屏/崩溃），说明插件或配置有问题，排查后再去打 APK。如果这步成功，再打独立 APK 做离线验证。

### 操作

1. 确保 PICO 通过 USB 连接，`adb devices` 能识别
2. PICO 头显戴上，保持唤醒状态
3. UE 编辑器：**File → Package Project → Android → 选择你的 PICO 设备**
4. 编辑器底部会显示进度：Cooking → Packaging → Deploying → Launching
5. 等待 PICO 头显内画面出现

### 验收清单（你在 PICO 上检查）

| 检查项 | 预期结果 | ✅/❌ |
|--------|---------|-------|
| 画面是否正常渲染 | 能看见 VR 双屏画面（非黑屏） | |
| 头显追踪 | 转头时画面跟随，不卡顿不漂移 | |
| 手柄是否显示 | 能看到 VR 模板的控制器模型 | |
| 手柄追踪 | 挥手时手柄位置跟随 | |
| 是否有崩溃/闪退 | 持续 30 秒以上不闪退 | |

---

## Phase 6：方式 B — Standalone APK（离线验证，用户操作，~15 分钟）

### 这是什么
把项目打包成一个独立的 .apk 文件，通过 adb 安装到 PICO。安装后可以断开 USB，像正式游戏一样从 PICO 应用列表冷启动。

### 为什么要做
一期产品是**买断制、离线可运行**的单机游戏。Standalone APK 才是最终产品形态。必须验证：
- 断网后能不能冷启动
- 不依赖编辑器能不能独立运行

### 操作

```powershell
# 设置环境
$env:ANDROID_HOME = "D:\AWork\Android_SDK\SDK"

# 构建 APK（首次约 10-20 分钟）
& "D:\AWork\Unreal\App\UE_5.8\Engine\Build\BatchFiles\RunUAT.bat" BuildCookRun -project="D:\AWork\Unreal\Project\VRSanguoYanWuchang\VRSanguoYanWuchang.uproject" -platform=Android -configuration=Development -build -cook -stage -pak -archive

# 成功后 APK 在项目根目录下的 Saved\StagedBuilds\Android\ 中
# 安装到 PICO
& "D:\AWork\Android_SDK\SDK\platform-tools\adb.exe" install -r "D:\AWork\Unreal\Project\VRSanguoYanWuchang\Saved\StagedBuilds\Android\VRSanguoYanWuchang.apk"
```

### 验收清单（你在 PICO 上检查）

| 检查项 | 预期结果 | ✅/❌ |
|--------|---------|-------|
| 断开 USB 后能否启动 | PICO 应用列表里能找到游戏图标，点击启动 | |
| 断网冷启动 | 关闭 Wi-Fi + 断开 USB，从 PICO 应用列表启动 | |
| 6DoF 头显追踪 | 蹲下、侧身、前后走，画面正确响应 | |
| 双控制器识别 | 左右手柄都能看到，挥手有反应 | |
| 基础帧率 | 转头不感觉明显卡顿 | |
| 退出 | 能从游戏内正常退出回到 PICO 主界面 | |
| 重新启动 | 退出后再启动不崩溃 | |

---

## Phase 7：AI 记录结果（执行模型执行）

### 验证登记册更新
| 验证 ID | 内容 | 证据 |
|---------|------|------|
| V-004 | 编辑器 VR 验证（插件加载、资产完整） | Phase 3 的 MCP/文件检查结果 |
| V-005 | PICO 真机验证（方式 A + 方式 B） | Phase 5 和 Phase 6 的验收清单结果 |

### 文档同步
- `PicoNeo3BuildGuide.md`：更新验证项目矩阵（14 项中已通过哪些）
- `EnvironmentSetup.md`：记录实际 Android SDK/NDK 版本号
- `TechnicalDecisions.md`：如有 JDK/build 兼容性问题，追加记录
- `CHANGELOG.md`：记录 T004 完成情况

### 真机数据采集（用户口述，AI 记录）
- PICO 设备 ID：`adb devices` 输出
- PICO 系统版本：设置 → 关于中查看
- 方式 A 部署耗时：从点"Launch"到画面出现
- 方式 B APK 大小：构建输出目录中 .apk 文件大小
- 验收清单中任何 ❌ 项的详细描述

---

## 完成定义（全部满足才算任务完成）

- [ ] Phase 1: Android SDK 含 android-35 + NDK r27c + build-tools 35.0.1
- [ ] Phase 2: UE Project Settings 中 Android 路径配置正确、Accept License 完成
- [ ] Phase 3: AI 核验通过（SDK 路径 + VR 资产 + 插件加载）
- [ ] Phase 4: PICO 开发者模式已开启，`adb devices` 可识别
- [ ] Phase 5: Launch on Device 成功，PICO 上能看 VR 画面
- [ ] Phase 6: Standalone APK 构建成功、安装成功、断网冷启动正常
- [ ] Phase 6: 验收清单中 6DoF 追踪 + 双控制器识别通过
- [ ] Phase 7: V-004、V-005 登记完成
- [ ] Phase 7: 三份知识文档（PicoNeo3BuildGuide / EnvironmentSetup / TechnicalDecisions）已更新
- [ ] `STATUS.json` 更新为 `awaiting_review`

## 报告路径
`.trae/execution/reports/tasks/M00-T004.md`
