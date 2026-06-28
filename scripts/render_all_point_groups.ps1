param(
    [string]$Quality = "-l",
    [int]$GifWidth = 720,
    [switch]$Full
)

$ProjectRoot = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot "activate_env.ps1")

$BatchScript = Join-Path $PSScriptRoot "render_all_point_groups.py"
$Arguments = @($BatchScript, "--quality", $Quality, "--gif-width", $GifWidth)
if ($Full) {
    $Arguments += "--full"
}
python @Arguments
exit $LASTEXITCODE
