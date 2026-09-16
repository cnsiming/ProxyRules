# ProxyRules

AI 服务分流规则集：把不同 AI 服务的流量分流到不同节点，互不影响。

**仅含公开域名规则，不含任何节点、订阅地址、密码或证书。**

## 文件说明

| 文件 | 用途 |
| --- | --- |
| `AI.list` | AI 总分类：通用 AI + OpenAI + Claude 的合集（去重后），适合简化配置 |
| `AI-General.list` | 通用 AI：Gemini、Grok、Perplexity、Poe、Copilot 等 |
| `OpenAI.list` | OpenAI / ChatGPT / LiveKit / Arkose / Azure（可选） |
| `Claude.list` | Anthropic / Claude / Statsig |
| `scripts/update.sh` | 自动更新：拉取本仓库最新列表到本地 |
| `scripts/dedupe.py` | 去重：检查列表内/列表间的重复与冲突 |
| `scripts/stats.py` | 统计：各列表规则数量（按类型分组） |

## 引用方式

### Quantumult X

```ini
[filter_remote]
https://raw.githubusercontent.com/cnsiming/ProxyRules/main/OpenAI.list, tag=OpenAI, force-policy=OpenAI, update-interval=86400, opt-parser=false, enabled=true
https://raw.githubusercontent.com/cnsiming/ProxyRules/main/Claude.list, tag=Claude, force-policy=Claude, update-interval=86400, opt-parser=false, enabled=true
https://raw.githubusercontent.com/cnsiming/ProxyRules/main/AI-General.list, tag=AI-General, force-policy=AI, update-interval=86400, opt-parser=false, enabled=true
```

### Surge

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/cnsiming/ProxyRules/main/OpenAI.list,OpenAI
RULE-SET,https://raw.githubusercontent.com/cnsiming/ProxyRules/main/Claude.list,Claude
RULE-SET,https://raw.githubusercontent.com/cnsiming/ProxyRules/main/AI-General.list,AI
```

策略组名（`OpenAI` / `Claude` / `AI`）换成你配置里实际的名字即可。
只想用一个统一入口的话，把上面三条换成 `AI.list`。

## 规则优先级说明

1. **从上到下匹配，先命中先生效**（QX 和 Surge 都一样），所以引用顺序就是优先级：
   先专属（OpenAI.list、Claude.list），后通用（AI-General.list），最后 `AI.list` 只做兜底。
2. **合集与子列表不要同时开**（如同时引用 `AI.list` 和 `OpenAI.list`），否则会重复命中，浪费匹配且无额外收益。
3. 想做拦截（如把遥测域名 REJECT）时，REJECT 规则必须放在放行规则**之前**。
4. 同一条域名只在一个列表里维护：Statsig 同时被 ChatGPT 和 Claude 使用，统一放在 Claude.list；合集 AI.list 已去重。

## 脚本用法

```bash
# 1. 自动更新（拉取最新列表到本地目录，默认 ~/ProxyRules）
bash scripts/update.sh ~/ProxyRules

# 2. 去重检查（在仓库根目录运行；有重复会列出并返回非 0 退出码）
python3 scripts/dedupe.py

# 3. 统计（各列表规则数，按 DOMAIN / DOMAIN-SUFFIX 等分组）
python3 scripts/stats.py
```

QX / Surge 均支持远程列表自动刷新（`update-interval`），日常无需手动跑脚本；
`update.sh` 适合引用本地副本（如路由器场景）。

## 免责与隐私

- 域名整理自公开资料，按「能用」原则取舍，不保证穷尽。
- 修改自用时建议 fork 后用 `scripts/update.sh` 指向自己的仓库地址。
- 本仓库永远不会包含节点、订阅、密码、证书等任何私密信息。
