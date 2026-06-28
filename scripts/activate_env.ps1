$ProjectRoot = Split-Path -Parent $PSScriptRoot
$VenvRoot = Join-Path $ProjectRoot ".venv"
$VenvScripts = Join-Path $VenvRoot "Scripts"
$CondaBin = "E:\VSCode\Conda\Library\bin"
$GitCmd = "E:\Git\cmd"
$MikTeXScripts = Join-Path $ProjectRoot "tools\miktex-env\Scripts"

if (-not (Test-Path -LiteralPath (Join-Path $VenvScripts "python.exe"))) {
    throw "Project virtual environment was not found at $VenvRoot"
}

$env:PATH = "$VenvScripts;$MikTeXScripts;$CondaBin;$GitCmd;$env:PATH"
$env:PYTHONPATH = $ProjectRoot

Write-Host "Pointgroup environment activated"
Write-Host "Project root: $ProjectRoot"
Write-Host "Python: $(Join-Path $VenvScripts 'python.exe')"
Write-Host "ManimGL: $(Join-Path $VenvScripts 'manimgl.exe')"
Write-Host "FFmpeg: $(Join-Path $CondaBin 'ffmpeg.exe')"
Write-Host "LaTeX: $(Join-Path $MikTeXScripts 'latex.exe')"
Write-Host "dvisvgm: $(Join-Path $MikTeXScripts 'dvisvgm.exe')"
Write-Host "Git: $(Join-Path $GitCmd 'git.exe')"
