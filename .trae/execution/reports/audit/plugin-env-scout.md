# 插件与环境侧排查报告（plugin-scout）

- 报告路径：`.trae/execution/reports/audit/plugin-env-scout.md`
- 作者身份：团队成员 `plugin-scout`（插件与环境侧排查）
- 生成时间：2026-09-12 22:0x（本地 +08:00）
- 任务来源：队长下发的 execution prompt（工作目录 `D:\AWork\Unreal\Project\VRSanguoYanWuchang`）
- 性质：**全程只读**。唯一写入 = 本文件。未删除/移动任何项目文件；未跑任何 git 写操作；未跑 `rebuild_v5.py`；未改写 `Docs/`、`Scene/`；未安装/卸载任何软件；未下载任何内容；未创建任何临时文件。
- 进程纪律：**未关闭、未重启、未 kill 任何 UnrealEditor 进程**。

---

## 0. 结论摘要（TL;DR）

| 编号 | 结论 | 证据强度 |
|------|------|----------|
| **C1** | **项目内不存在名为 `PicoStreamingXR` 的 UE 插件。** 它是 **PICO PC 端串流软件随附的 OpenXR 运行时 DLL**（`ProductName = PicoStreamingXR`），由操作系统 `HKLM\SOFTWARE\Khronos\OpenXR\1\ActiveRuntime` 注册，以 `openxr_loader.dll` 动态加载方式进入进程。**"PicoStreamingXR 插件 v1.1.46" 这个提法在事实层面应更正为"PICO 串流 OpenXR 运行时 v1.1.46"。** | 直接 |
| **C2** | **该运行时与本项目 PICOOpenXRHMD 补丁确实共存于同一进程，但在 Win64 上并不双重拦截 OpenXR 调用。** 本项目的 swapchain 补丁整体包裹在 `#if PLATFORM_ANDROID` 内，`FHMDPICO::InsertOpenXRAPILayer` 在非 Android 平台直接 `return false`。**⇒ PC 端二者"不打架"，补丁对本次崩溃无因果贡献。** | 直接 |
| **C3** | **崩溃栈顶的 `UnrealEditor_OpenXRHMD` 是引擎自带模块，不是本项目的 `UnrealEditor-PICOOpenXRHMD.dll`。** 崩溃链路 = 引擎 OpenXR HMD ↔ PICO 串流运行时，与 PICO 插件补丁无关。 | 直接 |
| **C4** | **崩溃是复发性的，不是一次性事件**：`Saved\Crashes\` 下 **10 个**崩溃报告，时间跨度 2026-09-11 23:27 → 2026-09-12 21:54，**其中 7 次为同一调用栈签名**。最新一次发生在 2026-09-12 21:54:14，5 分 35 秒后编辑器以新 pid 重启。 | 直接 |
| **C5** | **操作系统层没有任何显卡驱动重置 / TDR 记录**：Event 4101 = 0 条（90 天窗口与 20000 条扫描窗口均为 0）、`nvlddmkm` 提供商 = 0 条、Display/Video/Dxgkrnl = 0 条、Application Event 1000 = 0 条。但崩溃日志中出现 **NVIDIA Aftermath GPU 崩溃转储**（6/10 次），且 `Adapter Reset: False / Engine Reset: False`。**⇒ 不是经典 TDR，而是应用侧捕获到的 GPU 故障 + 随后的 CPU 空指针解引用。** | 直接 |
| **C6** | **约定中"禁止关闭编辑器 pid 24284"的前提已失效**：pid 24284 当前 **不存在**（不是我干的——我未对任何进程执行过终止动作）。当前存活的是**另一个**编辑器实例 `UnrealEditor` pid=**14372**（启动于 2026-09-12 21:59:49）。 | 直接 |

**对清理判定（A/B/C/D/E）的输入**：
- `PicoStreamingXR` 是**机器环境组件**（位于 `C:\Program Files\` 与 `D:\App\PicoConnected\`），**不是项目文件** ⇒ **不进入仓库 A/B/E 判定**；但它是崩溃现场的关键事实源，应登记为「运行环境事实源」。
- `Saved\Crashes`（19.31 MB / 48 文件）与 `Saved\Logs`（1.95 MB / 9 文件）属**已忽略构建产物**（`.gitignore` 含 `Saved/`）⇒ 无入库风险，无需清理动作。

---

## 1. picostreaming-openxr DLL：实际位置、版本、签名、修改时间

### 1.1 全机副本枚举

在 `C:\`、`D:\` 上按文件名 `picostreaming-openxr.dll` 递归检索（深度 6），命中 **2 份**：

| # | 路径 | 大小 | FileVersion | LastWriteTime | CreationTime | SHA256 |
|---|------|------|-------------|---------------|--------------|--------|
| **D** | `D:\App\PicoConnected\PICO Connect\openvr_driver\resources\ps_xrt\picostreaming-openxr.dll` | 2,040,696 B | **1.1.46.0** | **2025-08-22 12:10:28** | 2026-08-16 16:35:16 | `945DDFFEC3FDD18CB72D81FA36520B9960C502DA6A298805DAA6F675F07502A1` |
| **C** | `C:\Program Files\PICO Streaming Service\openxr_runtime_pc\PicoStreamingXRRuntime\picostreaming-openxr.dll` | 4,159,864 B | **1.1.46.0** | **2026-02-02 22:16:14** | 2026-08-10 17:05:23 | `7212D0C6C540DAB1EDE1D0F9451F827E3DD7155E15B007BAF35FC489C7E217A8` |

关键观察：
- **两份是不同二进制**（大小 2.04 MB vs 4.16 MB、SHA256 不同、mtime 相差约 5 个月），**却都自报版本 `1.1.46.0`** ⇒ **单凭版本号无法区分二者，必须按 SHA256**。这是本次排查最容易踩的事实陷阱。
- C 副本同目录还有 `.exp` / `.lib` / `.pdb`（含符号），D 副本同目录只有 DLL + JSON。**⇒ C 副本是开发/调试版构建（带 PDB），D 副本是随 PICO Connect 发布的精简版。**

### 1.2 签名（两份均有效）

| 项 | 值 |
|----|-----|
| 签名状态 | **Valid**（`Signature verified.`）——两份均通过 |
| 签名主体 | `CN="Douyin Vision Co., Ltd.", O="Douyin Vision Co., Ltd.", S=北京市, C=CN, SERIALNUMBER=91110107599635562F, OID.2.5.4.15=Private Organization, OID.1.3.6.1.4.1.311.60.2.1.1=石景山区, OID.1.3.6.1.4.1.311.60.2.1.2=北京市, OID.1.3.6.1.4.1.311.60.2.1.3=CN` |
| 证书指纹 | `2EAE126BBDB8B55B1B1437F41CA4803196CF1777` |
| 证书到期 | **2026-10-18 07:59:59**（注意：距今约 1 个月，**尚未过期**） |
| 公司字段 | 文件版本资源内 `CompanyName` 为空 |

### 1.3 哪一份真正被加载与使用（决定性）

**注册表（OpenXR 装载器权威路由）**

```
HKLM\SOFTWARE\Khronos\OpenXR\1
  ActiveRuntime = D:\App\PicoConnected\PICO Connect\openvr_driver\resources\ps_xrt\picostreaming-openxr.json

HKLM\SOFTWARE\Khronos\OpenXR\1\AvailableRuntimes
  C:\Program Files\PICO Streaming Service\openxr_runtime_pc\PicoStreamingXRRuntime\picostreaming-openxr.json  = 0
  D:\AGame\Steam\steamapps\common\SteamVR\steamxr_win64.json                                                 = 0
```

两个 JSON 内容对比（均 `library_path = .\picostreaming-openxr.dll`）：

| 副本 | runtime.name 字段 |
|------|-------------------|
| C | ` PICO XR Runtime` |
| D | ` PicoStreamingXR` |

**异常点（值得登记）**：D 副本是 **ActiveRuntime**，却 **未出现在 `AvailableRuntimes` 列表**里（列表里只有 C 与 SteamVR）。⇒ **PICO Connect 在运行期直接把 ActiveRuntime 指向自己的运行时，却不做 AvailableRuntimes 登记**；这解释了为什么 C 副本的 2.5.2.0 运行时"装了但用不上"。

**进程内实测（最硬的证据）**

对当前存活的 `UnrealEditor` **pid=14372** 做模块枚举，命中：

```
openxr_loader.dll            D:\AWork\Unreal\App\UE_5.6\Engine\Binaries\ThirdParty\OpenXR\win64\openxr_loader.dll
picostreaming-openxr.dll     D:\App\PicoConnected\PICO Connect\openvr_driver\resources\ps_xrt\picostreaming-openxr.dll   ← D 副本
```

⇒ **进程内加载的是 D 副本**，与 ActiveRuntime 一致。

**UE 侧自报**（崩溃日志原文）：

```
LogSlate: Window 'VRSanguoYanWuchang 预览 [NetMode: Standalone 0] （64-bit/PC D3D SM6） OpenXR  PicoStreamingXR (Standalone) (1.1.46)' being destroyed
...
PicoStreamingXR (Standalone) runtime version 1.1.46
```

⇒ UE 把 XR 系统名识别为 **`PicoStreamingXR`、版本 1.1.46、Standalone 模式**。**这就是"项目记录版本 v1.1.46"的真正来源 —— 它是运行时报出来的，不是项目里某个插件文件里写的。**

---

## 2. PicoStreamingXR 在项目内的"注册状态"：**不存在**

按 4 条独立路径交叉验证，结论一致 —— **项目内没有 PicoStreamingXR 插件**：

### 2.1 `.uproject`（`VRSanguoYanWuchang.uproject`，95 行，全文读过）

`"Plugins"` 数组共 8 项，逐项列出：

| Name | Enabled | 备注 |
|------|---------|------|
| PythonScriptPlugin | true | 引擎 |
| OpenXR | true | **引擎** OpenXR 集成 |
| OpenXREyeTracker | true | 引擎 |
| OpenXRHandTracking | true | 引擎 |
| **PICOOpenXR** | true | **本项目插件**（= `Plugins\PICOOpen174f9f81d266V8\PICOOpenXR.uplugin`） |
| OpenXRExpansionPlugin | **false** | 项目内存在但**已禁用** |
| Water | true | 引擎 |
| UE_MCP_Bridge | true | 项目内工具插件 |

**⇒ 无 `PicoStreamingXR` 项。**

### 2.2 `Plugins/` 目录（限深 4 列举）

| 目录 | LastWriteTime |
|------|---------------|
| `OpenXRExpansionPlugin` | 2026-08-16 13:10:37 |
| `PICOOpen174f9f81d266V8` | 2026-08-11 16:43:53 |
| `UE_MCP_Bridge` | 2026-08-31 21:46:26 |
| `VRExpansionPlugin` | 2026-08-16 15:14:18 |

**⇒ 无 `PicoStreamingXR`。**（注：`VRExpansionPlugin` 存在于 `Plugins/` 目录，但**未出现在 `.uproject` 的 Plugins 数组**中 —— 这属于插件/仓库侧的登记不一致，**转交 `scout-repo` / `verifier` 交叉确认**，本报告只登记事实。）

### 2.3 `*.uplugin` 清单（限深 4）

```
Plugins\OpenXRExpansionPlugin\OpenXRExpansionPlugin.uplugin      2026-08-26 23:21:08
Plugins\PICOOpen174f9f81d266V8\PICOOpenXR.uplugin                2026-08-11 11:31:32
Plugins\UE_MCP_Bridge\UE_MCP_Bridge.uplugin                      2026-08-31 21:46:01
Plugins\VRExpansionPlugin\VRExpansionPlugin.uplugin              2026-08-26 23:21:08
```

**⇒ 4 个 `.uplugin`，无一个叫 `PicoStreamingXR`。**

### 2.4 项目全树文件名匹配（限深 5，模式 `PicoStreaming|picostreaming`）

**命中数 = 0。**

### 2.5 小结

> **提法更正**：任务书中的「PicoStreamingXR 插件（项目记录版本 v1.1.46）」实际是 **PICO PC 端串流软件安装到系统里的 OpenXR 运行时**。项目里既没有它的 `.uplugin`，也没有它的 DLL/Binaries 副本，**没有任何项目文件需要为它做"清理/保留"判定**。真正需要登记的是：**机器上存在两份同版本号但不同二进制的运行时**，且 **ActiveRuntime 指向 D 副本**。

---

## 3. 与 PICOOpenXRHMD 补丁的共存与拦截关系

### 3.1 补丁本体（`Plugins\PICOOpen174f9f81d266V8\Source\PICOOpenXRHMD\Private\PICO_HMD.cpp`，3432 行）

补丁做两件事，**都在同一个 `#if PLATFORM_ANDROID` 区块内**：

| 行号 | 内容 |
|------|------|
| **76** | `#if PLATFORM_ANDROID` ← **区块开始** |
| 80–86 | `IsPICOBGRASRGBSwapchainFormat()`：只认 Vulkan `VkFormatB8G8R8A8Srgb = 50` |
| 88–128 | `PICOLayerEnumerateSwapchainFormats()`：从运行时返回的格式列表里**过滤掉 B8G8R8A8_SRGB** |
| 130 | `static PFN_xrCreateSwapchain GPICOChainedCreateSwapchain = nullptr;` |
| 132–136 | **注释原文**：`PICO Neo3 runtime (R2.1.12.0) fails to create Vulkan swapchains when extension structs are chained into XrSwapchainCreateInfo ... the runtime attempts an ION_FREE ioctl on a non-ION fd (ENOTTY) and returns XR_ERROR_RUNTIME_FAILURE. Strip the whole extension chain ... See task M00-T004.` |
| 137–150 | `PICOLayerCreateSwapchain()`：**把 `XrSwapchainCreateInfo` 拷一份、`CoreInfo.next = nullptr`（剥掉整条扩展链）**再调用真实 `xrCreateSwapchain` |
| 151–174 | `PICOLayerGetInstanceProcAddr()`：拦截 `xrEnumerateSwapchainFormats` 与 `xrCreateSwapchain` 两个入口并替换函数指针 |
| **175** | `#endif // PLATFORM_ANDROID` ← **区块结束** |

### 3.2 安装拦截器的入口也是 Android 专属

```cpp
306: bool FHMDPICO::InsertOpenXRAPILayer(PFN_xrGetInstanceProcAddr& InOutGetProcAddr)
307: {
308: #if PLATFORM_ANDROID
309:     if (!FAndroidMisc::GetDeviceMake().ToLower().Contains("pico"))
310:     {
311:         return false;
312:     }
...
319:     GPICOChainedGetInstanceProcAddr = InOutGetProcAddr;
320:     InOutGetProcAddr = PICOLayerGetInstanceProcAddr;      // ← 只有这里才替换
321:     UE_LOG(LogPICOOpenXRHMD, Log, TEXT("PICO OpenXR API layer enabled: filtering VK_FORMAT_B8G8R8A8_SRGB swapchain format."));
322:     return true;
323: #else
324:     return false;                                        // ← Win64 走到这里，什么都不装
325: #endif // PLATFORM_ANDROID
326: }
```

同类 Android 专属还有 `FHMDPICO::GetCustomLoader()`（238 行起，`#if PLATFORM_ANDROID` 240 … `#endif` 302，只加载 `libopenxr_loader_pico.so`）。

**全源码交叉复核**：在 `Plugins\PICOOpen174f9f81d266V8\Source\` 下检索 `PICOLayer|InsertOpenXRAPILayer|GPICOChainedGetInstanceProcAddr`，**除上述区块外没有任何其他赋值点**；其余 `xrGetInstanceProcAddr` 命中全部是**普通取函数指针**（`PICO_MR.cpp` / `PICO_Controller.cpp` / `PICO_SpatialAnchor.cpp` 等），**不替换指针、不构成拦截**。

### 3.3 判定

| 问题 | 结论 | 依据 |
|------|------|------|
| 两者是否共存于同一进程？ | **是** | pid 14372 模块表同时含 `picostreaming-openxr.dll`(D 副本) + `UnrealEditor-PICOOpenXRHMD.dll` + 项目内 PICO 全套模块（Input/Movement/MR/HandTracking/HandInteraction/Passthrough/Portal/Editor/RuntimeSettings）+ 引擎 `UnrealEditor-OpenXRHMD.dll` + `openxr_loader.dll`，共 1046 个模块 |
| 两者是否都拦截 OpenXR 调用？ | **否（Windows 上）** | `InsertOpenXRAPILayer` Win64 分支 `return false`（PICO_HMD.cpp:323-324）；拦截实现整体在 `#if PLATFORM_ANDROID`（76–175） |
| 二者是否"打架"？ | **不打架（PC 端）** | 只有引擎 OpenXRHMD 单向调用运行时；本项目补丁在 Win64 上被预处理器彻底剔除 |

> **重要澄清（防止误判因果）**：补丁注释里写的失败现象是 **`XR_ERROR_RUNTIME_FAILURE`**，而崩溃日志里确实也出现过 **`OpenXR call failed with result XR_ERROR_RUNTIME_FAILURE`**（2 次，见 §6.2）。**这两者形似而因果无关**：补丁针对的是 **Android/PICO Neo3 的内核 ioctl 问题**（`ION_FREE`/`ENOTTY`），而本机是 **Win64 + NVIDIA GA104 + D3D12 串流运行时**。**不得**把补丁注释里的 `XR_ERROR_RUNTIME_FAILURE` 当作本次崩溃的解释——那是**同一枚举值在不同平台的不同成因**。

---

## 4. 串流助手（PC 端软件）的安装路径、版本、日志

机器上**并存三套 PICO 系 PC 端串流软件**（互不覆盖，各自独立安装目录）：

| 软件 | 安装路径 | 版本 | 安装/文件时间 | 运行中 |
|------|----------|------|---------------|--------|
| **PICO Connect**（现行串流助手，Electron） | `D:\App\PicoConnected\PICO Connect\` | **10.6.6**（`FileVersion 10.6.6` / `ProductVersion 10.6.6.0`）；`version.txt` → `commit b2d17ad928f37114ad6423f1977d69bb75b614c5` / `build 86341163` | 主程序文件 2025-08-22 12:10:28；目录创建 2026-08-16 16:35:17 | **是**：pid 404 / 1188 / 5464 / 7376 |
| **PICO串流服务**（`PICO Streaming Service`） | `C:\Program Files\PICO Streaming Service\` | **2.5.2.0**；`version.txt` → `commit 8421f0789c04e9d42bfb23ec1e465466e9208d1e` / `build 92246031` | 安装日期 **20260810**；文件 2026-02-02 22:16 | 未取到（无该名进程） |
| **Streaming Service**（`ps_server`） | `C:\Program Files\Streaming Service\` | **2.2.4.4**；`version.txt` → `commit b1dcc4502d0ef8ea566ef27d7b8998de61118e45` / `build 87129070` | 目录 2026-08-16 16:35:28 | **是**：`ps_server` pid **5920** |

> 卸载登记确认：`PICO串流服务 版本 2.5.2.0`，`InstallLocation = C:\Program Files\PICO Streaming Service\`，`InstallDate = 20260810`。
> `C:\Program Files\Streaming Service` 由 PICO Connect 自带的 `StreamingServiceSetup.exe`（47,247,552 B）安装。

### 4.1 残留/历史目录（**只登记，不处置**）

| 路径 | 状态 |
|------|------|
| `C:\Users\PC\AppData\Local\Streaming Assistant\` | **存在但为空**（目录时间 2024-12-27 00:00:53）；递归 `-Force` 列举**零条目** |
| `C:\Users\PC\AppData\Local\streamingassistant-updater\` | 目录 2026-08-16 16:34:08；含 **`pending\PICOConnect-v10.6.6-win32-x64.exe`（225,922,864 B / 225 MB）** + `installer.exe`（同大小）+ `pending\update-info.json` |
| `C:\Users\PC\AppData\Local\PicoVR\RemotePlayAssistant\` | 旧版「RemotePlayAssistant」残留（2022-09-08 / 2023-04-01），含 `aLog`、`crashData`、`ttnet\netlog` 等空壳目录 |
| `C:\Users\PC\AppData\Local\pico-developer-center-updater\` | 2026-08-10 17:03:59 |

`update-info.json` 全文：

```json
{"fileName":"PICOConnect-v10.6.6-win32-x64.exe","sha512":"tqVlNJqsd5ifp0WQDb3hOnDA91u94ctIhbm9xzTgv6EghHDS1ZqFSL0oOfsX8sEYvlF/IhjN45K6pyywuctWQw==","isAdminRightsRequired":false}
```

> **注意**：pending 安装包版本号 **v10.6.6** 与已安装版本 **10.6.6 相同** ⇒ 该 225 MB 安装包是**同版本号的遗留安装包**（未能确认是"待安装升级"还是"已安装后未清理"）。**未安装、未删除**；仅登记为磁盘占用项（**位于 C: 用户目录，非项目文件**）。

### 4.2 日志位置

| 日志 | 路径 | 大小 | 最后写入 | 说明 |
|------|------|------|----------|------|
| ps_server 主日志 | `C:\Program Files\Streaming Service\ps_server.log` | **8,062,861 B**（读时仍在增长） | **2026-09-12 22:10:25（活动）** | 编码为 **GBK**（中文出现乱码，非 UTF-8） |
| ps_server 归档日志 | `C:\Program Files\Streaming Service\ps_server.{4..10}.log` | 各 ≈20.97 MB | 2026-08-25 | 7 个滚动归档，共 ≈147 MB |
| ps_server parfait 结构化日志 | `C:\Program Files\Streaming Service\parfait\alog\log\*__ps_server__default.alog.hot` | 数十个 | 活动文件 `2026_09_08_1788831655096__...hot` = 3,569,559 B，**mtime 2026-09-12 21:54:30** | 二进制 `.hot`；**未解析（内容未取到）** |
| 服务启动日志 | `C:\Program Files\Streaming Service\ps_service_launcher.log` | 5,838 B | 2026-09-08 09:41:30 | 读取返回空行（内容未取到有效文本） |
| 安装日志 | `...\ps_service_installer.log`（599 B）/ `...\logs\ps_device_installer.log`（8,396 B） | 小 | 2026-08-16 16:35 | — |
| PICO Connect 应用日志 | `D:\App\PicoConnected\PICO Connect\data\` | 仅 `icudtl.dat` | — | **该目录无日志** |
| PICO Connect 崩溃目录 | `D:\App\PicoConnected\PICO Connect\crash\` | — | — | **未取到**（`crash\reports\*` 各子目录为空，`crash_metadata`/`fulldmp_metadata` 为 0 字节） |
| PICO Streaming Service 崩溃目录 | `C:\Program Files\PICO Streaming Service\crash\` | — | 2026-08-10 17:08:43 | **未取到内容** |

### 4.3 只读日志摘要（崩溃窗口 21:50–22:00）

**结论先行：`ps_server` 在编辑器崩溃时没有崩溃，也没有报错——它是一条持续的编码/发送流水。**

崩溃窗口内的抽样（原文节选）：

```
[2026-09-12 21:50:22.731] [PSS] [debug] [5920|34568]video_stream_encoder.cpp:202 OnFrame: 0 500 389335827 ( 0,0,0 ) ( 0,0,0,0 )
[2026-09-12 21:50:23.577] [PSS] [info]  [5920|6772]switch_pico_connect_external.cpp:1306 ProcessPeerStopDisplayStreamingRequest: stop display_streaming {request_id: "H1gOQLvw" display_ids: "84219871"}
[2026-09-12 21:50:23.577] [PSS] [info]  [5920|6772]streaming_session_external.cpp:90 StopDisplayStreaming: stop display streaming, display_id count= 1
[2026-09-12 21:50:23.577] [PSS] [debug] [5920|6772]video_stream_encoder.cpp:108 Reset: reset video_stream_encoder
[2026-09-12 21:50:23.578] [PSS] [debug] [5920|6772]mft_encoder.cpp:55 Close: encode thread join.
```

⇒ **本地 21:50:23 串流会话被正常停止**（display_id `84219871`，session `81sq8Lxx`）；**4 分 49 秒后（21:54:12）编辑器发起新 XR 会话并在 17 ms 内崩溃**（时序见 §6.3）。**21:54 前后 `ps_server.log` 无任何 error/exception 行。**

持续错误模式（**非崩溃时刻，但为环境健康事实**）：

| 时间 | 级别 | 内容 | 次数 |
|------|------|------|------|
| 21:58 – 22:09 | error | `audio_sink_impl.cpp:173 OnAudioData: data in buffer out of range, readable size= 19200, max buffer size= 19200` | 高频反复（抽样区间内 ≥20 次） |
| 22:03:34 – 22:03:35 | error | `streaming_session_external.cpp:623 StartAudioSink: audio_sink has been inited` + `:252 SetRemoteSessionParam: start audio_sink failed`；`StartAudioSource: audio_source has been inited` + `start audio_source failed` | 各 2 次 |
| 22:03:37 | error | `transport_session_tcp3.cpp:201 HandleAsyncError: error=` 后接 **GBK 编码的中文错误串**（该日志文件整体为 GBK，非 UTF-8，故此处不作逐字节转写以免引入替换字符）；语义为"远端强制关闭了一个现有的连接" | 1 次 |

日志尾部（22:07–22:10）显示 `OnFrame` / `OnEncodedFrame` / `SendEncodedImage` 每 ≈8 s 稳定循环（帧序号 9000 → 20000）⇒ **撰写本报告时串流链路仍在活动**。

---

## 5. Windows 系统事件日志（限定 2026-09-10 至今）

**扫描口径**：`Get-WinEvent -LogName System -MaxEvents 20000`，实际覆盖窗口 **2025-01-12 01:45:05 → 2026-09-12 21:59:11**（即扫描窗口远比要求的 09-10 起更宽，**覆盖充分**）。System 日志最旧记录为 **2025-01-12 01:45:03**，说明日志**未被轮转截断** ⇒ 下述"0 条"是**真实不存在**，不是日志缺失造成的假阴性。

### 5.1 计数表（要求项）

| 事件 | 口径 | 计数 | 时间点 |
|------|------|------|--------|
| **Event ID 4101**（显示驱动程序已停止响应并已恢复 / TDR） | 2026-09-10 起 | **0** | — |
| **Event ID 4101** | 最近 90 天 | **0** | — |
| **`nvlddmkm` 提供商**（任何 ID） | 最近 20000 条 System 事件（覆盖至 2025-01-12） | **0** | — |
| **Display / Video / Dxgkrnl 提供商** | 最近 20000 条 System 事件 | **0** | — |
| **Event ID 1000**（应用程序崩溃） | Application 日志，2026-09-10 起 | **0** | — |
| **Event ID 1001**（WER 故障桶） | Application 日志，2026-09-10 起 | **2** | 见下 |
| System 日志 Error/Critical（Level 1,2） | 2026-09-10 起 | **8** | 见下 |

### 5.2 Event 1001 明细（2 条，均与 UnrealEditor/PICO 无关）

| 时间点 | 事件名 | 主体 |
|--------|--------|------|
| 2026-09-10 14:42:21 | `RADAR_PRE_LEAK_64`（Fault bucket 1967015007643011292, type 5） | `msedge.exe` 152.0.4191.66 |
| 2026-09-11 21:12:12 | `MoAppHang`（Fault bucket 1377603843633082659, type 5） | `Microsoft.XboxGamingOverlay_7.326.8061.0_x64__8wekyb3d8bbwe` |

### 5.3 System 日志 Error/Critical 明细（8 条）

| 次数 | 时间点 | 提供商 / ID | 内容 |
|------|--------|-------------|------|
| 5 | 09-10 06:00:01 / 09-10 18:00:01 / 09-11 06:00:02 / 09-11 18:00:02 / 09-12 06:00:02 / 09-12 18:00:02 | `Microsoft-Windows-TPM-WMI` / **1796** | Secure Boot 变量更新失败（本机未启用 Secure Boot）——**良性，与 VR/GPU 无关** |
| 2 | 2026-09-12 **12:59:29** | `Netwtw10` / **5005 + 5002** | `Intel(R) Wi-Fi 6E AX211 160MHz : Has encountered an internal error and has failed.` / `...the network adapter is not functioning properly.` |
| （含于上列 8 条内） | — | — | 无其他类别 |

### 5.4 判定

> **操作系统层完全没有显卡驱动重置 / TDR 记录，也没有 UnrealEditor 的应用崩溃记录。**
>
> 这一"全 0"不是日志缺失（§5 开头已证明覆盖充分），而是**真实结论**，并且**与 §6 的进程内证据互相印证**：编辑器的 10 次崩溃是由 **UE 自身的崩溃处理器**就地接管（写入 `Saved\Crashes\`），**未上报 Windows 错误报告**；而 GPU 侧故障被 **NVIDIA Aftermath** 捕获，其自报状态为 **`Adapter Reset: False` / `Engine Reset: False`** ⇒ **不是经典 TDR**（经典 TDR 会同时产生 4101）。

---

## 6. 崩溃取证补充（超出原任务 5 项，但直接决定因果判定）

> 本节与 `crash-analyst` 的职责有重叠；**我按"环境侧证据"角度给出，供其交叉验证，不代其结论。**

### 6.1 崩溃报告清册（`D:\AWork\Unreal\Project\VRSanguoYanWuchang\Saved\Crashes\`）

**10 个**报告目录，**48 文件 / 19.31 MB**。按时间升序：

| # | 崩溃目录（GUID 缩写） | 时间（本地） | pid | gpudmp | 签名 |
|---|----------------------|--------------|-----|--------|------|
| 1 | `CD3553E441BE92F06BFD54BBE8C626A7_0000` | 2026-09-11 23:27:40 | 29840 | 1 | **A** |
| 2 | `14BCED564264DCA02A902F8DEE1DD512_0000` | 2026-09-11 23:45:34 | 7632 | 1 | **A** |
| 3 | `ABC39CB2465045A1C2A8CCA977F584C7_0000` | 2026-09-12 11:20:06 | 34100 | 1 | **A** |
| 4 | `7F2957C84E4CC15A958DB080B0416C1D_0000` | 2026-09-12 11:24:59 | 3964 | 0 | **A** |
| 5 | `1EB29F53499A23F79EF934AAEA704935_0000` | 2026-09-12 11:31:02 | 4352 | 1 | **A** |
| 6 | `EEAFBA0141E95FB8904501B0AD4CEA71_0000` | 2026-09-12 11:35:13 | 23328 | 1 | **B** |
| 7 | `201553CB4D7C2C49B8C722963CE767CE_0000` | 2026-09-12 14:29:22 | 32284 | 0 | **A** |
| 8 | `A5DEF4AC48A09041D2E018B35B40B4E7_0000` | 2026-09-12 14:35:17 | 22868 | 0 | **B** |
| 9 | `A5DEF4AC48A09041D2E018B35B40B4E7_0001` | 2026-09-12 14:53:03 | 22868 | 0 | **C** |
| 10 | `CBC20AB844854D5BC624EB8C409AFC0F_0000` | **2026-09-12 21:54:14** | 29536 | 1 | **A** |

按日计数：**2026-09-11 = 2 次**；**2026-09-12 = 8 次**。

### 6.2 三种崩溃签名

**签名 A（7 次：#1,2,3,4,5,7,10）**

```
ErrorMessage : Unhandled Exception: EXCEPTION_ACCESS_VIOLATION reading address 0x0000000000000000
CrashType    : Crash        IsEnsure : false     IsAssert : false
CallStack    : picostreaming_openxr ×4
               UnrealEditor_OpenXRHMD ×6
               UnrealEditor_RenderCore ×2 / Core ×3 / ...
               kernel32 → ntdll
```

**签名 B（2 次：#6,8）**

```
ErrorMessage : Ensure condition failed: ((Result) >= 0)
               [File:D:\build\++UE5\Sync\Engine\Plugins\Runtime\OpenXR\Source\OpenXRHMD\Private\OpenXRHMD.cpp]
               [Line: 4093]  OpenXR call failed with result XR_ERROR_RUNTIME_FAILURE
CallStack    : UnrealEditor-OpenXRHMD ×3 → UnrealEditor-D3D12RHI ×3 → UnrealEditor-RHI ×6 → Core → RenderCore
```

**引擎源码定位（已实地核对，非推测）**：`D:\AWork\Unreal\App\UE_5.6\Engine\Plugins\Runtime\OpenXR\Source\OpenXRHMD\Private\OpenXRHMD.cpp` 第 **4093** 行为：

```cpp
4093: 		XR_ENSURE(xrEndFrame(Session, &EndInfo));
```

⇒ **签名 B = `xrEndFrame` 向串流运行时提交合成层失败（`XR_ERROR_RUNTIME_FAILURE`）。**

**签名 C（1 次：#9）**

```
ErrorMessage : 保存“../../../../../Project/VRSanguoYanWuchang/Content/VRSanguo/Dev/L_SkeletonTest.umap”时出现错误
CallStack    : KERNELBASE → Core → CoreUObject
```

⇒ **与 VR/OpenXR 无关的关卡保存失败**（涉 `L_SkeletonTest.umap`，属资产侧；建议 `scout-assets` / `crash-analyst` 关注）。

### 6.3 时序：最新一次崩溃的最后 17 毫秒（#10，本地 21:54:12）

日志时间戳为 UTC（`[2026.09.12-13.54.12:xxx]`），**本地 = UTC+8 = 21:54:12**：

```
21:54:12.769  LogProfilingDebugging: Warning: No layer resource or HMD swapchain available for stereo debug layer
21:54:12.776  LogPICOOpenXRHMD: XR session state changed: 3 (SYNCHRONIZED)
21:54:12.776  LogPICOOpenXRHMD: XR session state changed: 4 (VISIBLE)
21:54:12.776  LogPICOOpenXRHMD: XR session state changed: 5 (FOCUSED)          ← 新 XR 会话刚就绪
21:54:12.782  LogD3D12RHI: Starting late shader associations...
21:54:12.782  LogD3D12RHI: Late shader associations ignored 1307 pipelines based on frame fences
21:54:12.791  LogD3D12RHI: Created late shader associations, took 9.581000.5ms
21:54:12.793  LogNvidiaAftermath: Error:
              Writing Aftermath dump to: .../Saved/Logs/D3D12.0.2026.09.12-21.54.12.nv-gpudmp
              	Succeeded in writing Aftermath dump file.
              Decoding Aftermath GPU Crash:
              	Device Info:
              		Status       : Unknown (0x00000008)
              		Adapter Reset: False
              		Engine Reset : False
              → 随后 UnrealEditor 崩溃（进程 pid 29536）
```

Aftermath 转储内另含：`"Adapter LUID": 66608`、`"Adapter name": "GA104-A"`（NVIDIA GA104 级 GPU）。

### 6.4 环境侧因果判断

| 观察 | 环境侧解读 |
|------|-----------|
| `Adapter Reset: False` / `Engine Reset: False`，且 System 日志 4101 = 0 | **非经典 TDR**。GPU 故障由驱动侧 Aftermath 捕获，未触发 Windows TDR 恢复流程 |
| 6/10 次崩溃同秒伴随 Aftermath 转储 | GPU 侧故障与进程崩溃**时间上高度绑定** |
| 栈顶 4 帧在 `picostreaming_openxr` 内、首帧即访问地址 `0x0` | **运行时侧空指针解引用**——典型于"底层图形设备已失效 → 运行时内部对象为空 → 提交/查询时解引用" |
| 签名 B 明示 `xrEndFrame` 返回 `XR_ERROR_RUNTIME_FAILURE` | 运行时**主动报错**而非崩溃 ⇒ 与"设备失效后运行时无法完成帧提交"一致 |
| 崩溃发生在 XR 会话刚进入 `FOCUSED` 后 17 ms | **会话建立/首帧提交流程**是复现窗口 |
| 补丁在 Win64 被预处理剔除（§3） | **本项目代码不在因果链上** |
| 每次崩溃后编辑器以**新 pid** 重启（21:54 崩溃 → 21:59:49 新进程） | 属**人工/脚本自动重启**，非系统级恢复 |

> **注意**：以上为**环境侧相关性判断**，**不排除**运行时自身缺陷、PICO Connect/串流服务版本组合、GPU 驱动版本、D3D12 与运行时交换链互操作等多方因素。**成因定论应由 `crash-analyst` 在符号化/进一步取证后给出**；本报告不越界下结论。

### 6.5 崩溃产物体积（供清理判定）

| 目录 | 文件数 | 体积 | `.gitignore` 状态 |
|------|--------|------|-------------------|
| `Saved\Crashes` | 48 | **19.31 MB** | `Saved/` 已忽略 ⇒ 不入库 |
| `Saved\Logs` | 9 | 1.95 MB | 同上 |
| `Saved\` 全量 | — | 合计约 **703 MB**（`StagedBuilds` 335.5 / `Cooked` 154.2 / `Shaders` 74.1 / `Screenshots` 50.6 / `Evidence` 33.0 / `Autosaves` 30.2 / `Crashes` 19.3 / `Config` 2.2 / `Logs` 2.0 / `ShaderDebugInfo` 1.7） | 同上 |

---

## 7. 进程状态与硬约束核验

| 项 | 事实 |
|----|------|
| **pid 24284（约定中"禁止关闭的编辑器"）** | **当前不存在**（`Get-Process -Id 24284` 无返回；无同名进程）。**本会话未对其执行任何操作**；无法判断其消失原因（可能是自然退出/被上一次会话关闭/pid 复用），**不属本报告可归因范围** |
| 当前存活的 UE 进程 | `UnrealEditor` **pid=14372**（启动 **2026-09-12 21:59:49**）、`UnrealTraceServer` pid=31684（21:59:40） |
| 本会话对进程的动作 | **零**。未 start / stop / kill / restart 任何进程 |
| 其他存活的相关进程 | `PICO Connect` pid 404 / 1188 / 5464 / 7376；`ps_server` pid **5920** |
| 项目文件改动 | **零**（唯一写入 = 本报告） |
| git 写操作 | **零** |
| 临时文件 | **零**（未使用 `D:\AWork\TraeAdmin\VRSanguoYanWuchang\tmp\`） |

> **给队长的口径建议**：硬约束「禁止关闭编辑器 pid 24284」在**本次执行开始时已不可满足**（目标进程不存在）。**建议将约束重述为「禁止终止任何 `UnrealEditor*` 进程」**，以当前 pid 14372 为对象；本报告全程遵守该重述口径。

---

## 8. 未取到 / 局限声明

| 项 | 状态 |
|----|------|
| `ps_server` 的 parfait `.alog.hot` 结构化日志内容 | **未取到**（二进制格式，未解析） |
| `C:\Program Files\Streaming Service\crash\reports\*` 内容 | **未取到**（目录为空，无报告文件） |
| `C:\Program Files\PICO Streaming Service\crash\` 内容 | **未取到** |
| `D:\App\PicoConnected\PICO Connect\crash\` 内容 | **未取到**（各子目录为空；meta 文件 0 字节） |
| `ps_service_launcher.log` 有效文本 | **未取到**（读取返回空；文件 5,838 B 存在） |
| DLL 符号化调用栈 | **未做**（`picostreaming-openxr.pdb` 仅存在于 C 副本目录，**未被加载的 D 副本无 PDB** ⇒ 栈只有模块名） |
| `picostreaming-openxr.dll` 反汇编 / 字符串 / 导入表分析 | **未做**（超出只读排查范围，且需额外工具） |
| 两份同版本 DLL 的差异内容 | **未做**（仅比对大小/SHA256/时间/签名） |
| GPU 驱动版本与型号全称 | **未取到**（仅从 Aftermath 得到 `GA104-A` / LUID 66608）；`nvlddmkm` 无事件亦未取驱动版本 |
| `Streaming Assistant` 空目录的历史用途 | **未确定**（仅确认目录存在且为空） |
| pending 安装包 v10.6.6 是否等价于当前已装版本 | **未确定**（版本号相同，二进制未比对） |
| `VRExpansionPlugin` 在 `Plugins/` 却不在 `.uproject` 登记的原因 | **未判定**（转 `scout-repo` / `verifier` 交叉确认） |

---

## 9. 机读摘要（供 planner / verifier 直接引用）

```json
{
  "report": ".trae/execution/reports/audit/plugin-env-scout.md",
  "author": "plugin-scout",
  "generated_local": "2026-09-12T22:1x:00+08:00",
  "read_only": true,
  "files_written": [".trae/execution/reports/audit/plugin-env-scout.md"],
  "processes_touched": 0,

  "picostreaming_dll": {
    "copies": [
      {
        "id": "D",
        "path": "D:\\App\\PicoConnected\\PICO Connect\\openvr_driver\\resources\\ps_xrt\\picostreaming-openxr.dll",
        "size_bytes": 2040696,
        "file_version": "1.1.46.0",
        "product_name": "PicoStreamingXR",
        "last_write": "2025-08-22T12:10:28",
        "creation": "2026-08-16T16:35:16",
        "sha256": "945DDFFEC3FDD18CB72D81FA36520B9960C502DA6A298805DAA6F675F07502A1",
        "signature_status": "Valid",
        "signer": "CN=\"Douyin Vision Co., Ltd.\"",
        "cert_thumbprint": "2EAE126BBDB8B55B1B1437F41CA4803196CF1777",
        "cert_not_after": "2026-10-18T07:59:59",
        "is_active_runtime": true,
        "loaded_in_unrealeditor_pid14372": true
      },
      {
        "id": "C",
        "path": "C:\\Program Files\\PICO Streaming Service\\openxr_runtime_pc\\PicoStreamingXRRuntime\\picostreaming-openxr.dll",
        "size_bytes": 4159864,
        "file_version": "1.1.46.0",
        "product_name": "PicoStreamingXR",
        "last_write": "2026-02-02T22:16:14",
        "creation": "2026-08-10T17:05:23",
        "sha256": "7212D0C6C540DAB1EDE1D0F9451F827E3DD7155E15B007BAF35FC489C7E217A8",
        "signature_status": "Valid",
        "has_pdb_in_dir": true,
        "is_active_runtime": false,
        "registered_in_available_runtimes": true
      }
    ],
    "same_version_different_binary": true,
    "active_runtime_registry": "HKLM\\SOFTWARE\\Khronos\\OpenXR\\1\\ActiveRuntime = D:\\App\\PicoConnected\\PICO Connect\\openvr_driver\\resources\\ps_xrt\\picostreaming-openxr.json",
    "available_runtimes": [
      "C:\\Program Files\\PICO Streaming Service\\openxr_runtime_pc\\PicoStreamingXRRuntime\\picostreaming-openxr.json",
      "D:\\AGame\\Steam\\steamapps\\common\\SteamVR\\steamxr_win64.json"
    ],
    "anomaly": "ActiveRuntime (D) is NOT listed in AvailableRuntimes",
    "ue_reported_system": "PicoStreamingXR (Standalone) runtime version 1.1.46"
  },

  "plugin_registration": {
    "is_ue_plugin_in_project": false,
    "uproject_plugins": ["PythonScriptPlugin","OpenXR","OpenXREyeTracker","OpenXRHandTracking","PICOOpenXR","OpenXRExpansionPlugin(disabled)","Water","UE_MCP_Bridge"],
    "uproject_contains_picostreamingxr": false,
    "plugins_dir": ["OpenXRExpansionPlugin","PICOOpen174f9f81d266V8","UE_MCP_Bridge","VRExpansionPlugin"],
    "uplugin_files": ["OpenXRExpansionPlugin.uplugin","PICOOpenXR.uplugin","UE_MCP_Bridge.uplugin","VRExpansionPlugin.uplugin"],
    "project_tree_name_match_count": 0,
    "note": "PicoStreamingXR is an OS-registered OpenXR runtime supplied by PICO PC streaming software, not a project plugin. The 'v1.1.46' figure originates from the runtime's self-reported XR system name.",
    "side_finding": "VRExpansionPlugin exists in Plugins/ but is absent from .uproject Plugins array"
  },

  "pico_patch_interaction": {
    "patch_file": "Plugins\\PICOOpen174f9f81d266V8\\Source\\PICOOpenXRHMD\\Private\\PICO_HMD.cpp",
    "patch_region_lines": "76-175 (#if PLATFORM_ANDROID ... #endif)",
    "installer_fn": "FHMDPICO::InsertOpenXRAPILayer (line 306)",
    "installer_win64_behaviour": "returns false at line 324 (#else branch)",
    "intercepts_xrCreateSwapchain": "Android only",
    "intercepts_xrEnumerateSwapchainFormats": "Android only",
    "other_interception_sites": "none",
    "coexist_in_same_process": true,
    "both_intercept_on_win64": false,
    "do_they_conflict_on_pc": false,
    "caution": "Patch comment mentions XR_ERROR_RUNTIME_FAILURE for Android PICO Neo3 ION_FREE/ENOTTY; the same enum appearing in Win64 crash logs has a different cause. Do not conflate."
  },

  "streaming_software": [
    {"name":"PICO Connect","path":"D:\\App\\PicoConnected\\PICO Connect","version":"10.6.6","file_version":"10.6.6","product_version":"10.6.6.0","build":"86341163","commit":"b2d17ad928f37114ad6423f1977d69bb75b614c5","running_pids":[404,1188,5464,7376]},
    {"name":"PICO Streaming Service","path":"C:\\Program Files\\PICO Streaming Service","version":"2.5.2.0","build":"92246031","commit":"8421f0789c04e9d42bfb23ec1e465466e9208d1e","install_date":"20260810","running":false},
    {"name":"Streaming Service (ps_server)","path":"C:\\Program Files\\Streaming Service","version":"2.2.4.4","build":"87129070","commit":"b1dcc4502d0ef8ea566ef27d7b8998de61118e45","running_pids":[5920]}
  ],

  "streaming_logs": {
    "ps_server.log": {"path":"C:\\Program Files\\Streaming Service\\ps_server.log","size_bytes":8062861,"last_write":"2026-09-12T22:10:25","active":true,"encoding":"GBK"},
    "ps_server_archives": {"glob":"C:\\Program Files\\Streaming Service\\ps_server.{4..10}.log","count":7,"approx_bytes_each":20971450,"last_write":"2026-08-25"},
    "parfait_alog_active": {"path":"C:\\Program Files\\Streaming Service\\parfait\\alog\\log\\2026_09_08_1788831655096__ps_server__default.alog.hot","size_bytes":3569559,"last_write":"2026-09-12T21:54:30","parsed":false},
    "launcher_log": {"path":"C:\\Program Files\\Streaming Service\\ps_service_launcher.log","size_bytes":5838,"last_write":"2026-09-08T09:41:30","text_obtained":false},
    "summaries": {
      "crash_window_error_count": 0,
      "session_stopped_at": "2026-09-12T21:50:23.577",
      "recurring_errors": [
        "audio_sink_impl.cpp:173 OnAudioData: data in buffer out of range (readable 19200 / max 19200)",
        "streaming_session_external.cpp:623 StartAudioSink: audio_sink has been inited",
        "streaming_session_external.cpp:688 StartAudioSource: audio_source has been inited",
        "transport_session_tcp3.cpp:201 HandleAsyncError (remote forcibly closed connection, 2026-09-12T22:03:37)"
      ]
    }
  },

  "windows_event_log": {
    "system_scan_window": "2025-01-12T01:45:05 -> 2026-09-12T21:59:11",
    "system_log_oldest_record": "2025-01-12T01:45:03",
    "coverage_sufficient": true,
    "counts": {
      "EventID_4101_since_2026-09-10": 0,
      "EventID_4101_last_90_days": 0,
      "nvlddmkm_any_id": 0,
      "display_video_dxgkrnl": 0,
      "Application_EventID_1000_since_2026-09-10": 0,
      "Application_EventID_1001_since_2026-09-10": 2,
      "System_Error_Critical_since_2026-09-10": 8
    },
    "event_1001_timestamps": [
      {"t":"2026-09-10T14:42:21","name":"RADAR_PRE_LEAK_64","subject":"msedge.exe 152.0.4191.66"},
      {"t":"2026-09-11T21:12:12","name":"MoAppHang","subject":"Microsoft.XboxGamingOverlay 7.326.8061.0"}
    ],
    "system_errors_breakdown": {
      "TPM_WMI_1796_secureboot": 5,
      "Netwtw10_5005_5002_wifi_2026-09-12T12:59:29": 2,
      "other": 1
    },
    "verdict": "No GPU driver reset / TDR and no UnrealEditor application-crash record at OS level; editor crashes are absorbed by UE's in-process crash handler (Saved/Crashes), not reported to WER."
  },

  "crash_reports": {
    "dir": "D:\\AWork\\Unreal\\Project\\VRSanguoYanWuchang\\Saved\\Crashes",
    "count": 10,
    "file_count": 48,
    "total_bytes": 20247347,
    "by_day": {"2026-09-11": 2, "2026-09-12": 8},
    "signatures": {
      "A_access_violation_picostreaming": {"count": 7, "stack_top": ["picostreaming_openxr x4","UnrealEditor_OpenXRHMD x6"]},
      "B_xrEndFrame_runtime_failure": {"count": 2, "engine_source": "OpenXRHMD.cpp:4093 XR_ENSURE(xrEndFrame(Session, &EndInfo));"},
      "C_umap_save_failure": {"count": 1, "asset": "Content/VRSanguo/Dev/L_SkeletonTest.umap"}
    },
    "aftermath_dumps": 6,
    "latest": {
      "guid": "UECC-Windows-CBC20AB844854D5BC624EB8C409AFC0F_0000",
      "time_local": "2026-09-12T21:54:14",
      "pid": 29536,
      "signature": "A",
      "aftermath_device": {"status": "Unknown(0x00000008)", "adapter_reset": false, "engine_reset": false, "adapter_name": "GA104-A", "adapter_luid": 66608}
    },
    "note": "Saved/ is gitignored; crash artifacts are not repo risk"
  },

  "proc_discipline": {
    "pid_24284_present": false,
    "pid_24284_touched": false,
    "unrealeditor_alive_pid": 14372,
    "unrealeditor_start": "2026-09-12T21:59:49",
    "unrealtraceserver_pid": 31684,
    "processes_started_or_killed": 0
  },

  "repo_state_cross_check": {
    "note": "Out of plugin/env scope; recorded because it affects the team's baseline/backup premise. Authority: scout-repo / git-operator / verifier.",
    "head": "10f96ae26be71384c4cc4c5810c15481468353dd",
    "head_committed": "2026-09-12T20:20:21",
    "origin_master_local_ref": "10f96ae26be71384c4cc4c5810c15481468353dd",
    "remote_ls_remote_master": "10f96ae26be71384c4cc4c5810c15481468353dd",
    "remote_reachable": true,
    "head_vs_origin_divergence": {"origin_ahead": 0, "head_ahead": 0},
    "team_baseline_f255036": "2026-09-10T23:53:00",
    "commits_since_team_baseline": 49,
    "f255036_is_ancestor_of_head": true,
    "cb7ab79_is_ancestor_of_head": true,
    "history_rewritten": false,
    "cb7ab79_full_sha_corrected": "cb7ab790a155b5eb7b9c6ac905df46ff5cbce35b",
    "uncommitted_modified_tracked_files": [
      {"path": ".trae/CHANGELOG.md", "mtime": "2026-09-12T21:16:44"},
      {"path": ".trae/execution/sessions/session-20260830-001.md", "mtime": "2026-09-12T15:51:32"},
      {"path": ".trae/governance/judgement-discipline.md", "mtime": "2026-09-12T21:16:19"},
      {"path": ".trae/governance/rule-gate-matrix.md", "mtime": "2026-09-12T21:16:19"},
      {"path": ".trae/integrity.yaml", "mtime": "2026-09-12T21:07:10"},
      {"path": ".trae/standards/07-vr-comfort-standard.md", "mtime": "2026-09-12T21:06:50"},
      {"path": ".trae/systems/index.md", "mtime": "2026-09-12T21:04:47"},
      {"path": ".trae/vr/04-locomotion-and-comfort.md", "mtime": "2026-09-12T21:06:50"},
      {"path": "Content/VRSanguo/Dev/L_SkeletonTest.umap", "mtime": "2026-09-12T19:44:40"},
      {"path": "Content/VRSanguo/VR/Mesh/环首刀.uasset", "mtime": "2026-09-12T21:54:42"}
    ],
    "uncommitted_count": 10,
    "my_only_write": "?? .trae/execution/reports/audit/plugin-env-scout.md",
    "implication": "Staff baseline SHA is 49 commits stale; 10 working-tree modifications are covered by no version control (AGENTS.md rule 29). Remote is reachable now, so a new baseline commit + push is not network-blocked."
  },

  "not_obtained": [
    "parfait .alog.hot content (binary)",
    "Streaming Service crash/reports content (empty)",
    "PICO Streaming Service crash/ content",
    "PICO Connect crash/ content (empty; meta files 0 bytes)",
    "ps_service_launcher.log effective text",
    "DLL symbolication (D copy has no PDB)",
    "disassembly of picostreaming-openxr.dll",
    "GPU driver version/model full name",
    "historical purpose of empty 'Streaming Assistant' dir",
    "binary diff of the two same-version DLLs",
    "why VRExpansionPlugin is unregistered in .uproject"
  ]
}
```

---

## 10. 给下游的处理建议（**建议，非执行**）

| # | 建议 | 理由 | 归属 |
|---|------|------|------|
| R1 | 把"PicoStreamingXR 插件"在文档与结论中**统一更正为**「PICO 串流 OpenXR 运行时」 | 项目内不存在该插件；误称会误导后续排障方向 | planner |
| R2 | 登记**两份同版本号不同二进制**的运行时（C/D），以 **SHA256** 区分，**不要以 `1.1.46.0` 作身份** | 版本号不可作为身份依据 | planner / scout-repo |
| R3 | 登记 **ActiveRuntime = D 副本**、且 **D 未在 AvailableRuntimes 中** 这一架构事实 | 是复现崩溃现场的必要环境前提 | planner |
| R4 | 明确 **Win64 上补丁不生效**（Android 专属），**将补丁从本次崩溃因果链中排除** | 防 review/report 误判 | verifier / crash-analyst |
| R5 | 将硬约束「禁止关闭 pid 24284」**重述为「禁止终止任何 `UnrealEditor*` 进程」**并以 pid 14372 为对象 | 原目标进程已不存在 | captain |
| R6 | 复现窗口锁定在**「XR 会话进入 FOCUSED 后的首帧提交（`xrEndFrame`）」** | 10 次崩溃里 9 次落在该路径 | crash-analyst |
| R7 | 崩溃产物 `Saved\Crashes`（19.31 MB）**已被 `Saved/` 忽略**，**无需任何清理动作**；如后续要保留证据，应评估其是否需纳入受控证据目录（`Saved/Evidence` 已存在 33.0 MB） | 避免误判为"未跟踪冗余" | planner / scout-repo |
| R8 | 单独跟踪 **签名 C**（`L_SkeletonTest.umap` 保存失败）——它与 VR 无关，不要并入 VR 崩溃结论 | 避免混淆独立缺陷 | crash-analyst / scout-assets |

---

## 11. 跨域观察：仓库与 Git 状态已显著前移（**影响团队「基线/备份」前提**）

> 本节**超出**"插件与环境侧"范围，但由本次只读排查中派生，且**直接影响团队交付前提**，故据实登记。**判定与处置权归 `scout-repo` / `git-operator` / `verifier`**，本报告不越界下结论。

### 11.1 实测状态（2026-09-12 22:1x）

| 项 | 值 |
|----|-----|
| 本地 HEAD | **`10f96ae26be71384c4cc4c5810c15481468353dd`**（`docs(governance): 治理结构整理 …`，提交时间 2026-09-12 20:20:21） |
| `origin/master`（本地跟踪引用） | **`10f96ae`**（committerdate 2026-09-12 20:20:21） |
| **远端实测**（`git ls-remote origin master`，**本次网络可达**） | **`10f96ae26be71384c4cc4c5810c15481468353dd refs/heads/master`** |
| HEAD ↔ origin/master 分歧 | **`0 0`**（完全一致，无未推送、无未拉取） |
| 自团队基线 `f255036` 起的提交数 | **49 个** |
| `f255036` 是否为 HEAD 祖先 | **是**（`merge-base --is-ancestor` exit=0） |
| `cb7ab79` 是否为 HEAD 祖先 | **是**（exit=0）⇒ **历史未被改写（非强推）** |

团队基线提交原文：`f2550366827a717575332bed6a93c56d42c71f9c  2026-09-10 23:53:00  chore(baseline): 审计基线提交 — 盘点报告 + 治理同步 + .gitignore 增补`。
其后的 49 个提交从 `cb7ab79`（2026-09-11 00:20:16）连绵至 `10f96ae`（2026-09-12 20:20:21），内容以 `docs(governance)` 治理立法与台账回填为主。

### 11.2 工作区存在 10 个**未入库**的已跟踪修改

`git status --porcelain=v1` 全部 ` M` 条目（**mtime 全部早于本会话，均非本会话所致**）：

| 文件 | LastWriteTime |
|------|---------------|
| `.trae/execution/sessions/session-20260830-001.md` | 2026-09-12 15:51:32 |
| `Content/VRSanguo/Dev/L_SkeletonTest.umap` | 2026-09-12 19:44:40 |
| `.trae/systems/index.md` | 2026-09-12 21:04:47 |
| `.trae/standards/07-vr-comfort-standard.md` | 2026-09-12 21:06:50 |
| `.trae/vr/04-locomotion-and-comfort.md` | 2026-09-12 21:06:50 |
| `.trae/integrity.yaml` | 2026-09-12 21:07:10 |
| `.trae/governance/judgement-discipline.md` | 2026-09-12 21:16:19 |
| `.trae/governance/rule-gate-matrix.md` | 2026-09-12 21:16:19 |
| `.trae/CHANGELOG.md` | 2026-09-12 21:16:44 |
| `Content/VRSanguo/VR/Mesh/环首刀.uasset` | **2026-09-12 21:54:42** |

**本会话对仓库的唯一写入**：`?? .trae/execution/reports/audit/plugin-env-scout.md`（即本报告，未跟踪）。

两处值得注意的关联：
- `Content/VRSanguo/Dev/L_SkeletonTest.umap`（19:44:40）**正是崩溃签名 C 所报"保存失败"的关卡**（见 §6.2）。
- `Content/VRSanguo/VR/Mesh/环首刀.uasset`（**21:54:42**）的修改时间**晚于 21:54:14 的崩溃 28 秒** ⇒ 崩溃后存在资产落盘动作（编辑器重启后保存，或自动恢复）。

### 11.3 对团队交付的影响（供 captain 裁定）

1. **t10 / t16 的既有结论"推送即唯一备份、四方同 SHA"在其成文时刻成立**，但其**锚定的 SHA 已被 49 个提交取代**；引用该结论时必须**同时声明 SHA 已前移**，否则形成"用旧 SHA 断言当前状态"的口径漂移。
2. 上述 **10 个未入库修改当前只存在于工作区**。按 `AGENTS.md` 规则 29（唯一权威副本 = 项目工作区 + git 远端），**这些修改目前不受任何版本控制覆盖**；若工作区受损，它们**没有可恢复的远端副本**。
3. 远端**本次实测可达**（`ls-remote` 成功，exit=0）⇒ 若需补一次基线提交 + 推送，**网络侧无阻塞**（与 t1 记录的"github.com:443 不可达"不同，该阻塞已不复现）。

### 11.4 SHA 取值更正声明（据实）

排查过程中，我曾以 `cb7ab790a155b5eb7b9c6ac905de8e2ea4bfd5ba` 作为 `cb7ab79` 的完整 SHA 去调用 `merge-base --is-ancestor`，返回 exit=128。**经查该完整 SHA 是我按短 SHA 前缀拼接推测所得，属错误值，并非真实对象。**

实测取值（`git rev-parse cb7ab79`）：

```
cb7ab790a155b5eb7b9c6ac905df46ff5cbce35b
```

**正确尾段为 `df46ff5cbce35b`，我先前拼接的 `de8e2ea4bfd5ba` 是错的。** 使用正确 SHA 后 `merge-base --is-ancestor` 返回 exit=0（是祖先）。
**此处据实更正，防止错误 SHA 流入下游报告。**（另注：团队 t16 记录中该 SHA 亦被截断书写为 `cb7ab790a155b5eb7b9c6ac905d`，同样非完整值。）

---

**报告结束。** 本报告全部结论均来自本次会话的只读命令输出与文件读取；凡未取到者已在 §8 逐条列出，未作推测填充。§11.4 为对本次排查中一次取值失误的据实更正。
