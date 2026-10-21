@echo off
cd /d "%~dp0"
echo [1/2] installing segno ...
python -m pip install segno
echo.
echo [2/2] running build_site.py ...
python tools\build_site.py
echo.
echo Done. Press any key to close.
pause >nul
