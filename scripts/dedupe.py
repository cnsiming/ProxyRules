#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dedupe.py — 检查各 .list 规则文件中的重复项
用法：在仓库根目录运行  python3 scripts/dedupe.py
- 文件内重复：同一文件里同一条规则出现多次
- 跨文件重复：同一域名出现在多个列表中（合集 AI.list 除外）
发现任何问题退出码为 1，可用于提交前检查 / CI。
"""
import glob
import sys
from collections import defaultdict

IGNORE_FILES = {"AI.list"}  # 合集本身是子列表的并集，跳过跨文件检查
COMMENT_PREFIXES = ("#", ";", "//", "!")


def normalize(line: str) -> str:
    """统一大小写，便于比对：DOMAIN,gemini.GOOGLE.com -> DOMAIN,gemini.google.com"""
    parts = [p.strip() for p in line.split(",")]
    if len(parts) >= 2:
        parts[0] = parts[0].upper()
        parts[1] = parts[1].lower()
    return ",".join(parts)


def read_rules(path: str):
    rules = []
    with open(path, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith(COMMENT_PREFIXES):
                continue
            rules.append((lineno, normalize(line)))
    return rules


def main() -> int:
    files = sorted(glob.glob("*.list"))
    if not files:
        print("未找到任何 .list 文件，请在仓库根目录运行")
        return 1

    problems = 0
    domain_map = defaultdict(list)  # 域名 -> [(文件, 行号)]，用于跨文件检查

    for path in files:
        rules = read_rules(path)
        seen = {}
        for lineno, rule in rules:
            key = rule.split(",")[1] if "," in rule else rule  # 以域名维度查重
            if rule in seen:
                print(f"[文件内重复] {path}:{lineno} 与 {path}:{seen[rule]} → {rule}")
                problems += 1
            else:
                seen[rule] = lineno
            if path not in IGNORE_FILES:
                domain_map[key].append((path, lineno))

    for domain, where in sorted(domain_map.items()):
        files_hit = {p for p, _ in where}
        if len(files_hit) > 1:
            locs = ", ".join(f"{p}:{n}" for p, n in where)
            print(f"[跨文件重复] {domain} 出现在多处 → {locs}")
            problems += 1

    if problems:
        print(f"\n共发现 {problems} 个问题，请修复后再提交。")
        return 1
    total = sum(len(read_rules(f)) for f in files)
    print(f"✔ 检查通过：{len(files)} 个文件，共 {total} 条规则，无重复。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
