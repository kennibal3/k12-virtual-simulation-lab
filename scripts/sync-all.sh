#!/usr/bin/env bash
# 初始化或更新三大核心开源引擎的 Git Submodules + 同步 PhET 最新实验
set -e

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p packages phet-sims

echo "===================================================="
echo "1. 检查并挂载三大开源引擎的 Git Submodules..."
echo "===================================================="

add_submodule_if_missing() {
  local name="$1"
  local url="$2"
  local path="packages/$name"
  if [ ! -d "$path/.git" ] && [ ! -f "$path/.git" ]; then
    echo "➕ 正在添加子模块: $name ($url) -> $path"
    git submodule add "$url" "$path" || true
  else
    echo "✅ 子模块已存在: $path"
  fi
}

# 1. Ray Optics (几何光学沙盒)
add_submodule_if_missing "ray-optics" "https://github.com/ricktu288/ray-optics.git"

# 2. CircuitJS1 (动态电流电路仿真器)
add_submodule_if_missing "circuitjs1" "https://github.com/sharpie7/circuitjs1.git"

# 3. Concord Consortium Lab (微观分子动力学、化学反应与生物 DNA 引擎)
add_submodule_if_missing "concord-lab" "https://github.com/concord-consortium/lab.git"

# 4. 铜匠实验室 Tongjiang Lab (中国高中新课标 3D 互动科学实验)
add_submodule_if_missing "tongjiang-lab" "https://github.com/sdvch/tongjiang-lab.git"

echo ""
echo "===================================================="
echo "2. 从上游 GitHub 仓库拉取最新提交 (git submodule update --remote)..."
echo "===================================================="
git submodule update --init --recursive --remote --merge

echo ""
echo "===================================================="
echo "3. 同步铜匠实验室 catalog.json 全部 3D 课程到 experiments.json..."
echo "===================================================="
python3 scripts/sync-tongjiang.py

echo ""
echo "===================================================="
echo "4. 同步 PhET 最新版中文单文件实验 (scripts/sync-phet.py)..."
echo "===================================================="
python3 scripts/sync-phet.py

echo ""
echo "🎉 全部五大引擎（铜匠 3D + PhET + Ray Optics + CircuitJS1 + Concord Lab）同步完毕！"
