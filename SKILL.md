---
name: single-word-card
description: 单词油画卡生成器——一词一张精美单卡（黄框版式：单词大字/音标蓝框/中文绿框/油画大插图/例句紫框/同类词扩展紫框），配图为 AI 生成的无文字油画底图 + 确定性文字叠加，文字 100% 来自词表零出错。触发词：单词卡、单卡、一词一卡、油画卡、word card、single word card。与 flashcard skill（多词场景卡）互为补充，按老师想要的效果选用。
---

# single-word-card · 单词油画卡

一词一张卡，油画质感插图，确定性文字叠加。**本 skill 与 `flashcard` skill 的分工：**

| | flashcard（场景卡） | 本 skill（单词卡） |
|---|---|---|
| 卡型 | 3–5 词塞进一张场景图，标签连线指物 | **1 词 1 卡**，大插图 + 例句 + 同类词扩展 |
| 配图 | 扁平插画场景 | **油画质感**（impasto 厚涂、色彩饱满） |
| 适用 | 词汇量大的主题归类教学 | 单词精讲、例句、拓展联想 |

## 输入：词表

每词一行（用户给不齐就按常识补齐，补齐后先展示给用户过目再出图）：

```
word | ipa | 中文 | 例句英文(标红关键词) | 例句中文 | 同类词×3(英|中|emoji图标)
```

同类词图标默认用 emoji（快且稳）；用户明确要求"更像样图"再逐词生成小插画（出图额度 ×4，先提示）。

## 流水线（8 步，每步有验证，不许跳）

### Step 1 词义构图分析（本 skill 的灵魂，不许省）

对每个词先写出「语义要点 → 画面编码」，再写 prompt。**规则详见 `references/semantic-composition.md`**，速记：

- 单复数：some/several/few → 图中必须出现多个对象；an apple → 一个
- 动作词 → 人物正在做该动作的瞬间
- 抽象/方位/比较词 → 用可画的具体场景隐喻，禁止画抽象概念
- 每张图的 prompt 必须显式包含这些语义要素，否则批量出图必然「形对意错」

### Step 2 生成油画底图（无文字）

用 ImageGen（或等价出图工具），prompt 固定骨架 + Step 1 语义要素：

```
Oil painting masterpiece, rich impasto brushstrokes, vibrant colors,
<语义要点编码的场景>, masterful color blending, thick textured paint,
centered composition, classical painterly style.
NO text, NO letters, NO words, NO numbers, NO watermark.
```

参数：1024x1024，quality high。**额度提醒**：出图前告知用户每张约 5–10 额度。

### Step 3 逐张视觉验收

每张生成后立刻看图（视觉工具），三项全过才收：
1. 语义正确（some 是多个吗？动作对吗？）——不合格 → 改 prompt 重生成
2. 无任何 AI 伪文字/伪汉字——有 → 重生成
3. 构图居中、主题清晰

### Step 4 去水印（脚本，确定性）

ImageGen 每张右下角固定 `AI生成 / WORKBUDDX` 水印。**禁用纯色覆盖**（油画背景非纯色，会留明显色块）：

```bash
python scripts/repair_watermark.py <assets目录或单个png>
```

原理：克隆水印区正上方纹理 + 微抖动。依赖 numpy + Pillow。跑完抽查 1–2 张右下角确认无痕。

### Step 5 组装 HTML（确定性叠加）

复制 `references/card-template.html` 到交付目录，只改文件头部的 `CARDS` 数据数组：
- 所有文字（单词/IPA/中文/例句/同类词）100% 来自词表，**禁止**让 AI 手写或 OCR
- 配图路径指向 `*_clean.png`
- 7 段版式已在模板里：黄框 / 单词大字 / 音标蓝框 / 中文绿框 / 大插图 / 例句紫框（关键词标红）/ 同类词扩展紫框

### Step 6 无头截图自检（不许跳）

中文路径会让无头浏览器静默失败，**必须先拷到纯 ASCII 路径**：

```bash
rm -rf /d/card_check && mkdir -p /d/card_check
cp index.html /d/card_check/ && cp -r assets /d/card_check/
msedge --headless=new --disable-gpu --screenshot=D:/card_check/shot.png \
  --window-size=1120,<按卡片数调高> file:///D:/card_check/index.html
```

Edge 路径：`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`。
截图用视觉工具检查：7 段齐全 / 无水印残块 / 无裁切溢出 / 连接与排版正常。

### Step 7 已知坑（踩过的，别再踩）

- **SVG 线条用 `stroke="var(--x)"` 在 Edge headless 不渲染** → 用 CSS 类定义线条样式
- **标签 chip 贴边被 `overflow:hidden` 裁掉** → 内层 frame 负责裁剪图片，chip 放外层允许溢出
- **无头 rAF 不跑** → 演示类动画靠同步首帧静态验证即可
- **一次生成多图后逐张验收，别批量看完再改** → 语义错误越早发现越省额度

### Step 8 交付

`present_files` 打开 index.html，附一段总结：卡数、词条、额度消耗、下一步建议（调版式 / 加词 / 回写其他格式）。

## 交付物清单

```
<主题>_cards/
  index.html          # 卡片画廊（单文件，双击可看）
  assets/*_clean.png  # 去水印后的油画底图
  assets/             # 保留原始底图可选；不保留则删，clean 已够用
```
