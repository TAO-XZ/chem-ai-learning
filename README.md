# chem-ai-learning

应用化学本科 → **智能化工（化工过程数据科学）** 方向的学习记录。

- **起点**：编程零基础，AI 零基础
- **目标**：2027 年 7 月入组前，具备独立完成「数据处理 → 建模 → 优化 → 报告」全流程的能力
- **节奏**：25 小时/周，约 40 周

---

## 目录

- [P0 环境搭建（已完成）](#p0-环境搭建已完成)
- [学习路线](#学习路线)
- [进度日志](#进度日志)

---

## P0 环境搭建（已完成）

> **完成日期**：2026-10-12
> **实际耗时**：约 6 小时
> **产出**：一套可复现的 Python 科学计算环境 + 完整版本管理工具链

### 一、最终环境参数

| 项目 | 值 |
|---|---|
| 操作系统 | Windows |
| conda 安装路径 | `D:\conda` |
| 工作环境名 | `chem` |
| 工作环境路径 | `D:\conda\envs\chem` |
| 解释器路径 | `D:\conda\envs\chem\python.exe` |
| Python 版本 | 3.11 |
| 分工 | conda 建环境 / pip 装库 |
| 镜像源 | 中科大 USTC |
| 编辑器 | VS Code |
| 版本管理 | Git + GitHub |

### 二、已安装的核心库

| 库 | 版本 | 用途 |
|---|---|---|
| numpy | 2.4.6 | 数组与矩阵运算，一切数值计算的地基 |
| pandas | 3.0.6 | 表格数据处理与清洗 |
| matplotlib | 3.11.2 | 绘图（含论文级矢量图输出） |
| scipy | 1.17.1 | 曲线拟合、信号处理、数值优化 |
| scikit-learn | 1.9.1 | 机器学习算法 |
| jupyter | 1.1.1 | 交互式笔记本（代码 + 笔记 + 图 一体） |

### 三、为什么需要这套环境

对于「用代码处理化学数据」这件事，每个组件解决一个具体问题：

| 组件 | 它解决什么问题 |
|---|---|
| conda | 不同项目依赖的库版本会互相冲突，需要**环境隔离** |
| chem 环境 | 我的专属工作空间，所有学习与项目的依赖都装在这里 |
| numpy / pandas | 光谱、过程数据动辄几万行，Excel 打不开，必须用代码处理 |
| matplotlib | 批量出图、参数化重绘、直接输出投稿格式 |
| scipy | 谱图平滑求导、曲线拟合、参数寻优 |
| scikit-learn | 从数据里找规律——回归、分类、聚类、降维 |
| Jupyter | 边写代码边看结果，等于**电子版实验记录本** |
| Git / GitHub | 版本存档（改坏了能还原）+ 云端备份 + 作品集 |

### 四、完整复现步骤

> 换电脑 / 上服务器时，照这个顺序重做一遍。

**1. 安装 Miniforge（conda）**

- 下载：`Miniforge3-<版本>-Windows-x86_64.exe`（约 141 MB）
- 国内镜像：中科大 `https://mirrors.ustc.edu.cn/github-release/conda-forge/miniforge/LatestRelease/`
- 安装选项：
  - 路径改为 `D:\conda`（**路径不含中文和空格**）
  - ✅ Create shortcuts
  - ❌ Add to PATH
  - ❌ Register as default Python
  - ✅ Clear package cache

**2. 把 conda 接入 PowerShell**

在开始菜单打开 **Miniforge Prompt**，执行：

```
conda init powershell
```

关掉终端、重开普通 PowerShell，验证 `conda --version`。

**3. 配置国内镜像源**

```powershell
conda config --add channels https://mirrors.ustc.edu.cn/anaconda/cloud/conda-forge/
conda config --set show_channel_urls yes
pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/simple
```

**4. 创建并激活工作环境**

```powershell
conda create -n chem python=3.11 -y
conda activate chem
```

**5. 安装核心库**

```powershell
pip install numpy pandas matplotlib scikit-learn scipy jupyter
```

**6. 验证**

```powershell
python -c "import numpy, pandas, matplotlib, sklearn, scipy; print('全部就绪')"
```

**7. 配置 Git 与 SSH**

```powershell
git config --global user.name "TAO-XZ"
git config --global user.email "<GitHub 用户名>@users.noreply.github.com"
git config --global core.quotepath false
git config --global init.defaultBranch main

ssh-keygen -t ed25519 -C "<GitHub 用户名>@users.noreply.github.com"
# 三次回车；然后把 ~/.ssh/id_ed25519.pub 的内容加到 GitHub → Settings → SSH keys

ssh -T git@github.com
```

### 五、VS Code 配置

已安装扩展：

| 扩展 | 作用 |
|---|---|
| ms-python.python | Python 语法、运行、调试 |
| ms-toolsai.jupyter | 在 VS Code 内运行 notebook |
| ms-python.vscode-pylance | 智能补全与实时类型检查 |
| eamodio.gitlens | 代码修改历史可视化 |
| MS-CEINTL.vscode-language-pack-zh-hans | 中文界面 |

> ⚠️ **每次打开新文件夹，都要重新选解释器**：`Ctrl+Shift+P` → `Python: Select Interpreter` → `D:\conda\envs\chem\python.exe`
> VS Code 的「推荐解释器」按最近使用推荐，与本项目无关，**不可信**。

### 六、踩过的坑（重要）

| 问题 | 原因 | 解决 |
|---|---|---|
| 清华镜像站返回 403 拒绝访问 | 镜像站按 IP 归属地拦截 | 换中科大 / 南大镜像 |
| `conda : 无法将"conda"项识别为 cmdlet` | 安装时未加入 PATH，且未初始化 shell | Miniforge Prompt 里跑 `conda init powershell`，**并重开终端** |
| `无法加载文件...因为在此系统上禁止运行脚本` | PowerShell 执行策略默认受限 | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| VS Code 选了 Python 3.14，代码报 `ModuleNotFoundError` | 编辑器默认选了机器上原有的 Python | 手动选 `chem` 解释器；换文件夹要重选 |
| `error: no action specified` | 粘贴命令时两行粘成了一行 | 重新逐行执行 |
| 装的库 `import` 不到 | 命令行未激活环境 | 确认提示符前缀是 `(chem)` |

### 七、核心习惯（必须坚持）

1. **每次写代码前，先看命令行前缀是不是 `(chem)`** —— 90% 的「昨天还能跑」都是开错环境
2. **每打开一个新文件夹，先确认右下角解释器是 `chem`**
3. **库用 pip 装，环境用 conda 建**，不要混用同一种包的两个管理器
4. **每天都要有 commit**，哪怕只改一行

---

## 学习路线

| 阶段 | 周次 | 主题 | 状态 |
|:---:|:---:|---|:---:|
| **P0** | W1 | 环境与工具链 | ✅ 已完成 |
| **P1** | W2–W7 | Python 编程基础 | ⬜ |
| **P2** | W8–W12 | 科学计算 + 数据分析 + 论文级出图 | ⬜ |
| **P3** | W13–W16 | 数学补强 + 机器学习核心 | ⬜ |
| **P4** | W17–W22 | 化学计量学 + 光谱与过程数据 | ⬜ |
| **P5** | W23–W28 | 贝叶斯优化与自动实验闭环 ★ | ⬜ |
| **P6** | W29–W32 | 过程监测、故障诊断与软测量 | ⬜ |
| **P7** | W33–W36 | 深度学习 + LLM 科研工作流 | ⬜ |
| **P8** | W37–W40 | 论文复现 + 作品集 + 入组冲刺 | ⬜ |

### 每阶段验收标准

- **P1**：不查资料写出 100–150 行含函数、循环、文件读写的脚本；能读懂报错并自行修复
- **P2**：拿陌生 CSV 完成「读取→清洗→统计检验→建模→论文级出图」全流程
- **P3**：完成 2 个 sklearn 端到端项目；能解释交叉验证、正则化、偏差-方差权衡
- **P4**：在公开近红外数据集上完成预处理对比 + PLS 定量 + PCA 异常样本识别
- **P5**：在真实文献反应数据上跑通贝叶斯优化闭环，证明比随机搜索更省实验次数
- **P6**：在田纳西-伊斯曼过程数据集上完成 PCA-MSPC 监测与故障诊断
- **P7**：能用 PyTorch 从零写训练循环；完成 1D-CNN 与传统方法的同条件对比
- **P8**：精读并复现 2 篇课题组论文；GitHub 作品集完整可运行

---

## 进度日志

### 2026-10-12 · P0 完成

搭建了完整的 Python 科学计算环境与版本管理工具链。踩了 6 个坑，全部解决。

**当天的第一个程序**：`test.ipynb` —— 用 numpy 生成数据、matplotlib 绘制正弦曲线。

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 200)
plt.plot(x, np.sin(x))
plt.title("sin(x)")
plt.show()
```

---

*最后更新：2026-10-12*
