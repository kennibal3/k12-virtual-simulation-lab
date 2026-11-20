@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PORT=8765
echo 🚀 正在启动 K12 离线虚拟仿真实验室 (http://localhost:%PORT%) ...
start http://localhost:%PORT%
python -m http.server %PORT%
pause
