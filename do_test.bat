@echo off
cd /d D:\claw-агент
python -c "exec(open('simple_test.py').read())" > result.txt 2>&1
type result.txt
if exist test_run.log type test_run.log
pause