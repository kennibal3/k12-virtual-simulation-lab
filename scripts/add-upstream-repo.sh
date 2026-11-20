#!/usr/bin/env bash
# 快捷脚本：当你以后在 GitHub 上发现新的虚拟仿真仓库时，用它一键挂载为子模块
set -e

if [ "$#" -lt 2 ]; then
  echo "用法: ./scripts/add-upstream-repo.sh <简称目录名> <GitHub仓库克隆地址>"
  echo "示例: ./scripts/add-upstream-repo.sh 3dmol https://github.com/3dmol/3Dmol.js.git"
  exit 1
fi

NAME="$1"
REPO_URL="$2"
TARGET_PATH="packages/$NAME"

echo "🚀 正在将 $REPO_URL 作为 Git 子模块挂载到 $TARGET_PATH ..."
git submodule add "$REPO_URL" "$TARGET_PATH"
git submodule update --init --recursive "$TARGET_PATH"

echo ""
echo "✅ 挂载成功！接下来你只需要："
echo "1. 打开 config/experiments.json"
echo "2. 在 upstreams 和 experiments 数组中添加该实验的名称、学科和入口路径，网页门户即会自动显示！"
