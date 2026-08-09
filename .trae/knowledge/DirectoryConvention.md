# 目录规范

```text
VRSanguoYanWuchang/
├─ Config/
├─ Content/
├─ Plugins/
├─ Source/
├─ .trae/
│  ├─ README.md
│  ├─ CHANGELOG.md
│  ├─ governance/
│  ├─ rules/
│  ├─ knowledge/
│  ├─ standards/
│  ├─ vr/
│  ├─ systems/
│  ├─ execution/
│  ├─ tasks/
│  ├─ registers/
│  ├─ archive/
│  ├─ rules/
│  └─ skills/
│     └─ three-kingdoms-vr-arena/
│        └─ SKILL.md
├─ .gitattributes
├─ .gitignore
└─ VRSanguoYanWuchang.uproject
```

`.trae` 是规划、知识库、执行文档、AI 规则与历史审计资料的唯一目标根目录。项目唯一 Skill 位于 `.trae/skills/three-kingdoms-vr-arena/SKILL.md`，不在其他目录保存副本。`Build` 仅在存在项目构建脚本或平台资源时创建；当前为空，不保留。`Binaries`、`Intermediate`、`Saved`、`DerivedDataCache` 为 UE 自动生成目录，不纳入版本管理。

## Content 根目录

所有项目自有资源放在 `Content/VRSanguo`：

```text
Content/VRSanguo/
├─ Core/
├─ VR/
├─ Combat/
├─ Weapons/
├─ Characters/
├─ AI/
├─ Arena/
├─ UI/
├─ Audio/
├─ FX/
├─ Data/
├─ Maps/
├─ Developer/
└─ ThirdParty/
```

## 使用规则

- 不在 `Content` 根目录散放资源。
- 自制资源与第三方资源分开。
- 临时个人实验放入 `Developer/LocalExperiment`，按任务再建固定英文子目录。
- 第三方资源优先保持原包结构，放入 `ThirdParty/Vendor_Package`，目录名使用可追溯的供应商和资源包英文名。
- 地图集中放入 `Maps`，正式地图与测试地图分子目录。
- 插件只能放入工程级 `Plugins`，除非有明确理由修改引擎安装目录。
