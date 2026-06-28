$ProjectRoot = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot "activate_env.ps1")

foreach ($SceneName in @("PointGroup4", "PointGroupMMM", "PointGroup432")) {
    & (Join-Path $PSScriptRoot "render_one.ps1") -SceneName $SceneName -Quality "-m"
}

