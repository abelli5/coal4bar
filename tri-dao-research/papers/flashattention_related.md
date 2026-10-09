# FlashAttention 相关论文清单

> 包含 FlashAttention 系列原始论文及引用/扩展工作
> 按研究方向分类整理

---

## 一、FlashAttention 系列原始论文

| # | 论文 | 作者 | 会议/年份 | arXiv | 核心贡献 |
|---|------|------|-----------|-------|---------|
| 1 | FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness | Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, Christopher Ré | NeurIPS 2022 | 2205.14135 | IO-aware 精确注意力，分块计算+重计算，内存 O(N²)→O(N)，A100 上 2-4x 加速 |
| 2 | FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning | Tri Dao | ICLR 2024 | 2307.08691 | 改进工作划分，减少非 matmul FLOPs，跨线程块并行，A100 上达理论 50-73% |
| 3 | FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision | Jay Shah, Ganesh Bikshandi, Ying Zhang, Vijay Thakkar, Pradeep Ramani, Tri Dao | NeurIPS 2024 | 2407.08608 | 面向 Hopper 架构，warp specialization + 异步 + FP8，H100 上达理论 75% (740 TFLOPs/s) |
| 4 | FlashAttention-4: Algorithm and Kernel Pipelining Co-design for Asymmetric Hardware Scaling | Ted Zadouri, Markus Hoehnerbach, Jay Shah, et al., Tri Dao | MLSys 2026 | — | 面向 Blackwell 架构，算法+内核流水线协同设计，TMA + FP8/FP4 |

## 二、基于 FlashAttention 内核的扩展与变体

| # | 论文 | 作者 | 会议/年份 | 核心贡献 |
|---|------|------|-----------|---------|
| 1 | FlashMask: Efficient and Rich Mask Extension of FlashAttention | Guangxuan Xiao, Yuandong Tian, Beidi Chen, Song Han, Mike Lewis | ICLR 2025 | 扩展 FlashAttention 支持复杂掩码（padding、图像/视频掩码） |
| 2 | FlexAttention: A Programming Model for Generating Optimized Attention Kernels | Juechu Dong, Boyuan Feng, Driss Guessous, Yanbo Liang, Horace He | arXiv 2024 | 面向注意力变体的编程模型，结合 PyTorch 与 FA 内核思想 |
| 3 | FlashMLA: Efficient MLA Decoding Kernel | DeepSeek 团队 | 2025 | 面向 MLA 推理，结合 FA 的硬件感知分块与异步优化 |
| 4 | Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention | Jingyang Yuan, Huazuo Gao, et al. | ACL 2025 Best Paper | 硬件对齐且可原生训练的稀疏注意力 |
| 5 | Scaling Attention via Feature Sparsity (FlashSFA) | Yan Xie, Tiansheng Wen, et al. | ICLR 2026 | IO-aware 的 FlashSFA 内核，稀疏注意力扩展 |

## 三、线性注意力与硬件加速

| # | 论文 | 作者 | 会议/年份 | 核心贡献 |
|---|------|------|-----------|---------|
| 1 | Gated Linear Attention Transformers with Hardware-Efficient Training (FlashLinearAttention) | Songlin Yang, Bailin Wang, Yikang Shen, Rameswar Panda, Yoon Kim | ICML 2024 | FlashLinearAttention，硬件高效训练线性注意力 |
| 2 | FLA: A Triton-Based Library for Hardware-Efficient Implementations of Linear Attention | Songlin Yang, Yu Zhang | 2024 | Triton 实现库，为线性注意力/RNN 提供硬件高效内核 |
| 3 | Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths | Zhen Qin, Weigao Sun, et al. | arXiv 2024 | 长序列建模的 Lightning Attention，硬件友好实现 |
| 4 | Tiled Flash Linear Attention: More Efficient Linear RNN and xLSTM Kernels | Maximilian Beck, Korbinian Pöppel, Phillip Lippe, Sepp Hochreiter | arXiv 2025 | 分块优化 Flash Linear Attention，提升线性 RNN 与 xLSTM 效率 |

## 四、SSM 与注意力交叉方向

| # | 论文 | 作者 | 会议/年份 | 核心贡献 |
|---|------|------|-----------|---------|
| 1 | Mamba: Linear-Time Sequence Modeling with Selective State Spaces | Albert Gu, Tri Dao | COLM 2024 | 选择性 SSM，线性时间序列建模 |
| 2 | Transformers are SSMs (Mamba-2) | Tri Dao, Albert Gu | ICML 2024 | SSD 框架，SSM 与注意力的理论对偶 |
| 3 | Gated Delta Networks: Improving Mamba2 with Delta Rule | Songlin Yang, Jan Kautz, Ali Hatamizadeh | ICLR 2025 | 改进 Mamba2 的 delta rule |
| 4 | Retentive Network (RetNet) | Yutao Sun, Li Dong, et al. | arXiv 2023 | 结合并行训练与低开销推理的高效序列建模 |
| 5 | Log-Linear Attention | Han Guo, Songlin Yang, et al. | ICLR 2026 | 对数线性复杂度注意力 |

## 五、其他高效注意力机制

| # | 论文 | 作者 | 会议/年份 | 核心贡献 |
|---|------|------|-----------|---------|
| 1 | GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints | Joshua Ainslie, et al. | EMNLP 2023 | 分组查询注意力，减少 KV-cache |
| 2 | RACE Attention: Strictly Linear-Time Attention for Outrageously Large Contexts | Sahil Joshi, et al. | arXiv 2025 | 严格线性时间复杂度注意力 |
| 3 | Scaling Laws for Linear Complexity Language Models | Xuyang Shen, et al. | EMNLP 2024 | 线性复杂度语言模型的缩放规律 |

## 六、综述性文章

| # | 文章 | 来源 | 年份 | 说明 |
|---|------|------|------|------|
| 1 | Efficient Attention Mechanisms for Large Language Models: A Survey | arXiv | 2025 | 系统综述高效注意力机制 |
| 2 | The End of Transformers? On Challenging Attention and the Rise of Sub-Quadratic Architectures | arXiv | 2025 | 讨论 FA 等 GPU 优化注意力对 Transformer 的挑战 |
| 3 | The Evolution of FlashAttention | ICLR BlogPosts | 2026 | 综述 FlashAttention v1-v4 演进 |
| 4 | FlashAttention: From IO-Awareness to Hardware Specialization: A Comparative Literature Review | 台北大学 | 2025 | FA 从 IO-aware 到硬件专用化的文献综述 |

---

## FlashAttention 演进路线图

```
FlashAttention (2022, NeurIPS)
  └── IO-aware 分块计算 + 重计算
  └── A100: 25-40% 理论 FLOPs
       │
FlashAttention-2 (2023, ICLR)
  └── 更好的并行 + 工作划分
  └── A100: 50-73% 理论 FLOPs
       │
FlashAttention-3 (2024, NeurIPS)
  └── Hopper 架构: warp specialization + 异步 + FP8
  └── H100: 75% 理论 FLOPs (740 TFLOPs/s)
       │
FlashAttention-4 (2026, MLSys)
  └── Blackwell 架构: 算法+内核流水线协同设计
  └── TMA + FP8/FP4
```

## 生态扩展方向

```
FlashAttention 核心思想 (IO-aware, 分块计算)
  ├── 扩展: FlashMask (复杂掩码)
  ├── 编程模型: FlexAttention
  ├── 线性注意力: FlashLinearAttention, FLA
  ├── 稀疏注意力: Native Sparse Attention, FlashSFA
  ├── MLA 解码: FlashMLA
  └── SSM 交叉: Mamba-2/SSD, Gated Delta Networks
```
