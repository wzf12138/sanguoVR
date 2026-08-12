$ErrorActionPreference = 'Stop'

# PICO OpenXR 补丁恢复脚本（2026-08-11）
# 用途：PICO 插件升级或重装后，恢复本项目所需的三处修改：
#   1. PICOOpenXR.uplugin 的 "Installed": false
#   2. PICO_HMD.cpp 的 swapchain format list 剥离补丁（Neo3 兼容）
#   3. 全部模块 Build.cs 的 PrecompileForTargets = Any
# 用法：在项目根目录或任意位置执行（路径为绝对路径，无需 cd）
$pluginRoot = 'D:\AWork\Unreal\Project\VRSanguoYanWuchang\Plugins\PICOOpen174f9f81d266V8'
$bak = 'D:\AWork\Unreal\Project\VRSanguoYanWuchang\Build\Patches\PICOOpenXR'

# 1. uplugin: restore Installed=false
Copy-Item "$bak\PICOOpenXR.uplugin.patched" "$pluginRoot\PICOOpenXR.uplugin" -Force
Write-Host '[1/3] PICOOpenXR.uplugin restored (Installed=false).'

# 2. PICO_HMD.cpp: restore swapchain patch
Copy-Item "$bak\PICO_HMD.cpp.patched" "$pluginRoot\Source\PICOOpenXRHMD\Private\PICO_HMD.cpp" -Force
Write-Host '[2/3] PICO_HMD.cpp restored (swapchain patch).'

# 3. All Build.cs files with PrecompileForTargets
$bakBuild = Get-ChildItem "$bak\Source" -Recurse -Filter '*.Build.cs'
$targetBuild = Get-ChildItem "$pluginRoot\Source" -Recurse -Filter '*.Build.cs'
$map = @{}
foreach ($f in $bakBuild) { $map[$f.Name.ToLowerInvariant()] = $f.FullName }
$count = 0
foreach ($f in $targetBuild) {
    $key = $f.Name.ToLowerInvariant()
    if ($map.ContainsKey($key)) {
        Copy-Item $map[$key] $f.FullName -Force
        $count++
    }
}
Write-Host "[3/3] Restored $count Build.cs files (PrecompileForTargets)."

# Verify
$checkU = Select-String -Path "$pluginRoot\PICOOpenXR.uplugin" -Pattern 'Installed'
Write-Host "VERIFY uplugin: $($checkU.Line.Trim())"
$checkC = Select-String -Path "$pluginRoot\Source\PICOOpenXRHMD\Private\PICO_HMD.cpp" -Pattern 'PICOLayerCreateSwapchain'
Write-Host "VERIFY PICO_HMD.cpp patch: $($checkC.Count) match(es)"
$checkB = Select-String -Path "$pluginRoot\Source\PICOOpenXRHMD\PICOOpenXRHMD.Build.cs" -Pattern 'PrecompileForTargets'
Write-Host "VERIFY Build.cs precompile: $($checkB.Count) match(es)"
