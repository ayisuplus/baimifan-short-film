$projectRoot=Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
if (-not (Get-NetTCPConnection -LocalPort 8977 -State Listen -ErrorAction SilentlyContinue)) {
    Start-Process -FilePath 'E:/Python/python.exe' -ArgumentList 'scripts/serve_voice_revision_v004.py' -WorkingDirectory $projectRoot -WindowStyle Hidden
}
Write-Host '试听入口：http://127.0.0.1:8977/声音/声线返修试听-v004/试听.html'
