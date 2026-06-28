param(
    [Parameter(Mandatory = $true)]
    [string]$InputVideo,
    [string]$OutputGif = ""
)

$ProjectRoot = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot "activate_env.ps1")

if ($OutputGif -eq "") {
    $BaseName = [System.IO.Path]::GetFileNameWithoutExtension($InputVideo)
    $OutputGif = Join-Path $ProjectRoot "outputs\gifs\$BaseName.gif"
}

$OutputDir = Split-Path -Parent $OutputGif
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$Palette = Join-Path $env:TEMP "pointgroup_palette.png"
ffmpeg -y -i $InputVideo -vf "fps=15,scale=720:-1:flags=lanczos,palettegen" -frames:v 1 -update 1 $Palette
ffmpeg -y -i $InputVideo -i $Palette -lavfi "fps=15,scale=720:-1:flags=lanczos[x];[x][1:v]paletteuse" $OutputGif

Write-Host "GIF written to $OutputGif"
