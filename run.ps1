# BOM marker for UTF-8
$OutputEncoding = [System.Text.Encoding]::UTF8

Set-Location "D:\claw-агент"

python simple_test.py

if (Test-Path test_run.log) {
    Get-Content test_run.log
} else {
    Write-Host "No log found"
}

Read-Host "Press Enter to exit"