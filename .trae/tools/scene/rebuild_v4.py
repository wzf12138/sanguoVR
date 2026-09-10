# rebuild_v4.py — L_Prototype_1v1_v4 校场单源生成脚本（M01-T005 v4，用户 2026-09-10 白天拍板）
# 变更（相对 v3）：场地 70→120m；将台 16x10x4→24x14x5（中央台阶 15 步+后服务坡道）；廊庑 10x5→26x7 柱廊式；
# 地面/墙体换直角 SM_Cube（ChamferCube 圆角在 17.5m 尺度产生可见缝+破洞，用户实测反馈）；旗杆加粗加底座；
# 门墙接缝搭接 20cm。四门依据《武经总要·讲武》"方一千二百步，四出为和门"（用户问询，已裁定保留）。
# 单一事实源：任何改动 = 改本脚本参数重跑，禁止在编辑器里手补单件。
# 运行前提：编辑器已切到空关卡 /Game/VRSanguo/Dev/L_Prototype_1v1_v4（由 bridge level.create 创建）。
# 单位：UE 厘米(cm)。布局：上北(+Y)下南(-Y)，玩家南、将台北（古典方位）。
import unreal

# ---------- 资产 ----------
MESH_SQUARE = '/Engine/BasicShapes/Cube'                     # 直角 1m 立方体（地面/墙/台阶，无圆角缝）
MESH_CHAMFER = '/Game/LevelPrototyping/Meshes/SM_ChamferCube'  # 圆角 1m 立方体（塔楼/旗面等独立道具）
MESH_RAMP   = '/Game/LevelPrototyping/Meshes/SM_Ramp'        # 1m 楔形（枢轴在角点；高端恒在枢轴侧）
MESH_POLE   = '/Game/LevelPrototyping/Meshes/SM_Cylinder'    # 1m 圆柱
MAT_GRID    = '/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray_02'

# ---------- 总体参数 ----------
GROUND_HALF   = 6000     # 地面 120x120m（用户拍板）
WALL_LINE     = 5970     # 墙体中心线 @±59.7m（内净空约 119m）
WALL_H        = 300      # 墙高 3m（维持）
WALL_T        = 50       # 墙厚 0.5m
SEG           = 600      # 墙段长 6m（120m 周长控制段数）
JT_X, JT_Y    = 0, 4400  # 将台中心（北侧，古典方位）
JT_W, JT_D    = 2400, 1400   # 将台 24x14m（用户拍板）
JT_H          = 500      # 将台高 5m（用户拍板）
STAIR_N       = 15       # 中央台阶 15 步（步高 33.3cm < NavMesh 35cm 步高限制）
STAIR_W       = 500      # 台阶宽 5m
STAIR_RUN     = 50       # 每步进深 0.5m（总进深 7.5m）
SRAMP_W       = 150      # 后服务坡道宽 1.5m
SRAMP_RUN     = 750      # 后服务坡道水平投影 7.5m（33.7° < 44° NavMesh）
SOUTH_GATE_W  = 1200     # 南主门 12m
SIDE_GATE_W   = 400      # 东西北辕门 4m
TOWER_POS     = 5200     # 望楼 @ (±52,±52)
GAL_X, GAL_Y  = 1950, -5600  # 廊庑中心（沿南墙内侧，主门两侧）26x7x4.5m
GAL_W, GAL_D, GAL_H = 2600, 700, 450
SPAWN_Y       = 2000     # 出生 ±20m（120m 场同步拉开）
POLE_H_S      = 500      # 军旗/五方旗杆高 5m
POLE_H_MAIN   = 800      # 对旗杆杆高 8m
SHUAI_H       = 1000     # 帅旗杆高 10m（随将台加高）

counts = {}
mat = unreal.load_asset(MAT_GRID)
mesh_square = unreal.load_asset(MESH_SQUARE)
mesh_chamfer = unreal.load_asset(MESH_CHAMFER)
mesh_ramp = unreal.load_asset(MESH_RAMP)
mesh_pole = unreal.load_asset(MESH_POLE)
for name, obj in (('MAT', mat), ('SQUARE', mesh_square), ('CHAMFER', mesh_chamfer), ('RAMP', mesh_ramp), ('POLE', mesh_pole)):
    if obj is None:
        unreal.log_warning('REBUILD_V4_ABORT missing asset %s' % name)
        raise RuntimeError('missing asset %s — 先核对资产路径' % name)
actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

# 幂等守卫：只允许在空关卡（<5 actor）运行
existing = actor_sub.get_all_level_actors()
if len(existing) >= 5:
    raise RuntimeError('level not empty (%d actors) — v4 生成只允许跑在空关卡' % len(existing))

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
    return spawn_mesh(label, loc, yaw, scale, mesh_square)   # v4：默认直角块（无圆角缝）

def prop(label, loc, yaw, scale):
    return spawn_mesh(label, loc, yaw, scale, mesh_chamfer)  # 独立道具保留圆角

def ramp(label, loc, yaw, scale):
    return spawn_mesh(label, loc, yaw, scale, mesh_ramp)

def pole(label, loc, scale_z, diameter=30.0):
    return spawn_mesh(label, (loc[0], loc[1], loc[2] + scale_z * 50), 0, (diameter / 100.0, diameter / 100.0, scale_z), mesh_pole)

def banner(label, x, y, pole_h, flag_w=150, flag_h=100, dia=15, base=True):
    """旗杆+底座+旗面块（挂杆顶，语义占位）。v4：杆加粗 15cm、加底座，旗不再'悬空'。"""
    if base:
        box(label + '_Base', (x, y, 15), 0, (0.6, 0.6, 0.3))
    pole(label + '_Pole', (x, y, 0), pole_h / 100.0, dia)
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

# ---------- 1. 地面（4×4 直角砖 30m + 兜底板）----------
# v3 教训沿用：整板在 VR 相机平视被吞 → 保持分块；v4 用户反馈"圆角砖有缝/见地下" → 换直角 SM_Cube，
# 30m 整数倍使 1m 网格贴图跨砖对齐无缝；底下加一整块兜底板（任何缝都看不到"地下"）。
# 30.4m（20cm 互埋）：直角块 30.0m 严丝对缝在 PIE 相机下仍有发丝级黑缝（x=0 中缝实测），
# 放大 20cm 互埋消除；网格贴图 20cm 错位不可见。
for _ix in range(-2, 2):
    for _iy in range(-2, 2):
        box('SM_FloorTile_%d_%d' % (_ix + 2, _iy + 2),
            (_ix * 3000.0 + 1500.0, _iy * 3000.0 + 1500.0, -10), 0, (30.4, 30.4, 0.2))
box('SM_Floor_Under', (0, 0, -27), 0, (121, 121, 0.1))

# ---------- 2. 围墙 + 四出辕门（四门规制：《武经总要·讲武》四出为和门）----------
def wall_line(side, base, gap_center, gap_w):
    n = 0
    for k in range(20):
        c = -WALL_LINE + SEG / 2.0 + k * SEG
        lo, hi = gap_center - gap_w / 2.0, gap_center + gap_w / 2.0
        in_gap = (c > lo - SEG / 2.0) and (c < hi + SEG / 2.0)
        if not in_gap:
            px = (base, c) if side in ('E', 'W') else (c, base)
            sc = (0.5, 6, 3) if side in ('E', 'W') else (6, 0.5, 3)
            box('SM_Wall_%s_%d' % (side, k), (px[0], px[1], WALL_H / 2.0), 0, sc)
            n += 1
    return n

counts['WALL_S'] = wall_line('S', -WALL_LINE, 0, SOUTH_GATE_W)
counts['WALL_N'] = wall_line('N', WALL_LINE, 0, SIDE_GATE_W)
counts['WALL_E'] = wall_line('E', WALL_LINE, 0, SIDE_GATE_W)
counts['WALL_W'] = wall_line('W', -WALL_LINE, 0, SIDE_GATE_W)
# 4m 门补缺段：门柱外缘(±250)到首墙段边(±630) 之间 380cm（直角块搭接，消"门墙空隙"）
for sgn in (1, -1):
    box('SM_Wall_Filler_N_%d' % (sgn + 2), (sgn * 440, WALL_LINE, 150), 0, (3.8, 0.5, 3))
    box('SM_Wall_Filler_E_%d' % (sgn + 2), (WALL_LINE, sgn * 440, 150), 0, (0.5, 3.8, 3))
    box('SM_Wall_Filler_W_%d' % (sgn + 2), (-WALL_LINE, sgn * 440, 150), 0, (0.5, 3.8, 3))

# 辕门：门柱+横梁（南主门 12m，其余 4m）
def yuamen(tag, gate_w, axis, gate_y):
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

yuamen('S', SOUTH_GATE_W, 'Y', -WALL_LINE)
yuamen('N', SIDE_GATE_W, 'Y', WALL_LINE)
yuamen('E', SIDE_GATE_W, 'X', WALL_LINE)
yuamen('W', SIDE_GATE_W, 'X', -WALL_LINE)

# ---------- 3. 将台（北侧 24x14x5m，中央台阶+后服务坡道，用户拍板）----------
box('SM_Jiangtai_Body', (JT_X, JT_Y, JT_H / 2.0), 0, (JT_W / 100.0, JT_D / 100.0, JT_H / 100.0))
# 正面中央大台阶（古制：正面居中登台；15 步 x 0.5m 进深，步高 33.3cm 可被 NavMesh 接受）
jt_front_y = JT_Y - JT_D / 2.0
for k in range(1, STAIR_N + 1):
    h = JT_H * k / float(STAIR_N)
    y_k = jt_front_y - (STAIR_N - k) * STAIR_RUN - STAIR_RUN / 2.0
    box('SM_Jiangtai_Step_%02d' % k, (0, y_k, h / 2.0), 0, (STAIR_W / 100.0, STAIR_RUN / 100.0, h / 100.0))
# 后服务坡道（北面居中，抬鼓运械；SM_Ramp 高端恒在枢轴侧：yaw=0 时枢轴=最高端，坡体向 +Y 下降）
ramp('SM_Jiangtai_Ramp_Service', (-SRAMP_W / 2.0, JT_Y + JT_D / 2.0, 0.0), 0, (SRAMP_W / 100.0, SRAMP_RUN / 100.0, JT_H / 100.0))
# 台顶护栏（前中央留 5m 台阶口，后中央留 1.5m 坡道口）
rail_h = 100
rail_z = JT_H + rail_h / 2.0
box('SM_Jiangtai_Rail_W', (JT_X - JT_W / 2.0 + 25, JT_Y, rail_z), 0, (0.5, JT_D / 100.0, rail_h / 100.0))
box('SM_Jiangtai_Rail_E', (JT_X + JT_W / 2.0 - 25, JT_Y, rail_z), 0, (0.5, JT_D / 100.0, rail_h / 100.0))
seg_w = (JT_W / 2.0 - STAIR_W / 2.0) / 100.0
box('SM_Jiangtai_Rail_S_W', (-(STAIR_W / 2.0 + seg_w * 50), jt_front_y + 25, rail_z), 0, (seg_w, 0.5, rail_h / 100.0))
box('SM_Jiangtai_Rail_S_E', (STAIR_W / 2.0 + seg_w * 50, jt_front_y + 25, rail_z), 0, (seg_w, 0.5, rail_h / 100.0))
rear_seg_w = (JT_W / 2.0 - SRAMP_W / 2.0) / 100.0
box('SM_Jiangtai_Rail_N_W', (-(SRAMP_W / 2.0 + rear_seg_w * 50), JT_Y + JT_D / 2.0 - 25, rail_z), 0, (rear_seg_w, 0.5, rail_h / 100.0))
box('SM_Jiangtai_Rail_N_E', (SRAMP_W / 2.0 + rear_seg_w * 50, JT_Y + JT_D / 2.0 - 25, rail_z), 0, (rear_seg_w, 0.5, rail_h / 100.0))
# 鼓台（3x3x0.6）+ 三面战鼓（圆柱 r0.4 h1.2 立放）+ 点将桌（3x1x1.1）
box('SM_Jiangtai_DrumDais', (JT_X - 700, JT_Y + 300, JT_H + 30), 0, (3, 3, 0.6))
for i, dx in enumerate((-100, 0, 100)):
    pole('SM_Drum_%d' % i, (JT_X - 700 + dx, JT_Y + 300, JT_H + 60), 1.2, 80)
box('SM_Jiangtai_Table', (JT_X + 500, JT_Y + 200, JT_H + 55), 0, (3, 1, 1.1))
# 帅旗杆 10m（台顶东南角）+ 大旗
pole('SM_Jiangtai_ShuaiFlag_Pole', (JT_X + 1000, JT_Y + 500, JT_H), SHUAI_H / 100.0, 40)
box('SM_Jiangtai_ShuaiFlag_Flag', (JT_X + 1000, JT_Y + 500, JT_H + SHUAI_H - 150), 0, (3, 2, 1.4))
text('Text_JIANGTAI', (JT_X, jt_front_y - 650, JT_H + 250), 'JIANGTAI 24x14x5m', 80, yaw=270)

# ---------- 4. 旗阵 ----------
# 五方旗一排（将台台阶前 y=+27m；避让北出生 y=+20m 与台阶基础 y=+29.5m）
for i, fx in enumerate((-2400, -1200, 0, 1200, 2400)):
    banner('SM_Flag_Wufang_%d' % i, fx, 2700, POLE_H_S, 180, 120)
# 南主门对旗杆台 ×2（台基立杆，廊庑北缘留 1m 净距）
for sgn, tag in ((1, 'E'), (-1, 'W')):
    box('SM_FlagStand_%s_Base' % tag, (sgn * 800, -5150, 25), 0, (2, 2, 0.5))
    pole('SM_FlagStand_%s_Pole' % tag, (sgn * 800, -5150, 50), POLE_H_MAIN / 100.0, 30)
    box('SM_FlagStand_%s_Flag' % tag, (sgn * 800, -5150, 50 + POLE_H_MAIN - 50), 0, (1.8, 2, 1.1))
# 围墙内沿军旗 ×16（南墙 4 避让廊庑/门洞，东西各 4 避让门/望楼，北墙 4）
edge = WALL_LINE - 200
wall_flag_slots = [(-4800, -edge), (-3600, -edge), (3600, -edge), (4800, -edge),
                   (-4800, edge), (-2400, edge), (2400, edge), (4800, edge),
                   (edge, -4200), (edge, -2100), (edge, 2100), (edge, 4200),
                   (-edge, -4200), (-edge, -2100), (-edge, 2100), (-edge, 4200)]
for i, (fx, fy) in enumerate(wall_flag_slots):
    banner('SM_Flag_Wall_%d' % i, fx, fy, POLE_H_S, 150, 100)

# ---------- 5. 四角望楼（箭塔造型：细高塔身+出挑战棚+护栏+旗）----------
def wanglou(tag, cx, cy):
    prop('SM_Wanglou_%s_Shaft' % tag, (cx, cy, 450), 0, (2, 2, 9))
    prop('SM_Wanglou_%s_Deck' % tag, (cx, cy, 925), 0, (3, 3, 0.5))
    for dx, dy, sx_, sy_ in ((0, 1.5, 3.2, 0.2), (0, -1.5, 3.2, 0.2), (1.5, 0, 0.2, 3.2), (-1.5, 0, 0.2, 3.2)):
        box('SM_Wanglou_%s_Rail' % tag, (cx + dx * 100, cy + dy * 100, 1000), 0, (sx_, sy_, 1))
    pole('SM_Wanglou_%s_FlagPole' % tag, (cx, cy, 950), 5.0, 30)
    box('SM_Wanglou_%s_Flag' % tag, (cx, cy, 1400), 0, (1.2, 2, 0.8))

for sx, tagx in ((1, 'E'), (-1, 'W')):
    for sy, tagy in ((1, 'N'), (-1, 'S')):
        wanglou('%s%s' % (tagx, tagy), sx * TOWER_POS, sy * TOWER_POS)

# ---------- 6. 南门廊庑（26x7x4.5m 柱廊式一对，用户拍板：三面墙+正面廊柱+顶盖）----------
for sgn, tag in ((1, 'E'), (-1, 'W')):
    cx = sgn * GAL_X
    box('SM_Gallery_%s_Back' % tag, (cx, GAL_Y - GAL_D / 2.0 + 25, GAL_H / 2.0), 0, (GAL_W / 100.0, 0.5, GAL_H / 100.0))
    box('SM_Gallery_%s_EndA' % tag, (cx - GAL_W / 2.0 + 25, GAL_Y, GAL_H / 2.0), 0, (0.5, GAL_D / 100.0, GAL_H / 100.0))
    box('SM_Gallery_%s_EndB' % tag, (cx + GAL_W / 2.0 - 25, GAL_Y, GAL_H / 2.0), 0, (0.5, GAL_D / 100.0, GAL_H / 100.0))
    box('SM_Gallery_%s_Roof' % tag, (cx, GAL_Y, GAL_H + 15), 0, (GAL_W / 100.0 + 0.5, GAL_D / 100.0 + 0.5, 0.3))
    for i in range(6):
        px = cx - GAL_W / 2.0 + 425 + i * 350
        pole('SM_Gallery_%s_Post_%d' % (tag, i), (px, GAL_Y + GAL_D / 2.0 - 45, 0), GAL_H / 100.0, 40)
    text('Text_GALLERY_%s' % tag, (cx, GAL_Y + 600, 250), ('EAST' if sgn > 0 else 'WEST') + ' GALLERY 26x7m', 60, yaw=90)

# ---------- 7. 标注（朝场内；白色）----------
text('Text_ARENA', (0, -1600, 50), 'DRILL GROUND 120m x 120m', 60, yaw=270)
text('Text_GATE_S', (0, -WALL_LINE + 150, 480), 'SOUTH GATE 12m', 70, yaw=90)
text('Text_GATE_N', (0, WALL_LINE - 70, 480), 'YUANMEN 4m', 50, yaw=270)

# ---------- 8. 出生 / 武器点 ----------
ps = actor_sub.spawn_actor_from_class(unreal.PlayerStart, unreal.Vector(0, -SPAWN_Y, 100), rot(90))
ps.set_actor_label('PlayerStart_South')
op = actor_sub.spawn_actor_from_class(unreal.TargetPoint, unreal.Vector(0, SPAWN_Y, 100), rot(-90))
op.set_actor_label('TargetPoint_Opponent_North')
for sgn, tag in ((1, 'E'), (-1, 'W')):
    wp = actor_sub.spawn_actor_from_class(unreal.TargetPoint, unreal.Vector(sgn * 1200, 0, 50), rot(0))
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
# 雾：淡蓝灰薄地霾。inscattering_luminance 缺省 (0,0,0) 纯黑（v1/v2"黑天"病根），必须显式给色。
fc.set_editor_property('fog_inscattering_luminance', unreal.LinearColor(0.55, 0.68, 0.85, 1.0))
fc.set_editor_property('fog_density', 0.0002)
fc.set_editor_property('fog_height_falloff', 0.4)
fc.set_editor_property('start_distance', 5000)
atm = actor_sub.spawn_actor_from_class(unreal.SkyAtmosphere, unreal.Vector(0, 0, 0), rot(0))
atm.set_actor_label('SkyAtmosphere_01')

# ---------- 9b. 天空球（抄官方模板 VRTemplateMap；本项目游戏路径不画大气通道）----------
# 配方详见 registry-changes 广播（2026-09-09）；几何体 BP_Sky_Sphere 两条渲染路径通吃。
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

# ---------- 10. NavMesh Bounds（120m 场）----------
nav = actor_sub.spawn_actor_from_class(unreal.NavMeshBoundsVolume, unreal.Vector(0, 0, 400), rot(0))
nav.set_actor_label('NavMeshBounds_130x130x8')
nav.set_actor_scale3d(unreal.Vector(65, 65, 4))

# ---------- 11. 保存 ----------
saved = unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
total = 0
for k in sorted(counts):
    print('COUNT %s = %d' % (k, counts[k]))
    total += counts[k]
print('TOTAL_PROPS %d' % total)
print('SAVE_RESULT %s' % saved)
print('REBUILD_V4_DONE')
