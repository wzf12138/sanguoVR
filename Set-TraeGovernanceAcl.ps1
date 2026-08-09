#requires -Version 5.1
[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
param(
    [ValidateSet('Audit', 'Apply', 'Restore')]
    [string]$Mode = 'Audit',
    [string]$ProjectRoot = 'D:\AWork\Unreal\Project\VRSanguoYanWuchang',
    [string]$AdminRoot = 'D:\AWork\TraeAdmin\VRSanguoYanWuchang'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Assert-Administrator {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($identity)
    if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        throw '此操作需要以管理员身份运行 PowerShell。'
    }
}

function Resolve-SidAccount {
    param([Parameter(Mandatory)][string]$Sid)
    $sidObject = New-Object Security.Principal.SecurityIdentifier($Sid)
    $sidObject.Translate([Security.Principal.NTAccount]).Value
}

function Show-AclSummary {
    param([Parameter(Mandatory)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { Write-Warning "路径不存在: $Path"; return }
    $acl = Get-Acl -LiteralPath $Path
    Write-Host "`n[$Path]"
    Write-Host "Owner: $($acl.Owner)"
    Write-Host "Protected: $($acl.AreAccessRulesProtected)"
    $acl.Access | Sort-Object IdentityReference, AccessControlType, FileSystemRights |
        Format-Table IdentityReference, AccessControlType, FileSystemRights, IsInherited, InheritanceFlags, PropagationFlags -AutoSize
}

function Invoke-Icacls {
    param([string]$Path, [string[]]$Arguments)
    & icacls.exe $Path @Arguments
    if ($LASTEXITCODE -ne 0) { throw "icacls 执行失败，退出码 $LASTEXITCODE" }
}

$governanceRoot = Join-Path $ProjectRoot '.trae'
$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent().Name
$systemAccount = Resolve-SidAccount 'S-1-5-18'
$administrators = Resolve-SidAccount 'S-1-5-32-544'
$users = Resolve-SidAccount 'S-1-5-32-545'

if ($Mode -eq 'Audit') {
    Show-AclSummary $ProjectRoot
    Show-AclSummary $governanceRoot
    Show-AclSummary $AdminRoot
    return
}

Assert-Administrator
if (-not (Test-Path -LiteralPath $ProjectRoot)) { throw "项目根目录不存在: $ProjectRoot" }

if ($Mode -eq 'Apply') {
    if (-not (Test-Path -LiteralPath $governanceRoot)) { throw "治理目录不存在: $governanceRoot" }
    if (-not (Test-Path -LiteralPath $AdminRoot)) { New-Item -ItemType Directory -Force -Path $AdminRoot | Out-Null }

    if ($PSCmdlet.ShouldProcess($governanceRoot, '保护治理目录 ACL')) {
        Invoke-Icacls $governanceRoot @('/inheritance:r')
        Invoke-Icacls $governanceRoot @('/remove:g', $users)
        Invoke-Icacls $governanceRoot @('/grant:r', "$currentUser:(OI)(CI)M", "$systemAccount:(OI)(CI)F", "$administrators:(OI)(CI)F", "$users:(OI)(CI)RX", '/T', '/C')
    }
    if ($PSCmdlet.ShouldProcess($AdminRoot, '保护管理员脚本目录 ACL')) {
        Invoke-Icacls $AdminRoot @('/inheritance:r')
        Invoke-Icacls $AdminRoot @('/remove:g', $users)
        Invoke-Icacls $AdminRoot @('/grant:r', "$currentUser:(OI)(CI)M", "$systemAccount:(OI)(CI)F", "$administrators:(OI)(CI)F", '/T', '/C')
    }
    Show-AclSummary $governanceRoot
    Show-AclSummary $AdminRoot
    return
}

if ($Mode -eq 'Restore') {
    if ($PSCmdlet.ShouldProcess($governanceRoot, '恢复治理目录 ACL 继承')) {
        Invoke-Icacls $governanceRoot @('/inheritance:e', '/reset', '/T', '/C')
    }
    if (Test-Path -LiteralPath $AdminRoot) {
        if ($PSCmdlet.ShouldProcess($AdminRoot, '恢复管理员脚本目录 ACL 继承')) {
            Invoke-Icacls $AdminRoot @('/inheritance:e', '/reset', '/T', '/C')
        }
    }
    Show-AclSummary $governanceRoot
    Show-AclSummary $AdminRoot
}
