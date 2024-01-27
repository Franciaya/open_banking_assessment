@echo off
:loop
echo Running Python script...
C:\path\to\python\executable\python.exe C:\path\to\your_script.py
echo Waiting for 60 seconds before running the script again...
timeout /t 60 /nobreak >nul
goto loop