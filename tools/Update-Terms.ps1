param(
    [Parameter(Mandatory)][ValidateSet('FQ-Lite','CurbQuill','Day-Leaf','MileQuill-Lite','PocketQuill')][string]$App,
    [Parameter(Mandatory)][string]$Agreement,
    [switch]$Approved
)

$ErrorActionPreference = 'Stop'
$tool = Join-Path $PSScriptRoot 'update_terms.py'
$toolArgs = @($tool, $App, (Resolve-Path -LiteralPath $Agreement).Path)
if ($Approved) { $toolArgs += '--approved' }

$package = Get-AppxPackage -Name 'OpenAI.CodexPrimaryRuntime*' | Sort-Object Version -Descending | Select-Object -First 1
if ($package) {
    $runtime = Join-Path $package.InstallLocation 'dependencies\python\python.exe'
    if (Test-Path -LiteralPath $runtime) { & $runtime @toolArgs; exit $LASTEXITCODE }
}
if (Get-Command py.exe -ErrorAction SilentlyContinue) { & py.exe -3 @toolArgs; exit $LASTEXITCODE }
& python.exe @toolArgs
exit $LASTEXITCODE

