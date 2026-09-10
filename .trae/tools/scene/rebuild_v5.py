# rebuild_v5.py — L_Prototype_1v1_v5 校场单源生成脚本（M01-T005；v5.2 旗侧挂/鼓落台面/Docs；v5.3 坛面台阶修复；v5.4 旗统一东风+扁旗面；v5.5 坛厅分离/靶场重排/文档 HTML+实测俯视图；v5.6 圆草靶/北辕门撤除/平面图实测 bounds；v5.6b 鼓亭落地/两翼敞棚/md 恢复；v5.7 靶薄盘+红心贴面/东踏步撤除/廊庑功能化）
# v5 = v4 底座 + 史料升级：主坛三层退台（平乐观/拜将坛坛制）、鼓亭×2（亲执枹鼓）、演武厅（唐阅武厅宋演武亭）、
# 靶场+锦袍杆（铜雀台夺袍射红心）、碑石×2（拜将坛台脚立碑）、牌坊（演武场'部分设牌坊'）、跑马道净空（旗上墙顶）。
# **关键修复史**：SM_Cylinder 枢轴在底面（bounds z 0..100 实测），pole() 不再加半高偏移——v1~v4 旗杆/廊柱/鼓全部悬空半高；
# 墙段跳段判据=段体与开口相交(留 30cm 侵入)才跳——v4 南主门两侧各 5.7m 墙洞的根因。
# 文档：Docs/Scene 四件套由 MODULES 登记表自动生成（单源机制，防文档失联）。
# 单源：任何改动=改本脚本重跑；运行前提：编辑器已切到空关卡 /Game/VRSanguo/Dev/L_Prototype_1v1_v5。
import unreal

# ---------- 资产 ----------
MESH_SQUARE = '/Engine/BasicShapes/Cube'                      # 直角 1m 立方体（中心枢轴，bounds -50..50）
MESH_CHAMFER = '/Game/LevelPrototyping/Meshes/SM_ChamferCube' # 圆角块（独立道具）
MESH_RAMP   = '/Game/LevelPrototyping/Meshes/SM_Ramp'         # 楔形（角点枢轴 0..100，高端在枢轴侧）
MESH_POLE   = '/Game/LevelPrototyping/Meshes/SM_Cylinder'     # 圆柱（底面枢轴，bounds z 0..100）
MAT_GRID    = '/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray_02'

# ---------- 总体参数 ----------
GROUND_HALF   = 6000     # 120x120m
WALL_LINE     = 5970
WALL_H, WALL_T, SEG = 300, 50, 600
T1_W, T1_D, T1_H = 2400, 1250, 170   # 一层 24x12.5x1.7 @4100（南立面 3475：B 段台阶 250cm 坛面进深；北立面 4725 距演武厅 4.25m——v5.5 南移修"坛厅堆一起"）
T2_W, T2_D, T2_H = 1800, 1000, 340   # 二层 18x10x3.4 @4225（北立面与一层齐 4725）
T3_W, T3_D, T3_H = 1200, 600, 500    # 三层 12x6x5.0 @4325
T1_Y = 4100
STEP_N, STEP_W, STEP_RUN = 5, 500, 50  # 每段 5 步 x 0.34m（15 步到顶）
SRAMP_W, SRAMP_RUN = 150, 750        # 后服务坡道 1.5m x 7.5m（穿演武厅中央通道）
SOUTH_GATE_W, SIDE_GATE_W = 1200, 400
TOWER_POS     = 5200
GAL_X, GAL_Y  = 1950, -5600
GAL_W, GAL_D, GAL_H = 2600, 700, 450
HALL_W2, HALL_PASS, HALL_D, HALL_H = 700, 200, 800, 550  # 演武厅双翼各 7m 深/中央通道 2m/进深 8m/高 5.5m
SPAWN_Y       = 2000
POLE_H_S, POLE_H_MAIN, SHUAI_H = 500, 800, 1000

counts = {}
mat = unreal.load_asset(MAT_GRID)

def _make_colored_mat(name, rgb):
    """靶场专用着色材质（麦秆靶面/正红红心）：灰盒唯一着色件——西墙背光带里也能一眼读出'这是靶子'。
    幂等：已存在则直接加载。MaterialEditingLibrary 无 create_material（5.8 移除）→ 走 AssetTools+MaterialFactoryNew。"""
    mil = unreal.MaterialEditingLibrary
    path = '/Game/VRSanguo/Dev/' + name
    m = unreal.load_asset(path)
    if m is None:
        tools = unreal.AssetToolsHelpers.get_asset_tools()
        m = tools.create_asset(name, '/Game/VRSanguo/Dev', unreal.Material, unreal.MaterialFactoryNew())
        expr = mil.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -400, 0)
        expr.set_editor_property('constant', unreal.LinearColor(rgb[0], rgb[1], rgb[2], 1.0))
        mil.connect_material_property(expr, '', unreal.MaterialProperty.MP_BASE_COLOR)
        e2 = mil.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -400, 220)
        e2.set_editor_property('constant', unreal.LinearColor(rgb[0] * 0.35, rgb[1] * 0.35, rgb[2] * 0.35, 1.0))
        mil.connect_material_property(e2, '', unreal.MaterialProperty.MP_EMISSIVE_COLOR)
        mil.recompile_material(m)
        unreal.EditorAssetLibrary.save_loaded_asset(m)
    return m

mat_straw = _make_colored_mat('M_GrayBox_Straw', (0.83, 0.72, 0.42))   # 草靶麦秆色
mat_red   = _make_colored_mat('M_GrayBox_Red',   (0.78, 0.10, 0.08))   # 红心正红
mesh_square = unreal.load_asset(MESH_SQUARE)
mesh_chamfer = unreal.load_asset(MESH_CHAMFER)
mesh_ramp = unreal.load_asset(MESH_RAMP)
mesh_pole = unreal.load_asset(MESH_POLE)
mesh_sphere = unreal.load_asset('/Engine/BasicShapes/Sphere')
for name, obj in (('MAT', mat), ('SQUARE', mesh_square), ('CHAMFER', mesh_chamfer), ('RAMP', mesh_ramp), ('POLE', mesh_pole), ('SPHERE', mesh_sphere)):
    if obj is None:
        unreal.log_warning('REBUILD_V5_ABORT missing asset %s' % name)
        raise RuntimeError('missing asset %s' % name)
actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
existing = actor_sub.get_all_level_actors()
if len(existing) >= 5:
    raise RuntimeError('level not empty (%d actors) - v5 only runs on an empty level' % len(existing))

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
    return spawn_mesh(label, loc, yaw, scale, mesh_square)

def prop(label, loc, yaw, scale):
    return spawn_mesh(label, loc, yaw, scale, mesh_chamfer)

def ramp(label, loc, yaw, scale):
    return spawn_mesh(label, loc, yaw, scale, mesh_ramp)

def pole(label, loc, height, diameter=30.0):
    """SM_Cylinder 底面枢轴（bounds z 0..100）：loc.z=杆底，向上长 height。v1~v4 悬空 bug 的修复。"""
    return spawn_mesh(label, (loc[0], loc[1], loc[2]), 0, (diameter / 100.0, diameter / 100.0, height / 100.0), mesh_pole)

def disc(label, loc, dia, thickness, mat_override=None, yaw=0):
    """立式圆盘（SM_Sphere 非均匀缩放成透镜盘）。缩放 (dia, thick, dia) 的扁轴=Y：yaw=0 时圆面朝南北，
    **yaw=90 才朝东西**（v5.7 实锤：v5.6 注释误写"圆面朝东西"，靶面侧对射手——用户特写看到的"蛋"
    就是 8cm 盘的边缘透镜轮廓；yaw 旋转在本构建完全正常，v5.6 只是不敢用）。
    pitch 旋转缺陷记录不变：StaticMeshActor pitch 旋转六法实测全败（渲染恒为水平盘），立式仍靠 Z 缩放。
    枢轴=球心（loc 即盘心）。"""
    a = spawn_mesh(label, loc, yaw, (dia / 200.0, thickness / 100.0, dia / 200.0), mesh_sphere)
    if mat_override is not None:
        a.get_component_by_class(unreal.StaticMeshComponent).set_material(0, mat_override)
    return a

def banner(label, x, y, pole_h, flag_w=150, flag_h=100, dia=15, base=True, base_z=0.0, face='+X'):
    """旗：杆 + 扁平侧挂旗面（厚度 6cm，不再用厚盒子——用户 v5.3 反馈"正常的旗帜是扁的"）。
    face: 旗面伸出方向。v5.4 起全场景统一 '+X'（东风），东墙旗杆内移使旗面仍在场内。"""
    if base:
        box(label + '_Base', (x, y, base_z + 15), 0, (0.6, 0.6, 0.3))
    pole(label + '_Pole', (x, y, base_z), pole_h, dia)
    dx, dy = {'+X': (1, 0), '-X': (-1, 0), '+Y': (0, 1), '-Y': (0, -1)}[face]
    fx = x + dx * (flag_w / 2.0 + 10)
    fy = y + dy * (flag_w / 2.0 + 10)
    fz = base_z + pole_h - flag_h / 2.0
    if dy == 0:
        box(label + '_Flag', (fx, fy, fz), 0, (flag_w / 100.0, 0.06, flag_h / 100.0))
    else:
        box(label + '_Flag', (fx, fy, fz), 0, (0.06, flag_w / 100.0, flag_h / 100.0))

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

# ---------- 1. 地面（4×4 直角砖 30.4m 互埋 + 兜底板）----------
for _ix in range(-2, 2):
    for _iy in range(-2, 2):
        box('SM_FloorTile_%d_%d' % (_ix + 2, _iy + 2),
            (_ix * 3000.0 + 1500.0, _iy * 3000.0 + 1500.0, -10), 0, (30.4, 30.4, 0.2))
box('SM_Floor_Under', (0, 0, -27), 0, (121, 121, 0.1))

# ---------- 2. 围墙 + 三出辕门（v5.6：北辕门撤除——厅背对门的"门"无人能用=纯缺陷；
# 北端由演武厅收尾，合"北堂南向"通制。跳段判据：gap_w<=0 视为无门）----------
def wall_line(side, base, gap_center, gap_w):
    # 跳段判据（v4 缺陷修正）：段体与开口（留 30cm 侵入余量）相交才跳。
    # 南主门 12m：v4 的旧判据把 ±870 两段也跳掉 → 门两侧各留 5.7m 墙洞；v5 判据下 ±570..±1170 段照建。
    for k in range(20):
        c = -WALL_LINE + SEG / 2.0 + k * SEG
        lo, hi = gap_center - gap_w / 2.0, gap_center + gap_w / 2.0
        seg_lo, seg_hi = c - SEG / 2.0, c + SEG / 2.0
        skip = gap_w > 0 and (seg_hi > lo + 30 and seg_lo < hi - 30)
        if not skip:
            px = (base, c) if side in ('E', 'W') else (c, base)
            sc = (0.5, 6, 3) if side in ('E', 'W') else (6, 0.5, 3)
            box('SM_Wall_%s_%d' % (side, k), (px[0], px[1], WALL_H / 2.0), 0, sc)

wall_line('S', -WALL_LINE, 0, SOUTH_GATE_W)
wall_line('N', WALL_LINE, 0, 0)
wall_line('E', WALL_LINE, 0, SIDE_GATE_W)
wall_line('W', -WALL_LINE, 0, SIDE_GATE_W)
for sgn in (1, -1):
    box('SM_Wall_Filler_E_%d' % (sgn + 2), (WALL_LINE, sgn * 440, 150), 0, (0.5, 3.8, 3))
    box('SM_Wall_Filler_W_%d' % (sgn + 2), (-WALL_LINE, sgn * 440, 150), 0, (0.5, 3.8, 3))

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
yuamen('E', SIDE_GATE_W, 'X', WALL_LINE)
yuamen('W', SIDE_GATE_W, 'X', -WALL_LINE)

# ---------- 3. 南门牌坊（两柱一梁，演武场"部分设牌坊"）----------
for sgn in (1, -1):
    pole('SM_Arch_Paifang_Post_%d' % (sgn + 2), (sgn * 480, -WALL_LINE, 0), 600, 50)
box('SM_Arch_Paifang_Beam', (0, -WALL_LINE, 630), 0, (10, 0.5, 60 / 100.0))

# ---------- 4. 主坛：三层退台（平乐观/拜将坛坛制；北移让出南向登台进深）----------
box('SM_Jiangtai_Tier1', (0, T1_Y, T1_H / 2.0), 0, (T1_W / 100.0, T1_D / 100.0, T1_H / 100.0))
box('SM_Jiangtai_Tier2', (0, 4225, (T1_H + T2_H) / 2.0), 0, (T2_W / 100.0, T2_D / 100.0, (T2_H - T1_H) / 100.0))
box('SM_Jiangtai_Tier3', (0, 4325, (T2_H + T3_H) / 2.0), 0, (T3_W / 100.0, T3_D / 100.0, (T3_H - T2_H) / 100.0))

# 三段登台台阶（每段 5 步 x 0.34m，步高 < NavMesh 35cm 限制；每段必须完全落在承载面上）
def stair_segment(tag, base_z, face_y, width):
    for k in range(1, STEP_N + 1):
        h = T3_H * k / 15.0
        y = face_y - (STEP_N - k) * STEP_RUN - STEP_RUN / 2.0
        box('SM_Jiangtai_Step_%s_%02d' % (tag, k), (0, y, base_z + h / 2.0), 0,
            (width / 100.0, STEP_RUN / 100.0, h / 100.0))
stair_segment('A', 0.0, T1_Y - T1_D / 2.0, 500)   # 地面 -> 一层顶 1.7m（贴一层南立面 3475）
stair_segment('B', T1_H, 3725, 300)               # 一层顶 -> 二层顶 3.4m @ 3725（全落在坛面 3475..4725）
stair_segment('C', T2_H, 4025, 300)               # 二层顶 -> 三层顶 5.0m @ 4025

# v5.7（用户"将台侧边突然多了个楼梯，怎么引入"）：东侧翼服务踏步整体撤除——v5.5 为还厅内通道设的服务线
# 在灰盒里读作"多余侧梯"，服务动线归并南主台阶（主台阶独用）。三层顶东侧护栏恢复整段。

# 三层顶护栏（南留 C 段台阶口，西/北/东整段）
rail_z = T3_H + 50
box('SM_Jiangtai_Rail_W', (-575, 4325, rail_z), 0, (0.5, 5, 1))
box('SM_Jiangtai_Rail_E', (575, 4325, rail_z), 0, (0.5, 5, 1))
box('SM_Jiangtai_Rail_S_W', (-375, 4050, rail_z), 0, (4.5, 0.5, 1))
box('SM_Jiangtai_Rail_S_E', (375, 4050, rail_z), 0, (4.5, 0.5, 1))
box('SM_Jiangtai_Rail_N', (0, 4600, rail_z), 0, (11, 0.5, 1))

# 鼓亭×2（坛脚地面东西两侧；平乐观"亲执枹鼓"；
# v5.5b：从坛面窄条移到坛脚——原来挡住坛东窄条服务踏步的通行路线，寻路测试暴露）
# v5.6b（用户截图"两个鼓亭悬空"实锤）：v5.3 移位时 z 基准漏改——柱/板/架/鼓全套仍按坛面基准 T1_H 起建，
# 整亭浮空 1m。现全部落地：柱底 0、鼓架 0..90、鼓坐架上 90..180、柱加粗 40。
for sgn, tag in ((1, 'E'), (-1, 'W')):
    bx, by = sgn * 1500, 3850
    for dx in (-75, 75):
        for dy in (-75, 75):
            pole('SM_DrumPavilion_%s_Post_%d%d' % (tag, dx // 75 + 2, dy // 75 + 2), (bx + dx, by + dy, 0), 260, 40)
    box('SM_DrumPavilion_%s_CapA' % tag, (bx, by, 270), 0, (2.2, 2.2, 0.2))
    box('SM_DrumPavilion_%s_CapB' % tag, (bx, by, 300), 0, (1.4, 1.4, 0.2))
    box('SM_DrumPavilion_%s_Stand' % tag, (bx, by, 45), 0, (0.5, 0.5, 0.9))
    pole('SM_DrumPavilion_%s_Drum' % tag, (bx, by, 90), 100, 90)

# 三层顶：三面战鼓直接落台面（不垫鼓台——用户反馈"鼓太高/与护栏重叠"；点位避开西护栏 125cm）
for i, dx in enumerate((-450, -300, -150)):
    pole('SM_Drum_%d' % i, (dx, 4425, T3_H), 110, 80)
box('SM_Jiangtai_Table', (350, 4375, T3_H + 55), 0, (3, 1, 1.1))
pole('SM_Jiangtai_ShuaiFlag_Pole', (500, 4525, T3_H), SHUAI_H, 40)
box('SM_Jiangtai_ShuaiFlag_Flag', (500 + 160, 4525, T3_H + SHUAI_H - 150), 0, (3, 0.06, 1.4))  # 东风统一

# 碑石×2（拜将坛制：台脚东西立碑）
for sgn, tag in ((1, 'E'), (-1, 'W')):
    box('SM_Stele_%s' % tag, (sgn * 1300, 4150, 130), 0, (1, 0.4, 2.6))
text('Text_JIANGTAI', (0, 3050, 750), 'JIANGTAI 24x12.5x5m 3-TIER', 80, yaw=270)

# ---------- 5. 演武厅（北厅南场；两翼=将佐观武敞棚）----------
# 考据（2026-09-10 已补验在线检索，搜索栈恢复）：唐已有"阅武堂"、宋称"演武亭/大教场"（演武场/演武厅百科词条，
# 核心设施=阅兵台/旗杆台/合院建筑）；"北端面南"通制说法未逐条核到原文，如实标注。
# v5.6b（用户"半封闭小房间看不懂"）：两翼 5.5m 高实墙房改 1.2m 矮墙敞棚（看棚/廊庑式样）+ 翼内长案（将佐观武席）
# + TEXT 标注；柱列 3→6 根贴顶板（原 3 柱顶 520 与顶板底 550 脱空 30cm，一并修正为 550 贴合）。
for sgn, tag in ((1, 'E'), (-1, 'W')):
    cx_edge = sgn * HALL_PASS / 2.0
    wx = sgn * (HALL_PASS / 2.0 + HALL_W2 / 2.0)
    box('SM_Hall_%s_Back' % tag, (wx, 5925, 60), 0, (HALL_W2 / 100.0, 0.5, 1.2))
    box('SM_Hall_%s_Side_Out' % tag, (sgn * 800, 5550, 60), 0, (0.5, HALL_D / 100.0, 1.2))
    box('SM_Hall_%s_Side_In' % tag, (cx_edge + sgn * 25, 5550, 60), 0, (0.5, HALL_D / 100.0, 1.2))
    for i in range(6):
        px = sgn * (225 + (i % 3) * 225)
        py = 5175 if i < 3 else 5875
        pole('SM_Hall_%s_Post_%d' % (tag, i), (px, py, 0), 550, 40)
    box('SM_Hall_%s_Table' % tag, (wx, 5600, 45), 0, (3.5, 1.0, 0.9))
    box('SM_Hall_%s_Roof' % tag, (wx, 5550, HALL_H + 15), 0, (HALL_W2 / 100.0 + 0.5, HALL_D / 100.0 + 0.5, 0.3))
box('SM_Hall_Lintel', (0, 5175, 430), 0, (16, 0.5, 80 / 100.0))
text('Text_HALL', (0, 5060, 500), 'REVIEW HALL 16x8m', 60, yaw=270)
text('Text_HALL_WING_E', (450, 5060, 250), 'E-WING STAND', 45, yaw=270)
text('Text_HALL_WING_W', (-450, 5060, 250), 'W-WING STAND', 45, yaw=270)

# ---------- 6. 靶场（西墙内侧；铜雀台比射红心）+ 锦袍杆（夺袍彩头锚点）----------
# v5.6（用户"靶子不像靶子/正常靶子是圆的"）：圆草靶制——木桩+直径1.3m 圆草靶盘+直径0.4m 红心圆盘（桩穿盘安装）。
# 靶位东移出墙影区（太阳西照，墙投影带实测远超 4m 估算——射位线视角复核定案）；靶面麦秆色/红心正红，
# 灰盒唯一着色件，背光也一眼读出"这是靶子"。
# 考据标注（2026-09-10 已补验在线检索，搜索栈恢复）：WA 标准圆靶 dia122cm、靶雏形为草垛、稻草加麻布厚 15-25cm
# （好物爆料/快懂百科词条）；本场 dia130×30 与标准吻合。射礼古制"侯"为方形布靶，明以降通行圆毡/草靶；
# 项目取圆靶（用户拍板方向）。
for i, ty in enumerate((900, 1800, 2700)):
    pole('SM_Target_%d_Stake' % i, (-5415, ty, 0), 260, 25)          # 木桩（穿透靶盘，接触保证）
    disc('SM_Target_%d_Face' % i, (-5400, ty, 160), 130, 8, mat_straw, yaw=90)   # 靶盘 dia130 厚8 面朝东（对射手）
    disc('SM_Target_%d_Heart' % i, (-5393.5, ty, 160), 40, 3, mat_red, yaw=90)   # 红心 dia40 厚3 贴面凸2cm
    box('SM_Target_Lane_%d' % i, (-4900, ty, 5), 0, (14, 0.1, 0.1))  # 射道标线：棚口延伸到靶前
for sx in (-4750, -4550):
    for sy in (1400, 2200):
        pole('SM_Target_Shed_Post_%d_%d' % ((sx + 4750) // 200, (sy - 1400) // 800), (sx, sy, 0), 300, 30)
box('SM_Target_Shed_Roof', (-4650, 1800, 310), 0, (3, 9, 0.25))
pole('SM_JinPao_Pole', (-4600, 3300, 0), 800, 30)
box('SM_JinPao_Base', (-4600, 3300, 20), 0, (1.5, 1.5, 0.4))
box('SM_JinPao_Robe', (-4600, 3300, 690), 0, (1.2, 0.15, 1.8))  # 挂袍式（夺袍彩头）
text('Text_TARGETS', (-4350, 1800, 30), 'ARCHERY RANGE / PRIZE ROBE JINPAO', 50, yaw=0)

# ---------- 7. 旗阵（v5.4：全场景统一东风 +X；旗面 6cm 扁板）----------
for i, fx in enumerate((-2400, -1200, 0, 1200, 2400)):
    banner('SM_Flag_Wufang_%d' % i, fx, 2700, POLE_H_S, 180, 120, face='+X')
for sgn, tag in ((1, 'E'), (-1, 'W')):
    box('SM_FlagStand_%s_Base' % tag, (sgn * 800, -4900, 25), 0, (2, 2, 0.5))
    pole('SM_FlagStand_%s_Pole' % tag, (sgn * 800, -4900, 50), POLE_H_MAIN, 30)
    box('SM_FlagStand_%s_Flag' % tag, (sgn * 800 + 100, -4900, 50 + POLE_H_MAIN - 50), 0, (1.8, 0.06, 1.1))  # 东风统一
edge = WALL_LINE
wall_flag_slots = [(-4800, -edge), (-3600, -edge), (3600, -edge), (4800, -edge),
                   (-4800, edge), (-2400, edge), (2400, edge), (4800, edge),
                   (edge, -4200), (edge, -2100), (edge, 2100), (edge, 4200),
                   (-edge, -4200), (-edge, -2100), (-edge, 2100), (-edge, 4200)]
for i, (fx, fy) in enumerate(wall_flag_slots):
    # v5.5：全部旗回墙顶、统一东风 +X（修"落地旗"——上一轮东墙杆落地是错误方案）。
    # 东墙旗杆立墙顶、旗面飘出墙外上空（城楼旗式样，z700+ 高于 3m 墙顶，场内外均可见）。
    banner('SM_Flag_Wall_%d' % i, fx, fy, POLE_H_S, 150, 100, base_z=WALL_H, face='+X')

# ---------- 8. 四角望楼 ----------
def wanglou(tag, cx, cy):
    prop('SM_Wanglou_%s_Shaft' % tag, (cx, cy, 450), 0, (2, 2, 9))
    prop('SM_Wanglou_%s_Deck' % tag, (cx, cy, 925), 0, (3, 3, 0.5))
    for dx, dy, sx_, sy_ in ((0, 1.5, 3.2, 0.2), (0, -1.5, 3.2, 0.2), (1.5, 0, 0.2, 3.2), (-1.5, 0, 0.2, 3.2)):
        box('SM_Wanglou_%s_Rail' % tag, (cx + dx * 100, cy + dy * 100, 1000), 0, (sx_, sy_, 1))
    pole('SM_Wanglou_%s_FlagPole' % tag, (cx, cy, 950), 500, 30)
    box('SM_Wanglou_%s_Flag' % tag, (cx + 70, cy, 1400), 0, (1.2, 0.06, 0.8))  # 东风统一（不穿杆）

for sx, tagx in ((1, 'E'), (-1, 'W')):
    for sy, tagy in ((1, 'N'), (-1, 'S')):
        wanglou('%s%s' % (tagx, tagy), sx * TOWER_POS, sy * TOWER_POS)

# ---------- 9. 南门廊庑（26x7x4.5m 柱廊一对；v5.7 功能化——用户"以为是马厩"：空廊读不出功能，
# 加长凳×3+兵器架×1+标注 ARMORY，语义=兵士整备/列队/遮阳候命廊）----------
for sgn, tag in ((1, 'E'), (-1, 'W')):
    cx = sgn * GAL_X
    box('SM_Gallery_%s_Back' % tag, (cx, GAL_Y - GAL_D / 2.0 + 25, GAL_H / 2.0), 0, (GAL_W / 100.0, 0.5, GAL_H / 100.0))
    box('SM_Gallery_%s_EndA' % tag, (cx - GAL_W / 2.0 + 25, GAL_Y, GAL_H / 2.0), 0, (0.5, GAL_D / 100.0, GAL_H / 100.0))
    box('SM_Gallery_%s_EndB' % tag, (cx + GAL_W / 2.0 - 25, GAL_Y, GAL_H / 2.0), 0, (0.5, GAL_D / 100.0, GAL_H / 100.0))
    box('SM_Gallery_%s_Roof' % tag, (cx, GAL_Y, GAL_H + 15), 0, (GAL_W / 100.0 + 0.5, GAL_D / 100.0 + 0.5, 0.3))
    for i in range(6):
        px = cx - GAL_W / 2.0 + 425 + i * 350
        pole('SM_Gallery_%s_Post_%d' % (tag, i), (px, GAL_Y + GAL_D / 2.0 - 45, 0), GAL_H, 40)
    for i in range(3):   # 长凳×3（兵士坐候）
        box('SM_Gallery_%s_Bench_%d' % (tag, i), (cx - 800 + i * 800, GAL_Y + 150, 22), 0, (2.5, 0.8, 0.45))
    box('SM_Gallery_%s_Rack_Base' % tag, (cx, GAL_Y - 200, 10), 0, (0.6, 2, 0.2))      # 兵器架（器械陈设）
    for i in range(3):
        box('SM_Gallery_%s_Rack_Blade_%d' % (tag, i), (cx, GAL_Y - 275 + i * 75, 80), 0, (0.08, 0.4, 1.4))
    box('SM_Gallery_%s_Rack_Bar' % tag, (cx, GAL_Y - 200, 160), 0, (0.6, 2, 0.1))
    text('Text_GALLERY_%s' % tag, (cx, GAL_Y + 600, 250), ('EAST' if sgn > 0 else 'WEST') + ' GALLERY ARMORY', 60, yaw=90)

# ---------- 10. 标注 / 出生 / 武器点 / 兵器架 ----------
text('Text_ARENA', (0, -1600, 50), 'DRILL GROUND 120m x 120m', 60, yaw=270)
text('Text_GATE_S', (0, -WALL_LINE + 150, 480), 'SOUTH GATE 12m', 70, yaw=90)
ps = actor_sub.spawn_actor_from_class(unreal.PlayerStart, unreal.Vector(0, -SPAWN_Y, 100), rot(90))
ps.set_actor_label('PlayerStart_South')
op = actor_sub.spawn_actor_from_class(unreal.TargetPoint, unreal.Vector(0, SPAWN_Y, 100), rot(-90))
op.set_actor_label('TargetPoint_Opponent_North')
for sgn, tag in ((1, 'E'), (-1, 'W')):
    wp = actor_sub.spawn_actor_from_class(unreal.TargetPoint, unreal.Vector(sgn * 1200, 0, 50), rot(0))
    wp.set_actor_label('TargetPoint_Weapon_%s' % tag)
    box('SM_WeaponRack_%s_Base' % tag, (sgn * 1350, 250, 10), 0, (0.6, 2, 0.2))
    for i in range(3):
        box('SM_WeaponRack_%s_Blade_%d' % (tag, i), (sgn * 1350, 175 + i * 75, 80), 0, (0.08, 0.4, 1.4))
    box('SM_WeaponRack_%s_Bar' % tag, (sgn * 1350, 250, 160), 0, (0.6, 2, 0.1))

# ---------- 11. 光照（蓝天+薄雾）----------
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
# 雾：淡蓝灰薄地霾。inscattering_luminance 缺省 (0,0,0) 纯黑（黑天病根），必须显式给色。
fc.set_editor_property('fog_inscattering_luminance', unreal.LinearColor(0.55, 0.68, 0.85, 1.0))
fc.set_editor_property('fog_density', 0.0002)
fc.set_editor_property('fog_height_falloff', 0.4)
fc.set_editor_property('start_distance', 5000)
atm = actor_sub.spawn_actor_from_class(unreal.SkyAtmosphere, unreal.Vector(0, 0, 0), rot(0))
atm.set_actor_label('SkyAtmosphere_01')

# ---------- 11b. 天空球（官方模板配方，几何体两条渲染路径通吃）----------
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

# ---------- 12. NavMesh Bounds ----------
nav = actor_sub.spawn_actor_from_class(unreal.NavMeshBoundsVolume, unreal.Vector(0, 0, 400), rot(0))
nav.set_actor_label('NavMeshBounds_130x130x8')
nav.set_actor_scale3d(unreal.Vector(65, 65, 4))

# ---------- 12b. 文档自动生成（单源机制：文档是脚本的生成物，永不手写）----------
# 原则：MODULES 登记表是唯一事实源；每次重建自动重写 Docs/Scene/ 四件套。
# 任何手工改关卡 = 违规；任何场景改动 = 改本脚本重跑，文档自动跟上。
import json, os, datetime

DOCS_DIR = r'D:\AWork\Unreal\Project\VRSanguoYanWuchang\Docs\Scene'
DESIGN_INTRO = """## 设计理念（静态稿，随脚本版本维护）

**场景定位**：三国题材 VR 1v1 演武竞技场（灰盒阶段）。历史原型=汉代讲武/演武制度：平乐观讲武（188 年，双坛制、
华盖、亲执枹鼓）、刘邦拜将坛（双夯土台、设坛场具礼）、历代演武场通制（阅兵台+旗杆台+合院+牌坊）、
《三国演义》铜雀台夺锦袍（红锦袍彩头+分队比射=本项目 PK 玩法的历史原型）。门制出自《武经总要·讲武》
"方一千二百步，四出为和门"——v5.6 起取三出（南主门+东西辕门）：北端由演武厅收尾（北堂南向通制），
北门背对厅堂无人能用，强设四门反成缺陷。

**布局语法**：北厅南场纵轴序列——南门(牌坊)→照迎空间→120m 校场(跑马环道+功能角)→三层拜将坛→演武厅(北端，背靠北墙)。
统帅面南（北置将台）合"面南而王"；出生点位于南轴上，开门即见全场与坛剪影（第一眼构图已验证）。
**动线**：中轴仪式线 + 围墙内 8m 跑马环道（骑战）+ 西侧功能角（靶场）+ 南门两侧廊庑（集结）。
**地标天际线**：三层坛(5m) → 望楼(14.5m) → 帅旗(15m)，三层高度保证任意点位方向感。
**灰盒纪律**：全部由 rebuild_v5.py 单源生成；改场景=改脚本重跑（文档自动重生成）；禁止编辑器手改。
"""

CHANGELOG = """## 变更记录

- **v5.7（本次）**：①**靶子近观重制**（用户特写"你这叫靶子？"）：两层根因——**靶面朝向 90° 错**
  （disc 扁轴在 Y=盘面朝南北、侧对射手，注释还误写"朝东西"；用户看到的"蛋"是 8cm 盘缘的透镜轮廓，
  "浮球"是红心缘的视差脱开）+ 盘厚 30cm 太厚。修复：disc 增 yaw 参数，靶盘/红心 yaw=90 面朝东对射手，
  盘厚 30→8cm、红心贴面凸 2cm——正对射手见完整圆盘+盘心红心；**判读教训：证据图核验也必须先验朝向假设**；
  ②**将台东侧服务踏步撤除**（用户"侧边突然多了个楼梯，怎么引入"）：v5.5 为还厅内通道设的服务线
  读作多余侧梯，撤除后登坛只走南主台阶，三层顶东侧护栏恢复整段；③**廊庑功能化**
  （用户"以为是马厩"）：空柱廊加长凳×3+兵器架×1+标注 ARMORY，语义=兵士整备/列队/候命廊；
  ④**演武厅视线答复**（用户"厅在将台后面被遮挡怎么看演武，你怎么规划的"）：如实答复——观武位=
  将台顶（5m 全场无遮挡，这正是将台的功能；从厅内地面看确实被坛挡，几何如此），厅=主帅居停/军议/
  受贺（"厅后于台"布置）；厅与坛谁移位=布局级决策，已列三方案（将台东移/维持/厅升台基）请用户拍板，
  本轮北侧布局不动。
- **v5.6b**：①**鼓亭悬空根修**（用户截图"两个鼓亭悬空"）：v5.3 鼓亭移坛脚时 z 基准漏改——
  柱/顶板/鼓架/鼓全套仍按坛面基准 T1_H 起建，整亭浮空 1m；现全部落地（柱底 0、鼓坐鼓架 90..180），
  柱加粗 30→40；②**演武厅两翼敞棚化**（用户"半封闭小房间看不懂"）：5.5m 高实墙房改 1.2m 矮墙敞棚
  （看棚/廊庑式样）+翼内长案（将佐观武席）+TEXT 标注；柱列 3→6 根并修正柱顶 520 与顶板底 550 脱空 30cm；
  ③**md 文档恢复**（用户"资产清单 md 和场景介绍 md 怎么没了"）：scene_overview.md + asset_checklist.md
  恢复生成，与 html/json/俯拍 png 同代同戳（v5.6 三文件制误删，致歉——"清旧文件"应清"旧代次"而非"md 正文"）；
  ④考据补验（用户实测搜索栈已恢复）：WA 标准圆靶 dia122cm/草靶雏形/厚 15-25cm 与本场 dia130×30 吻合 ✓；
  唐"阅武堂"/宋"演武亭"=厅堂式设施 ✓（百科词条）；"北端面南"通制未逐条核到原文，如实标注。
- **v5.6**：①靶子改**圆草靶**制（用户"正常靶子是圆的"）：木桩+直径1.3m 草靶圆盘+直径0.4m 红心圆盘，
  桩穿盘安装（接触保证），东移出墙影区（太阳西照墙投影带实测远超估算——射位线视角复核定案）；靶面麦秆色+
  微自发光 0.35、红心正红（灰盒唯一着色件，背光带里也一眼读出"这是靶子"；M02 换真材质时移除）——
  同时根除旧"红心板悬空 1.25m"被读作华盖的缺陷（用户"两个华盖悬空"）；实现记录：StaticMeshActor 的
  pitch 旋转在本构建不生效（六法实测全败），圆盘改 Sphere 非均匀缩放（立式透镜盘）绕过；
  ②北辕门撤除（用户"演武厅挨着门正常吗"：北门在厅背后=堵死的门无人能用，撤除后北墙连续、北端由厅收尾，
  合"北堂南向"讲武通制；厅位本身=历史有据：唐阅武厅/宋演武亭置场北端面南；若需北出口可改门东/西移）；
  ③平面图改为**由关卡组件实测包围盒生成**（用户"平面图对不上"：每组件一个矩形，与场景严格一致），
  HTML 内嵌；④Docs/Scene 精简为三文件（html/json/实测俯视图 png），旧 md/svg/raw 自动清理
  （用户"谁知道哪个最新"）。
- **v5.5**：①坛组南移 2.75m，坛↔演武厅间距 1.5→4.25m（用户"堆一起"）；②服务坡道撤出演武厅
  （厅内通道复原，用户"人怎么进去"），改为坛东侧翼 B/C 两段服务踏步（贴坛壁，全在坛 footprint 内）；
  ③靶场重排：靶垛贴西墙做靶墙+红心板+地面 3 条射道标线，射位棚距靶 10m（用户"靶子放哪"）；
  ④锦袍杆加基座+挂袍式（用户"很高的竖着的是啥"）；⑤16 面墙旗全部回墙顶+统一东风，东墙旗飘出墙外上空
  （修上一轮"落地旗"错误方案）；⑥文档改版：scene_plan.html 自包含主文档 + scene_topdown.png 实测正交俯视图
  （用户"生成的图完全不可用"）。
- **v5.4**：全场景旗面统一东风（一律 +X）；旗面厚度 2m→6cm（真正的"扁旗"，此前是厚盒子——用户反馈"正常的旗帜是扁的"）。
- **v5.3**：一层坛进深 11→12.5m（南立面 3750）——v5.2 把 B 段台阶下三步悬到坛外空中（B 段需 250cm 坛面进深，
  立面到二层立面只剩 100cm），寻路正确拒登；现 B 段全落坛面，与北演武厅仍保持 1.5m 间距。
- **v5.2**：旗面改侧挂（不再穿杆居中）；撤鼓台、三鼓直接落台面（修"鼓垫太高/与护栏重叠"）；新增 Docs/Scene 四件套自动生成。
- **v5.1**：三层坛（24×14/18×10/12×6）+三段台阶（15 步 0.34m）+北服务坡道穿演武厅中央通道；鼓亭×2；
  演武厅（双翼 7×8×5.5+中央 2m 通道）；西靶场 3 靶+射位棚+锦袍杆；南门牌坊；碑石×2；兵器架×2；
  军旗 16 上墙顶净出 8m 跑马环道；对旗杆台移 (±800,-4900)。修复：SM_Cylinder 底面枢轴（v1~v4 全体杆件悬空半高）；
  南主门两侧 5.7m 墙洞（跳段判据缺陷）。考据：平乐观 188 年讲武/拜将坛遗址/演武场通制/铜雀台夺袍。
- **v4**：场地 70→120×120m；直角 SM_Cube 地砖 30.4m 互埋（ChamferCube 圆角缝+发丝黑缝双教训）；
  将台改中央台阶（15 步）+后服务坡道；南门廊庑改 26×7×4.5m 柱廊对；门墙搭接 20cm。
- **v3**：初版规制校场（70×70 分块地面/3m 墙四门/16×10×4 将台/五方旗/望楼/雾与天空球配方）。
"""

CAT_COLORS = {'结构': '#6b7280', '建筑': '#8b6f47', '仪式': '#b91c1c', '功能': '#15803d',
              '氛围': '#d97706', '机制': '#6d28d9', '渲染': '#2563eb', '辅助': '#9ca3af'}

MODULES = [
    dict(id='floor', name='校场地坪', cat='结构', anchor=(0, 0), size=(12000, 12000, 20),
         source='—', func='承载全场景；1m 网格提供 VR 尺度感与深度参照', assets='材质：夯土/沙场 PBR 贴图', prio='M02 白模'),
    dict(id='walls', name='围墙系统', cat='结构', anchor=(0, 0), size=(12000, 12000, 300),
         source='营垒垣墙', func='场地边界+围合感', assets='材质：砖石墙体+压顶', prio='M02 白模'),
    dict(id='gates', name='三出辕门', cat='结构', anchor=(0, -5970), size=(1300, 100, 450),
         source='《武经总要·讲武》"四出为和门"；v5.6 取三出（北端为演武厅，北门撤除——厅背堵门缺陷）',
         func='出入动线：南主门 12m+东西辕门 4m；北墙连续由厅收尾', assets='模型：木构辕门+门旗', prio='M02 白模'),
    dict(id='paifang', name='南门牌坊', cat='结构', anchor=(0, -5970), size=(1000, 50, 660),
         source='演武场"部分设牌坊"', func='主门仪式门面', assets='模型：木牌坊+匾额', prio='M03'),
    dict(id='altar', name='三层拜将坛', cat='仪式', anchor=(0, 4100), size=(2400, 1250, 500),
         source='平乐观大坛(188)+拜将坛遗址', func='点将/授印/颁奖高点；三层坛制+南主台阶(15步0.34m；v5.7 东翼服务踏步撤除，登坛只走主台阶)', assets='材质：夯土+石包边', prio='M02 白模'),
    dict(id='drum_pavilions', name='鼓亭×2', cat='仪式', anchor=(1500, 3850), size=(220, 220, 300),
         source='平乐观"亲执枹鼓"', func='指挥鼓点（坛脚东西各一，不占坛面服务路线）', assets='模型：木构鼓亭+战鼓', prio='M02 白模'),
    dict(id='command_deck', name='坛顶指挥组', cat='仪式', anchor=(0, 4425), size=(1200, 600, 150),
         source='—', func='三面战鼓/点将桌/10m 帅旗杆', assets='模型：战鼓、案桌、帅旗', prio='M02 白模'),
    dict(id='steles', name='碑石×2', cat='仪式', anchor=(1300, 4150), size=(100, 40, 260),
         source='拜将坛台脚立碑', func='场景叙事锚点', assets='模型：石碑+碑文贴图', prio='M03'),
    dict(id='hall', name='演武厅', cat='建筑', anchor=(0, 5550), size=(1600, 800, 580),
         source='唐"阅武厅"/宋"演武亭"', func='点将/轮换/观战机制位（M02/M03 接机制）', assets='模型：木构厅堂+匾额"演武厅"', prio='M02 白模'),
    dict(id='galleries', name='南门廊庑×2', cat='建筑', anchor=(1950, -5600), size=(2600, 700, 480),
         source='演武场"合院建筑"', func='兵士整备/列队/遮阳候命（v5.7 内设长凳+兵器架+ARMORY 标注，修"像马厩"）', assets='模型：木构廊庑+长凳+兵器架', prio='M02 白模'),
    dict(id='archery', name='西靶场', cat='功能', anchor=(-5480, 1800), size=(450, 2400, 260),
         source='铜雀台比射红心(演义56回)；圆草靶形制(2026-09-10 已在线补验：WA 标准 dia122/草靶雏形/厚15-25cm)', func='射术玩法区：3 圆草靶(木桩+麦秆色薄靶盘 dia1.3m 厚8cm+贴面红心 dia0.4m 厚3cm 桩穿盘，出墙影区)+地面射道标线+射位棚(距靶7m)', assets='模型：草靶圆盘/红心盘/棚架/地面标线', prio='M02 白模'),
    dict(id='jinpao', name='锦袍杆', cat='功能', anchor=(-4600, 3300), size=(150, 150, 800),
         source='铜雀台夺袍', func='彩头锚点：胜利机制挂点（先中红心得彩头；基座+挂袍式）', assets='模型：红锦袍', prio='M03 机制'),
    dict(id='wufang', name='五方旗阵', cat='仪式', anchor=(0, 2700), size=(4800, 100, 620),
         source='五方五色旗制', func='方位识别/仪式感', assets='模型：五色军旗', prio='M02 白模'),
    dict(id='flagstands', name='对旗杆台×2', cat='仪式', anchor=(800, -4900), size=(200, 200, 850),
         source='—', func='南门仪仗', assets='模型：大纛旗', prio='M03'),
    dict(id='wall_flags', name='军旗墙顶阵×16', cat='氛围', anchor=(0, 5970), size=(11940, 60, 500),
         source='—', func='营垒气势；全部墙顶立杆+统一东风（东墙旗飘出墙外上空，城楼旗式样）', assets='模型：军旗布幔', prio='M02 白模'),
    dict(id='towers', name='望楼×4', cat='结构', anchor=(5200, 5200), size=(300, 300, 1450),
         source='箭楼形制', func='制高点/警戒塔（跑马道角落例外位）', assets='模型：木构塔楼', prio='M02 白模'),
    dict(id='racks', name='兵器架×2', cat='功能', anchor=(1350, 250), size=(60, 200, 170),
         source='教场兵器房', func='武器拾取点包装', assets='模型：木架+陈列兵器', prio='M03'),
    dict(id='spawns', name='出生/对手/武器点', cat='机制', anchor=(0, -2000), size=(100, 100, 100),
         source='—', func='PK 出生(0,±2000 面向场心)+武器拾取(±1200,0)', assets='标记：出生特效/光柱', prio='M03 机制'),
    dict(id='lighting', name='光照组', cat='渲染', anchor=(0, 0), size=(0, 0, 0),
         source='官方模板配方', func='太阳10lux 5600K -38°/天光实时捕获/雾0.0002/大气/几何天空球', assets='—（配方已定稿）', prio='—'),
    dict(id='texts', name='灰盒标注组', cat='辅助', anchor=(0, -1600), size=(0, 0, 0),
         source='—', func='读图标注（8 处白字）', assets='替换：场景标识牌/木牌', prio='M02 白模'),
]

stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
os.makedirs(DOCS_DIR, exist_ok=True)

def total_props_hint():
    return sum(counts.values())

# 1) 机读登记（唯一事实源导出）
with open(os.path.join(DOCS_DIR, 'scene_modules.json'), 'w', encoding='utf-8') as f:
    json.dump(dict(stamp=stamp, script='rebuild_v5.py', props=total_props_hint(), modules=MODULES),
              f, ensure_ascii=False, indent=1)

# 2) 资产行（并入 HTML；v5.6 起不再单独产出 md——文档夹只保留 3 个文件）
rows = '\n'.join('| %s | %s | %s | (%d,%d) | %dx%d | %s | %s |' % (
    m['id'], m['name'], m['cat'], m['anchor'][0], m['anchor'][1],
    m['size'][0], m['size'][1], m['source'], m['func']) for m in MODULES)
arows = '\n'.join('| %s | %s | %s | %s | %s |' % (m['name'], m['assets'].replace('；', ' ｜ '), m['func'][:40], m['prio'], m['cat']) for m in MODULES)

# 3) 平面图 SVG（v5.6：由关卡组件实测包围盒生成——每个 StaticMeshActor 一个矩形，与场景严格一致；
# 旧版按 MODULES 锚点画示意块，与实建位置有出入，被用户判"对不上"）
def _svgx(x):
    return 120 + (x + 6000) * 0.075
def _svgy(y):
    return 70 + (6000 - y) * 0.075

def _prefix_color(name):
    for pres, col in ((('SM_Wall', 'SM_Gate'), '#cbb994'), (('SM_Floor',), '#e9e4d6'),
                      (('SM_Jiangtai', 'SM_Step'), '#b45309'), (('SM_Hall', 'SM_Gallery'), '#8b5a2b'),
                      (('SM_Flag',), '#c0392b'), (('SM_Target', 'SM_JinPao'), '#1e7e46'),
                      (('SM_Wanglou',), '#4a55a2'), (('SM_Drum',), '#7c2d12'),
                      (('SM_Stele',), '#64748b'), (('SM_WeaponRack',), '#374151'),
                      (('SM_Arch_Paifang',), '#6b7280')):
        for p in pres:
            if name.startswith(p):
                return col
    return '#9aa5b1'

rects = []
for _a in actor_sub.get_all_level_actors():
    if _a.get_class().get_name() != 'StaticMeshActor':
        continue
    _o, _e = _a.get_actor_bounds(False)
    rects.append((_a.get_actor_label(), _o.x, _o.y, _e.x * 2.0, _e.y * 2.0))
rects.sort(key=lambda r: -(r[3] * r[4]))
svg = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<svg xmlns="http://www.w3.org/2000/svg" width="1240" height="1060" font-family="Microsoft YaHei,sans-serif">',
       '<rect width="1240" height="1060" fill="#f6f4ef"/>',
       '<text x="120" y="35" font-size="20" font-weight="bold">三国演武场 平面图（组件实测包围盒 %d 个）· %s</text>' % (len(rects), stamp),
       '<text x="120" y="55" font-size="12" fill="#666">由关卡 StaticMeshActor 实测包围盒生成，与场景严格一致 · 鼠标悬停矩形可看组件名 · 北▲上</text>',
       '<rect x="%f" y="%f" width="900" height="900" fill="#efe9dc" stroke="#6b7280" stroke-width="3"/>' % (_svgx(-6000), _svgy(6000))]
for _lbl, _ox, _oy, _ex, _ey in rects:
    svg.append('<rect x="%f" y="%f" width="%f" height="%f" fill="%s" opacity="0.55" stroke="#4b5563" stroke-width="0.4"><title>%s</title></rect>'
               % (_svgx(_ox - _ex / 2.0), _svgy(_oy + _ey / 2.0), max(_ex * 0.075, 0.8), max(_ey * 0.075, 0.8),
                  _prefix_color(_lbl), _lbl))
# 关键标签
for lx, ly, txt in ((0, 4450, '拜将坛(三层)'), (0, 5550, '演武厅(北端)'), (1950, -5600, '廊庑E'), (-1950, -5600, '廊庑W'),
                    (-5400, 1800, '靶场(圆草靶×3)'), (0, -5970, '南门+牌坊'), (0, -2000, '出生点▲'),
                    (0, 2700, '五方旗'), (5200, 5200, '望楼×4'), (1500, 3850, '鼓亭'), (-4600, 3300, '锦袍杆'), (0, -5300, '▼')):
    svg.append('<text x="%f" y="%f" font-size="13" fill="#1f2937" text-anchor="middle" stroke="#fff" stroke-width="3" paint-order="stroke">%s</text>' % (_svgx(lx), _svgy(ly), txt))
# 图例（按组件前缀着色）
LEGEND = (('墙/门', '#cbb994'), ('地面', '#e9e4d6'), ('拜将坛', '#b45309'), ('厅/廊', '#8b5a2b'),
          ('旗', '#c0392b'), ('靶/锦袍', '#1e7e46'), ('望楼', '#4a55a2'), ('鼓', '#7c2d12'),
          ('碑', '#64748b'), ('兵器架', '#374151'), ('牌坊', '#6b7280'), ('其他', '#9aa5b1'))
lx0, ly0 = 1050, 90
svg.append('<text x="%d" y="%d" font-size="14" font-weight="bold">图例</text>' % (lx0, ly0))
for _i, (_nm, _col) in enumerate(LEGEND):
    svg.append('<rect x="%d" y="%d" width="14" height="14" fill="%s"/><text x="%d" y="%d" font-size="12">%s</text>'
               % (lx0, ly0 + 20 + _i * 24, _col, lx0 + 20, ly0 + 31 + _i * 24, _nm))
svg.append('<text x="%d" y="%d" font-size="11" fill="#666">比例尺 30m ┊ 北▲上</text>' % (lx0, ly0 + 320))
svg.append('<line x1="120" y1="1010" x2="345" y2="1010" stroke="#333" stroke-width="2"/><text x="120" y="1030" font-size="11">30m</text>')
svg.append('</svg>')

# 4) 自包含主文档 HTML（v5.6：单一人读文档；平面图=实测 bounds；文档夹只保留 3 个文件）
html_doc = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><title>三国演武场 · 场景文档 v5.6</title>
<style>
body{font-family:'Microsoft YaHei',sans-serif;max-width:1280px;margin:24px auto;padding:0 16px;background:#faf9f6;color:#1f2937}
h1{border-bottom:3px solid #b91c1c;padding-bottom:8px} h2{color:#7c2d12;margin-top:36px}
table{border-collapse:collapse;width:100%%;font-size:13px} td,th{border:1px solid #d1cfc7;padding:5px 8px;text-align:left}
th{background:#efe9dc} .meta{color:#666;font-size:13px} .warn{background:#fef3c7;border:1px solid #f59e0b;padding:10px;border-radius:6px}
figure{margin:16px 0;text-align:center} figcaption{color:#666;font-size:12px}
</style></head><body>
<h1>三国演武场 · 场景文档（自动生成）</h1>
<p class="meta">生成：%s ｜ 单源：<code>rebuild_v5.py</code> ｜ 组件：%d ｜ 关卡：<code>/Game/VRSanguo/Dev/L_Prototype_1v1_v5</code> ｜ 版本 v5.6</p>
<div class="warn"><b>勿手改本文档。</b>场景任何改动必须改脚本重跑——本文档与 <code>scene_modules.json</code>、
<code>scene_topdown.png</code> 一同自动重写（<code>Docs\\Scene</code> 只保留这三个文件，旧版 md/svg/raw 已自动清理），手改无效。</div>
%s
<h2>平面图（组件实测包围盒）</h2>
<figure>
%s
<figcaption>俯视平面 · 北朝上 · 每个矩形=一个场景组件的实测包围盒，与场景严格一致，悬停可看组件名；
另附 <code>scene_topdown.png</code> 为引擎正交俯拍实景（同向北上，与平面图互证）</figcaption>
</figure>
<h2>模块总表（%d 个模块 · 资产/锚点/史料）</h2>
<table><tr><th>id</th><th>名称</th><th>类别</th><th>锚点(cm)</th><th>尺寸(cm)</th><th>史料/出处</th><th>功能</th></tr>
%s
</table>
<h2>资产清单（M02/M03 换皮生产）</h2>
<table><tr><th>模块</th><th>目标资产</th><th>说明</th><th>阶段</th><th>类别</th></tr>
%s
</table>
<h2>渲染与光照（定稿配方）</h2>
<p>太阳 10lux/5600K/pitch-38° + 天光 0.8 实时捕获 + 淡蓝灰薄雾(density 0.0002) + 大气 + 官方模板几何天空球
（本项目游戏路径不渲染大气通道，几何天空是两条渲染路径通吃的解法）。</p>
<h2>已知观察项（P1"天空渲染专查"跟踪）</h2>
<p>1. HMD-less VR pawn 平视近场渲染怪癖；2. pawn 视图冷色调（SceneCapture/编辑器正常）；3. PIE 抓拍通道偶发粘编辑器视口。</p>
<h2>变更记录</h2>
%s
</body></html>""" % (stamp, total_props_hint(), DESIGN_INTRO, '\n'.join(svg), len(MODULES), rows, arows, CHANGELOG)
with open(os.path.join(DOCS_DIR, 'scene_plan.html'), 'w', encoding='utf-8') as f:
    f.write(html_doc)

# 4b) 正文 md 两件（v5.6b 恢复：用户指出资产清单/场景介绍 md 不应删除；与 html 同代生成，全部同戳）
md_overview = ['# 三国演武场 场景介绍（%s）' % stamp, '',
               '> 勿手改：单源 rebuild_v5.py 重跑生成；交互版见 scene_plan.html，俯视图见 scene_topdown.png。', '',
               DESIGN_INTRO, '',
               '| 模块 | 类别 | 锚点(x,y)cm | 史料依据 | 功能 | 阶段 |',
               '|---|---|---|---|---|---|']
for m in MODULES:
    md_overview.append('| %s %s | %s | (%d, %d) | %s | %s | %s |' % (
        m['id'], m['name'], m['cat'], m['anchor'][0], m['anchor'][1], m['source'], m['func'], m['prio']))
md_overview += ['', '## 变更记录（摘要）', '', '见 scene_plan.html 变更记录节；当前代 v5.6b。', '']
with open(os.path.join(DOCS_DIR, 'scene_overview.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_overview))

md_assets = ['# 资产生产清单（%s）' % stamp, '',
             '> 勿手改：单源 rebuild_v5.py 重跑生成。灰盒锚定 → M02 起逐模块换皮：每行=该模块需要的正式资产。',
             '', '| 模块 | 需要资产 | 优先级 | 阶段 |', '|---|---|---|---|']
for m in MODULES:
    md_assets.append('| %s %s | %s | %s | %s |' % (m['id'], m['name'], m['assets'], m['prio'], m['prio'].split()[0]))
md_assets += ['', '## 通用资产', '',
              '- 材质：夯土/沙场 PBR（地坪）、砖石墙（围墙/望楼）、木构（辕门/牌坊/廊柱/鼓亭/射位棚）、布幔（旗/锦袍）、草靶+红漆（靶）。',
              '- 音频：鼓/号角/喝彩（M02）。', '']
md_assets = '\n'.join(md_assets)
with open(os.path.join(DOCS_DIR, 'asset_checklist.md'), 'w', encoding='utf-8') as f:
    f.write(md_assets)

# 4c) 文档夹清理（旧代次文件移除：svg 老图与 raw 中间产物）
for _stale in ('plan.svg', 'scene_topdown_raw.png'):
    try:
        os.remove(os.path.join(DOCS_DIR, _stale))
    except OSError:
        pass

# 5) 引擎实测正交俯视图（真实场景俯拍，永远与场景一致——比手绘平面图可信）
# UE 正交俯拍固定带水平镜像（handedness 翻转，任何 yaw 不可避）：
# 配方 = yaw=-90 捕获（南上西左）→ flip_topdown.ps1 垂直翻转 → scene_topdown.png（北上东右无镜像）。
# v5.6：raw 中间产物移出文档夹（TraeAdmin\tmp），Docs\Scene 不再留 raw。
TMP_DIR = r'D:\AWork\TraeAdmin\VRSanguoYanWuchang\tmp'
os.makedirs(TMP_DIR, exist_ok=True)
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
rt = unreal.RenderingLibrary.create_render_target2d(world, 1920, 1920, unreal.TextureRenderTargetFormat.RTF_RGBA8, unreal.LinearColor(0, 0, 0, 1), False)
cap = actor_sub.spawn_actor_from_class(unreal.SceneCapture2D, unreal.Vector(0, 0, 3500), unreal.Rotator(roll=0.0, pitch=-90.0, yaw=-90.0))
cap.set_actor_label('CAP_Topdown_Temp')
cc = cap.get_component_by_class(unreal.SceneCaptureComponent2D)
cc.set_editor_property('capture_source', unreal.SceneCaptureSource.SCS_FINAL_COLOR_LDR)
cc.set_editor_property('texture_target', rt)
cc.set_editor_property('projection_type', unreal.CameraProjectionMode.ORTHOGRAPHIC)
cc.set_editor_property('ortho_width', 14500.0)
cc.capture_scene()
unreal.RenderingLibrary.export_render_target(world, rt, TMP_DIR, 'scene_topdown_raw.png')
actor_sub.destroy_actor(cap)
print('DOCS_WRITTEN %s -> html + 2md + json（俯拍 raw 在 %s）— 再跑 flip_topdown.ps1 生成 scene_topdown.png' % (DOCS_DIR, TMP_DIR))

# ---------- 13. 保存 ----------
saved = unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
total = 0
for k in sorted(counts):
    print('COUNT %s = %d' % (k, counts[k]))
    total += counts[k]
print('TOTAL_PROPS %d' % total)
print('SAVE_RESULT %s' % saved)
print('REBUILD_V5_DONE')
