# 判断力训练机 · 双轨制改造 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 JudgmentEngine 从"单一循环"改造为"学习轨(不记分,练理解) + 判断轨(记分,测泛化)"双轨制,并重写相关模板、索引、协议与自评清单。

**Architecture:** 在现有工作区上做文档层改造,不动 `toolkit/`。新增 `explanations/`(解释稿)与 `sources/`(素材源索引)两个目录;重写 `ledgers/` 模板与示例为判断轨格式;更新 README、故障字典、陪练协议、自评清单。所有改动保持现有约束(中文文档/英文提交信息)。

**Tech Stack:** markdown(全部为文档改动,无代码);git 提交沿用现有分支 `judgment-engine`。

## Global Constraints

- 模板与文档用**中文**书写;代码、注释、git commit message 用**英文**
- toolkit 只依赖 numpy(唯一第三方依赖);测试额外依赖 pytest —— 本次改造不改 toolkit,无需动测试
- 升级规则(来自 spec §六):判断轨命中率按负重级分段,**每一级内连续 2 轮命中率 ≥80% → 升一级**;命中率只统计新场景
- 学习轨不直接升级,但**学习轨连续 2 次被追问卡住同一原理 → 禁止升级**
- 判断轨难度:**先固定在①级**,连续 2 轮命中率 ≥80% 后再提升难度
- 一个代码文件只能被判断轨用一次;AI 生成变体必须"换场景不换原理"
- 工作区根目录:`c:/Users/win/Desktop/MachineLearning/JudgmentEngine/`

---

## File Structure

```
JudgmentEngine/
├── README.md                      # 更新:双轨说明 + 新升级规则 + 素材源规则
├── ledgers/
│   ├── _template.md               # 重写为判断轨模板
│   └── example_cycle_001.md       # 重写为判断轨格式
├── explanations/                  # 新增:学习轨解释稿
│   └── _template.md
├── sources/
│   └── index.md                   # 新增:素材源索引
├── toolkit/                       # 不变
├── dictionaries/
│   └── fault_dictionary.md        # 增加"理解缺口"分类
├── protocols/
│   ├── ai_sparring.md             # 更新:新增"内行追问"模式
│   └── sparring_log.md
├── checklists/
│   └── weekly_review.md           # 更新:双轨分别统计
└── objects/level1/                # 降级为学习轨素材(本次不删,README 说明)
```

---

### Task 1: 更新 README.md 为双轨制说明

**Files:**
- Modify: `README.md`(全文重写)

**Interfaces:**
- Consumes: 无
- Produces: 双轨总览、新升级规则、素材源规则;作为整个工作区的入口文档

- [ ] **Step 1: 重写 README.md**

```markdown
# 判断力训练机（Judgment Engine）

目标：培养 AI 时代无法外包的判断力——**验真 / 修错 / 评判**。
第一性原理：判断力 = 脑内内部模型与现实之间的吻合度。训练 = 反复制造"预测 vs 现实"的碰撞并修复内部模型。

理解 ≠ 背诵。见过的问题答得再好不算数（过拟合），没见过的场景预测得对才是真懂（泛化）。判断力 = 能讲清机制 + 能迁移。

## 双轨制

- **学习轨**（不记分，练理解）：认领物体 → 写解释稿 → AI 内行追问 → 产出存 `explanations/`
- **判断轨**（记分，测泛化）：给陌生物体 → 限时预测 → 用 `toolkit/` 验证 → 产出存 `ledgers/`
- 训练集 / 测试集分离：见过的题不算数，命中率只统计新场景

## 核心循环（判断轨）
选一个陌生物体 → 预测（写可证伪的量化断言）→ 现实验证（toolkit / numpy 实测）→ 记录偏差 → 修复内部模型

## 目录
- `ledgers/`      判断轨预测账本（记分，只用新场景）
- `explanations/` 学习轨解释稿（不记分）
- `sources/`      素材源索引（防过拟合：已用过的题不再当新题）
- `toolkit/`      验证工具箱（"现实"的代言人，已测试）
- `dictionaries/` 故障字典（症状 → 根因 → 定位方法）
- `protocols/`    AI 陪练协议与记录（含内行追问模式）
- `checklists/`   每周自评清单
- `objects/`      学习轨素材（按负重级递增：①形状 ②动态 ③组件 ④系统 ⑤研究）

## 素材源
- **GitHub**（机器学习 / 图像处理 / 因果推断）：每周取 1 个函数/文件作题，没读过才能当题
- **AI 生成变体**：换场景不换原理（如学过 softmax → 出 attention 里的 softmax + 温度缩放），带难度标签
- **.Prime 存量**：自己 AI 敲过但没消化的旧代码，直接当题

## 升级规则
判断轨按负重级分段：**每一级内连续 2 轮命中率 ≥ 80% → 升一级**。命中率只统计新场景。
学习轨不直接升级，但**连续 2 次被追问卡住同一原理 → 禁止升级**。
判断轨难度先固定在①级，有把握后再上调。

## 铁律
- AI 输出永远是"待验证的命题"，不是终点。你负责验真、修错、评判。
- 见过的题不算数；一个文件只能被判断轨用一次。
```

- [ ] **Step 2: 验证内容**

Run: `cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && rg -n "双轨制|升级规则|素材源" README.md`
Expected: 三处都命中,且 README 中出现"判断轨难度先固定在①级"。

- [ ] **Step 3: Commit**

```bash
cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && git add README.md && git commit -m "docs: update README to dual-track system"
```

---

### Task 2: 重写 ledgers/_template.md 为判断轨模板

**Files:**
- Modify: `ledgers/_template.md`(全文重写)

**Interfaces:**
- Consumes: 无
- Produces: 判断轨账本格式约定;Task 3 的示例与后续判断轨记录按此格式写

- [ ] **Step 1: 重写 _template.md**

```markdown
# 判断轨记录 #N — <陌生物体>

日期： | 负重级： | 来源：（GitHub/AI变体/.Prime） | 是否新场景：是

## 1. 题目
（这个函数/文件做什么的——只贴签名/注释，不贴实现）

## 2. 预测（3-5条，每条必含：预测内容 + 通过判据）
| # | 预测 | 判据 | 结果 |
|---|------|------|------|
| 1 | <具体到可证伪> | <数值/形状/行为> | 对/错 |

## 3. 验证
（跑了什么 toolkit/实验，贴关键结果）

## 4. 偏差记录（最值钱）
（哪条预测错了，为什么错——内部模型哪里和现实不符）

## 5. 修复（内部模型更新）
（下次同类预测该怎么做）
```

- [ ] **Step 2: 验证内容**

Run: `cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && rg -n "判断轨记录|是否新场景|判据" ledgers/_template.md`
Expected: 三处都命中;且文件**不含**"建立内部模型"和"闭卷"(旧格式残留)。

- [ ] **Step 3: Commit**

```bash
cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && git add ledgers/_template.md && git commit -m "docs: rewrite ledger template for judgment track"
```

---

### Task 3: 重写 ledgers/example_cycle_001.md 为判断轨格式

**Files:**
- Modify: `ledgers/example_cycle_001.md`(全文重写)

**Interfaces:**
- Consumes: Task 2 的模板格式
- Produces: 判断轨第一条正式记录(示例),示范预测的可证伪写法

- [ ] **Step 1: 重写 example_cycle_001.md**

```markdown
# 判断轨记录 #001 — 认领：线性回归的梯度下降（.Prime/Phase0/LinearRegression.py）

日期：2026-07-31 | 负重级：② 动态 | 来源：.Prime | 是否新场景：是

## 1. 题目
.Prime/Phase0/LinearRegression.py —— AI 敲的、没消化的代码。用判断轨把它认领。

## 2. 预测（每条必含：预测内容 + 通过判据）
| # | 预测 | 判据 | 结果 |
|---|------|------|------|
| 1 | 若 lr=10，loss 先震荡再发散成 NaN | 跑实验，loss 在训练中途出现 NaN | 对 |
| 2 | 若 lr=1e-8，loss 几乎不动 | 跑实验，|loss_end − loss_start| < 0.01 | 对 |
| 3 | 收敛后 w 接近 2.0、b 接近 1.0 | 跑实验，|w-2|<1e-2 且 |b-1|<1e-2 | 对 |
| 4 | 数值梯度与手写梯度 dL/dw=mean(-2x(y-pred)) 一致 | 相对误差 < 1e-5 | 对 |

## 3. 验证
- `toolkit/gradient_check.py`：数值梯度 vs 手写梯度，相对误差 3e-7 ✅
- 分别跑 lr=10 / 1e-8 / 0.1 三组，对比 loss 曲线
- 收敛后 w≈2.001、b≈1.002 ✅

## 4. 偏差记录（最值钱）
- 我以为"lr 大就立刻发散"，实际 lr=10 是先震荡几个 epoch 再发散——发散前有震荡期
- 我之前没意识到 `np.mean()` 里的 1/n 会随样本数影响实际步长

## 5. 修复（内部模型更新）
- 学习率的"危险区间"是一个范围，不是单点；发散前往往先震荡
- 有效步长 ≈ lr / n（batch 大小通过均值影响实际学习率）；预测 lr 行为时先想有效步长
```

- [ ] **Step 2: 验证内容**

Run: `cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && rg -n "判断轨记录|判据|偏差记录" ledgers/example_cycle_001.md`
Expected: 三处都命中;命中率为 4/4。

- [ ] **Step 3: Commit**

```bash
cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && git add ledgers/example_cycle_001.md && git commit -m "docs: rewrite example cycle as judgment track record"
```

---

### Task 4: 新增 explanations/_template.md(学习轨解释稿模板)

**Files:**
- Create: `explanations/_template.md`

**Interfaces:**
- Consumes: 无
- Produces: 解释稿格式约定;后续学习轨每次产出解释稿按此格式

- [ ] **Step 1: 创建目录**

```bash
cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && mkdir -p explanations
```

Expected: `explanations/` 目录创建成功。

- [ ] **Step 2: 写解释稿模板**

```markdown
# 解释稿 #N — <原理名>

日期： | 负重级： | 关联物体：

## 三句话讲清核心
（这个机制解决什么问题 + 怎么解决的，3 句以内）

## 展开（300-500 字）
（关键推导/关键代码行 + 1-2 个自创例子）

## 依赖条件
（"如果没有 X，会怎样？"——强制写出泛化边界）

## AI 内行追问记录
（3-5 轮追问，每轮：问题 → 我的回答 → 卡住的地方）
```

- [ ] **Step 3: 验证内容**

Run: `cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && rg -n "三句话讲清核心|依赖条件|追问记录" explanations/_template.md`
Expected: 三处都命中。

- [ ] **Step 4: Commit**

```bash
cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && git add explanations/ && git commit -m "docs: add explanation draft template for learning track"
```

---

### Task 5: 新增 sources/index.md(素材源索引)

**Files:**
- Create: `sources/index.md`

**Interfaces:**
- Consumes: 无
- Produces: 素材源防重索引;判断轨取题前先查此表,用过的不算新场景

- [ ] **Step 1: 创建目录**

```bash
cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && mkdir -p sources
```

Expected: `sources/` 目录创建成功。

- [ ] **Step 2: 写索引**

```markdown
# 素材源索引

> 规则：一个代码文件只能被判断轨用一次。用过的文件标"是"；再取到同一文件不算新场景。

## 来源
1. **GitHub**（机器学习 / 图像处理 / 因果推断）：每周取 1 个函数/文件
2. **AI 生成变体**：换场景不换原理，带难度标签（①-⑤）
3. **.Prime 存量**：自己敲过但没消化的旧代码

## 索引表
| 仓库/来源 | 文件 | 方向 | 难度 | 是否已用 | 用后命中率 |
|-----------|------|------|------|---------|-----------|
|（示例）.Prime | Phase0/LinearRegression.py | 机器学习 | ② | 是 | 4/4 |
```

- [ ] **Step 3: 验证内容**

Run: `cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && rg -n "索引表|是否已用|换场景不换原理" sources/index.md`
Expected: 三处都命中。

- [ ] **Step 4: Commit**

```bash
cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && git add sources/ && git commit -m "docs: add material source index to prevent overfitting"
```

---

### Task 6: 故障字典增加"理解缺口"分类

**Files:**
- Modify: `dictionaries/fault_dictionary.md`(末尾追加一节)

**Interfaces:**
- Consumes: 无
- Produces: 学习轨追问暴露的"理解缺口"记账格式;与已有"训练事故"条目并列

- [ ] **Step 1: 追加"理解缺口"节**

在 `dictionaries/fault_dictionary.md` 末尾(现有"全零初始化对称性"节之后)追加：

```markdown
## 理解缺口（学习轨追问暴露）
- 症状：解释稿里说不清"为什么这样做"；AI 追问 2 轮以上就卡住
- 根因：只背了做法，没建立"做法 ↔ 目的"的因果链 | 依赖条件不清（"没有 X 会怎样"答不出）
- 定位：回到解释稿补"依赖条件"一节；换场景重述一遍（举一反三）；连续 2 次卡同一原理 → 禁止升级
```

- [ ] **Step 2: 验证内容**

Run: `cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && rg -n "理解缺口|禁止升级" dictionaries/fault_dictionary.md`
Expected: 两处都命中。

- [ ] **Step 3: Commit**

```bash
cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && git add dictionaries/fault_dictionary.md && git commit -m "docs: add understanding-gap category to fault dictionary"
```

---

### Task 7: AI 陪练协议增加"内行追问"模式

**Files:**
- Modify: `protocols/ai_sparring.md`(追加一节 + 更新场景数)
- Modify: `protocols/sparring_log.md`(追加一行说明)

**Interfaces:**
- Consumes: 无
- Produces: 学习轨的追问协议(3-5 轮连续追问);每次学习轨解释稿走此协议

- [ ] **Step 1: 更新场景标题**

把 `## 三种场景（轮换）` 改为 `## 四种场景（轮换）`,并在场景 3 之后追加：

```markdown
4. **内行追问**（学习轨专用）：你写完解释稿后，AI 扮演内行连续追问 3-5 轮（如"为什么减 max？不减会怎样？温度缩放 T 改变什么？"），你答；答不上来的地方 = 理解缺口 → 记入故障字典 → 回解释稿补
```

- [ ] **Step 2: 在"每场记录"前追加追问轮次格式**

在 `## 每场记录` 之前插入：

```markdown
## 内行追问轮次格式（学习轨）
每轮：`追问：<AI 的问题> | 我的回答：<你的回答> | 卡住：是/否`
卡住的点抄进 `dictionaries/fault_dictionary.md` 的"理解缺口"节。
```

- [ ] **Step 3: 更新 sparring_log.md**

在表格说明行追加一句：

```markdown
（场景列新增取值：内行追问；追问卡住的原理记为"暴露的内部模型缺口"）
```

- [ ] **Step 4: 验证内容**

Run: `cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && rg -n "四种场景|内行追问|追问轮次" protocols/ai_sparring.md && rg -n "内行追问" protocols/sparring_log.md`
Expected: ai_sparring.md 三处命中;sparring_log.md 一处命中。

- [ ] **Step 5: Commit**

```bash
cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && git add protocols/ && git commit -m "docs: add insider-quiz mode to AI sparring protocol"
```

---

### Task 8: 每周自评清单改为双轨统计

**Files:**
- Modify: `checklists/weekly_review.md`(全文重写)

**Interfaces:**
- Consumes: 无
- Produces: 双轨分别统计的周自评格式

- [ ] **Step 1: 重写 weekly_review.md**

```markdown
# 每周自评清单

每周日花 15 分钟填一次。

## 本周双轨进度
- 学习轨解释稿数：____（目标 ≥ 2）
- 判断轨预测记录数：____（目标 2-3）

## 判断轨量化指标（对应升级标准）
- 预测命中率：____%（命中/总数，只算新场景）→ 每负重级内连续 2 轮 ≥ 80% 才升级
- 边界攻击命中数：____（发现了几个问题）

## 学习轨指标
- 解释稿通过追问数：____
- 被追问卡住的原理：____（连续 2 次卡同一原理 → 禁止升级）

## 中期信号检查（对号入座）
- [ ] 见到新代码，第一反应是"拆解 / 预测 / 验证"而不是"抄来跑"
- [ ] 能对一个 AI 给的结论说"我不信，让我验一下"
- [ ] 训练出问题时，第一反应是"症状 → 病因"而不是瞎改参数

## 本周暴露的判断力缺口
（写 1-2 条最痛的缺口 → 下周优先补它）

## 下周计划
- 学习轨物体：____
- 判断轨物体（GitHub/AI变体/.Prime）：____
```

- [ ] **Step 2: 验证内容**

Run: `cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && rg -n "双轨|判断轨量化指标|学习轨指标" checklists/weekly_review.md`
Expected: 三处都命中;且文件**不含**"闭卷重写"(旧指标残留)。

- [ ] **Step 3: Commit**

```bash
cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && git add checklists/weekly_review.md && git commit -m "docs: rewrite weekly review for dual-track stats"
```

---

### Task 9: 全量验证 + 收尾

**Files:**
- 无新增/修改

**Interfaces:**
- Consumes: Task 1-8 的全部产物
- Produces: 改造完成的验证与收尾

- [ ] **Step 1: 全量验证(结构 + 无旧格式残留 + 无测试破坏)**

```bash
cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && echo "--- 结构 ---" && ls && echo "--- 新目录 ---" && ls explanations/ sources/ && echo "--- 旧格式残留(应为空) ---" && rg -n "闭卷|建立内部模型" --glob "*.md" || echo "(无残留)" && echo "--- 测试 ---" && python -m pytest toolkit/ -q
```

Expected: 结构含 explanations/ 与 sources/;旧格式残留为空;测试 19 passed, 0 failed。

- [ ] **Step 2: 提交状态确认**

```bash
cd "c:/Users/win/Desktop/MachineLearning/JudgmentEngine" && git status
```

Expected: working tree clean(所有改动已提交)。

---

## Self-Review 记录

- **Spec coverage**:spec §三学习轨 → Task 4 解释稿模板 ✅;§四判断轨 → Task 2/3 账本模板与示例 ✅;§五素材源 → Task 5 索引 ✅;§六升级判定 → Task 1 README 升级规则 + Task 6 故障字典禁止升级 ✅;§七工作区结构 → Task 1-8 ✅;§八模板 → Task 2/4/5 ✅;§九协议自评 → Task 7/8 ✅;§十铁律 → Task 1 README 铁律 ✅
- **Placeholder scan**:无 TBD/TODO;所有模板与示例内容完整 ✅
- **Type consistency**:`ledgers/` 新格式统一含"题目/预测(判据)/验证/偏差/修复";`explanations/` 统一含"三句话/展开/依赖条件/追问记录";`sources/index.md` 与 Task 1 README 素材源描述一致;`ai_sparring.md` 场景数从"三种"改"四种"且与 sparring_log 取值一致 ✅
- **测试影响**:Task 9 用 pytest 全量回归,toolkit 未动,预期 19 passed ✅
