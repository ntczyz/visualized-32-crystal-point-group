param(
    [string]$SceneName = "PointGroup4",
    [string]$Quality = "-m",
    [string]$FileName = ""
)

$ProjectRoot = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot "activate_env.ps1")

$SceneFile = Join-Path $ProjectRoot "scenes\point_groups.py"
$VideoDir = Join-Path $ProjectRoot "outputs\videos"

if ($FileName -eq "") {
    manimgl $SceneFile $SceneName -w $Quality --video_dir $VideoDir
} else {
    manimgl $SceneFile $SceneName -w $Quality --video_dir $VideoDir --file_name $FileName
}
