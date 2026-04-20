@echo off
chcp 65001 >nul
cd /d "D:\claw-агент"
python -c "import main; print('Import OK')" 2>&1
echo Done
pause