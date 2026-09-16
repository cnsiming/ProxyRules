#!/usr/bin/env bash
# ============================================================
# update.sh — 拉取 ProxyRules 最新列表到本地
# 用法：
#   bash scripts/update.sh [目标目录]        默认 ~/ProxyRules
# 环境变量：
#   PROXYRULES_BASE  覆盖仓库 raw 地址（fork 后改成自己的）
# ============================================================
set -euo pipefail

BASE="${PROXYRULES_BASE:-https://raw.githubusercontent.com/cnsiming/ProxyRules/main}"
DEST="${1:-$HOME/ProxyRules}"
FILES=(AI.list AI-General.list OpenAI.list Claude.list)

mkdir -p "$DEST"

for f in "${FILES[@]}"; do
  echo "→ 下载 $f"
  curl -fsSL --retry 3 "$BASE/$f" -o "$DEST/$f"
done

echo "✔ 完成，共 ${#FILES[@]} 个列表，保存在：$DEST"
