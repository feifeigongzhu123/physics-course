param(
  [string]$Manifest,
  [string]$Root,
  [string]$Ffmpeg = "",
  [string]$Bitrate = "48k"
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$items = Get-Content $Manifest -Raw -Encoding UTF8 | ConvertFrom-Json
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice('Microsoft Huihui Desktop')
$synth.Rate = -1
$fmt = New-Object System.Speech.AudioFormat.SpeechAudioFormatInfo(
  16000,
  [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen,
  [System.Speech.AudioFormat.AudioChannel]::Mono
)
$n = 0
$skipped = 0
foreach($it in $items){
  $path = Join-Path $Root $it.path
  $dir = Split-Path $path -Parent
  if(!(Test-Path $dir)){ New-Item -ItemType Directory -Path $dir -Force | Out-Null }
  if((Test-Path $path) -and ((Get-Item $path).Length -gt 1000)){
    $skipped++
    Write-Output ("[skip] {0}" -f $it.path)
    continue
  }
  if($path.ToLower().EndsWith('.mp3')){
    if(!$Ffmpeg){ throw "MP3 输出需要 -Ffmpeg 参数" }
    $tmp = "$path.tmp.wav"
    $synth.SetOutputToWaveFile($tmp, $fmt)
    $synth.Speak($it.text)
    $synth.SetOutputToNull()
    & $Ffmpeg -hide_banner -loglevel error -y -i $tmp -vn -ac 1 -ar 16000 -c:a libmp3lame -b:a $Bitrate $path
    if($LASTEXITCODE -ne 0){ throw "ffmpeg 失败：$($it.path)" }
    Remove-Item $tmp -Force
  }else{
    $synth.SetOutputToWaveFile($path, $fmt)
    $synth.Speak($it.text)
    $synth.SetOutputToNull()
  }
  $n++
  Write-Output ("[{0}/{1}] {2}" -f $n, $items.Count, $it.path)
}
$synth.Dispose()
Write-Output "DONE new=$n skipped=$skipped"
