@echo off
for %%i in (%*) do (
    if not exist %%i (
        type nul > %%i
    ) else (
        echo %%i already exists
    )
)
