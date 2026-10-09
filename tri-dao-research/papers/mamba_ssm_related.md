# Mamba / SSM 相关论文清单

> 包含 S4/HiPPO/Mamba 系列原始论文及引用/扩展工作
> 按研究主题分类整理

---

## 一、理论基础：HiPPO 与 S4

| # | 论文 | 作者 | 会议/年份 | arXiv | 核心贡献 |
|---|------|------|-----------|-------|---------|
| 1 | HiPPO: Recurrent Memory with Optimal Polynomial Projections | Albert Gu, Tri Dao, Stefano Ermon, Atri Rudra, Christopher Ré | NeurIPS 2020 | 2008.07669 | HiPPO 框架，最优多项式投影记忆机制，为 S4 提供理论基础 |
| 2 | S4: Efficiently Modeling Long Sequences with Structured State Spaces | Albert Gu, Karan Goel, Christopher Ré | ICLR 2022 | 2111.00396 | 结构化状态空间序列模型，高效建模长期依赖 |
| 3 | How to Train Your HiPPO: State Space Models with Generalized Orthogonal Basis Projections | Albert Gu, Isys Johnson, Aman Timalsina, Atri Rudra, Christopher Ré | ICLR 2023 | 2206.13737 | 广义正交基投影，系统化 HiPPO 框架 |

## 二、Mamba 系列

| # | 论文 | 作者 | 会议/年份 | arXiv | 核心贡献 |
|---|------|------|-----------|-------|---------|
| 1 | Mamba: Linear-Time Sequence Modeling with Selective State Spaces | Albert Gu*, Tri Dao | COLM 2024 (Outstanding Paper) | 2312.00752 | 选择性 SSM (S6)，输入依赖的状态转移，线性时间复杂度，去除注意力/MLP 的端到端 SSM 架构 |
| 2 | Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality (Mamba-2) | Tri Dao, Albert Gu | ICML 2024 | 2405.21060 | SSD 框架，SSM 与注意力对偶理论；Mamba-2 支持更大状态维度 (N=64/256)，训练速度比 Mamba-1 快 2-8x |
| 3 | Mamba-3: Improved Sequence Modeling using State Space Principles | Aakash Lahoti, Kevin Li, Berlin Chen, et al., Tri Dao, Albert Gu | ICLR 2026 | 2603.15569 | 复数值状态转移，改进离散化过程，推理效率进一步提升 |

### Mamba 核心创新

```
HiPPO (2020) — 多项式投影记忆
    │
S4 (2022) — 结构化状态空间，高效长序列建模
    │
Mamba / S6 (2023) — 选择性 SSM，输入依赖状态转移
    ├── 选择性: B, C, Δ 由输入决定
    ├── 全局卷积: 训练时并行计算
    ├── 线性时间: O(N) 复杂度
    └── 简化架构: 去除 attention/MLP
         │
Mamba-2 / SSD (2024) — 状态空间对偶理论
    ├── SSM ↔ Attention 理论联系
    ├── 更大状态维度 (N=64→256+)
    └── 训练速度 2-8x 加速
         │
Mamba-3 (2026) — 复数状态转移
    ├── 改进离散化
    └── 推理效率优化
```

## 三、视觉领域扩展

| # | 论文 | 作者 | 会议/年份 | 核心贡献 |
|---|------|------|-----------|---------|
| 1 | Vision Mamba (Vim): Efficient Visual Representation Learning with Bidirectional State Space Model | Lianghui Zhu, Bencheng Liao, Qian Zhang, et al. | ICML 2024 | 双向 SSM 用于视觉任务，ImageNet/COCO/ADE20K |
| 2 | VMamba: Visual State Space Model | Yue Liu, Yunjie Tian, Yuzhong Zhao, et al. | NeurIPS 2024 | 1D→2D 扩展，解决视觉空间局部性 |
| 3 | QuadMamba: Learning Quadtree-based Selective Scan for Visual State Space Model | Fei Xie, Weijia Zhang, Zhongdao Wang, Chao Ma | NeurIPS 2024 | 四叉树自适应选择性扫描，保留 2D 空间局部性 |
| 4 | LocalMamba: Visual State Space Model with Windowed Selective Scan | Tao Huang, Xiaohuan Pei, Shan You, Fei Wang | ECCV 2024 | 窗口化选择性扫描，处理图像局部空间结构 |
| 5 | 2DMamba: Efficient State Space Model for Image Representation | Jingwei Zhang, Anh Tien Nguyen, et al. | CVPR 2024 | 2D 空间结构引入 Mamba，用于超大病理切片分类 |
| 6 | VSSD: Visual State Space Duality | — | ICCV 2025 | 视觉角度扩展 SSD，非因果化 SSD |
| 7 | Selective Visual Prompting in Vision Mamba | Yifeng Yao, Zichen Liu, et al. | arXiv 2024 | 选择性视觉提示，微调中激活 update/forget gates |
| 8 | S4ND: Modeling Images and Videos as Multidimensional Signals with State Spaces | Evan Nguyen, et al., Tri Dao, et al. | NeurIPS 2022 | 多维信号的状态空间建模 |

## 四、NLP 与语言模型

| # | 论文 | 作者 | 会议/年份 | 核心贡献 |
|---|------|------|-----------|---------|
| 1 | Jamba: A Hybrid Transformer-Mamba Language Model | Opher Lieber, Barak Lenz, et al. (AI21 Labs) | arXiv 2024 | Transformer-Mamba 混合 + MoE，52B 总参/12B 活跃，256K 上下文 |
| 2 | An Empirical Study of Mamba-based Language Models | NVIDIA Research | 2024 | 8B 参数 Mamba/Mamba-2/Transformer/Hybrid 对比，纯 SSM 在复制/ICL/长上下文推理仍有差距 |
| 3 | ReMamba: Equip Mamba with Effective Long-Sequence Modeling | Danlong Yuan, Jiahao Liu, et al. | Findings of EMNLP 2025 | 增强 Mamba 长序列理解能力 |
| 4 | Mamba Retriever: Utilizing Mamba for Effective and Efficient Dense Retrieval | — | arXiv 2024 | Mamba 用于稠密检索任务 |

## 五、理论与可解释性

| # | 论文 | 作者 | 会议/年份 | 核心贡献 |
|---|------|------|-----------|---------|
| 1 | Understanding Input Selectivity in Mamba: Impact on Approximation Power, Memorization, and Associative Recall Capacity | Ningyuan Huang, et al. | ICML 2025 | S6 层可表示 Haar 小波投影，逼近不连续函数优于 S4D |
| 2 | Exploring the Limitations of Mamba in COPY and CoT Reasoning | Ruifeng Ren, Zhicong Li, Yong Liu | EMNLP 2025 | Mamba 在 COPY 和 CoT 推理中的局限性分析 |
| 3 | Demystify Mamba in Vision: A Linear Attention Perspective | D. Han, Z. Wang, et al. | NeurIPS 2024 | 线性注意力视角分析 Vision Mamba，揭示设计差异 |
| 4 | Interpreting and Steering State-Space Models via Activation Subspace Bottlenecks | — | OpenReview 2025 | mechanistic interpretability 工具识别 SSM 激活子空间瓶颈，平均提升 8.27% |

## 六、跨模态与多领域应用

| # | 论文 | 作者 | 会议/年份 | 核心贡献 |
|---|------|------|-----------|---------|
| 1 | Caduceus: Bi-directional Equivariant Long-Range DNA Sequence Modeling | Yair Schiff, et al., Tri Dao, et al. | ICML 2024 | 双向等变长程 DNA 序列建模 |
| 2 | Mamba Fusion: Learning Actions Through Questioning | — | arXiv 2024 | MambaVL，选择性 SSM 模态融合，视觉-语言长程依赖 |
| 3 | HydraMamba: Multi-Head State Space Model for Global Point Cloud Learning | — | ACM MM 2025 | 多头部 SSM 用于全局点云学习 |

## 七、系统与训练优化

| # | 论文 | 作者 | 会议/年份 | 核心贡献 |
|---|------|------|-----------|---------|
| 1 | Characterizing the Behavior of Training Mamba-based State Space Models on GPUs | Trinayan Baruah, et al. | arXiv 2025 | Mamba 类 SSM 在 GPU 上的训练行为分析 |

## 八、Mamba vs Transformer 对比研究

| # | 论文 | 对比维度 | 核心结论 |
|---|------|----------|---------|
| 1 | An Empirical Study of Mamba-based Language Models (2024) | 8B 参数大规模训练 | 纯 SSM 在多数任务匹配/超过 Transformer，但复制/ICL/长上下文推理仍有差距 |
| 2 | Demystify Mamba in Vision (2024) | 线性注意力视角 | Vision Mamba 可视为线性注意力变体，设计差异在于 gate/normalization/head 数量 |
| 3 | Exploring the Limitations of Mamba in COPY and CoT (2025) | 理论任务分析 | 固定大小 Mamba 难以完成某些 COPY；状态大小随序列增长时效率优势下降 |
| 4 | ReMamba (2025) | 长上下文效率 | Mamba 长序列效率优于 Transformer，但理解能力需增强 |
| 5 | Mamba-2 / SSD (2024) | 理论对偶 | SSM 与注意力存在形式化对偶关系，统一两种视角 |
| 6 | Understanding Input Selectivity (2025) | 函数逼近/记忆 | S6 逼近不连续函数优于 S4D，Haar 小波投影 |

---

## SSM 研究生态全景

```
理论基础层
  ├── HiPPO (2020) — 多项式投影记忆
  ├── S4 (2022) — 结构化状态空间
  └── How to Train Your HiPPO (2023) — 广义正交基
       │
核心模型层
  ├── Mamba / S6 (2023) — 选择性 SSM
  ├── Mamba-2 / SSD (2024) — 状态空间对偶
  └── Mamba-3 (2026) — 复数状态转移
       │
应用扩展层
  ├── 视觉: Vim, VMamba, QuadMamba, LocalMamba, 2DMamba, VSSD
  ├── NLP: Jamba (混合), ReMamba, Mamba Retriever
  ├── 生物: Caduceus (DNA)
  ├── 跨模态: MambaVL, HydraMamba (点云)
  └── 系统优化: GPU 训练行为分析
       │
理论分析层
  ├── 选择性理解: Input Selectivity (ICML 2025)
  ├── 局限性分析: COPY/CoT, 长上下文
  ├── 统一视角: Linear Attention Perspective
  └── 可解释性: Activation Subspace Bottlenecks
```
