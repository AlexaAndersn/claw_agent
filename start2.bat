@echo off
chcp 65001 >nul
cd /d "D:\claw-агент"
python -c "
import sys
import io
old_stdout = sys.stdout
old_stderr = sys.stderr
sys.stdout = io.TextIOWrapper(open('stdout.log', 'wb', encoding='utf-8'), encoding='utf-8', line_buffering=True)
sys.stderr = io.TextIOWrapper(open('stderr.log', 'wb', encoding='utf-8'), encoding='utf-8', line_buffering=True)
import main
" 2>&1
echo Check logs:
type stdout.log 2>&1
type stderr.log 2>&1
pause