# M01-T005 灰盒竞技场关卡

- 任务编号：M01-T005
- 状态：见 `STATUS.json`
- 里程碑：M01
- 优先级：P1
- 执行方：AI
- 前置依赖：**无**（可与 T005/T006 并行执行）
- 预估耗时：~2h

## 目标

使用 UE5.6 LevelPrototyping 灰盒素材搭建 1v1 战斗测试竞技场，为 M01 战斗切片提供关卡基础。关卡包含玩家出生点、AI 出生点、掩体、视觉边界和 NavMesh。

## 为什么无前置依赖

本任务只搭建关卡几何体和 NavMesh，不涉及 C++ 接口或战斗逻辑。T005 的 `L_SkeletonTest` 是空场景验证，本任务是正式的战斗测试场景。两者可并行。

## 实施步骤

### Step 1：创建关卡与基础地面（~0.5h）

**新增文件**：
- `Content/VRSanguo/Dev/L_Prototype_1v1.umap`

**操作**：
- 创建新关卡，使用 `Content/LevelPrototyping/` 素材
- 地面尺寸：20m x 20m（1v1 测试规模，小于 3v3 的 50x50m）
- 地面材质：`MI_PrototypeGrid_Gray`
- 四周围墙：高度 4m，材质 `MI_PrototypeGrid_Gray_02`
- 天花板：不添加（VR 室外场景）

### Step 2：出生点与掩体布局（~0.5h）

**布局**（对称开放型）：

```
         ┌─────────────────────────┐
         │                         │
         │     [掩体A]   [掩体B]    │
         │         ↕ 4m             │
         │  P出生            AI出生  │
         │   ●                ●     │
         │         ↕ 12m            │
         │     [高台C]              │
         │                         │
         └─────────────────────────┘
              20m × 20m
```

**元素**：
- 玩家出生点：`PlayerStart`，位置 (0, -5, 0)，朝向 +Y
- AI 出生点：`TargetPoint`，位置 (0, 5, 0)，朝向 -Y
- 掩体 A/B：`SM_ChamferCube`，尺寸 2m x 0.8m x 1.2m（半身高），位于两侧
- 高台 C：`SM_Ramp` + `SM_ChamferCube`，高度差 1m，提供射界
- 出生区周围 2m x 2m 无障碍空间

### Step 3：NavMesh 生成（~0.3h）

**操作**：
- 添加 `NavMeshBoundsVolume`，覆盖全部可行走区域
- 缩放至 20m x 20m x 4m
- 构建 NavMesh（`Project Settings -> Navigation -> Build`
- 验证：NavMesh 覆盖地面，出生点和高台均可达
- NavMesh 边界距掩体 >= 0.5m

### Step 4：光照与性能（~0.3h）

**操作**：
- 添加 1 个 `DirectionalLight`（主光源，模拟日光）
- 添加 1 个 `SkyLight`（环境光）
- 添加 `ExponentialHeightFog`（简单雾效，辅助深度感知）
- 烘焙光照（Lightmass）
- 检查性能：`stat unit`、`stat fps` 在 PIE 中目标 >= 90fps（VR 基线）

### Step 5：关卡配置与标注（~0.4h）

**操作**：
- 设置 `World Settings`：
  - GameMode：`BP_VRGameMode`（T005 产出，若未就绪用模板默认）
  - Default Pawn Class：`BP_VRPlayerPawn`（T005 产出，若未就绪用模板默认）
- 添加 `TextRenderActor` 标注关键尺寸（"20m"、"4m"、"出生点"等）
- 添加 `PlayerStart` 以外的 `TargetPoint` 作为武器生成位置（2 个，位于场地两侧）

## 验收清单

| # | 验收项 | 验证方式 |
|---|--------|----------|
| 1 | 关卡可在编辑器中打开 | 双击 `L_Prototype_1v1.umap` |
| 2 | 地面 20x20m，围墙 4m 高 | 编辑器测量工具 |
| 3 | 玩家出生点和 AI 出生点对称 | 编辑器坐标检查 |
| 4 | 掩体半身高（~1.2m），高台 1m 差 | 编辑器目视 |
| 5 | NavMesh 覆盖全部可行走区域 | `Show -> Navigation` 绿色覆盖 |
| 6 | 高台可通过斜坡到达 | NavMesh 连续性检查 |
| 7 | PIE 运行 >= 90fps | `stat fps` |
| 8 | 出生区 2m x 2m 无障碍 | 编辑器目视 |
| 9 | 灰盒材质正确（LevelPrototyping） | 编辑器目视 |

## 停止条件

- LevelPrototyping 素材缺失或损坏
- NavMesh 生成异常且无法修复
- PIE 性能低于 90fps 且无法通过简化几何体解决

## 回退

- 删除 `Content/VRSanguo/Dev/L_Prototype_1v1.umap`

## 报告路径

`.trae/execution/reports/tasks/M01-T005.md`
