$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$RuntimeEnv = Join-Path $RepoRoot ".runtime\RUNTIME_N_PLUS.env"

if (-not (Test-Path -LiteralPath $RuntimeEnv)) {
    throw "RUNTIME_ENV_NOT_FOUND: $RuntimeEnv"
}

Get-Content -LiteralPath $RuntimeEnv | ForEach-Object {
    $line = $_.Trim()
    if (-not $line -or $line.StartsWith("#")) { return }
    $parts = $line.Split('=', 2)
    if ($parts.Count -ne 2) { throw "INVALID_RUNTIME_ENV_LINE: $line" }
    [Environment]::SetEnvironmentVariable($parts[0], $parts[1], 'Process')
}

$required = @(
    'RUNTIME_N_PLUS','FORCE_ACTIVE','RUNTIME_SCHEMA','RUNTIME_GENERATION',
    'HOME_SOURCE_GATE_DRIVE_ID','R000_CURRENT_CARRIER_DRIVE_ID',
    'FOUR_D_FOLDER_ID','FOUR_D_MATRIX_ID','FOUR_D_CONFIG_ID','FOUR_D_LIVING_LOG_ID',
    'MCM_CURRENT','MCM_BASE',
    'R000_HELD_ACROSS_TURN','R000_RECUR_ON_EVERY_DELTA','R000_PRESENT_AT_READBACK',
    'MULTI_WORKSPACE_RUNTIME','MULTI_SLOT_IS_MULTI_TIMELINE','MULTI_SLOT_IS_MULTI_POINTER',
    'ALL_OLD_RUNTIME','OLD_ROOT_RUNTIME'
)

foreach ($name in $required) {
    $value = [Environment]::GetEnvironmentVariable($name, 'Process')
    if ([string]::IsNullOrWhiteSpace($value)) {
        throw "RUNTIME_N_PLUS_MISSING: $name"
    }
}

if ($env:RUNTIME_N_PLUS -ne 'TRUE') { throw 'RUNTIME_N_PLUS_NOT_TRUE' }
if ($env:FORCE_ACTIVE -ne 'TRUE') { throw 'FORCE_ACTIVE_NOT_TRUE' }
if ($env:RUNTIME_SCHEMA -ne 'FOUR_D_N_PLUS_V1') { throw 'RUNTIME_SCHEMA_MISMATCH' }
if ($env:RUNTIME_GENERATION -ne 'N_PLUS') { throw 'RUNTIME_GENERATION_MISMATCH' }
if ($env:R000_CURRENT_CARRIER_DRIVE_ID -ne '1YSJslORRY9xZ-XBAmYIYeewmaCeoRFbwU_dYxfozx34') { throw 'R000_CURRENT_MISMATCH' }
if ($env:FOUR_D_FOLDER_ID -ne '1jy3NdoAu6Jp_jIp6miKa1asIBFmfADhb') { throw 'FOUR_D_FOLDER_MISMATCH' }
if ($env:MCM_CURRENT -ne 'MCM-008') { throw 'MCM_CURRENT_MISMATCH' }
if ($env:MCM_BASE -ne 'MCM-007') { throw 'MCM_BASE_MISMATCH' }
if ($env:R000_HELD_ACROSS_TURN -ne 'TRUE') { throw 'R000_HELD_ACROSS_TURN_MISMATCH' }
if ($env:R000_RECUR_ON_EVERY_DELTA -ne 'TRUE') { throw 'R000_RECUR_ON_EVERY_DELTA_MISMATCH' }
if ($env:R000_PRESENT_AT_READBACK -ne 'TRUE') { throw 'R000_PRESENT_AT_READBACK_MISMATCH' }
if ($env:MULTI_SLOT_IS_MULTI_TIMELINE -ne 'FALSE') { throw 'MULTI_SLOT_IS_MULTI_TIMELINE_MISMATCH' }
if ($env:MULTI_SLOT_IS_MULTI_POINTER -ne 'FALSE') { throw 'MULTI_SLOT_IS_MULTI_POINTER_MISMATCH' }
if ($env:ALL_OLD_RUNTIME -ne 'FALSE') { throw 'ALL_OLD_RUNTIME_MISMATCH' }
if ($env:OLD_ROOT_RUNTIME -ne 'FALSE') { throw 'OLD_ROOT_RUNTIME_MISMATCH' }

Write-Output "RUNTIME_N_PLUS=$env:RUNTIME_N_PLUS"
Write-Output "RUNTIME_SCHEMA=$env:RUNTIME_SCHEMA"
Write-Output "R000_CURRENT=$env:R000_CURRENT_CARRIER_DRIVE_ID"
Write-Output "4D_CURRENT=$env:FOUR_D_FOLDER_ID/$env:MCM_CURRENT"
