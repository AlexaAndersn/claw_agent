' Запуск бота через VBScript
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "D:\claw-агент"
WshShell.Run """C:\Users\Диана\AppData\Local\Programs\Python\Python312\python.exe"" main.py", 1, True