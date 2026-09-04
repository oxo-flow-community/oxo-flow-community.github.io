# Site 美化设计系统 v2 — 设计 spec

日期: 2026-09-05
分支: feat/site-v2-beautify
站点: https://oxo-flow-community.github.io/ (MkDocs Material, docs/ 源 + 提交的 site/ 镜像)

## 目标

全面打磨美化社区目录站：布局、色彩、排版。浅色模式保持默认并精修；暗色（slate）方案整体替换为新的"仪器暗色"身份。

## 决策记录（视觉伴读 mockup 逐题确认）

Mockup 原件在 `.superpowers/brainstorm/60867-1788539142/content/`，本 spec 只收录定稿值。

| 题目 | 选择 | 说明 |
|---|---|---|
| 方向 | **A · 精修现有** | 绿+白科研风基座，不改气质只做精 |
| 首页 hero | **V2 · 左右分栏** | 文字左、终端+数据右，垂直居中，CTA 入左栏 |
| 卡片 | **W2 · 证据优先** | 顶部证据色线 + 层级重排，工具降级为轻 tag |
| 详情页头部 | **P2 · 侧栏数据面板** | 左描述右 "At a glance" 面板，与 V2 左右骨架呼应 |
| 暗色方案 | **D2 · 仪器暗色** | 荧光绿点缀、终端微光、命令行语气（用户全权委托锁定） |

用户委托："按你自己最推荐的往后推动完成就行" — 以下剩余决策均由我定：字号/间距节奏、筛选条最小打磨、页脚、3 个构建警告、rating 后缀对账。

## 范围

**In**: extra.css 设计令牌与组件、index.md hero 重构、catalog.js 卡片重构+筛选条打磨、generate.py 详情页头部重构 + 重生成 24 页 + pipelines-data.js、3 个构建警告修复、页脚、site/ 镜像同步。

**Out**: 内容变更（描述/评级数据）、新页面、mkdocs.yml 结构变更（copyright 文案除外）、引擎侧任何改动。

## 设计令牌

### 浅色（default，保持现有基座）

现有 extra.css `:root` 令牌保留，仅组件样式精修：

| 令牌 | 值 |
|---|---|
| --bg | #f7faf8 |
| --ink | #17211c |
| --ink-2 | #3f5047 |
| --muted | #6b7d73 |
| --faint | #97a69e |
| --edge | #dfe8e3 |
| --edge-strong | #c6d5cd |
| --panel | #fff |
| --panel-2 | #eff4f1 |
| --brand | #0e7a5f |
| --brand-deep | #0a5c47 |
| --brand-soft | #e4f2ec |
| --ok（live 语义绿） | #0F9D6E（边框 #9fd8c3 / 底 #ecf9f3） |
| --cyan | #0b93b8 |
| --nf | #0c8a5d |
| --sn | #1a64b8 |
| --star | #b45309 |
| --code-bg | #eff4f1 |
| 卡片阴影 | `0 1px 2px rgba(23,33,28,.05), 0 4px 14px rgba(23,33,28,.04)` |
| 渐变规则线 | `linear-gradient(90deg, #0b93b8, #0e7a5f)` |

live 徽章: color #0F9D6E / border #9fd8c3 / bg #ecf9f3。
终端红绿灯: #e36c5f / #b45309 / #0e7a5f，头条底 #eff4f1。

### 暗色（slate，整体替换为 D2 仪器暗色）

**删除现有 slate 令牌块**（bg #0c1210 / panel #131b17 / panel-2 #18221d / edge #24302a / ink #e7efea / brand #2bb58a / cyan #35c2e0），替换为：

| 令牌 | 值 |
|---|---|
| --bg | #0a0f0d |
| --edge | #1d2a24 |
| --panel（卡片/面板） | #101915 |
| --term-bg（终端） | #0e1613 |
| --cmd-bg（命令条/深嵌） | #0c1310 |
| --brand（荧光绿） | #34d399 |
| --ink | #eef7f2 |
| --ink-2（副文/term-body） | #8ca096 |
| --muted | #5e6f65 |
| --faint | #5e6f65（复用 muted，面板标签可再压） |
| --ok（live 语义绿，证据色跨主题不变） | #34d399 |
| --cyan | #22b8d4 |
| --nf | #34d399（引擎点统一荧光绿，区分靠文案） |
| --code-bg / --panel-2 | #16211b（tchip 底） |
| 渐变规则线 | `linear-gradient(90deg, #22b8d4, #34d399)` |
| CTA | background #34d399 / color #04120c |

组件特效（D2 独有）：
- 终端窗口 `box-shadow: 0 0 22px rgba(52,211,153,.07)`
- 交通灯 `background:#3ddc84; box-shadow: 0 0 5px #3ddc8488`（三灯同绿）
- term-body 加粗行 `color:#34d399; text-shadow: 0 0 7px #34d39955`
- live 徽章 `color:#34d399; border-color:#1f4d38; background:#0f2a1e; font-weight:600`，小写文案 `✔ live-tested`
- tchip `background:#16211b; color:#8ca096`
- 命令条 `background:#0c1310`（白底反转）
- 统计块 .v #eef7f2 / .k #5e6f65
- 导航条 #1d2a24 边线，brand 荧光绿，条目 #5e6f65

**CSS 可行的文案切换**：
1. 首页 eyebrow 用双 span 标记（见 §1），按 `[data-md-color-scheme]` 显示其一：浅色 "oxo-flow · community catalog" / 暗色 "$ catalog --list"。
2. 徽章文案暗色小写：`[data-md-color-scheme="slate"]` 下对 .ox-badge / live 徽章加 `text-transform: lowercase`。
3. 导航 brand 文案在 mkdocs.yml 级 — 仅改颜色，不换文案（务实）。

## 组件规格

### 1. 首页 hero（V2 分栏）— docs/index.md

结构：

```
.ox-hero
  .ox-hero-split            (grid: 1fr 1.15fr; gap 16px; align-items center)
    左栏:
      .ox-eyebrow           双 span: .ox-eyebrow-light / .ox-eyebrow-dark
      h1.ox-hero-title      "Curated workflows.<br>Ready to run."  23px / 700 / -0.02em / lh 1.06
      p.ox-sub              24 bioinformatics workflows …（max-width 220px 级）
      .ox-rule              58×3px, radius 2px, 渐变规则线
      a.ox-cta              pill: bg --brand, 白字, radius 99px, w600, "Browse the catalog →", href pipelines/
    右栏:
      .ox-term（现有，内容不变: 3 点 + "oxo-flow run main.oxoflow" + 4 行 body）
      #ox-stats（现有，catalog.js 渲染，值不变）
```

- 移动端 ≤720px 单列堆叠，stats 可保持 4 列（现有样式已有）。
- hero 下方 "Start here"（featured 卡片）/ "Where workflows come from" / "How to run" 三个区块不动。

### 2. 目录卡片（W2 证据优先）— catalog.js cardHTML 重构 + CSS

卡片 DOM 顺序（新）：

1. `.ox-card-top`：名称（mono 600，现有样式）+ 域名徽章（新，普通 .ox-badge）
2. 标题行（11px, color --ink, lh 1.45）— 用 `-` 或 `—` 分隔的现有 title 文案
3. `.ox-card-meta`：rules 徽章（`{rule_count} rules`）+ ⚙ compute 徽章（如存在）+ 工具 `.tchip` ×3（首 3 个工具，其余省略）
4. `.ox-card-foot`：live/verified/community 徽章（左）+ 引擎点徽章（右，.dot + nf-core/snakemake 短名），`border-top:1px solid --panel-2; padding-top:8px; margin-top:auto`
5. 命令条 `.ox-card-cmd`（bg --panel 白，作为底部锚点）
6. 链接行 Run notes / GitHub ↗（现有）

- `.ox-card.live-card` 顶边 3px `border-top:3px solid var(--ok)`；非 live 卡 `#dfe8e3`。
- **卡片 rating 徽章去掉 coverage 后缀**（✔ Live-tested 不加 " · full-line"）— 见 §Rating 后缀对账。
- 卡片删除 origin 徽章与旧工具行（信息并入 foot/顶行）；domain 徽章上移至顶行右侧。
- 引擎徽章在卡片上只留点+短名（nf-core / snakemake），去掉 "port" 字（foot 位置紧张）。
- 暗色下 live 顶线 = 荧光绿，徽章文案小写。

### 3. 详情页头部（P2 侧栏数据面板）— generate.py make_page 重构 + CSS

新头部结构（替换现有 `# {title}` → badges → description → meta_table 区域）：

```
.ox-detail-head
  .ox-crumb              mono: "Pipelines / {name}"（Pipelines 链到 ../ 目录页），b --brand
  .ox-detail-cols        grid: 1.6fr 1fr; gap 16px; align-items start
    左:
      h1                 20px / 700 / -0.02em / --ink（即页面标题，不再加 meta 表格）
      .ox-page-badges    rating（**带后缀**）+ origin + 引擎徽章（现有 badges()）
      p 描述              10.5px 级 / --ink-2 / lh 1.55
    右 .ox-glance        白底面板: border --edge, radius 10px, padding 10px 12px, 卡片阴影
      .ox-glance-title   "At a glance"（mono 7.5px, ls .14em, uppercase, --faint）
      .ox-kv × n         Rating（✔ Live-tested · full-line 等，live 绿）/
                         Rules / Compute（如有）/ Engine / Origin /
                         Domain / Source（链接）/ Pinned version（如有）/
                         Ported（如有）/ License
      .ox-card-cmd       快速启动命令条，display:block，margin-top:8px
```

- 数据完全来自现有 `meta_table(p)` 的行内容 — 把表格渲染函数改为生成面板 kv 行；**行内容、链接、后缀一字不改**（唯一例外：Rating 后缀在详情页保留，见对账节）。
- ≤720px 单列堆叠（面板落到描述下方）。
- 后续正文（Run it / Parameters / DAG / Scope / Fidelity / Links）不动。

### 4. 筛选条（最小打磨）— CSS only

- 只做: chip 尺寸统一、aria-pressed 态与 focus 环对齐卡片语言、`#ox-count` 行与搜索框基线对齐。
- **不改过滤逻辑**。

### 5. 页脚 — mkdocs.yml copyright + CSS

- copyright 文案改为带链接的 mono 风格一行：org 仓库 / 引擎 oxo-flow / Issue 入口 / 证据阶梯图例 "✔ live-tested ⊃ ★ verified ⊃ ☆ community"。
- CSS: .md-footer 小号 mono、发丝线、间距对齐。

### 6. 字号/间距节奏

- Mockup 数值是 12px 基准的缩比图 — 落地时映射到站点实际 rem 尺度，保持比例关系；卡标题沿用 `.ox-card-title` 现值。
- 标题统一 `letter-spacing:-0.02em`；hero h1 保留现有 clamp 值，追加 `line-height:1.06`。
- 全站卡片/面板统一 radius 10px、发丝线 --edge。

### 7. 三个构建警告修复

1. **porting.md `upstream-repo-url` 模板占位符被解析成链接**（736/796/825 行附近）— 模板示例 `<upstream-repo-url>` 用反引号包裹或转义，使 mkdocs strict 不告警。
2. **chipseq.md `#multi-antibody-runs` 锚点**（286 行引用）— 对齐标题或链接，锚点必须存在。
3. **curation.md:11 `[catalog page](../pipelines/)`** 目录式索引链接 — 改为站内绝对 `/pipelines/` 形式。

构建门禁：`mkdocs build` 零警告。

## Rating 后缀对账

- **卡片**（catalog.js）：plain 文案 "✔ Live-tested" / "★ Verified" / "☆ Community"，无 coverage 后缀（定稿 W2 mockup）。
- **详情页面板**（generate.py `rating_badge`）：保留 " · full-line" / " · default-path" 后缀。
- 首页 stats 注脚（证据阶梯说明句）不变。

## 文件变更地图

| 文件 | 变更 |
|---|---|
| docs/stylesheets/extra.css | 令牌块（slate 整体替换 D2）、V2 hero、W2 卡片、P2 面板、筛选条/页脚打磨 |
| docs/index.md | V2 分栏 hero + eyebrow 双 span |
| docs/javascripts/catalog.js | cardHTML 重构（W2 结构 + 后缀移除），renderStats/renderFeatured/筛选逻辑不动 |
| scripts/generate.py | make_page 头部重构（crumb + cols + glance 面板），rating_badge 保持后缀 |
| docs/pipelines/*.md (24) | 重生成 |
| docs/javascripts/pipelines-data.js | 重生成（内容不变） |
| mkdocs.yml | copyright 文案 |
| docs/about/porting.md, docs/about/curation.md, docs/pipelines/oxo-flow-chipseq.md | 警告修复 |
| site/ | 镜像同步（同 commit，排除 3 个 stale clindet SVG） |

## 验证

1. `python3 scripts/generate.py` 干净通过，24 页 + pipelines-data.js 重生成。
2. `mkdocs build` 零警告（3 修复验证）。
3. 手动视觉走查: 首页 + 目录 + rnaseq 详情页，两种配色 × 桌面/移动宽度（用本地 build 打开或部署后站点）。
4. catalog.js 无测试框架 — 以构建 + 手动渲染验证；逻辑改动保持最小。
5. site/ 镜像与 docs/ 同 commit。

## 发布流程

feat/site-v2-beautify 分支 → 完整 PR → squash 合入 main → GitHub Pages 部署后验证线上站点（两种配色、移动端、卡片/详情头部）。

## 已知坑

- index.md / mkdocs.yml 的历史编辑曾被用户编辑器回退 — 每次编辑后 `git diff` 复查。
- mockup 数值是缩比图 — 落地映射 rem，不要照抄 px。
- generate.py + mkdocs build 会弄脏 site/ 镜像（~46 文件 + 3 个 stale clindet SVG）— 修复路径 `git checkout -- site/ && git clean -fd site/assets/dag/`，重生成后再提交。
- 嵌套双引号的复合 bash 命令会触发 JSON 校验错 — 命令保持简单。
