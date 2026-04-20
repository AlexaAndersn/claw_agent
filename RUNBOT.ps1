$ErrorActionPreference = "Continue"
$python = "C:\Users\Диана\AppData\Local\Programs\Python\Python312\python.exe"
$project = "D:\claw-агент\main.py"
$dir = "D:\claw-агент"

Write-Host "Starting Claw-Agent..."
& $python $project

Read-Host "Press Enter to exit"