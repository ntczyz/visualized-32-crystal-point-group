$ProjectRoot = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot "activate_env.ps1")

Write-Host ""
Write-Host "Checking command versions..."
python --version
python -m pip --version
manimgl --version
ffmpeg -version | Select-Object -First 1
git --version

Write-Host ""
Write-Host "Checking Python imports..."
python -c "import manimlib, numpy, scipy, imageio, imageio_ffmpeg; print('imports ok'); print('imageio ffmpeg:', imageio_ffmpeg.get_ffmpeg_exe())"

Write-Host ""
Write-Host "Environment check complete."

