# 视觉 SSM 研究学习路线

> 方向 B：视觉 SSM 扩展 — 从理论基础到前沿探索的完整学习路径
> 共 26 篇论文，分 4 个阶段，建议 8-12 周完成

---

## 论文清单与目录结构

```
papers/pdf/
├── 1-foundations/          ← 阶段一：SSM 基础理论 (6 篇)
│   ├── 01_HiPPO_NeurIPS2020.pdf
│   ├── 02_S4_ICLR2022.pdf
│   ├── 03_HowToTrainHiPPO_ICLR2023.pdf
│   ├── 04_Mamba_COLM2024.pdf
│   ├── 05_Mamba2_SSD_ICML2024.pdf
│   └── 06_FlashAttention_NeurIPS2022.pdf
│
├── 2-visual-ssm-core/      ← 阶段二：视觉 SSM 核心论文 (6 篇)
│   ├── 01_Vim_VisionMamba_ICML2024.pdf
│   ├── 02_VMamba_NeurIPS2024.pdf
│   ├── 03_S4ND_NeurIPS2022.pdf
│   ├── 04_LocalMamba_ECCV2024.pdf
│   ├── 05_2DMamba_CVPR2024.pdf
│   └── 06_QuadMamba_NeurIPS2024.pdf
│
├── 3-visual-ssm-advanced/   ← 阶段三：视觉 SSM 进阶 (7 篇)
│   ├── 01_DemystifyMambaVision_NeurIPS2024.pdf
│   ├── 02_VSSD_ICCV2025.pdf
│   ├── 03_Caduceus_ICML2024.pdf
│   ├── 04_SelectiveVisualPrompting_arXiv2024.pdf
│   ├── 05_MambaVL_Fusion_arXiv2024.pdf
│   ├── 06_HydraMamba_ACMmm2025.pdf
│   └── 07_Jamba_arXiv2024.pdf
│
└── 4-analysis-comparison/   ← 阶段四：分析与对比 (7 篇)
    ├── 01_EmpiricalStudyMambaLM_NVIDIA2024.pdf
    ├── 02_UnderstandingInputSelectivity_ICML2025.pdf
    ├── 03_ExploringLimitationsMamba_EMNLP2025.pdf
    ├── 04_ReMamba_EMNLP2025.pdf
    ├── 05_InterpretingSteeringSSM_ICML2026.pdf
    ├── 06_Mamba3_ICLR2026.pdf
    └── 07_LogLinearAttention_ICLR2026.pdf
```

---

## 阶段一：SSM 基础理论 (2-3 周)

> 目标：理解状态空间模型的数学基础和核心创新，建立 SSM 从理论到 Mamba 的完整认知

### 1.1 HiPPO 框架 — SSM 的起源
**论文**: `1-foundations/01_HiPPO_NeurIPS2020.pdf`
**预计阅读**: 2-3 天
**核心问题**: 如何用最优多项式投影压缩历史信息？

**阅读重点**:
- 连续时间状态空间方程: x'(t) = Ax(t) + Bu(t), y(t) = Cx(t) + Du(t)
- HiPPO 矩阵的构造: Legendre 多项式基下的最优投影
- 在线记忆问题: 如何在固定大小状态中压缩历史序列

**关键概念**:
- HiPPO 矩阵 A: 决定了信息遗忘的速度和方式
- 正交多项式基: Legendre, Fourier, Chebyshev 等
- 测度函数 μ: 决定对不同时间步的权重分配

### 1.2 S4 — 结构化状态空间模型
**论文**: `1-foundations/02_S4_ICLR2022.pdf`
**预计阅读**: 2-3 天
**核心问题**: 如何让 SSM 在实际训练中高效且有效？

**阅读重点**:
- DPLR (Diagonal Plus Low-Rank) 参数化: A = Λ - PP^T
- 卷积视图: 通过 FFT 实现 O(N log N) 的序列计算
- 连续→离散转换: 双线性变换 (bilinear transform)
- 长序列基准测试 (Long Range Arena, Path-X 等) 上的突破性结果

**关键公式**:
- 离散化: A_bar = (I - ΔA/2)^{-1}(I + ΔA/2)
- 卷积核: K = (CB, CAB, CA²B, ...) 可通过 FFT 高效计算

### 1.3 How to Train Your HiPPO — 广义正交基
**论文**: `1-foundations/03_HowToTrainHiPPO_ICLR2023.pdf`
**预计阅读**: 1-2 天
**核心问题**: 不同正交基对 SSM 表现有何影响？

**阅读重点**:
- HiPPO 框架的泛化: 从 Legendre 到 Fourier/Chebyshev
- 不同基函数对应的 HiPPO 矩阵
- S4D: S4 的简化版本，更易训练

### 1.4 Mamba (S6) — 选择性状态空间
**论文**: `1-foundations/04_Mamba_COLM2024.pdf`
**预计阅读**: 3-4 天 ⚠️ **本方向最核心论文**
**核心问题**: 如何让 SSM 具备输入依赖的选择性？

**阅读重点**:
- 选择性机制: B(x), C(x), Δ(x) 由输入决定 (vs S4 中的固定参数)
- 选择性扫描 (selective scan) 算法: 硬件感知的高效实现
- 全局卷积 (训练) → 循环 (推理) 的模式切换
- 简化架构: 去除 attention 和 MLP，仅用 SSM 层搭建模型
- Mamba block 的完整结构 (conv1d + SSM + gate + 投影)

**关键洞察**:
- 选择性 = 门控 = attention 的隐式形式
- 线性时间 O(N) vs 注意力 O(N²)
- 硬件感知: 利用 GPU SRAM 的分块扫描

### 1.5 Mamba-2 / SSD — 状态空间对偶
**论文**: `1-foundations/05_Mamba2_SSD_ICML2024.pdf`
**预计阅读**: 3-4 天 ⚠️ **理解 SSM-Attention 关系的关键**
**核心问题**: SSM 和 Attention 之间是否存在数学对偶？

**阅读重点**:
- SSD (State Space Duality) 框架: SSM 等价于半可分离矩阵的乘法
- 1-半可分离矩阵的结构与性质
- 对偶形式: 从 SSM 视角 ↔ Attention 视角的自洽转换
- Mamba-2 的改进: 更大状态维度 (N=64→256), 训练速度 2-8x 加速
- 理论统一: SSM, Attention, 线性 attention 都在 SSD 框架下

**关键公式**:
- SSD 注意力形式: Q, K, V 的特定结构化版本
- 半可分离矩阵: L[i,j] = C_i A^{i-j-1} B_j

### 1.6 FlashAttention (背景知识)
**论文**: `1-foundations/06_FlashAttention_NeurIPS2022.pdf`
**预计阅读**: 1-2 天 (快速浏览)
**核心问题**: 如何通过 IO-aware 实现高效注意力？

**阅读重点** (与 SSM 的关联):
- 分块计算 (tiling) 策略: 与 Mamba 选择性扫描的分块思路类比
- 硬件感知设计理念: GPU 内存层级 (SRAM vs HBM) 的利用
- 重计算策略: 不存储中间结果, 反向传播时重新计算

---

## 阶段二：视觉 SSM 核心论文 (2-3 周)

> 目标：理解 SSM 从 1D 序列到 2D 图像的核心挑战和现有解决方案

### 2.1 S4ND — 多维信号的状态空间建模
**论文**: `2-visual-ssm-core/03_S4ND_NeurIPS2022.pdf`
**预计阅读**: 1-2 天
**核心问题**: 如何将 1D SSM 扩展到多维 (图像/视频)？

**阅读重点**:
- N-D 状态空间: 多个 1D SSM 的组合
- 各向异性 vs 各向同性的处理方式
- 非因果性: 图像建模不需要因果约束
- 与 CNN 的联系: SSM 卷积核与可学习卷积的关系

**为什么先读**: 这是 SSM 用于视觉的最早尝试，理解其设计思路有助于后续工作的理解。

### 2.2 Vim (Vision Mamba) — 双向视觉 SSM
**论文**: `2-visual-ssm-core/01_Vim_VisionMamba_ICML2024.pdf`
**预计阅读**: 2-3 天 ⚠️ **视觉 SSM 最重要的论文之一**
**核心问题**: 如何用 Mamba 替代 ViT 中的自注意力做视觉表征学习？

**阅读重点**:
- 双向扫描: forward + backward 扫描解决非因果视觉任务
- 2D 图像 → 1D 序列的展开策略 (raster scan)
- Vim block 结构: 与 Mamba block 的差异
- 位置编码: 如何为 SSM 引入空间位置信息
- 实验结果: ImageNet 分类、COCO 检测、ADE20K 分割

**关键设计决策**:
- 为什么选择双向而非单向
- 类比 ViT: class token, patch embedding, position embedding 的保留与修改

### 2.3 VMamba — 视觉状态空间模型
**论文**: `2-visual-ssm-core/02_VMamba_NeurIPS2024.pdf`
**预计阅读**: 2-3 天 ⚠️ **与 Vim 并列的视觉 SSM 核心工作**
**核心问题**: 如何解决 2D 图像中空间局部性和全局依赖的矛盾？

**阅读重点**:
- SS2D (2D Selective Scan) 模块: 四个方向的交叉扫描
- 2D-SSM vs 1D-SSM 的维度适配
- 与 Vim 的核心差异: 扫描策略不同 (四方向 vs 双向)
- VSS (Visual State Space) block 的完整结构
- 架构变体: Tiny/Small/Base

**对比思考**:
- Vim 的双向扫描 vs VMamba 的四方向扫描: 谁更合理？
- 位置信息的引入方式有何不同？

### 2.4 LocalMamba — 窗口化选择性扫描
**论文**: `2-visual-ssm-core/04_LocalMamba_ECCV2024.pdf`
**预计阅读**: 1-2 天
**核心问题**: 局部窗口扫描能否更好地捕捉图像中的空间局部性？

**阅读重点**:
- 窗口划分策略: 类似 Swin Transformer 的窗口分割
- 多方向窗口内扫描
- 全局-局部信息融合
- 与 Swin Transformer 的对比

### 2.5 2DMamba — 真正的 2D 状态空间
**论文**: `2-visual-ssm-core/05_2DMamba_CVPR2024.pdf`
**预计阅读**: 1-2 天
**核心问题**: 能否直接构建 2D 状态空间而非用 1D 近似？

**阅读重点**:
- 2D 选择性扫描的数学定义
- 与 1D 扫展策略 (raster scan) 的对比
- 在 Gigapixel 病理切片上的应用
- 2D 状态矩阵的参数化

### 2.6 QuadMamba — 四叉树自适应扫描
**论文**: `2-visual-ssm-core/06_QuadMamba_NeurIPS2024.pdf`
**预计阅读**: 1-2 天
**核心问题**: 如何让扫描策略自适应图像内容？

**阅读重点**:
- 四叉树分区: 根据图像内容自适应划分区域
- 内容感知的扫描顺序: 而非固定 raster scan
- 可学习的扫描策略
- 与固定扫描策略的对比

---

## 阶段三：视觉 SSM 进阶 (2-3 周)

> 目标：理解视觉 SSM 的理论分析、跨模态扩展和前沿应用

### 3.1 Demystify Mamba in Vision — 线性注意力视角
**论文**: `3-visual-ssm-advanced/01_DemystifyMambaVision_NeurIPS2024.pdf`
**预计阅读**: 2 天 ⚠️ **理解 SSM 本质的关键论文**
**核心问题**: Vision Mamba 与线性注意力 Transformer 有何本质区别？

**阅读重点**:
- 将 Mamba SSM 重新表述为线性注意力变体
- 六个关键设计差异: input gate, forget gate, shortcut, 无 attention normalization, single-head, modified block design
- 消融实验: 哪些设计选择真正重要？
- 统一视角: SSM = 特定形式的线性注意力 + 额外的门控

**重要意义**: 这篇论文为理解 "SSM 到底比线性注意力好在哪" 提供了系统性分析。

### 3.2 VSSD — 视觉状态空间对偶
**论文**: `3-visual-ssm-advanced/02_VSSD_ICCV2025.pdf`
**预计阅读**: 2 天
**核心问题**: 如何将 SSD 对偶理论应用于视觉任务？

**阅读重点**:
- 非因果化 SSD: 去除因果约束后的视觉版本
- 全局感受野的实现
- 与 Vim/VMamba 的对比
- SSD 的视觉变体: 2D 扩展方式

### 3.3 Caduceus — 双向等变 DNA SSM
**论文**: `3-visual-ssm-advanced/03_Caduceus_ICML2024.pdf`
**预计阅读**: 1 天
**核心问题**: 如何为生物序列设计等变 SSM？

**阅读重点**:
- 反转等变性 (reverse equivariance): DNA 序列的特性
- 双向 Mamba 的等变版本
- 与 Vim 双向扫描的关系
- 从 DNA 到视觉: 等变性概念的迁移可能性

### 3.4 Selective Visual Prompting — SSM 微调
**论文**: `3-visual-ssm-advanced/04_SelectiveVisualPrompting_arXiv2024.pdf`
**预计阅读**: 1 天
**核心问题**: 如何高效微调 Vision Mamba？

**阅读重点**:
- SSM 中的 update/forget gate 与微调的关系
- 选择性 prompt 设计: 哪些 gate 需要激活
- Parameter-efficient fine-tuning (PEFT) 的 SSM 版本
- 微调中的信息瓶颈

### 3.5 MambaVL — 跨模态 SSM 融合
**论文**: `3-visual-ssm-advanced/05_MambaVL_Fusion_arXiv2024.pdf`
**预计阅读**: 1-2 天
**核心问题**: 如何用 SSM 实现视觉-语言跨模态融合？

**阅读重点**:
- 选择性 SSM 模态融合机制
- 跨模态长程依赖建模
- 问题引导的注意力/SSM 路由
- 与传统 cross-attention 的对比

### 3.6 HydraMamba — 多头 SSM 点云
**论文**: `3-visual-ssm-advanced/06_HydraMamba_ACMmm2025.pdf`
**预计阅读**: 1 天
**核心问题**: 如何将 SSM 扩展到 3D 点云？

**阅读重点**:
- 多头 SSM: 类似多头注意力
- 点云的无序性: 如何定义扫描顺序
- 全局点云学习的 SSM 策略
- 3D 任务的 SSM 适用性

### 3.7 Jamba — 混合 Transformer-Mamba
**论文**: `3-visual-ssm-advanced/07_Jamba_arXiv2024.pdf`
**预计阅读**: 1 天
**核心问题**: 大规模混合架构的工程实现与性能表现？

**阅读重点**:
- Transformer-Mamba 交替层设计
- MoE (Mixture of Experts) 集成
- 52B 总参/12B 活跃参数的工程优化
- 256K 上下文窗口的实现
- 混合架构在大规模下的表现

---

## 阶段四：分析与对比 (2-3 周)

> 目标：理解 SSM 的局限性、理论分析和最新进展，为选题提供支撑

### 4.1 Mamba 经验研究 — 大规模对比
**论文**: `4-analysis-comparison/01_EmpiricalStudyMambaLM_NVIDIA2024.pdf`
**预计阅读**: 1-2 天
**核心问题**: 纯 SSM vs 纯 Transformer vs 混合，在 8B 规模上谁更强？

**阅读重点**:
- 8B 参数 Mamba / Mamba-2 / Transformer / Mamba-2-Hybrid 对比
- 不同任务的表现差异: COPY, ICL, 长上下文推理
- SSM 的失败模式: 什么时候不如 Transformer
- 混合架构的优势点: 最优混合比例

### 4.2 Input Selectivity 理论 — 选择性机制分析
**论文**: `4-analysis-comparison/02_UnderstandingInputSelectivity_ICML2025.pdf`
**预计阅读**: 2 天
**核心问题**: Mamba 的选择性机制在数学上意味着什么？

**阅读重点**:
- S6 层与 Haar 小波投影的关系
- 逼近不连续函数: S6 vs S4D 的优势
- 记忆容量分析: 固定状态大小能记住多少信息
- 关联召回 (associative recall) 能力

### 4.3 Mamba 局限性 — COPY 和 CoT
**论文**: `4-analysis-comparison/03_ExploringLimitationsMamba_EMNLP2025.pdf`
**预计阅读**: 1-2 天
**核心问题**: Mamba 在哪些任务上根本性不如 Transformer？

**阅读重点**:
- COPY 任务: 固定状态 SSM 无法精确复制长序列
- CoT 推理: SSM 在多步推理中的瓶颈
- 状态大小 vs 序列长度: 状态增长时效率优势消失
- 对视觉任务的启示: 视觉中的 "COPY" 等价任务是什么

### 4.4 ReMamba — 长序列 Mamba 增强
**论文**: `4-analysis-comparison/04_ReMamba_EMNLP2025.pdf`
**预计阅读**: 1 天
**核心问题**: 如何在不引入 attention 的前提下增强 Mamba 的长序列能力？

**阅读重点**:
- 再处理 (reprocessing) 机制
- 全局信息的选择性重读
- 与 Transformer 长序列能力的对比
- 对视觉长序列的启示

### 4.5 SSM 可解释性 — 激活子空间瓶颈
**论文**: `4-analysis-comparison/05_InterpretingSteeringSSM_ICML2026.pdf`
**预计阅读**: 2 天
**核心问题**: SSM 内部的信息流存在怎样的瓶颈？能否通过干预改善？

**阅读重点**:
- Mechanistic interpretability 方法在 SSM 上的应用
- 激活子空间瓶颈的发现
- 测试时干预 (steering) 方法
- 7 个 SSM 模型上平均提升 8.27%
- 与 Transformer 可解释性工作的对比

### 4.6 Mamba-3 — 复数状态空间
**论文**: `4-analysis-comparison/06_Mamba3_ICLR2026.pdf`
**预计阅读**: 2 天 ⚠️ **最新前沿**
**核心问题**: 复数状态转移能否突破实数 SSM 的表达瓶颈？

**阅读重点**:
- 复数状态转移矩阵 A ∈ C^{N×N}
- 改进的离散化方案
- 模拟卷积的新方法
- 推理效率的进一步提升
- 与 Mamba-1/2 的对比

### 4.7 Log-Linear Attention — 注意力新范式
**论文**: `4-analysis-comparison/07_LogLinearAttention_ICLR2026.pdf`
**预计阅读**: 1 天
**核心问题**: 对数线性复杂度的注意力能否成为 SSM 的替代/补充？

**阅读重点**:
- 对数线性复杂度: O(N log N)
- 与线性注意力和标准注意力的关系
- 与 SSM 的复杂度对比
- 在视觉任务中的潜在应用

---

## 学习策略建议

### 通用阅读方法
1. **第一遍快速浏览** (30 分钟): 读 Abstract, Introduction, 结论, 看图表
2. **第二遍理解核心** (2-3 小时): 重点关注 Method 部分，理解关键公式和设计选择
3. **第三遍深入细节** (按需): 复现关键实验，验证论文声明
4. **做笔记**: 每篇论文记录 ① 核心创新 ② 设计选择 ③ 局限性 ④ 与其他论文的关系

### 代码实践建议
- Mamba 官方代码: https://github.com/state-annels/mamba
- Vim 官方代码: https://github.com/hustvl/Vim
- VMamba 官方代码: https://github.com/MzeroMiko/VMamba
- 建议在 ImageNet-1K 上复现 Vim-T 或 VMamba-T 的训练

### 论文关系图
```
HiPPO (2020)
  └── S4 (2022) ─── S4ND (2022) ← 视觉最早尝试
        │              │
        │         How to Train HiPPO (2023)
        │              │
        └── Mamba (2023) ──┐
              │             ├── Vim (2024) ← 双向扫描
              │             ├── VMamba (2024) ← 四方向扫描
              │             ├── LocalMamba (2024) ← 窗口扫描
              │             ├── 2DMamba (2024) ← 2D 状态空间
              │             ├── QuadMamba (2024) ← 自适应扫描
              │             ├── Demystify (2024) ← 理论分析
              │             ├── VSSD (2025) ← 非因果 SSD
              │             ├── MambaVL (2024) ← 跨模态
              │             └── HydraMamba (2025) ← 3D 点云
              │
        └── Mamba-2/SSD (2024) ── VSSD (2025)
              │
        └── Mamba-3 (2026) ← 复数状态
```
