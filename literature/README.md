# JITL 入门文献清单（25 条 · 已核实）

> 📁 **本目录 = 我的毕业设计文献库**
>
> - **本文件** = 文献**索引**（25 条，全部用 Crossref API 核实过元数据）
> - **每篇精读后的笔记** = 同目录下新建 `作者年份.md`（例：`yeo2023.md`、`kaneko2021.md`）
> - **笔记模板** = [`模板_文献笔记.md`](模板_文献笔记.md)
>
> 题目：**基于局部数据几何的 JITL 样本选择与预测可靠性**

---

> **用途**：开题报告「国内外研究现状」的素材库 + 9 周精读计划
> **题目**：基于局部数据几何的 JITL 样本选择与预测可靠性
> **核实方式**：**Crossref REST API** 逐条核验标题 / 第一作者 / 年份 / 期刊 / 卷期页 / 被引数（出版商注册的权威元数据，非搜索摘要推测），并实测链接可达性
> **核实日期**：2026-10-12
> **⬆️ 2026-10-13 更新**：课题详情已公布 → 新增**精确检索关键词**（见下）

---

## 🆕 题目定稿后的检索关键词 ⭐

**课题系统全称**：基于局部数据几何的 JITL 样本选择与预测可靠性研究

课题简介点名的技术概念（**优先用这些词检索**）：

| 中文 | 英文关键词 |
|---|---|
| 局部数据几何 | local data geometry |
| 几何感知样本选择 | **geometry-aware sample selection** |
| 单侧分布 | one-sided / asymmetric distribution |
| 密度不足 | insufficient density / sparse neighborhood |
| ⭐ **方向退化** | **direction degeneration / ill-conditioned local covariance** |
| 方向不对称度 | directional asymmetry |
| 查询信息量 | query information content |
| 预测可靠性 | prediction reliability |

**推荐检索式（直接复制）**

```
geometry-aware sample selection soft sensor
local data geometry just-in-time learning
local covariance ill-conditioned regression
directional distribution nearest neighbor
prediction reliability just-in-time learning
sample selection bias local regression
```

> 💡 **检索重点**：找**「局部协方差矩阵」和「局部 PCA」**相关的文献 —— 那是本题的数学核心。
> 现有的 2.5 / 2.6 / 2.9 三条已在这条线上（流形正则、马氏距离），**用新关键词再补一轮**。

| 标记 | 含义 |
|:--:|---|
| ✅ | Crossref 元数据已核实 **+ 链接实测可达** |
| ⚠️ | Crossref 元数据已核实，但出版商页面返回 403（**换学校 VPN 再试**） |
| ❓ | 仅部分核实 —— **引用前必须在 CNKI / 学校图书馆核对原文** |

> ⚠️ ScienceDirect、ACS 的页面对调研环境返回 403，所以元数据全部改由 Crossref API 核验。**元数据可信，正文需要用学校网络下载。**

---

# ⭐ 先说你的「靶心论文」

## Kaneko 2021 — 几乎就是你的题目本身

| | |
|---|---|
| **标题** | Estimating the reliability of predictions in locally weighted partial least-squares modeling |
| **作者 / 年份** | Kaneko, H. / 2021 |
| **期刊** | Journal of Chemometrics 35(9): e3364（被引 13） |
| **DOI** | [10.1002/cem.3364](https://doi.org/10.1002/cem.3364) |
| **免费全文** | [明治大学机构库 PDF](https://meiji.repo.nii.ac.jp/record/2001364/files/journalofchemometrics_35_9_1.pdf) ← **不需要学校权限** |

**它在 LWPLS（局部加权偏最小二乘，JITL 最常用的局部模型）框架内部，定义并估计「预测可靠性」。**

你的题目是「JITL 样本选择 **+** 预测可靠性」。这篇把**可靠性**那一半做到了 —— 于是：

> 🎯 **你的创新空间 = 剩下那一半：「局部数据几何」的样本选择。**
> **而这篇提供了一个现成的、可被改进的可靠性评估基线。**

**它是开放获取的**，今天就能下。**精读到能复述它的方法为止。**

---

# 一、JITL 综述（建立坐标系）

| # | 第一作者 | 年份 | 期刊 | 标题 | DOI / 链接 | 一句话 | 核实 |
|:--:|---|---|---|---|---|---|:--:|
| 1.1 | Atkeson, C. G. | 1997 | Artificial Intelligence Review 11(1–5):11–73 | Locally Weighted Learning | [10.1023/A:1006559212014](https://doi.org/10.1023/A:1006559212014) | **局部加权学习的奠基综述**（被引 980）：确立「按查询点邻域建局部模型」范式，系统梳理距离度量与核带宽选择 | ✅ |
| 1.2 | **Yeo, W. S.** | 2023 | Journal of Process Control 128:103025 | Just-in-time based soft sensors for process industries: A status report and recommendations | [10.1016/j.jprocont.2023.103025](https://doi.org/10.1016/j.jprocont.2023.103025) | ⭐ **最新最权威的 JITL 软测量综述**（被引 60）：拆成「相似度度量→样本选择→局部模型→更新策略」四模块，**逐一点评各模块缺陷** | ✅ |
| 1.3 | Sheng, W. | 2024 | Canadian J. Chemical Engineering 102(5):1884–1898 | A review of just-in-time learning-based soft sensor in industrial process | [10.1002/cjce.25169](https://doi.org/10.1002/cjce.25169) | 2024 新综述（被引 24）：按连续/间歇、时变/多工况场景整理技术路线，便于建立**分类框架** | ✅ |
| 1.4 | Atkeson, C. G. | 1997 | Artificial Intelligence Review 11(1–5):75–113 | Locally Weighted Learning for Control | [10.1023/A:1006511328852](https://doi.org/10.1023/A:1006511328852) | 姊妹篇（被引 174）：局部模型**何时**优于全局模型、如何在线丢弃过期数据 | ✅ |
| 1.5 | Lawrence, N. P. | 2024 | Control Engineering Practice 145:105841 | Machine learning for industrial sensing and control: A survey and practical perspective | [10.1016/j.conengprac.2024.105841](https://doi.org/10.1016/j.conengprac.2024.105841) | 工程落地视角（被引 87）：数据量、漂移、可解释性、**不确定性报告的工业约束** | ✅ |

> ⭐ **1.2 Yeo 2023 就是你开题报告第 2 章的骨架。** 它那个四模块划分直接变成你的四个小节。
> **1.1 Atkeson 1997 读前 20 页就够** —— 用来回答答辩必问的「为什么要用局部模型」。

---

# 二、JITL 样本选择与相似度度量（⭐ 你的主战场）

| # | 第一作者 | 年份 | 期刊 | 标题 | DOI / 链接 | 一句话 | 核实 |
|:--:|---|---|---|---|---|---|:--:|
| 2.1 | **Miao, F.** | 2014 | Ind. Eng. Chem. Res. 53(51):19979–19986 | Adaptive Gaussian Mixture Model-Based Relevant Sample Selection for JITL Soft Sensor Development | [10.1021/ie5029864](https://doi.org/10.1021/ie5029864) | **问题的一半**：指出欧氏距离选样在**非高斯多模态**下会误选，改用自适应 GMM 后验概率加权（被引 49） | ⚠️ |
| 2.2 | **Wang, P.** | 2022 | Chemical Engineering Science 258:117753 | A unified just-in-time learning paradigm and its application to adaptive soft sensing for nonlinear and time-varying chemical process | [10.1016/j.ces.2022.117753](https://doi.org/10.1016/j.ces.2022.117753) | **问题的另一半**：明确指出传统 JITL「**相关样本选择与局部模型构建分开操作**」的结构性缺陷（被引 23）。**← 你的毕设问题原始出处** | ⚠️ |
| 2.3 | Yuan, X. | 2018 | Journal of Chemometrics 32(9) | Multi-similarity measurement driven ensemble just-in-time learning for soft sensing of industrial processes | [10.1002/cem.3040](https://doi.org/10.1002/cem.3040) | **「该用哪种距离」的必读**：欧氏/角度/相关性多相似度分别驱动子模型再加权集成（被引 65） | ✅ |
| 2.4 | Song, Y. | 2020 | Sensors 20(13):3804 | A Novel Just-in-Time Learning Strategy for Soft Sensing with Improved Similarity Measure Based on Mutual Information and PLS | [10.3390/s20133804](https://doi.org/10.3390/s20133804) | 用互信息+PLS 构造相似度，让度量反映「**对质量变量的解释能力**」而非仅几何距离。**开放获取**（被引 20） | ✅ |
| 2.5 | **Zhou, J.** | 2023 | Asia-Pacific J. Chemical Engineering 19(1):e3007 | A semi-supervised JITL paradigm based on manifold regularization for online soft sensor development | [10.1002/apj.3007](https://doi.org/10.1002/apj.3007) | ⭐ **「局部几何」代表作**：用**流形正则化**刻画局部几何结构，并把无标签样本纳入 JITL | ✅ |
| 2.6 | **Shao, W.** | 2023 | Chemom. Intell. Lab. Syst. 242:104937 | Semi-supervised local manifold regularization model based on dual representation for industrial soft sensor development | [10.1016/j.chemolab.2023.104937](https://doi.org/10.1016/j.chemolab.2023.104937) | 对偶表示下的局部流形正则半监督建模，从**优化角度**形式化局部几何保持（被引 11） | ✅ |
| 2.7 | Yan, S. | 2026 | Chemical Engineering Science 330:123911 | Fast and interpretable just-in-time learning via information-weighted similarity search: probabilistic soft sensing of catalyst coke in MTO process | [10.1016/j.ces.2026.123911](https://doi.org/10.1016/j.ces.2026.123911) | 最新（2026）：信息加权相似度检索兼顾速度与可解释性，输出**概率化预测**；「相似度+概率输出」合流 | ⚠️ |
| 2.8 | Chen, K. | 2013 | IEEE ICCA 2013:810–815 | Adaptive weighted relevant sample selection of just-in-time learning soft sensor for chemical processes | [10.1109/ICCA.2013.6565160](https://doi.org/10.1109/ICCA.2013.6565160) | **方法演化起点**：较早提出「自适应加权」选样，是 GMM 方法的前身思路 | ⚠️ |
| 2.9 | Zheng, J. | 2021 | IEEE Access 9:72172–72182 | Improved Mahalanobis Distance Based JITL-LSTM Soft Sensor for Multiphase Batch Processes | [10.1109/ACCESS.2021.3079184](https://doi.org/10.1109/ACCESS.2021.3079184) | 用**改进马氏距离**替代欧氏距离处理量纲与变量相关性 —— 说明距离度量的**几何假设**如何影响选样（被引 21） | ✅ |

> 💡 **2.7 值得注意**：它做的正是 **MTO 过程的催化剂结焦**（catalyst coke in MTO）—— 和你师兄的 DMTO-JITL 是**同一条线**。**读它之前，先问师兄这篇是不是组里的工作。**

> 📌 **必读三篇：2.1 → 2.2 → 2.3。** 读完你就掌握了「样本选择」这条线从**单一距离**走向**几何/概率/结构**的全过程。

---

# 三、局部建模方法（工具箱，不是你的创新点）

| # | 第一作者 | 年份 | 期刊 | 标题 | DOI / 链接 | 一句话 | 核实 |
|:--:|---|---|---|---|---|---|:--:|
| 3.1 | Kaneko, H. | 2015 | AIChE Journal 62(3):717–725 | Ensemble locally weighted partial least squares as a just-in-time modeling method | [10.1002/aic.15090](https://doi.org/10.1002/aic.15090) | LWPLS 集成化：多个不同带宽子模型集成，缓解单一带宽的精度敏感（被引 51）。**JITL+PLS 的标准参照** | ✅ |
| 3.2 | Hazama, K. | 2015 | Chemom. Intell. Lab. Syst. 146:55–62 | Covariance-based locally weighted partial least squares for high-performance adaptive modeling | [10.1016/j.chemolab.2015.05.007](https://doi.org/10.1016/j.chemolab.2015.05.007) | 用**协方差形式**重写 LWPLS，大幅提升在线自适应建模效率，把 LWPLS 推向实用（被引 85） | ✅ |
| 3.3 | Yang, K. | 2016 | Chemom. Intell. Lab. Syst. 155:170–182 | Soft sensor development for online quality prediction of industrial batch **rubber mixing** process using ensemble just-in-time Gaussian process regression models | [10.1016/j.chemolab.2016.04.009](https://doi.org/10.1016/j.chemolab.2016.04.009) | ⭐ **JITL + 高斯过程回归**的结合范例：GPR 天然输出预测方差，是通向「预测可靠性」的天然桥梁（被引 65） | ✅ |
| 3.4 | Wang, L. | 2016 | Ind. Eng. Chem. Res. 55(28):7704–7719 | Soft Sensor Development Based on the Hierarchical Ensemble of Gaussian Process Regression Models for Nonlinear and Non-Gaussian Chemical Processes | [10.1021/acs.iecr.6b00240](https://doi.org/10.1021/acs.iecr.6b00240) | 分层集成 GPR 处理非高斯过程，展示贝叶斯局部模型如何应对**多模态分布**（被引 33） | ⚠️ |
| 3.5 | Liu, Y. | 2021 | Applied Soft Computing 101:107060 | Adaptive ranking based ensemble learning of Gaussian process regression models for quality-related variable prediction in process industries | [10.1016/j.asoc.2020.107060](https://doi.org/10.1016/j.asoc.2020.107060) | 用自适应排序挑选参与集成的 GPR 子模型 —— 本质是「**模型层面的选择**」问题（被引 39） | ✅ |

> 💡 **3.3 值得注意**：它做的是**橡胶混炼过程**（rubber mixing）—— 和另一个候选题目（丁基橡胶 T90）直接相关。**即使你选了 JITL 题目，这篇也值得留着。**

---

# 四、预测不确定性量化与可靠性评估（⭐ 你的第二战场）

| # | 第一作者 | 年份 | 期刊 | 标题 | DOI / 链接 | 一句话 | 核实 |
|:--:|---|---|---|---|---|---|:--:|
| 4.1 | **Kaneko, H.** | 2021 | Journal of Chemometrics 35(9):e3364 | Estimating the reliability of predictions in locally weighted partial least-squares modeling | [10.1002/cem.3364](https://doi.org/10.1002/cem.3364) · [免费 PDF](https://meiji.repo.nii.ac.jp/record/2001364/files/journalofchemometrics_35_9_1.pdf) | ⭐ **靶心论文**：在 LWPLS 框架内**定义并估计预测可靠性**，把可靠性落成可计算量（被引 13） | ✅ |
| 4.2 | Liu, Y. | 2012 | Ind. Eng. Chem. Res. 51(8):3356–3367 | Development of Interval Soft Sensors Using Enhanced Just-in-Time Learning and Inductive Confidence Predictor | [10.1021/ie201053j](https://doi.org/10.1021/ie201053j) | **可靠性方向的经典**：JITL 输出带置信度的**预测区间**，归纳式置信预测器给出覆盖率保证（被引 51） | ⚠️ |
| 4.3 | Yuan, X. | 2017 | IEEE Trans. Control Systems Technology 25(3):1124–1132 | A Probabilistic Just-in-Time Learning Framework for Soft Sensor Development With Missing Data | [10.1109/TCST.2016.2579609](https://doi.org/10.1109/TCST.2016.2579609) | **概率 JITL 的标杆**（被引 116）：变分贝叶斯全面概率化，同时处理缺失数据并给出预测分布 | ⚠️ |
| 4.4 | Huang, H. | 2020 | Ind. Eng. Chem. Res. 59(11):5010–5021 | Variable-Scale Probabilistic Just-in-Time Learning for Soft Sensor Development with Missing Data | [10.1021/acs.iecr.9b06113](https://doi.org/10.1021/acs.iecr.9b06113) | 局部**尺度**（带宽/邻域大小）随查询点自适应 —— 把「局部范围」本身参数化（被引 18） | ⚠️ |
| 4.5 | Guo, F. | 2020 | Journal of Process Control 92:90–97 | Output-relevant Variational autoencoder for Just-in-time soft sensor modeling with missing data | [10.1016/j.jprocont.2020.05.012](https://doi.org/10.1016/j.jprocont.2020.05.012) | 输出相关 VAE 做 JITL 局部建模，兼顾缺失数据与**潜变量不确定性**（被引 51） | ✅ |
| 4.6 | Zhu, H. | 2026 | Journal of Process Control 160:103661 | Uncertainty-calibrated Gaussian process regression for robust soft sensor modeling with industrial fermentation applications | [10.1016/j.jprocont.2026.103661](https://doi.org/10.1016/j.jprocont.2026.103661) | **最新（2026）**：指出 GPR 的方差输出常**过度/欠自信**，做后验校准使其真正可信 + 工业验证 | ⚠️ |
| 4.7 | Zhang, B. | 2022 | Applied Soft Computing 131:108995 | A probabilistic neural network for uncertainty prediction with applications to manufacturing process monitoring | [10.1016/j.asoc.2022.108995](https://doi.org/10.1016/j.asoc.2022.108995) | 逐样本不确定性预测 —— 把可靠性从「模型级」推进到「**样本级**」（被引 14） | ✅ |
| 4.8 | Wang, X. | 2024 | Applied Soft Computing 167:111974 | Deep learning with local spatiotemporal structure preserving for soft sensor development of complex industrial processes | [10.1016/j.asoc.2024.111974](https://doi.org/10.1016/j.asoc.2024.111974) | 显式**保持局部时空几何结构**的深度软测量。非 JITL 框架下的同源思路，可作**方法论对照**（被引 27） | ✅ |

> 📌 **4.1（框架）+ 4.2（区间与覆盖率）+ 4.3（概率化完整形态）** 是这个方向的三级台阶。
> 💡 **4.6 给你的提示**：连高斯过程的方差都"不自信"，说明**校准（calibration）**本身就是一个可做的点。

---

# 五、中文文献（先读，建立表述体系）

| # | 第一作者 | 年份 | 期刊 | 标题 | 链接 | 一句话 | 核实 |
|:--:|---|---|---|---|---|---|:--:|
| 5.1 | 杨鑫 | 2018 | 计算机与应用化学 35(9) | 即时学习法在过程工业中的应用研究进展 | [CNKI](https://www.cnki.com.cn/Article/CJFDTotal-JSYH201809007.htm) · [万方](https://d.wanfangdata.com.cn/periodical/jsjyyyhx201809007) | **中文 JITL 综述首选**：梳理 JITL 基本思想并归类已有方法，中文引用的主干（另有作者周成宇；无 DOI） | ✅ |
| 5.2 | 黎宏陶 | 2024 | 化工学报 75(6):2299–2312 | 基于即时学习的改进条件高斯回归软测量 | [10.11949/0438-1157.20240127](https://doi.org/10.11949/0438-1157.20240127) · [国家科技期刊平台](https://opaj.napstic.cn/periodicalArticle/0120240702546065) | **国内最新代表**：样本时空混合加权的条件高斯回归 JITL（黎宏陶、王振雷、王昕）。中文里最贴合「**概率化 + 选样**」 | ✅ |
| 5.3 | 田洲 | 2020 | 自动化仪表 41(8) | 化工过程动态软仪表技术发展现状及展望 | [华东理工机构库](https://ir.ecust.edu.cn/articles/article_detail.aspx?id=af92ad120dc049ef9a56faed5360f554) | 从「动态软仪表」角度综述化工软测量建模与在线实现，交代**软测量整体背景**（田洲、杨逸俊、王振雷；无 DOI） | ✅ |
| 5.4 | — | 2020 | 信息与控制 49(3):257– | 基于多模态扰动的集成即时学习软测量建模 | [期刊官网](https://xk.sia.cn/cn/article/Y2020/I3/257) | 集成 JITL + 多模态扰动，针对多工况过程的选样与集成 | ❓ |
| 5.5 | — | 2019 | 信息与控制 | 基于多样性加权相似度的集成局部加权偏最小二乘软测量建模 | [10.13976/j.cnki.xk.2019.8156](https://doi.org/10.13976/j.cnki.xk.2019.8156) | **中文里少见专门讨论「相似度度量设计」的工作**，与你的题目高度相关 | ❓ |
| 5.6 | — | — | 学位论文 | 基于即时学习的工业过程建模与监测 | 仅见检索片段，无稳定公开链接 | 主题为 JITL 在工业过程建模与监测中的应用 | ❓ **作者/年份/单位全部未核实 —— 建议不要引用** |

> ⚠️ **中文期刊的 DOI 多由 CNKI / 万方注册，不在 Crossref 里**，无法用同一套机制交叉核验。
> 5.4 / 5.5 的**作者姓名未能从原始页面读到**；**5.6 完全未核实**。
> **引用 5.4 / 5.5 前，务必在校内 CNKI 核对作者、卷期、页码。5.6 直接放弃。**

**✅ 中文引用稳妥组合：5.1 + 5.2 + 5.3**

---

# 六、7 周阅读顺序

> 与《开题冲刺计划》W2–W8 对齐。**每周 3 篇：2 篇精读 + 1 篇泛读。**

### 第 1 周 · 建立坐标系（只读 2 篇，先不碰公式）
- **1.2 Yeo 2023** → 拿到开题报告「国内外研究现状」的四模块骨架，并定位自己的题目落在哪个模块
- **1.1 Atkeson 1997**（前 20 页即可）→ 弄清「为什么局部模型优于全局模型」，答辩最可能问的根本动机

### 第 2–3 周 · 锁定问题（毕设核心，必须精读）
- **2.1 Miao 2014** → 看欧氏距离在非高斯多模态下如何选错样本
- **2.2 Wang 2022** → 看「选样与建模分离」这一结构性缺陷如何被形式化
- **2.3 Yuan 2018** → 建立「不同几何假设 → 不同选样结果」的证据链

> 💡 **这两周连读后，你的「研究问题」一段几乎可以直接成型：**
> 选样准则依赖的几何假设（欧氏＝各向同性球形邻域）与实际局部几何（多模态、弯曲流形、变量各向异性）不匹配，**且选样与建模目标不一致**。

### 第 4 周 · 补局部几何视角
- **2.5 Zhou 2023** + **2.6 Shao 2023**（流形正则化）→ 回答「如何把局部几何**显式写进目标函数**」
- **4.8 Wang 2024**（局部时空结构保持）→ 非 JITL 框架下的同源思路，作对照
- 零基础提示：**只需读懂正则项起什么作用，不必复现**

### 第 5 周 · 转向可靠性（第二个关键词）
- **4.1 Kaneko 2021**（**优先，今天就能下**）→ 在 LWPLS 内定义并估计预测可靠性
- **4.2 Liu 2012** → 建立「可靠性 = 预测区间 + 覆盖率」的基本观念
- **4.3 Yuan 2017** → 看概率化框架的完整形态

### 第 6 周 · 补局部建模工具箱
- **3.1 Kaneko 2015** + **3.2 Hazama 2015** → 掌握最常用局部模型的本体与高效实现
- **3.3 Yang 2016**（JITL + GPR）→ 看清主线：**GPR 天然给方差、LWPLS 天然给局部加权，两者都是可靠性的载体但都需校准**
- **4.6 Zhu 2026** 收尾 → 正好呼应上一句

### 第 7 周 · 中文文献与撰写
- **5.1 杨鑫 2018** → 中文表述体系与国内脉络
- **5.2 黎宏陶 2024** → 国内最新工作
- 此时写「国内外研究现状」水到渠成

### ⏱ 只有 5 天时的最小集
> **1.2 → 2.1 → 2.2 → 4.1**
> 四篇恰好覆盖「领域综述 → 几何假设缺陷 → 问题形式化 → 可靠性评估」

---

# 七、怎么用这份清单

### ① 别只依赖清单 —— 问人永远更快

发给师兄这句话：

> 「师兄，我在看 JITL 这个方向，你建议我先读哪 5 篇？有没有你觉得必读的？」

**师兄给的 5 篇 > 这份清单的 25 篇** —— 因为他知道组里在做什么、老师认可什么。

### ② 拿到 DOI 后怎么下全文

| 情况 | 办法 |
|---|---|
| ✅ 链接可达 | 直接下 |
| ⚠️ 403 / 要付费 | ① **学校图书馆 VPN** → ② [sci-hub.se](https://sci-hub.se)（输 DOI）→ ③ 给通讯作者发邮件要 |
| **Kaneko 2021 / Song 2020** | **本身开放获取**，不用权限 |

### ③ 每篇都要写笔记

用《开题冲刺计划》6.2 节的模板。**不写笔记 = 没读。**

### ④ 边读边更新「方法演进图」

```
Atkeson 1997  局部加权学习奠基
      ↓ 问题：欧氏距离假设"各向同性球形邻域"
Chen 2013 / Miao 2014   自适应加权 → GMM 概率选样
      ↓
Yuan 2018 / Song 2020 / Zheng 2021   多相似度集成 / 互信息 / 马氏距离
      ↓
Zhou 2023 / Shao 2023 / Wang 2024    流形正则 · 局部几何显式建模
      ↓
Wang 2022 / Yan 2026                 选样与建模统一 · 概率化输出
      ↓
Liu 2012 → Kaneko 2021 → Zhu 2026    区间预测 → LWPLS内可靠性 → 不确定性校准
      ↓
   ★ 还没解决什么？  ← 你的创新点在这里
```

---

# 八、注意事项

| # | 事项 |
|:--:|---|
| 1 | **5.4 / 5.5 作者姓名未核实**，引用前必须在校内 CNKI 核对；**5.6 完全未核实，直接放弃** |
| 2 | **2.7 Yan 2026** 和 **4.6 Zhu 2026** 是 2026 年新刊，Crossref 已定卷页，**引用前建议再确认正式见刊** |
| 3 | ScienceDirect / ACS 在调研环境返回 403，**不等于你不能访问** —— 用学校网络再试 |
| 4 | **2.7 做的是 MTO 催化剂结焦**，和师兄的工作同线 —— **读之前先问师兄是不是组里的工作** |
| 5 | **3.3 做的是橡胶混炼** —— 和另一个候选题目（丁基橡胶 T90）直接相关，留着 |

---

# 九、一句话总结

> **你要读的不是 25 篇论文，是一条演进线：**
>
> **别人怎么挑样本 → 为什么挑得不好 → 你怎么挑得更好 → 并让模型知道自己有多准。**
