@echo off
:loop
echo Waiting for files in the directory...
REM Check if there are any files in the specific directory
for %%f in (C:\path\to\directory\*.*) do (
    echo Found new file: %%~nxf
    REM Execute the Python script with the new file as argument
    python C:\path\to\your_script.py "%%~f"
    REM Optionally, you can move or delete the processed file here
    REM move "%%~f" C:\path\to\destination\   (to move the file)
    REM del "%%~f"   (to delete the file)
)
echo No new files found. Waiting for 10 seconds before checking again...
timeout /t 10 /nobreak >nul
goto loop