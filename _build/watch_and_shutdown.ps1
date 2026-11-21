param(
  [string]$WatchLog = 'D:\AI\ZCode\physics\_build\shutdown-watch.log',
  [string]$PidFile = 'D:\AI\ZCode\physics\_build\shutdown-watch.pid',
  [string]$QueueLog = 'D:\AI\ZCode\english-daily\audio\queue.log'
)
$ErrorActionPreference = 'Stop'
function Write-Log($t) {
  Add-Content -Path $WatchLog -Value ((Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + ' ' + $t) -Encoding UTF8
}
$PID | Set-Content -Path $PidFile -Encoding ASCII
Write-Log ("WATCH_START pid=" + $PID)
$seen = $false
while ($true) {
  $queue = Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" |
    Where-Object { $_.CommandLine -like '*run_high_school_queue.ps1*' }
  if (-not $queue) { break }
  if (-not $seen) {
    Write-Log ("QUEUE_ALIVE pid=" + ($queue.ProcessId -join ','))
    $seen = $true
  }
  Start-Sleep -Seconds 60
}
Write-Log 'QUEUE_GONE'
try {
  $tail = Get-Content $QueueLog -Tail 4 -ErrorAction SilentlyContinue
  Write-Log ('LAST: ' + ($tail -join ' | '))
} catch {}
Start-Sleep -Seconds 30
Write-Log 'SHUTDOWN_SCHEDULED'
shutdown /s /t 60 /c "物理语音第二批与英词通音频队列均已完成，系统将在 60 秒后关机"
