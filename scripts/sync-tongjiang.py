#!/usr/bin/env python3
"""
读取 packages/tongjiang-lab/catalog.json 中的全部 54 门中国高中 3D 互动科学实验课程，
自动合并到 config/experiments.json 中，使得前端门户可以直接按学科和引擎浏览全部课程。
"""
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "config" / "experiments.json"
TONGJIANG_CATALOG = ROOT_DIR / "packages" / "tongjiang-lab" / "catalog.json"

SUBJECT_MAP = {
    "phys": ("physics", "物理"),
    "chem": ("chemistry", "化学"),
    "bio": ("biology", "生物"),
    "geo": ("earth", "地理/地科"),
}


def sync_tongjiang():
    if not TONGJIANG_CATALOG.exists():
        print(f"⚠️ 未找到 {TONGJIANG_CATALOG}，请先初始化 packages/tongjiang-lab 子模块。")
        return

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    with open(TONGJIANG_CATALOG, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    # 1. 确保 upstreams 中包含 tongjiang-lab
    upstreams = config.get("upstreams", [])
    if not any(u.get("id") == "tongjiang-lab" for u in upstreams):
        upstreams.append({
            "id": "tongjiang-lab",
            "name": "铜匠实验室 (Tongjiang Lab)",
            "repo": "https://github.com/sdvch/tongjiang-lab",
            "submodulePath": "packages/tongjiang-lab",
            "syncType": "git-submodule",
            "badgeColor": "#f43f5e",
            "description": "面向中国高中新课标的 3D 互动科学实验课程（物理、化学、生物、地理 54 门单文件 3D 实验）"
        })
        config["upstreams"] = upstreams

    # 2. 移除旧的 tongjiang-lab 实验条目，重新从最新 catalog.json 导入
    other_exps = [e for e in config.get("experiments", []) if e.get("source") != "tongjiang-lab"]

    tj_exps = []
    for item in catalog:
        slug = item["slug"]
        sub_key = item.get("subject", "phys")
        subject, subject_label = SUBJECT_MAP.get(sub_key, ("physics", "物理"))
        title = item["title"]
        question = item.get("question", "")
        textbooks = item.get("textbook", [])
        steps = item.get("steps", [])
        course_type = item.get("type", "3D实验")

        desc_parts = []
        if question:
            desc_parts.append(question)
        if textbooks:
            desc_parts.append(f"【课标：{textbooks[0]}】")
        description = " ".join(desc_parts)

        tags = [course_type] + steps[:3]

        tj_exps.append({
            "id": f"tj-{slug}",
            "title": f"{title} (3D)",
            "source": "tongjiang-lab",
            "sourceLabel": "铜匠 3D",
            "subject": subject,
            "subjectLabel": subject_label,
            "grade": ["高中"],
            "tags": tags,
            "description": description,
            "onlineUrl": f"./packages/tongjiang-lab/courses/{slug}.html",
            "localUrl": f"./packages/tongjiang-lab/courses/{slug}.html",
            "repoUrl": "https://github.com/sdvch/tongjiang-lab"
        })

    # 将精选的几个铜匠 3D 代表实验排到最前面方便体验，其余保持跟在后面
    featured_slugs = {"tj-photoelectric-step", "tj-current-field-step", "tj-ball-stick-step", "tj-galvanic-step", "tj-mitosis-step", "tj-insolation-step"}
    featured_tj = [e for e in tj_exps if e["id"] in featured_slugs]
    rest_tj = [e for e in tj_exps if e["id"] not in featured_slugs]

    config["experiments"] = other_exps + featured_tj + rest_tj

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    print(f"✅ 成功从铜匠实验室 catalog.json 导入 {len(tj_exps)} 门中国高中 3D 虚拟实验！当前平台总实验数: {len(config['experiments'])}")


if __name__ == "__main__":
    sync_tongjiang()
