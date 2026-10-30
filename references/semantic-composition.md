# 语义构图规则 + 油画出图规格

> 这是 single-word-card 的 Step 1 依据。**配图失败的绝大多数原因不是画得不好，而是「形对意错」**——画面漂亮但没编码单词的核心语义。先分析，再画。

## 一、语义构图规则（词义 → 画面编码）

写 prompt 前必须先为每个词填这张表：

```
word: ______
1. 核心语义：词的本义/引申义是什么？
2. 数量特征：单数 / 复数 / 不可数？（直接决定画面里对象数量）
3. 动作特征：是动作词吗？谁在做？进行到哪个瞬间？
4. 关系特征：介词/方位/比较？（in/on/under/bigger→两物位置或大小关系）
5. 情感/状态：happy/tired→人物表情姿态
6. 画面编码：以上要点 → 一句话场景描述（写进 prompt 的素材）
```

### 硬规则

1. **单复数零妥协**：`some / several / many / few` → 图中必须清晰出现多个对象（3 个以上，主对象手持/怀抱 + 环境再散布一些最稳）；`an apple` → 恰好一个主对象。反例（真实踩坑）：some 的卡画了「手里一个苹果」——形对意错，返工。
2. **动作词画瞬间**：`swim/swim` → 人物或动物正处于该动作中，不是摆 pose。
3. **抽象词用具象隐喻**：`happy` → 开怀大笑的人物场景；禁止画文字、符号、抽象图形。
4. **一词一焦点**：画面主体唯一且居中，背景可以呼应语义但不要喧宾夺主。
5. **环境复现语义**：主对象 + 周围环境都应指向词义（some → 碗里/台面也摆满；sea → 海 must 占画面主导）。

## 二、油画出图规格（固定骨架，只换场景段）

```
Oil painting masterpiece, rich impasto brushstrokes, vibrant colors,
<语义要点编码的场景，含数量/动作/关系要素>,
masterful color blending, thick textured paint,
centered composition, classical painterly style.
NO text, NO letters, NO words, NO numbers, NO watermark.
```

- 尺寸 1024×1024，quality high
- 风格词不要换：`impasto`（厚涂）+ `vibrant`（饱满）是"油画色彩感十足"的关键；flat/cartoon/storybook 都会被用户判"不够油画"
- 负向词一个不能少：NO text/letters/words/numbers/watermark

## 三、验收三问（每张必过）

1. **语义对吗？** 对照第 1 步的画面编码逐条核对（数量数出来、动作看出来）。
2. **干净吗？** 无 AI 伪文字/伪汉字；右下角水印交由 `repair_watermark.py` 处理，不在这步管。
3. **像"油画色彩感十足"吗？** 厚涂笔触可见、色彩饱和。偏扁平 → 重生成，不要将就。

任何一条不过 → 改 prompt 重出图，**不要**在坏图上做局部修补。
