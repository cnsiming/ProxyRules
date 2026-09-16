#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stats.py — 统计各 .list 规则文件的数量（按规则类型分组）
用法：在仓库根目录运行  python3 scripts/stats.py
"""
import glob
from collections import Counter

COMMENT_PREFIXES = ("#", ";", "//", "!")


def main() -> int:
    files = sorted(glob.glob("*.list"))
    if not files:
        print("未找到任何 .list 文件，请在仓库根目录运行")
        return 1

    grand = 0
    for path in files:
        counter = Counter()
        with open(path, encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith(COMMENT_PREFIXES):
                    continue
                rtype = line.split(",", 1)[0].strip().upper()
                counter[rtype] += 1
        total = sum(counter.values())
        grand += total
        detail = "，".join(f"{k} × {v}" for k, v in counter.most_common())
        print(f"{path:<18} 共 {total:>3} 条  |  {detail}")

    print("-" * 50)
    print(f"{'合计':<18} 共 {grand:>3} 条")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
