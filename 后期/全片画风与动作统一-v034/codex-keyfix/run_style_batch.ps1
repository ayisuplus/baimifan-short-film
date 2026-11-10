# 中段画风统一：第一批硬偏离镜头重绘（Codex image-to-image）
# 逐张串行执行，避免并发触发节流；每张单独留日志便于复查。
$ErrorActionPreference = 'Continue'
$dir = 'E:\projects\内容创作\故事短片\白米饭\后期\全片画风与动作统一-v034\codex-keyfix'
$v32 = 'G:\comfyui\ComfyUI\ComfyUI\output\Baimifan\v032'

$jobs = @(
  @{ prompt = 'prompt-090b.txt'; src = "$v32\090b-key-r1_00001_.png"; log = 'codex-090b.log' },
  @{ prompt = 'prompt-074.txt';  src = "$v32\074-key-r1_00001_.png";  log = 'codex-074.log' },
  @{ prompt = 'prompt-065b.txt'; src = "$v32\065b-key-r2_00001_.png"; log = 'codex-065b.log' },
  @{ prompt = 'prompt-062b.txt'; src = "$v32\062b-key-r1_00001_.png"; log = 'codex-062b.log' }
)

foreach ($j in $jobs) {
  Write-Output "=== START $($j.prompt) ==="
  $text = Get-Content -Raw (Join-Path $dir $j.prompt)
  $text | codex exec --sandbox workspace-write --skip-git-repo-check -i $j.src - 2>&1 |
    Tee-Object -FilePath (Join-Path $dir $j.log) |
    Select-Object -Last 18
  Write-Output "=== END $($j.prompt) ==="
}
Write-Output 'ALL DONE'
