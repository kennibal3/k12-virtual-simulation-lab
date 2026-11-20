#!/usr/bin/env bash
# Mac / Linux 一键启动离线虚拟实验室脚本
cd "$(dirname "$0")"
PORT=8765
echo "🚀 正在启动 K12 离线虚拟仿真实验室 (http://localhost:$PORT) ..."
(sleep 1 && open "http://localhost:$PORT" 2>/dev/null || xdg-open "http://localhost:$PORT" 2>/dev/null) &
python3 -m http.server $PORT
