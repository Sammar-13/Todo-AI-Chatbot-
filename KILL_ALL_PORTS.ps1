# PowerShell Script to Kill ALL Processes on Ports 3000-3005 and 8000
# Run this as Administrator

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  KILLING ALL PROCESSES ON PORTS"
Write-Host "========================================" -ForegroundColor Cyan

# Kill all processes listening on ports 3000-3005 and 8000
$ports = @(3000, 3001, 3002, 3003, 3004, 3005, 8000)

foreach ($port in $ports) {
    Write-Host "`nKilling processes on port $port..." -ForegroundColor Yellow

    $processes = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue

    if ($processes) {
        foreach ($proc in $processes) {
            $process = Get-Process -Id $proc.OwningProcess -ErrorAction SilentlyContinue
            if ($process) {
                Write-Host "  Killing: $($process.Name) (PID: $($process.Id))"
                Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
            }
        }
    } else {
        Write-Host "  Port $port is FREE" -ForegroundColor Green
    }
}

# Wait for ports to be released
Write-Host "`nWaiting 5 seconds for ports to be released..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Verify all ports are free
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  VERIFYING PORTS ARE FREE"
Write-Host "========================================" -ForegroundColor Cyan

$allFree = $true
foreach ($port in $ports) {
    $connection = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($connection) {
        Write-Host "❌ Port $port is STILL IN USE" -ForegroundColor Red
        $allFree = $false
    } else {
        Write-Host "✅ Port $port is FREE" -ForegroundColor Green
    }
}

Write-Host ""
if ($allFree) {
    Write-Host "✅ ALL PORTS ARE FREE! You can now start the servers." -ForegroundColor Green
} else {
    Write-Host "❌ Some ports are still in use. Please try again or restart Windows." -ForegroundColor Red
}
