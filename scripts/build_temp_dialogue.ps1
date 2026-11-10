param(
  [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot),
  [string]$ManifestPath = '镜头设计\shot-plan-v0.5.json',
  [string]$Revision = 'v005'
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$manifest = Get-Content -LiteralPath (Join-Path $ProjectRoot $ManifestPath) -Raw -Encoding UTF8 | ConvertFrom-Json
$recordPath = Join-Path $ProjectRoot ("镜头设计\生成记录\临时读稿-{0}.json" -f $Revision)
if (Test-Path -LiteralPath $recordPath) { throw "Preserve existing generation record: $recordPath" }
$destination = Join-Path $ProjectRoot '镜头设计\临时声音'
New-Item -ItemType Directory -Path $destination -Force | Out-Null
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$voices = @{DeepSeek='Microsoft Yaoyao'; ChatGPT='Microsoft Huihui Desktop'; Claude='Microsoft Huihui'; '教主'='Microsoft Kangkang'; '教徒'='Microsoft Kangkang'; Qwen='Microsoft Huihui'; '千问'='Microsoft Huihui'; Gemini='Microsoft Yaoyao'; Grok='Microsoft Huihui'; Kimi='Microsoft Huihui'}
$available = @($synth.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name })
$records = @()
$reused = @()
foreach ($shot in $manifest.shots) {
  foreach ($cue in $shot.dialogue_cues) {
    if ($available -notcontains $voices[$cue.speaker]) { throw "Missing voice for speaker: $($cue.speaker)" }
  }
}
try {
  foreach ($shot in $manifest.shots) {
    foreach ($cue in $shot.dialogue_cues) {
      $target = Join-Path $ProjectRoot $cue.file
      if (Test-Path -LiteralPath $target) {
        $reused += [pscustomobject]@{shot_id=$shot.id; file=$cue.file; sha256=(Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash}
        continue
      }
      $voice = $voices[$cue.speaker]
      if ($available -notcontains $voice) { throw "Missing configured local temporary voice: $voice" }
      $synth.SelectVoice($voice)
      $synth.Rate = 1
      $synth.Volume = 85
      $spoken = $cue.text.Replace('Claude','克劳德').Replace('Gemini','杰米奈').Replace('Grok','格洛克').Replace('Kimi','基米').Replace('Llama','拉玛')
      $synth.SetOutputToWaveFile($target)
      $synth.Speak($spoken)
      $synth.SetOutputToNull()
      $records += [pscustomobject]@{shot_id=$shot.id; speaker=$cue.speaker; original_text=$cue.text; spoken_text=$spoken; pronunciation_note='英文角色名用中文近似读音，仅用于临时节奏检查，剧本原文不改。'; voice=$voice; rate=1; file=$cue.file; sha256=(Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash; engine='Windows System.Speech local'; listening_status='未完成实际听审；不是正式声线或表演'}
    }
  }
} finally { $synth.Dispose() }
[pscustomobject]@{generated=$records; reused=$reused; manifest=$ManifestPath} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $recordPath -Encoding UTF8
Write-Output ("Generated {0} local temporary dialogue clips." -f $records.Count)
