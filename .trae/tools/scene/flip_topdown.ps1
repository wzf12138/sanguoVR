# flip_topdown.ps1 — rebuild_v5.py 俯视图后处理
# 背景：UE SceneCapture2D 正交俯拍(pitch -90)固定带水平镜像（handedness 翻转，任何 yaw 均不可避）。
# 配方：脚本内 yaw=-90 捕获（南上西左·镜像）导出 scene_topdown_raw.png → 本脚本【垂直翻转】
#       （去镜像+南北归位，等效水平镜像+180°旋转）→ scene_topdown.png（北上东右·非镜像，与 plan.svg 同向）。
# 用法：powershell -File flip_topdown.ps1
$tmp = 'D:\AWork\TraeAdmin\VRSanguoYanWuchang\tmp'
$raw = Join-Path $tmp 'scene_topdown_raw.png'
$out = 'D:\AWork\Unreal\Project\VRSanguoYanWuchang\Docs\Scene\scene_topdown.png'
Add-Type -AssemblyName System.Drawing
$img = [System.Drawing.Image]::FromFile($raw)
$img.RotateFlip([System.Drawing.RotateFlipType]::RotateNoneFlipY)
$img.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
$img.Dispose()
Write-Output ("FLIPPED(V) -> " + $out)
