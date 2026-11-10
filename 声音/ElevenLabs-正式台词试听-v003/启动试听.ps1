$projectRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
if (-not (Get-NetTCPConnection -State Listen -LocalPort 8971 -ErrorAction SilentlyContinue)) {
    Start-Process -FilePath 'E:/Python/python.exe' -ArgumentList 'scripts/serve_eleven_review_v003.py' -WorkingDirectory $projectRoot -WindowStyle Hidden
}
Start-Process 'http://127.0.0.1:8971/%E5%A3%B0%E9%9F%B3/ElevenLabs-%E6%AD%A3%E5%BC%8F%E5%8F%B0%E8%AF%8D%E8%AF%95%E5%90%AC-v003/%E8%AF%95%E5%90%AC.html'
