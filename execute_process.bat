@echo off
:loop
echo Running Python script...
C:\Users\olumi\AppData\Local\Programs\Python\Python311\python.exe D:\open_banking_assessment\pipeline\dataProcessing.py
echo Waiting for 60 seconds before running the script again...
timeout /t 120 >nul
goto loop