# rebuild_v3.py — L_Prototype_1v1_v3 校场单源生成脚本（M01-T005 v3 重建）
# 单一事实源：任何改动 = 改本脚本参数重跑，禁止在编辑器里手补单件。
# 运行前提：编辑器已切到空关卡 /Game/VRSanguo/Dev/L_Prototype_1v1_v3（由 bridge level.create 创建）。
# 单位：UE 厥米(cm)。布局：上北(+Y)下南(-Y)，玩家南、将台北（古典方位）。
import unreal

# ---------- 资产 ----------
MESH_CUBE = '/Game/LevelPrototyping/Meshes/SM_ChamferCube'   # 1m 立方体基模
MESH_RAMP = '/Game/LevelPrototyping/Meshes/SM_Ramp'          # 1m 楔形（+X 坡向升高）
MESH_POLE = '/Game/LevelPrototyping/Meshes/SM_Cylinder'      # 1m 圆柱
MAT_GRID  = '/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray_02'

# ---------- 总体参数 ----------
GROUND_HALF   = 3500     # 地面 70x70m
WALL_LINE     = 3470     # 墙体中心线 @±34.7m（内净空约 69m）
WALL_H        = 300      # 墙高 3m（用户拍板）
WALL_T        = 50       # 墙厚 0.5m
SEG           = 200      # 墙段长 2m
JT_X, JT_Y    = 0, 2600  # 将台中心（北侧，用户拍板）
JT_W, JT_D    = 1600, 1000   # 将台 16x10m
JT_H          = 400      # 将台高 4m
RAMP_W        = 300      # 坡道宽 3m
RAMP_RUN      = 800      # 坡道水平投影 8m（26.6° <= 44° NavMesh）
RAMP_X        = 600      # 坡道中心 x=±6m
SOUTH_GATE_W  = 1200     # 南主门 12m
SIDE_GATE_W   = 400      # 东西北辕门 4m
TOWER_POS     = 3300     # 角楼 @ (±33,±33)
HALL_Y        = -2900    # 南门廊庑
HALL_X        = 1100     # 廊庑中心 x=±11m
SPAWN_Y       = 1500     # 出生 ±15m（用户拍板）
FLAG_WALL_N   = 12       # 围墙内沿军旗数
POLE_H_S      = 600      # 军旗/五方旗杆高 6m
POLE_H_MAIN   = 800      # 主旗杆/帅旗杆高 8m

counts = {}
mat = unreal.load_asset(MAT_GRID)
mesh_cube = unreal.load_asset(MESH_CUBE)
mesh_ramp = unreal.load_asset(MESH_RAMP)
mesh_pole = unreal.load_asset(MESH_POLE)
for name, obj in (('MAT', mat), ('CUBE', mesh_cube), ('RAMP', mesh_ramp), ('POLE', mesh_pole)):
    if obj is None:
        unreal.log_warning('REBUILD_V3_ABORT missing asset %s' % name)
        raise RuntimeError('missing asset %s — 先核对资产路径' % name)
actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

# 幂等守卫：只允许在空关卡（<5 actor）运行
existing = actor_sub.get_all_level_actors()
if len(existing) >= 5:
    raise RuntimeError('level not empty (%d actors) — v3 生成只允许跑在空关卡' % len(existing))

def rot(yaw, pitch=0.0, roll=0.0):
    return unreal.Rotator(roll=roll, pitch=pitch, yaw=yaw)

def spawn_mesh(label, loc, yaw, scale, mesh):
    a = actor_sub.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(*loc), rot(yaw))
    a.set_actor_label(label)
    a.set_actor_scale3d(unreal.Vector(*scale))
    c = a.get_component_by_class(unreal.StaticMeshComponent)
    c.set_static_mesh(mesh)
    c.set_material(0, mat)
    counts[label.rsplit('_', 1)[0]] = counts.get(label.rsplit('_', 1)[0], 0) + 1
    return a

def box(label, loc, yaw, scale):
    return spawn_mesh(label, loc, yaw, scale, mesh_cube)

def ramp(label, loc, yaw, scale):
    return spawn_mesh(label, loc, yaw, scale, mesh_ramp)

def pole(label, loc, scale_z, diameter=30.0):
    return spawn_mesh(label, (loc[0], loc[1], loc[2] + scale_z * 50), 0, (diameter / 100.0, diameter / 100.0, scale_z), mesh_pole)

def banner(label, x, y, pole_h, flag_w=120, flag_h=80):
    """旗杆+灰盒旗面块（挂杆顶，语义占位）"""
    pole(label + '_Pole', (x, y, 0), pole_h / 100.0)
    box(label + '_Flag', (x, y, pole_h - flag_h / 2.0), 0, (flag_w / 100.0, 2, flag_h / 100.0))

def text(label, loc, txt, size, yaw=0.0):
    a = actor_sub.spawn_actor_from_class(unreal.TextRenderActor, unreal.Vector(*loc), rot(yaw))
    a.set_actor_label(label)
    c = a.get_component_by_class(unreal.TextRenderComponent)
    c.set_editor_property('text', txt)
    c.set_editor_property('world_size', float(size))
    c.set_editor_property('text_render_color', unreal.Color(255, 255, 255, 255))
    try:
        c.set_editor_property('horizontal_alignment', unreal.HorizTextAlignment.CENTER)
    except Exception:
        pass
    counts['TEXT'] = counts.get('TEXT', 0) + 1
    return a

# ---------- 1. 地面（4×4 分块，单块 17.5m）----------
# 2026-09-09 实测：70×70×0.1 整板在游戏视口（VR 相机、平视/掠射角）被整块吞黑，
# 低头 35° 或 SceneCapture 才可见；L_SkeletonTest 的 2m 密铺小砖全角度正常。
# 分块铺地是本项目已验证的正确模式。
for _ix in range(-2, 2):
    for _iy in range(-2, 2):
        box('SM_FloorTile_%d_%d' % (_ix + 2, _iy + 2),
            (_ix * 1750.0 + 875.0, _iy * 1750.0 + 875.0, -5), 0, (17.5, 17.5, 0.1))

# ---------- 2. 围墙 + 四出辕门 ----------
# 通用直线墙：axis 'X'（东/西墙，沿 Y 排）或 'Y'（南/北墙，沿 X 排），gap 段跳过
def wall_line(side, base, gap_center, gap_w):
    n = 0
    coord = -WALL_LINE + SEG / 2.0
    idx = 0
    while coord < WALL_LINE:
        c = coord + SEG / 2.0
        lo, hi = gap_center - gap_w / 2.0, gap_center + gap_w / 2.0
        in_gap = (c > lo - SEG / 2.0) and (c < hi + SEG / 2.0)
        if not in_gap:
            px = (base, c) if side in ('E', 'W') else (c, base)
            sc = (0.5, 2, WALL_H / 100.0) if side in ('E', 'W') else (2, 0.5, WALL_H / 100.0)
            box('SM_Wall_%s_%d' % (side, idx), (px[0], px[1], WALL_H / 2.0), 0, sc)
            n += 1
        idx += 1
        coord += SEG
    return n

counts['WALL_S'] = wall_line('S', -WALL_LINE, 0, SOUTH_GATE_W)
counts['WALL_N'] = wall_line('N', WALL_LINE, 0, SIDE_GATE_W)
counts['WALL_E'] = wall_line('E', WALL_LINE, 0, SIDE_GATE_W)
counts['WALL_W'] = wall_line('W', -WALL_LINE, 0, SIDE_GATE_W)

# 辕门：门柱+横梁（南主门 12m，其余 4m）
def yuamen(tag, base, gate_w, axis, gate_y):
    """axis='Y': 门在南北墙上（门洞沿 X 展开）；axis='X': 东西墙"""
    h = 420
    beam_len = gate_w + 2 * WALL_T
    if axis == 'Y':
        px = gate_w / 2.0 + WALL_T / 2.0
        box('SM_GatePost_%s_L' % tag, (-px, gate_y, h / 2.0), 0, (0.5, 0.5, h / 100.0))
        box('SM_GatePost_%s_R' % tag, (px, gate_y, h / 2.0), 0, (0.5, 0.5, h / 100.0))
        box('SM_GateBeam_%s' % tag, (0, gate_y, h + 15), 0, (beam_len / 100.0, 0.5, 30 / 100.0))
    else:
        py = gate_w / 2.0 + WALL_T / 2.0
        box('SM_GatePost_%s_L' % tag, (gate_y, -py, h / 2.0), 0, (0.5, 0.5, h / 100.0))
        box('SM_GatePost_%s_R' % tag, (gate_y, py, h / 2.0), 0, (0.5, 0.5, h / 100.0))
        box('SM_GateBeam_%s' % tag, (gate_y, 0, h + 15), 0, (0.5, beam_len / 100.0, 30 / 100.0))

yuamen('S', 0, SOUTH_GATE_W, 'Y', -WALL_LINE)
yuamen('N', 0, SIDE_GATE_W, 'Y', WALL_LINE)
yuamen('E', 0, SIDE_GATE_W, 'X', WALL_LINE)
yuamen('W', 0, SIDE_GATE_W, 'X', -WALL_LINE)

# ---------- 3. 将台（北侧，古典方位）----------
box('SM_Jiangtai_Body', (JT_X, JT_Y, JT_H / 2.0), 0, (JT_W / 100.0, JT_D / 100.0, JT_H / 100.0))
# 双坡道：从台前缘(南面 y=JT_Y-JT_D/2)向南延伸 8m，高端接台顶
# SM_Ramp 实测特性（2026-09-09 v3 修正）：网格枢轴在包围盒角点；坡向沿局部 Y（yaw=0 高端在局部 Y=0 侧
# ——v1 报告"+X 坡向"为错误假设）；yaw=180 时高端朝世界 +Y 接将台，且世界包围盒 = loc+([-宽,0],[-长,0],[0,高])
ramp_front_y = JT_Y - JT_D / 2.0
for sgn, tag in ((1, 'E'), (-1, 'W')):
    ramp('SM_Jiangtai_Ramp_%s' % tag, (sgn * RAMP_X + RAMP_W / 2.0, ramp_front_y, 0.0), 180, (RAMP_W / 100.0, RAMP_RUN / 100.0, JT_H / 100.0))
# 台顶三面护栏（南面开口进出台面：护栏沿东西+北缘）— 南面留坡道口两侧
rail_h = 100
for sgn, tag in ((1, 'E'), (-1, 'W')):
    box('SM_Jiangtai_Rail_%s' % tag, (sgn * (JT_W / 2.0 - 25), JT_Y, JT_H + rail_h / 2.0), 0, (0.5, JT_D / 100.0, rail_h / 100.0))
box('SM_Jiangtai_Rail_N', (JT_X, JT_Y + JT_D / 2.0 - 25, JT_H + rail_h / 2.0), 0, (JT_W / 100.0, 0.5, rail_h / 100.0))
# 帅旗杆（台顶中央）+ 鼓台
pole('SM_Jiangtai_ShuaiFlag_Pole', (JT_X, JT_Y + 100, JT_H), POLE_H_MAIN / 100.0, 40)
box('SM_Jiangtai_ShuaiFlag_Flag', (JT_X, JT_Y + 100, JT_H + POLE_H_MAIN - 50), 0, (2.4, 2, 1.4))
box('SM_Jiangtai_Drum', (JT_X - 500, JT_Y - 200, JT_H + 40), 0, (1.5, 1.5, 0.8))
text('Text_JIANGTAI', (JT_X, JT_Y - JT_D / 2.0 - 100, JT_H + 280), 'JIANGTAI / COMMAND PLATFORM H4m', 80, yaw=270)

# ---------- 4. 旗阵 ----------
# 五方旗一排（将台前 y=+11.5m，避开对手出生 ±15m 中轴点）
for i, fx in enumerate((-1200, -600, 0, 600, 1200)):
    banner('SM_Flag_Wufang_%d' % i, fx, 1150, POLE_H_S)
# 南主门对旗杆台 ×2（台基立杆；y=-33m 避开廊庑）
for sgn, tag in ((1, 'E'), (-1, 'W')):
    box('SM_FlagStand_%s_Base' % tag, (sgn * 800, -3300, 25), 0, (2, 2, 0.5))
    pole('SM_FlagStand_%s_Pole' % tag, (sgn * 800, -3300, 50), POLE_H_MAIN / 100.0, 40)
    box('SM_FlagStand_%s_Flag' % tag, (sgn * 800, -3300, 50 + POLE_H_MAIN - 50), 0, (1.8, 2, 1.1))
# 围墙内沿军旗 ×14（避开门洞/角楼/廊庑；南墙跳过 12m 门洞，东西墙跳过 4m 门）
edge = WALL_LINE - 200
wall_flag_slots = [(-2500, -edge), (-1000, -edge), (1000, -edge),
                   (-2500, edge), (-1000, edge), (1000, edge),
                   (edge, -2500), (edge, -1200), (edge, 1200), (edge, 2500),
                   (-edge, -2500), (-edge, -1200), (-edge, 1200), (-edge, 2500)]
for i, (fx, fy) in enumerate(wall_flag_slots):
    banner('SM_Flag_Wall_%d' % i, fx, fy, POLE_H_S)

# ---------- 5. 四角望楼（箭塔造型：细高塔身+出挑战棚+护栏+旗，用户拍板）----------
def wanglou(tag, cx, cy):
    box('SM_Wanglou_%s_Shaft' % tag, (cx, cy, 450), 0, (2, 2, 9))
    box('SM_Wanglou_%s_Deck' % tag, (cx, cy, 925), 0, (3, 3, 0.5))
    for dx, dy, sx_, sy_ in ((0, 1.5, 3.2, 0.2), (0, -1.5, 3.2, 0.2), (1.5, 0, 0.2, 3.2), (-1.5, 0, 0.2, 3.2)):
        box('SM_Wanglou_%s_Rail' % tag, (cx + dx * 100, cy + dy * 100, 1000), 0, (sx_, sy_, 1))
    pole('SM_Wanglou_%s_FlagPole' % tag, (cx, cy, 950), 5.0, 30)
    box('SM_Wanglou_%s_Flag' % tag, (cx, cy, 1400), 0, (1.2, 2, 0.8))

for sx, tagx in ((1, 'E'), (-1, 'W')):
    for sy, tagy in ((1, 'N'), (-1, 'S')):
        wanglou('%s%s' % (tagx, tagy), sx * TOWER_POS, sy * TOWER_POS)

# ---------- 6. 南门廊庑（演武厅 ×2）----------
for sgn, tag in ((1, 'E'), (-1, 'W')):
    box('SM_YanwuHall_%s' % tag, (sgn * HALL_X, HALL_Y, 175), 0, (10, 5, 3.5))
text('Text_YANWU_E', (HALL_X + 550, HALL_Y, 420), 'YANWU HALL', 60, yaw=270)
text('Text_YANWU_W', (-HALL_X - 550, HALL_Y, 420), 'YANWU HALL', 60, yaw=90)

# ---------- 7. 标注（朝场内：南北向文字面 +Y/-Y 用 yaw 90/270；白色）----------
text('Text_ARENA', (0, -900, 40), 'DRILL GROUND 70m x 70m', 40, yaw=270)
text('Text_GATE_S', (0, -WALL_LINE + 150, 480), 'SOUTH GATE 12m', 70, yaw=90)
text('Text_GATE_N', (0, WALL_LINE - 150, 480), 'YUANMEN 4m', 50, yaw=270)

# ---------- 8. 出生 / 武器点 ----------
ps = actor_sub.spawn_actor_from_class(unreal.PlayerStart, unreal.Vector(0, -SPAWN_Y, 100), rot(90))
ps.set_actor_label('PlayerStart_South')
op = actor_sub.spawn_actor_from_class(unreal.TargetPoint, unreal.Vector(0, SPAWN_Y, 100), rot(-90))
op.set_actor_label('TargetPoint_Opponent_North')
for sgn, tag in ((1, 'E'), (-1, 'W')):
    wp = actor_sub.spawn_actor_from_class(unreal.TargetPoint, unreal.Vector(sgn * 1000, 0, 50), rot(0))
    wp.set_actor_label('TargetPoint_Weapon_%s' % tag)

# ---------- 9. 光照（蓝天+薄雾）----------
sun = actor_sub.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0, 0, 3000), rot(0, -38.0, 0))
sun.set_actor_label('DirectionalLight_Sun')
sc = sun.get_component_by_class(unreal.DirectionalLightComponent)
sc.set_editor_property('intensity', 10.0)
sc.set_editor_property('use_temperature', True)
sc.set_editor_property('temperature', 5600.0)
sc.set_editor_property('light_source_angle', 1.0)
sc.set_editor_property('atmosphere_sun_light', True)
for i, nm in enumerate(('SkyLight_Ambient', 'SkyLight_01')):
    sl = actor_sub.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(2000 + i * 500, 0, 3000), rot(0))
    sl.set_actor_label(nm)
    slc = sl.get_component_by_class(unreal.SkyLightComponent)
    slc.set_editor_property('intensity', 0.8)
    slc.set_editor_property('real_time_capture', True)
fog = actor_sub.spawn_actor_from_class(unreal.ExponentialHeightFog, unreal.Vector(-2000, 0, 0), rot(0))
fog.set_actor_label('ExponentialHeightFog_01')
fc = fog.get_component_by_class(unreal.ExponentialHeightFogComponent)
# 雾：淡蓝灰薄地霾。注意：inscattering_luminance 缺省为 (0,0,0) 纯黑 —— 黑雾会在天空距离
# 100% 覆盖大气（黑天）并吞掉贴地低层（地面远处变黑），v1/v2 "黑天" 病根即此，必须显式给色。
fc.set_editor_property('fog_inscattering_luminance', unreal.LinearColor(0.55, 0.68, 0.85, 1.0))
fc.set_editor_property('fog_density', 0.0002)
fc.set_editor_property('fog_height_falloff', 0.4)
fc.set_editor_property('start_distance', 5000)
atm = actor_sub.spawn_actor_from_class(unreal.SkyAtmosphere, unreal.Vector(0, 0, 0), rot(0))
atm.set_actor_label('SkyAtmosphere_01')

# ---------- 9b. 天空球（2026-09-09 依用户指示抄官方模板 VRTemplateMap） ----------
# 关键发现：本项目游戏渲染路径不画 SkyAtmosphere 通道（PIE 与离屏捕获天空均黑；官方模板里
# 根本没有大气组件），天空必须用几何体 BP_Sky_Sphere（/Engine/EngineSky/，模板同款）。
# 参数抄自 VRTemplateMap 的 SkySpherePC2；Sun Height=sin(太阳仰角 38°)≈0.616。
skysphere = actor_sub.spawn_actor_from_class(
    unreal.load_asset('/Engine/EngineSky/BP_Sky_Sphere').generated_class(),
    unreal.Vector(0, 0, 0), rot(0))
skysphere.set_actor_label('SkySphere_Template')
skysphere.set_editor_property('Sun Height', 0.616)
skysphere.set_editor_property('Sun Brightness', 50.0)
skysphere.set_editor_property('Stars Brightness', 0.1)
skysphere.set_editor_property('Cloud Color', unreal.LinearColor(0.855778, 0.919020, 1.0, 1.0))
skysphere.set_editor_property('Horizon Color', unreal.LinearColor(1.979559, 2.586644, 3.0, 1.0))
skysphere.set_editor_property('Zenith Color', unreal.LinearColor(0.034046, 0.109247, 0.295, 1.0))
skysphere.set_editor_property('Overall Color', unreal.LinearColor(1.0, 1.0, 1.0, 1.0))
skysphere.call_method('RefreshMaterial', args=())

# ---------- 10. NavMesh Bounds ----------
nav = actor_sub.spawn_actor_from_class(unreal.NavMeshBoundsVolume, unreal.Vector(0, 0, 400), rot(0))
nav.set_actor_label('NavMeshBounds_80x80x8')
nav.set_actor_scale3d(unreal.Vector(40, 40, 4))

# ---------- 11. 保存 ----------
saved = unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
total = 0
for k in sorted(counts):
    print('COUNT %s = %d' % (k, counts[k]))
    total += counts[k]
print('TOTAL_PROPS %d' % total)
print('SAVE_RESULT %s' % saved)
print('REBUILD_V3_DONE')
