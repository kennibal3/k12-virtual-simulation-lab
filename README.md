# 🔬 K12 开源虚拟仿真实验室总仓 (K12 Virtual Simulation Lab Hub)

这是一个面向 **K12 基础教育（小学 / 初中 / 高中）**，集成了全球四大顶尖开源理科虚拟仿真引擎的统一门户与自动化同步仓库。

## 🌟 核心集成的四大上游开源引擎

| 引擎名称 | 上游 GitHub 仓库 | 适用学科与核心特色 | 同步机制 |
| :--- | :--- | :--- | :--- |
| **🟠 PhET** | [`phetsims`](https://github.com/phetsims) | 覆盖物理、化学、生物、地科课标的引导式交互实验 | `scripts/sync-phet.py` 自动拉取最新中文单文件版 |
| **🟢 Ray Optics** | [`ricktu288/ray-optics`](https://github.com/ricktu288/ray-optics) | 初高中 2D 几何光学自由沙盒（透镜、棱镜、光栅、光纤） | `git submodule` (`packages/ray-optics`) |
| **🔵 CircuitJS1** | [`sharpie7/circuitjs1`](https://github.com/sharpie7/circuitjs1) | 初高中电学可视化神器（动态电子流动动画 + 电势颜色 + 示波器） | `git submodule` (`packages/circuitjs1`) |
| **🟣 Concord Lab** | [`concord-consortium/lab`](https://github.com/concord-consortium/lab) | 微观分子热运动与相变、化学键断裂生成、生物 DNA 转录翻译蛋白质 | `git submodule` (`packages/concord-lab`) |

---

## 📁 仓库目录结构

```text
.
├── .github/workflows/
│   └── sync-and-deploy.yml      # GitHub Actions: 每周自动拉取四大上游更新并部署 GitHub Pages
├── config/
│   └── experiments.json         # 【核心配置文件】所有实验的分类、标签、在线/本地路径清单
├── packages/                    # 挂载上游 Git Submodules 的目录
│   ├── ray-optics/              # -> github.com/ricktu288/ray-optics
│   ├── circuitjs1/              # -> github.com/sharpie7/circuitjs1
│   └── concord-lab/             # -> github.com/concord-consortium/lab
├── phet-sims/                   # 存放自动同步下来的 PhET 单文件离线包 (*_zh_CN.html)
├── scripts/
│   ├── sync-all.sh              # 一键初始化/更新所有 Git 子模块并下载最新 PhET 实验
│   ├── sync-phet.py             # 根据 config/experiments.json 自动同步 PhET 实验
│   └── add-upstream-repo.sh     # 一键扩充新的第三方 GitHub 仿真仓库作为子模块
└── index.html                   # 统一前端门户（支持学科筛选、引擎筛选、关键词搜索、在线/本地源切换）
```

---

## 🚀 快速开始

### 1. 本地预览门户
由于浏览器安全策略限制直接双击读取 JSON，请在项目根目录下启动任意静态服务：
```bash
python3 -m http.server 8765
```
然后浏览器访问：`http://localhost:8765`

### 2. 一键同步所有上游最新源码与实验包
当你想把 **Ray Optics**、**CircuitJS1**、**Concord Lab** 和 **PhET** 同步到本地或更新到官方最新版本时，只需运行：
```bash
chmod +x scripts/*.sh
./scripts/sync-all.sh
```
同步完成后，你可以在网页右上角将模式从 **「🌐 在线源」** 切换为 **「📂 本地仓库源」**，实现完全断网离线秒开！

### 3. 以后如何扩充新的 GitHub 虚拟仿真仓库？
1. 运行一键挂载脚本：
   ```bash
   ./scripts/add-upstream-repo.sh <新项目目录名> <GitHub仓库地址>
   ```
2. 打开 [`config/experiments.json`](./config/experiments.json)，在 `experiments` 数组中添加新实验的标题、学科（`physics` / `chemistry` / `biology` / `earth`）和路径即可，前端会自动生成分类卡片！
