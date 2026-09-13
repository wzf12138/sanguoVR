# 编辑器反复闪退根因排查报告（执行会话独立取证）

| 项 | 值 |
|---|---|
| 任务来源 | `AgentHub` 派工信 `msg-20260912-221102-manager-001`（urgent，ref：编辑器闪退排查） |
| 执行会话 | executor（独立取证会话，与指挥台/用户/其他执行会话并行） |
| 取证窗口 | 2026-09-12 22:11 – 22:35（本地时间） |
| 工作目录 | `D:\AWork\Unreal\Project\VRSanguoYanWuchang` |
| 引擎/平台 | UE 5.6.1-44394996（`WindowsEditor`）· Windows · D3D12（SM6）· NVIDIA GeForce RTX 3070 |
| 显卡驱动（崩溃时刻自报） | 560.94（内部 32.0.15.6094，2024-08-14；排查时 `nvidia-smi` 实测当前仍为 560.94） |
| OpenXR 运行时 | **PicoStreamingXR**（注册表 `HKLM\SOFTWARE\Khronos\OpenXR\1\ActiveRuntime` → `D:\App\PicoConnected\PICO Connect\openvr_driver\resources\ps_xrt\picostreaming-openxr.json`；DLL 实测 v**1.1.46.0**，D 副本 2,040,696 B / 2025-08-22 构建） |
| 项目 VR 插件 | `Plugins/PICOOpen174f9f81d266V8/`（PICO OpenXR Plugin OS5，v1.6.1，含 swapchain 补丁） |
| 证据 | `Saved/Crashes/` 下 **12 个** `UECC-Windows-*` 目录（首查 10 个，取证期间新增 2 个，见 §1） |
| 红线遵守 | 未关闭/重启/挂起/kill 任何 `UnrealEditor*` 进程；未增删移动 `Saved/Crashes/` 任何文件；除本报告外未写项目任何文件；未安装/下载任何软件；临时文件仅写 `D:\AWork\TraeAdmin\VRSanguoYanWuchang\tmp\` 并已删除 |

---

## 0. 执行摘要

1. **VR 闪退根因（A/B 类，9 例）：同一编辑器进程内第 2 次建立 OpenXR 会话时，PICO 串流运行时 `picostreaming-openxr` 在渲染线程空指针崩溃；B 类变体为同路径上 `xrEndFrame` 返回 `XR_ERROR_RUNTIME_FAILURE`。** 9/9 例 VR 相关崩溃全部发生在"同进程第 2 次连接"（会话状态日志：READY 或 FOCUSED 后 1–75 秒内）；7 例 A 类栈**逐 RVA 完全一致**（程序化哈希比对，见 §2.2），是确定性单一代码路径。
2. **用户报告的两个触发场景是同一根因的两种观感。** "长时间不用后闪退"= 长会话闲置后的第 2 次连接（3/9 例，闲置 2h40m–5h52m）；"第二次连接闪退"= 短间隔第 2 次连接（9/9 例全部如此，含间隔仅 1–3 分钟的 4 例）。**"二次连接"是不变触发条件；"长时间闲置"是常见伴随但非必要条件**（反例：A5DEF4AC 连接间隔仅 1.5 分钟仍触发 Ensure）。
3. **H3（本项目 swapchain 补丁）排除。** 补丁代码整体位于 `#if PLATFORM_ANDROID`（`PICO_HMD.cpp` L76–175），`InsertOpenXRAPILayer` 在 Win64 直接 `return false`（L323–324，本会话独立复读源码确认）。PC 串流路径（D3D12）下补丁不参与。
4. **第二个独立根因（C 类，3 例）：UE-MCP 桥驱动的保存遇到只读内容文件 → `LogSavePackage: Error` → `appError` → 编辑器 Assert 终止。** 3 次均由桥的保存调用触发（14:53 `L_SkeletonTest.umap`；22:20:55 与 22:29:37 均为 `BP_VRCharacter.uasset`，该文件**当前实测 `IsReadOnly=True`**）。**后 2 次发生在本次排查期间（22:20:55、22:29:37）——崩溃目录在取证窗口内从 10 个增至 12 个，自动化在崩溃循环中反复重试同一保存，问题正在进行时。**
5. **H2（显卡驱动）为未证实的伴随因素。** 6/12 例含 NVIDIA `nv-gpudmp`（`RHI.Aftermath=true`），但 Windows 事件日志在窗口内**无任何 nvlddmkm/Display TDR 记录**；GPU 侧异常与运行时空指针的因果方向无法用现有数据判定。驱动 560.94（2024-08）过旧本身是独立风险项。

---

## 1. 证据基础与勘误

- **数量勘误**：指挥台信中为 10 个崩溃目录（09-11 至 09-12）。取证期间新增 2 个（22:20:55、22:29:37，均为 C 类桥保存崩溃）。本报告按 **12 个**分析。
- **B 类附带文件勘误**：信中 B 类未提 gpudmp；实测 11:35 那例（`EEAFBA01`）**含** `nv-gpudmp`。gpudmp 总分布：A 类 5/7、B 类 1/2、C 类 0/3。
- **标签名勘误**：该引擎版本 `CrashContext.runtime-xml` 中**不存在 `PortableCallStack` 标签**（10/12 验证）；可移植栈在 `<CallStack>` 标签（模块名序列，与 PCallStack 同形）+ Ensure 类的 ErrorMessage 内嵌带地址栈。下文"完整栈"均以 `<PCallStack>` 为准并注明。
- 高价值标签实测：`TimeOfCrash`（UE `FDateTime` ticks，epoch 0001-01-01，非 Windows FILETIME）、`SecondsSinceStart`、per-thread `<Thread>`（含 `IsCrashed` 标志与线程名）、`RHI.*`（含 `Aftermath`）、`UserActivityHint`、`Platform.AppHasFocus`。
- 每个崩溃目录均含 `VRSanguoYanWuchang.log`（崩溃时会话完整日志副本）+ `UEMinidump.dmp`；`Breadcrumbs_RHIThread_0.txt` 仅 2 例存在且内容仅 2 行（`Frame 17562` / `Frame 24735`），无有效面包屑标记。

## 2. 逐次崩溃取证表

### 2.1 总表（12 例；时间为本地时间；"会话起始"= 崩溃时刻 − `SecondsSinceStart`）

| # | 目录（短） | 崩溃时刻 | 类别 | 崩溃线程 | 会话时长 | 会话起始 | 进程内 XR 连接史（来自日志会话状态序列） | 触发点 | nv-gpudmp |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `CD3553E4` | 09-11 23:27:40 | A | RenderThread | 30764s（8h33m） | 14:54:56 | ①23:14:51 建立→23:17:00 **清洁断开**；②23:27:36 建立 | FOCUSED+4s | 有 |
| 2 | `14BCED56` | 09-11 23:45:34 | A | RenderThread | 1068s（17.8m） | 23:27:46 | ①23:28:23→23:30:18 清洁；②23:45:32 建立 | READY+2s | 有 |
| 3 | `ABC39CB2` | 09-12 11:20:06 | A | RenderThread | 1799s（30m） | 10:50:07 | ①10:50:55→10:53:23 清洁；②11:20:03 建立 | FOCUSED+3s | 有 |
| 4 | `7F2957C8` | 09-12 11:24:59 | A | RenderThread | 279s（4.7m） | 11:20:20 | ①11:20:39→11:22:19 清洁；②11:24:54 建立 | READY+5s | 无 |
| 5 | `1EB29F53` | 09-12 11:31:02 | A | RenderThread | 358s（6m） | 11:25:04 | ①11:25:50→11:27:45 清洁；②11:31:01 建立 | FOCUSED+1s | 有 |
| 6 | `EEAFBA01` | 09-12 11:35:13 | **B**（Ensure） | RHIThread | 240s（4m） | 11:31:13 | ①11:31:30→11:33:00 清洁；②11:33:58 建立 | FOCUSED+75s | 有 |
| 7 | `201553CB` | 09-12 14:29:22 | A | RenderThread | 10406s（2h53m） | 11:35:56 | ①11:48:21→11:48:58 清洁；②14:29:17 建立 | READY+5s | 无 |
| 8 | `A5DEF4AC_0000` | 09-12 14:35:17 | **B**（Ensure） | RHIThread | 347s（5.8m） | 14:29:30 | ①14:30:01→14:33:06 清洁；②14:34:33 建立 | FOCUSED+43s | 无 |
| 9 | `A5DEF4AC_0001` | 09-12 14:53:03 | **C**（Assert） | GameThread | 1415s | （同 #8 进程） | （XR 会话已于 14:35:28 清洁收尾） | 桥保存 `L_SkeletonTest.umap` 只读失败 | 无 |
| 10 | `CBC20AB8` | 09-12 21:54:15 | A | RenderThread | 25216s（7h00m） | 14:53:59 | ①16:02:16→16:02:49 清洁；②21:54:12 建立 | FOCUSED+3s | 有 |
| 11 | `F0FE7906` | 09-12 22:20:55 | **C**（Assert） | GameThread | 1262s（21m） | 21:58:49 | ①22:01:31→22:03:37 **清洁**（无第 2 次连接） | 桥保存 `BP_VRCharacter.uasset` 只读失败 | 无 |
| 12 | `AE9F260B` | 09-12 22:29:37 | **C**（Assert） | GameThread | 146s（2.4m） | 22:27:11 | 无 XR 会话 | 桥保存 `BP_VRCharacter.uasset` 只读失败 | 无 |

类定义：
- **A**：`Unhandled Exception: EXCEPTION_ACCESS_VIOLATION reading address 0x0000000000000000`，`CrashType=Crash`。
- **B**：`Ensure condition failed: ((Result) >= 0) [File:...OpenXRHMD\Private\OpenXRHMD.cpp] [Line: 4093] OpenXR call failed with result XR_ERROR_RUNTIME_FAILURE`，`CrashType=Ensure`。
- **C**：`保存"…<umap/uasset>"时出现错误`，`CrashType=Assert`（`appError`）。

其他常量（12/12 全部一致）：`EngineVersion=5.6.1-44394996`、`RHIName=D3D12`、`FeatureLevel=SM6`、GPU=RTX 3070（DeviceId 2488）、驱动 560.94、`RHI.Aftermath=true`、`RHI.DRED=false`、`EngineMode=Editor`。B 类与 C 类各例含 `IsEnsure`/`IsAssert` 标志；A 类 `IsCrashed=false`（顶层标志语义限制，以 `CrashType` 为准）。

### 2.2 A 类完整栈（7/7 程序化比对逐 RVA 一致）

归一化（去基址）SHA256 短哈希：7 例全部 = `C1F4B9F291E4997B`。帧数 21，崩溃线程 RenderThread。以下为代表例 `CD3553E4`（09-11 23:27:40）的 `<PCallStack>` 全文：

```
picostreaming-openxr 0x00007ff8bc490000 + 5cf6f
picostreaming-openxr 0x00007ff8bc490000 + 6402d
picostreaming-openxr 0x00007ff8bc490000 + f2a4c
picostreaming-openxr 0x00007ff8bc490000 + 83b79
UnrealEditor-OpenXRHMD 0x00007ff8aeac0000 + 65a5
UnrealEditor-OpenXRHMD 0x00007ff8aeac0000 + 23c51
UnrealEditor-OpenXRHMD 0x00007ff8aeac0000 + 23295
UnrealEditor-OpenXRHMD 0x00007ff8aeac0000 + 1ea7c
UnrealEditor-OpenXRHMD 0x00007ff8aeac0000 + 1e78b
UnrealEditor-OpenXRHMD 0x00007ff8aeac0000 + 16c11
UnrealEditor-RenderCore 0x00007ff93c520000 + 1a78e7
UnrealEditor-RenderCore 0x00007ff93c520000 + 1ce728
UnrealEditor-Core 0x00007ff93d5c0000 + 10fb72
UnrealEditor-Core 0x00007ff93d5c0000 + 10284f
UnrealEditor-Core 0x00007ff93d5c0000 + 102ece
UnrealEditor-RenderCore 0x00007ff93c520000 + 1f2b19
UnrealEditor-RenderCore 0x00007ff93c520000 + 1f3c04
UnrealEditor-Core 0x00007ff93d5c0000 + 7937cd
UnrealEditor-Core 0x00007ff93d5c0000 + 78c91f
KERNEL32 0x00007ff9a0560000 + 1259d
ntdll 0x00007ff9a1830000 + 5af38
```

其余 6 例（`14BCED56`、`ABC39CB2`、`7F2957C8`、`1EB29F53`、`201553CB`、`CBC20AB8`）仅模块基址（ASLR）不同，RVA 序列与上表逐帧相同（程序化哈希比对通过）。`<CallStack>`（可移植）在 7 例中亦为同形模块序列：`picostreaming-openxr×4 → OpenXRHMD×6 → RenderCore×2 → Core×3 → RenderCore×2 → Core×2 → kernel32 → ntdll`。

**读法**：RenderCore（渲染线程主循环/任务）→ `UnrealEditor-OpenXRHMD`（引擎 OpenXR HMD，6 层调用链）→ `picostreaming-openxr`（PICO 串流运行时实现，4 层）→ 解引用空地址。

### 2.3 B 类完整栈（2/2 程序化比对逐 RVA 一致，哈希 `A6DFAA7FC1B67BDF`）

帧数 20，崩溃线程 RHIThread。代表例 `EEAFBA01`（09-12 11:35:13）：

```
UnrealEditor-OpenXRHMD 0x00007ff8ca190000 + 60d1f
UnrealEditor-OpenXRHMD 0x00007ff8ca190000 + 40b4c
UnrealEditor-OpenXRHMD 0x00007ff8ca190000 + 45200
UnrealEditor-D3D12RHI 0x00007ff8c8700000 + 188976
UnrealEditor-D3D12RHI 0x00007ff8c8700000 + 18849d
UnrealEditor-D3D12RHI 0x00007ff8c8700000 + 18b0fb
UnrealEditor-RHI 0x00007ff941cc0000 + 9fe3e
UnrealEditor-RHI 0x00007ff941cc0000 + 9d918
UnrealEditor-RHI 0x00007ff941cc0000 + d00c3
UnrealEditor-RHI 0x00007ff941cc0000 + 840ae
UnrealEditor-RHI 0x00007ff941cc0000 + 9f321
UnrealEditor-RHI 0x00007ff941cc0000 + a1d2a
UnrealEditor-Core 0x00007ff93c910000 + 10fb72
UnrealEditor-Core 0x00007ff93c910000 + 10284f
UnrealEditor-Core 0x00007ff93c910000 + 102ece
UnrealEditor-RenderCore 0x00007ff93b870000 + 1f3aeb
UnrealEditor-Core 0x00007ff93c910000 + 7937cd
UnrealEditor-Core 0x00007ff93c910000 + 78c91f
KERNEL32 0x00007ff9a0560000 + 1259d
ntdll 0x00007ff9a1830000 + 5af38
```

`A5DEF4AC_0000`（09-12 14:35:17）RVA 逐帧一致。**引擎源码定位（本会话独立读取 `D:\AWork\Unreal\App\UE_5.6\Engine\Plugins\Runtime\OpenXR\Source\OpenXRHMD\Private\OpenXRHMD.cpp`）**：第 **4093** 行 = `XR_ENSURE(xrEndFrame(Session, &EndInfo));`，位于 RHI 线程的帧提交函数内（`PipelinedFrameStateRHI` 上下文）。即 B 类 = **XR 帧提交在 RHI 线程失败（XR_ERROR_RUNTIME_FAILURE）**。该例 Ensure 未杀进程（同进程 18 分钟后死于 C 类）。

### 2.4 C 类完整栈（3 例同形 26 帧；仅桥内顶部 1–2 帧不同）

帧数 26，崩溃线程 GameThread。三例差异仅在 `UnrealEditor-UE_MCP_Bridge` 顶部帧（对应桥的不同保存调用入口），其余逐 RVA 一致：

- #9 `A5DEF4AC_0001`（14:53:03）：桥顶部帧 `+121d14`，下方 `+3ae31/+51dde/+3ae7f/+27e38`
- #11 `F0FE7906`（22:20:55）：桥顶部帧 `+9ef56/+cf697`，下方同
- #12 `AE9F260B`（22:29:37）：桥顶部帧 `+9ef56/+c7a49`，下方同

共同主体（以 #11 为例，全文）：

```
KERNELBASE 0x00007ff99ee70000 + 5fb4c
UnrealEditor-Core 0x00007ff93c2a0000 + 719db2
UnrealEditor-Core 0x00007ff93c2a0000 + 71d3bb
UnrealEditor-Core 0x00007ff93c2a0000 + 50da5b
UnrealEditor-CoreUObject 0x00007ff93e030000 + 596562
UnrealEditor-CoreUObject 0x00007ff93e030000 + 5bb87a
UnrealEditor-CoreUObject 0x00007ff93e030000 + 5a3d04
UnrealEditor-CoreUObject 0x00007ff93e030000 + 5ba5a3
UnrealEditor-CoreUObject 0x00007ff93e030000 + 5ba7e1
UnrealEditor-CoreUObject 0x00007ff93e030000 + 5bbc16
UnrealEditor-UE_MCP_Bridge 0x000001f35efc0000 + 9ef56
UnrealEditor-UE_MCP_Bridge 0x000001f35efc0000 + cf697
UnrealEditor-UE_MCP_Bridge 0x000001f35efc0000 + 3ae31
UnrealEditor-UE_MCP_Bridge 0x000001f35efc0000 + 51dde
UnrealEditor-UE_MCP_Bridge 0x000001f35efc0000 + 3ae7f
UnrealEditor-UE_MCP_Bridge 0x000001f35efc0000 + 27e38
UnrealEditor-Core 0x00007ff93c2a0000 + 17707e
UnrealEditor-Core 0x00007ff93c2a0000 + 1c50fe
UnrealEditor 0x00007ff6e50d0000 + da75
UnrealEditor 0x00007ff6e50d0000 + 2e5ac
UnrealEditor 0x00007ff6e50d0000 + 2e6ba
UnrealEditor 0x00007ff6e50d0000 + 3209e
UnrealEditor 0x00007ff6e50d0000 + 44e44
UnrealEditor 0x00007ff6e50d0000 + 480fa
KERNEL32 0x00007ff9a0560000 + 1259d
ntdll 0x00007ff9a1830000 + 5af38
```

日志错误链（3/3 一致）：`LogSavePackage: Moving output files…` → `LogSavePackage: Error: Cannot remove '…' as it is read only` → `LogSavePackage: Error: Error saving '…'` → `LogWindows: Error: appError called: 保存…时出现错误` → `Windows GetLastError: 当文件已存在时，无法创建该文件。(183)`。#11 日志明确桥处理方法 `LogMCPBridge: [UE-MCP] Processing method: save_dirty`。实测文件属性（22:33）：`BP_VRCharacter.uasset IsReadOnly=True`；`L_SkeletonTest.umap IsReadOnly=False`（14:53 之后有人/某会话清除过其只读位，当时失败原因以日志为准）。

## 3. 跨次聚合（12 例 PCallStack 模块统计）

| 模块 | 总帧数 | 出现崩溃数 | 位置 |
|---|---|---|---|
| `UnrealEditor-Core` | 60 | 12/12 | A 类 13–15/18–19 帧；B 类 13–17；C 类 2–4/17–18（任务分发与 appError 链） |
| `UnrealEditor-OpenXRHMD` | 48 | **9/12**（7A+2B） | **A 类 5–10 帧（pico 栈下）；B 类栈顶 1–3 帧** |
| `UnrealEditor-RenderCore` | 30 | 9/12 | A 类 11–12/16–17（渲染线程入口）；B 类 18 |
| **`picostreaming-openxr`** | 28 | **7/12（全部 A 类）** | **A 类栈顶 1–4 帧（恒定）** |
| `UnrealEditor-CoreUObject` | 18 | 3/12（全部 C 类） | 5–10 帧（对象保存链） |
| `UnrealEditor`（exe 主循环） | 18 | 3/12（C 类） | 19–24 帧 |
| `UnrealEditor-UE_MCP_Bridge` | 17 | 3/12（C 类） | 11–16 帧（**保存调用发起方**） |
| `KERNEL32` / `ntdll` | 12+12 | 12/12 | 栈底 |
| `UnrealEditor-RHI` | 12 | 2/12（B 类） | 7–12 帧 |
| `UnrealEditor-D3D12RHI` | 6 | 2/12（B 类） | 4–6 帧 |
| `KERNELBASE` | 3 | 3/12（C 类） | 栈顶（异常引发） |

要点：`picostreaming-openxr` 只在 A 类出现且恒为栈顶；`OpenXRHMD` 在 A 类为第 2 层、B 类为栈顶；`D3D12RHI`/`RHI` 仅 B 类；`UE_MCP_Bridge` 仅 C 类且为发起方。**A/B 两类同属 OpenXR 会话路径（XR 帧/会话），C 类与 VR 无关。**

## 4. 时间线与触发场景对应

崩溃序列（相邻间隔）：23:27:40 →（17m54s）→ 23:45:34 →（11h34m32s）→ 11:20:06 →（4m53s）→ 11:24:59 →（6m03s）→ 11:31:02 →（4m11s，Ensure）→ 14:29:22 →（5m55s，Ensure）→ 14:53:03 →（7h01m12s）→ 21:54:15 →（26m40s）→ 22:20:55 →（8m42s）→ 22:29:37。

崩溃→重启→再崩的节奏（由 `SecondsSinceStart` 反推会话起始时刻）：

| 前次事件 | 下次编辑器启动 | 间隔 |
|---|---|---|
| #1 崩 23:27:40 | #2 会话 23:27:46 | **6 秒** |
| #3 崩 11:20:06 | #4 会话 11:20:20 | **14 秒** |
| #4 崩 11:24:59 | #5 会话 11:25:04 | **5 秒** |
| #5 崩 11:31:02 | #6 会话 11:31:13 | **11 秒** |
| #6 Ensure 11:35:13（进程存活） | 用户关闭后 #7 会话 11:35:56 | ~43 秒 |
| #7 崩 14:29:22 | #8/#9 进程 14:29:30 | **8 秒** |
| #9 崩 14:53:03 | #10 会话 14:53:59 | 56 秒 |
| #10 崩 21:54:15 | #11 会话 21:58:49 | 4m34s |

**与用户两个触发场景的对应（证据等级：日志会话状态序列 = 直接证据；用户意图 = 无法回溯，不作断言）：**

- **"连接过一次 VR 串流、第二次连接时闪退"**：9/9 例 VR 相关崩溃（7A+2B）的进程内连接史均为"第 1 次建立 → 清洁断开（STOPPING→IDLE→EXITING）→ 第 2 次建立 → 崩溃/Ensure"。触发点距第 2 次会话 READY/FOCUSED 仅 1–75 秒（A 类 1–5 s，B 类 43/75 s）。**有直接证据，全部归属。**
- **"长时间不用后闪退"**：#1（闲置 5h47m 后第 2 连）、#7（闲置 2h40m 后第 2 连）、#10（闲置 5h52m 后第 2 连；21:54 会话日志 17:00–21:00 本地时间每小时仅 55–113 行，接近空转）。这 3 例同时满足两个描述。**但"长时间闲置"不是必要条件**（#4/#5/#6/#8 连接间隔仅 1–3 分钟仍触发），故该场景**与"二次连接"是同一根因**。单独的"编辑器空闲"未见致崩证据（11:58 会话空闲 22 分钟仅死于桥保存；空闲本身无崩溃记录）——**对"编辑器无 VR 会话长时间挂起后自行崩溃"这一严格命题：无直接证据，无法归属（样本中不存在无任何 XR 会话而闪退的 A/B 类案例）**。
- C 类 3 例与 VR/闲置均无关，触发者 = 桥保存只读文件（#11、#12 发生在排查窗口内，属进行时事件）。

## 5. H1–H4 逐条判定

### H1：`picostreaming-openxr` 第二次建立会话时未清理上次状态 → 空指针 —— **支持（强）**

- 支持证据：9/9 例 VR 崩溃均发生在同进程第 2 次会话建立后 1–75 秒（§2.1 连接史列，日志直接证据）；A 类 7/7 栈逐 RVA 一致（确定性路径，运行时模块栈顶）；B 类 2 例同为第 2 次会话后的帧提交失败；对照组——21:58:49 会话"新进程第 1 次连接"完整清洁（22:01:31 FOCUSED → 22:03:37 断开 → 22:20:55 正常退出），证明单次连接路径健康。
- 反对证据：无。（"跨进程残留"假说被否定：每个崩溃进程的第 1 次连接都成功且清洁结束，包括崩溃后 5–14 秒极速重启的场景——运行时跨进程残留不阻断"第 1 次"。）
- 无法判定：缺陷的确切内部机制（哪个对象为空、哪次调用未清理）——`picostreaming-openxr` 无公开符号。
- 进一步区分方法：§6 R1（边界确认）+ R2（重启 PICO Connect 对照，判定残留状态在运行时侧还是编辑器侧）。

### H2：长时间空闲后显卡驱动状态失效（TDR/设备移除）—— **部分相关，非已证根因**

- 支持证据：6/12 例含 `nv-gpudmp`（NVIDIA GPU 故障转储；`RHI.Aftermath=true` 使能了捕获）；3 例 A 类前确有 2h40m–5h52m 闲置；驱动 560.94 为 2024-08 版本，已两年未更新，属高风险环境。
- 反对证据：Windows 事件日志（System）09-11 20:00 – 09-12 23:59 窗口内**无任何 nvlddmkm/Display 事件（无 OS 级 TDR/驱动复位）**；4 例 A/B 类崩溃前无长时间闲置（间隔 1–26 分钟）；"长时间空闲"不构成必要条件。
- 无法判定：GPU 侧异常与运行时空指针的**因果方向**（GPU 故障在前导致运行时对象失效？还是运行时 bug 崩溃时 Aftermath 顺带捕获 GPU 状态？）；`nv-gpudmp` 内容未解析（需 NVIDIA 工具，任务禁止安装）。
- 进一步区分方法：§6 R3（升级驱动后复现）+ gpudmp 解析（需 NVIDIA 工具/厂商支持，用户授权后进行）。

### H3：本项目 `PICO_HMD.cpp` swapchain 补丁与串流插件冲突 —— **排除**

- 支持证据：无。
- 反对证据（独立复核源码，本会话亲手读取）：补丁全部代码在 `Plugins/PICOOpen174f9f81d266V8/Source/PICOOpenXRHMD/Private/PICO_HMD.cpp` **L76–175 的 `#if PLATFORM_ANDROID` 块内**；`FHMDPICO::InsertOpenXRAPILayer` 在非 Android 平台走 `#else return false;`（L323–324）。PC 串流（Win64 + D3D12）下补丁不挂钩任何 xr 函数。此外补丁目标为 Vulkan 格式协商（Android 真机 Neo3 ION 问题），与 PC D3D12 路径无关。A 类栈中亦无任何 `PICOOpenXR*` 项目模块帧。
- 备注：`GetOptionalExtensions` 添加的若干 EXT 扩展在 1.1.46 运行时不可用（仅日志告警，OpenXR 可选扩展被跳过），不构成崩溃路径。

### H4：串流插件 v1.1.46 与 UE 5.6.1 兼容问题 —— **无法精确归因；缺陷代码确在运行时 DLL 内部**

- 支持证据：A 类栈顶 4 帧全部位于 `picostreaming-openxr`（PicoStreamingXR 1.1.46.0，PICO Connect 分发）内部；该运行时已知有其他缺陷史（项目记录：输入路由、battery 扩展缺失等）；同版本号两份不同二进制（D 盘 2,040,696 B/2025-08-22，C 盘 4,159,864 B/2026-02-02），版本管理混乱本身是风险。
- 反对证据：无直接反证。
- 无法判定："与 UE 5.6.1 不兼容"这一具体命题——无运行时符号、无厂商变更日志可比对。可以证实的更弱命题：**确定性缺陷位于 `picostreaming-openxr` 内部，引擎（OpenXRHMD）仅是调用方**。
- 进一步区分方法：§6 R4（升级 PICO Connect/运行时后复现）、R5（换 SteamVR 运行时对照）。

## 6. 复现方案（未排除候选 → 可判定实验）

> 标注 ★ = 必须用户本人在场操作（涉及真机/串流/驱动/系统级变更）。

- **R1 边界确认（★，约 5 分钟）**：前置：PICO Connect 已连接、编辑器已启动。步骤：进入 VR Preview（连接①）→ 正常退出 PIE → 保存全部工作 → 再次进入 VR Preview（连接②）。预期观察：连接② 建立（READY/FOCUSED）后 1–75 秒崩溃或 Ensure 对话框；日志出现 `XR session state changed` 第二轮序列。判定：复现 = H1 边界坐实。
- **R2 残留状态归属（★，约 10 分钟）**：R1 前半之后，**完全退出并重启 PICO Connect（不动编辑器）**，再在同一编辑器进程连接②。若不再崩 → 残留状态在 PICO Connect/运行时侧；若仍崩 → 状态在编辑器进程侧（UE 与运行时之间的会话句柄）。此实验直接决定缓解策略是"重连前重启 PICO Connect"还是"重连前重启编辑器"。
- **R3 驱动维度（★，约 30 分钟 + 重启）**：升级 NVIDIA 驱动（560.94 → 当前 Studio/GameReady 驱动）后重复 R1。若复现消失 → H2 与驱动相关；若仍复现 → 缺陷与驱动版本无关（A 类空指针在运行时内部，预期仍崩）。
- **R4 运行时版本（★，约 20 分钟）**：升级 PICO Connect（1.1.46 运行时 → 新版）后重复 R1。消失 = 厂商已修；仍崩 = 1.1.46 之外同样存在问题，上报证据增强。
- **R5 运行时对照（★，约 15 分钟）**：将 `ActiveRuntime` 切至 SteamVR（项目有登记过的切换/回切程序，CR-20260905 时期实践）重复 R1。若 SteamVR 下二次连接正常 → 缺陷特异性锁定 PICO 运行时。注意：切换影响输入路径（历史记录 XR_EXT_UUID 相关问题），实验后必须回切。
- **R6 空闲对照（★，约 1 小时挂机）**：连接①后保持 PIE/VR 会话挂起 1 小时**不做第二次连接**，观察是否自行崩溃。预期不崩（分离"空闲"与"二次连接"两个变量）。
- **R7 C 类复现（非 ★，约 2 分钟，可由任意桥会话执行）**：对任一只读内容文件（如 `BP_VRCharacter.uasset`，实测仍只读）执行桥 `save_dirty`。预期：`Cannot remove … read only` → appError → 编辑器终止。已自然发生 3 次（14:53:03 / 22:20:55 / 22:29:37），可直接采信为已复现。

## 7. 分层缓解建议

**立即（不改代码/配置，今天可做）**

| 措施 | 代价 | 风险 | 可逆 |
|---|---|---|---|
| M1 **同一编辑器进程内需要第 2 次进入 VR 前，先完全退出并重启编辑器**（新进程第 1 次连接被证明健康）；进入 VR 前先保存全部工作 | 工作流改变，每次 ~1 分钟 | 低 | 是 |
| M2 **让共享编辑器的自动化（桥）会话暂停对 `Content/` 的保存**，直至只读文件解除——`BP_VRCharacter.uasset` 仍只读，当前正在触发崩溃循环（22:27 启动的编辑器 146 秒后即被再次杀死） | 自动化保存暂停 | 低 | 是 |
| M3 恢复崩溃后不要 5–14 秒极速重启编辑器（给系统几秒清理）——非必要措施，配合 M1 | 几乎无 | 低 | 是 |

**短期（改配置，需用户执行）**

| 措施 | 代价 | 风险 | 可逆 |
|---|---|---|---|
| M4 解除受影响内容文件的只读属性（`attrib -r`，并核查 NTFS 保护脚本为何覆盖到这两个文件——治理脚本范围应核对） | 需确认保护策略边界 | 低（保护脚本重新应用即可恢复） | 是 |
| M5 升级 NVIDIA 驱动至 2025/2026 版本 | 需重启 | 低-中（老驱动→新驱动首次配置变化） | 是（可回滚） |
| M6 升级 PICO Connect（运行时 1.1.46 → 新版） | 需真机联调验证；输入行为可能变化（历史教训 CR-20260905） | 中 | 是（旧安装包可留存 E 盘） |
| M7 （备选）编辑器工作期临时切 SteamVR 运行时（有登记回切程序） | 输入路径行为差异 | 中 | 是（必须回切） |

**根治（改代码/换版本，需走治理流程）**

| 措施 | 说明 |
|---|---|
| M8 **上报 PICO**：附 `UEMinidump.dmp` + `nv-gpudmp` + A 类 21 帧 PCallStack（7 例逐 RVA 恒定，哈希 `C1F4B9F291E4997B`）+ 会话状态日志序列，指认 `picostreaming-openxr` 1.1.46 同进程二次 `xrCreateSession` 渲染线程 AV@0x0 与二次会话 `xrEndFrame` XR_ERROR_RUNTIME_FAILURE；请其提供符号版或修复。根治责任在运行时厂商 | 无本地代码可改（缺陷在闭源运行时内部；引擎侧无法拦截运行时内部解引用） |
| M9 C 类根治：UE-MCP 桥的保存调用失败应返回错误结果而非触发引擎 `appError`（改 `Plugins/UE_MCP_Bridge` = 改代码，需认领门禁 + 白名单）；保存前检查目标文件 `IsReadOnly` | 中等改动；可逆 |
| M10 建议登记册新增风险条目（由 manager 落册）：① PicoStreamingXR 二次会话建立崩溃（A/B 类）；② 桥保存只读内容文件闪退（C 类） | 文档工作 |

## 8. 不确定清单（未取到数 / 无法判定；不含推测填充）

**未取到数：**
1. `picostreaming-openxr` 无符号文件（PDB）——RVA `+5cf6f/+6402d/+f2a4c/+83b79` 无法映射到函数名。
2. 引擎模块（`UnrealEditor-OpenXRHMD` 等）RVA 无 PDB（安装版未附带）——`+65a5` 等帧的具体函数未命名（仅 4093 行 `xrEndFrame` 由源码文本定位）。
3. `nv-gpudmp` 未解析——需 NVIDIA 专有工具，任务禁止安装；其内含 GPU 故障类型（页故障/超时/设备移除）未知。
4. PICO Connect 应用侧日志——常见路径（`D:\App\PicoConnected\PICO Connect\log(s)`、`%LOCALAPPDATA%\PICO`、`%APPDATA%\PICO`）未找到日志目录，运行时侧视角缺位。
5. Windows 应用事件日志（WER）未查询。
6. `L_SkeletonTest.umap` 在 14:53 失败时的只读状态——现已 `IsReadOnly=False`，当时的属性/ACL 状态无法回溯（日志文字"read only"为当时唯一证据）。
7. 只读属性的来源（NTFS 保护脚本 / 手动 / git 流程）未取证——需核对 `D:/AWork/TraeAdmin/` 管理脚本范围。
8. 取证窗口（22:11–22:35）内崩溃目录仍在增长（10→12）；22:29:37 之后是否继续发生未持续监视。
9. 用户实际操作意图（何时戴头显、何时离开）无法从日志回溯——时间线对应仅基于会话状态序列。

**无法判定：**
1. A 类崩溃中 GPU 侧异常与运行时空指针的因果方向（H2 内已述）。
2. "与 UE 5.6.1 不兼容"作为独立命题的真伪（H4 内已述）。
3. 无任何 XR 会话的编辑器长时间空闲是否会自行崩溃——样本中不存在此类 A/B 案例，**无法归属**。
4. 缺陷的内部机制（哪个指针、哪次状态未清理）——需厂商符号/源码。

## 9. 取证纪律声明

- 全程仅只读取证；未触碰任何 `UnrealEditor*` 进程（仅 `Get-Process` 只读查询）；`Saved/Crashes/` 未增删改移。
- 文本读取全部使用 `[System.IO.File]::ReadAllText/ReadAllLines` + UTF-8；XML 用具名标签正则提取，未整文件打印。
- 临时产物仅两个（`D:\AWork\TraeAdmin\VRSanguoYanWuchang\tmp\crash_extract_1.xmltags.txt`、`crash_extract_2.callstack.txt`），报告成文后删除。
- 本报告为唯一写入项目的文件（派工信第五节授权路径）。按派工信"仓库只读"约束，未创建会话记录、未改 STATUS.json/登记册/CHANGELOG——风险登记建议（M10）提请 manager 落册。
- 所有"通过/一致"表述均对应本会话真实执行的比对（栈哈希比对、标签提取、源码行读取、文件属性查询）；未执行/未取到的项一律在 §8 列明。

*报告完。执行会话 executor，2026-09-12。*
