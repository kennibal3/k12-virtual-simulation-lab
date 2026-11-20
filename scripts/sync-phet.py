#!/usr/bin/env python3
"""
自动读取 config/experiments.json 中所有的 PhET 实验 (source == "phet")，
并从 PhET 官方构建源自动拉取最新的中文单文件离线版 (_zh_CN.html) 到 phet-sims/ 目录。
"""
import json
import os
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "config" / "experiments.json"
OUTPUT_DIR = ROOT_DIR / "phet-sims"


def sync_phet():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    experiments = data.get("experiments", [])
    phet_exps = [e for e in experiments if e.get("source") == "phet" and e.get("phetSlug")]

    print(f"🔍 发现 {len(phet_exps)} 个配置在册的 PhET 实验，开始检查与同步最新版本...")

    for exp in phet_exps:
        slug = exp["phetSlug"]
        title = exp["title"]
        url = f"https://phet.colorado.edu/sims/html/{slug}/latest/{slug}_zh_CN.html"
        target_file = OUTPUT_DIR / f"{slug}_zh_CN.html"

        print(f"⬇️  正在同步 [{title}] ({slug})...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 K12-Virtual-Lab-Sync"})
            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read()
                with open(target_file, "wb") as out:
                    out.write(content)
            size_mb = len(content) / (1024 * 1024)
            print(f"   ✅ 已更新至本地: {target_file.relative_to(ROOT_DIR)} ({size_mb:.2f} MB)")
        except Exception as e:
            print(f"   ❌ 同步失败 [{slug}]: {e}")

    print("\n🎉 所有 PhET 实验离线单文件同步完成！")


if __name__ == "__main__":
    sync_phet()
