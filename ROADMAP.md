# Forensics-Agent · 学习与项目打卡路线图

> 一个基于 LangGraph 的图像篡改检测 Agent 系统。把经典取证工具与 IMDL-BenCo 里的 SoTA 模型封装成 MCP 工具，由 Agent 自适应路由并融合，产出可溯源、可评测的证据化解释。
>
> 核心冲刺 14 周（约 3.5 个月），之后第 4 到 6 个月用于论文返修与求职。每天一行，做完把该行 `产出` 列的 ☐ 改成 ✅。

---

## 北极星目标

**项目最终形态（简历句）**

> Forensics-Agent — A LangGraph agent for image manipulation detection. Detection capabilities (ELA, noise residual, copy-move, and a SoTA IMDL-BenCo model) are exposed as MCP tools; the agent performs cost-aware tool routing with evidence-grounded reasoning, and ships with full tracing, structured-output guardrails, and a two-tier evaluation harness covering detection accuracy and agent-trajectory faithfulness.

**论文角度（诚实定位）**
- 贡献点 1：agentic 工具编排框架，把经典信号工具 + IMDL-BenCo SoTA 模型统一为 MCP 工具，做成本感知的自适应路由与证据融合。
- 贡献点 2（更值钱、更不拥挤）：针对取证 Agent 的**推理忠实度评测方法**，衡量解释是否真的 grounded 在工具输出与真实篡改区域，而非幻觉。
---

## 如何使用本表

- 每行是一个学习日，建议工作日 5 天推进，周末做缓冲与复盘。
- 节奏可调。你在做研究，若某周太紧，优先级是 **评测 > MCP > 可观测 > RAG**。
- 每完成一天，把 `产出 ☐` 改成 `产出 ✅`，并把当天产物 commit 到 repo。
- 卡住的知识点直接拿来和我沟通，我会按你的进度补讲或调整后面的安排。

**前置环境**：Python 3.11+、uv 或 conda、Gemini API key、A800（80G）+ RTX 3090（24G）。本地开源 VLM 用 vLLM 自托管，**优先 Qwen**。

---

## 模型与硬件策略（Qwen 优先）

Agent 的推理大脑用 Gemini（你已有，多模态强）。本地再用 vLLM 自托管一个开源 VLM，理由是省 eval 费、可复现、可微调、且是实打实的简历信号。开源侧**先用 Qwen**，许可 Apache 2.0，对开源 repo 和发论文都干净。

| 角色 | 模型 | 跑在哪 | 说明 |
|---|---|---|---|
| Agent 推理大脑（主力） | Gemini 2.5 Pro / Flash | API | Flash 跑量大的 eval，Pro 啃难例 |
| 本地开源 VLM（开源主力） | Qwen3-VL-30B-A3B 或 Qwen2.5-VL-32B（FP8/量化） | A800 80G | vLLM 起 OpenAI 兼容服务 |
| 快速迭代 + 检测模型 | Qwen2.5-VL-7B + IMDL-BenCo IML 模型 | 3090 24G | 小模型快迭代，IML 模型本就轻量 |

关键工程：agent 内部统一走 **OpenAI 兼容接口**，换 Gemini 还是本地 Qwen 只改一行配置。这样第 12 周能直接做一组「闭源 Gemini vs 开源 Qwen-VL」消融，回应审稿人对泛化性的质疑。

实操起步：先在 3090 上把 Qwen2.5-VL-7B 跑起来打通流程，再到 A800 上起 30B/32B 当主力。开源前沿基本每月在变，选定版本后**钉死 commit / 权重哈希**保证可复现。具体部署步骤见 Week 5 附加轨道。

---

## 阶段总览

| 阶段 | 周次 | 主题 | 关键产出 |
|---|---|---|---|
| Phase 0 | W1–W2 | 基础：LLM / Prompt / LangChain / RAG | 单工具检测 + 解释闭环 |
| Phase 1 | W3–W4 | LangGraph + 多工具 + 结构化融合 | 状态机式多步推理 |
| Phase 2 | W5–W6 | MCP 化 + 本地 Qwen-VL 服务 + 接入 IMDL-BenCo 模型 | 标准协议工具层 + 可切换模型 |
| Phase 3 | W7–W8 | 可观测性 + 可靠性 / guardrails | trace 可视化 + 健壮性 |
| Phase 4 | W9–W10 | FastAPI 服务化 + Docker 部署 | 可访问的在线 demo |
| Phase 5 | W11–W12 | 双层评测（检测 + Agent 轨迹） | 完整实验系统 |
| Phase 6 | W13–W14 | 论文初稿 + 开源 + 求职物料 | 投稿版 + repo v1.0 |

---

## Phase 0 · 基础闭环

### Week 1 · LLM 与 Prompt 基础
> 目标：跑通 LLM 调用，做出第一个「ELA → LLM 解释」闭环。

| 天 | 阅读材料 | 核心知识点 | 项目任务 | 产出 ☐ |
|---|---|---|---|---|
| D1 | 所用厂商官方 SDK quickstart（Anthropic / OpenAI / Qwen） | messages 结构、temperature、token、function calling 概念 | 搭环境，跑通首个 LLM 调用 | `hello_llm.py` ✅ |
| D2 | Anthropic Prompt Engineering 指南 | system / user / few-shot / CoT | 为「解释篡改证据」写 system prompt + few-shot | `prompts/v0` ☐ |
| D3 | JSON mode / Pydantic 文档 | 结构化输出、字段约束 | 让 LLM 输出 `{verdict, confidence, evidence}` | `schema.py` ☐ |
| D4 | VLM 多模态输入文档 | base64 图像输入、视觉 token | 把图像传给 VLM 做初步真伪描述 | `vlm_describe.py` ☐ |
| D5 | ELA / JPEG 重压缩资料（你领域） | ELA 原理、压缩痕迹 | 实现 ELA detector，输出 ELA map | `detectors/ela.py` + README v0 ☐ |

### Week 2 · LangChain 与 RAG / 向量库
> 目标：把闭环重写成 LangChain，并诚实判断 RAG 是否值得保留。

| 天 | 阅读材料 | 核心知识点 | 项目任务 | 产出 ☐ |
|---|---|---|---|---|
| D1 | LangChain LCEL 文档 | Runnable、LCEL、`Prompt \| LLM \| Parser` | 把 W1 闭环重写成 LCEL chain | `chain.py` ☐ |
| D2 | FAISS / Chroma 快速上手 | embedding、相似度、chunking | 用你的取证笔记 / 论文摘要建小知识库 | 索引构建脚本 ☐ |
| D3 | LangChain RAG 教程 | retriever、上下文注入 | 检索取证启发式知识为解释提供依据 | `rag_chain.py` ☐ |
| D4 | RAG 评估基础 | 检索命中率、答案相关性 | 对比有无 RAG 的解释质量 | 对比笔记（决定保留/精简/砍） ☐ |
| D5 | SRM / 噪声残差资料 | 噪声不一致性 | 实现第二个 detector：noise | `detectors/noise.py` + README v1 ☐ |

---

## Phase 1 · LangGraph 多步推理

### Week 3 · LangGraph 入门
> 目标：把流程改成状态机，让 LLM 决定调用哪个 detector。

| 天 | 阅读材料 | 核心知识点 | 项目任务 | 产出 ☐ |
|---|---|---|---|---|
| D1 | LangGraph 官方 docs quickstart + LangChain Academy | StateGraph、node、edge、state | 画出 agent 状态图设计 | 状态图设计（md） ☐ |
| D2 | LangGraph State 文档 | TypedDict / Pydantic state | 定义 State + decision/detector 两个 node | `graph.py` v0 ☐ |
| D3 | LangGraph 条件边文档 | conditional edge、路由 | 让 LLM 决定调用哪个 detector | 路由逻辑 ☐ |
| D4 | LangGraph 循环 / 多步 | 多步调用、循环终止条件 | detector → reasoning →（是否需更多证据）→ 再调 | 多步 graph ☐ |
| D5 | LangGraph checkpoint 文档 | 持久化、state logging | 记录每步 state | state 日志 + README v2 ☐ |

### Week 4 · 工具抽象与证据融合
> 目标：三个 detector 统一接口，做证据化融合输出。

| 天 | 阅读材料 | 核心知识点 | 项目任务 | 产出 ☐ |
|---|---|---|---|---|
| D1 | tool / function schema 设计资料 | 清晰描述、输入输出类型 | 把 3 个 detector 统一成 tool 接口 | `tools.py` ☐ |
| D2 | copy-move / JPEG ghost 资料 | 块匹配、双重压缩痕迹 | 实现第三个 detector：patch / copy-move | `detectors/patch.py` ☐ |
| D3 | evidence-based reasoning 资料 | 多证据综合、可溯源 | LLM 综合多 detector 输出给证据化判断 | reasoning node v2 ☐ |
| D4 | Pydantic 校验文档 | 输出校验、字段约束 | 输出 `{verdict, regions, evidence[], confidence}` 并校验 | `schema` v2 ☐ |
| D5 | — | 端到端联调 | 单图 → graph → 结构化解释 | demo 可跑 + README v3 ☐ |

---

## Phase 2 · MCP 化（核心差异点）

### Week 5 · 把检测器封装成 MCP 工具
> 目标：用 FastMCP 暴露工具，agent 通过 MCP 调用。

| 天 | 阅读材料 | 核心知识点 | 项目任务 | 产出 ☐ |
|---|---|---|---|---|
| D1 | modelcontextprotocol.io「Build an MCP server」 | resources / tools / prompts、FastMCP | 跑通官方示例 | 能跑的示例 ☐ |
| D2 | MCP Python SDK README | `@mcp.tool()`、类型提示生成 schema | 把 ELA 封成 MCP tool | `mcp_server.py` v0 ☐ |
| D3 | MCP Image / 返回类型文档 | Image 返回、多 tool 注册 | noise / patch 也封进 server | 完整 MCP server ☐ |
| D4 | langchain-mcp-adapters 文档 | MCP client、tool 发现 | LangGraph agent 经 MCP 调用工具 | MCP 接入 ☐ |
| D5 | MCP 生产实践（错误处理 / 校验 / 超时） | 结构化错误、Pydantic 输入校验 | 加固 server | README v4 + MCP 文档 ☐ |

### Week 5 · 附加轨道：本地 Qwen-VL 服务（vLLM）
> 与 MCP 并行推进，可占用本周周末缓冲。先在 3090 起小模型打通流程，再到 A800 起主力。

| 天 | 阅读材料 | 核心知识点 | 项目任务 | 产出 ☐ |
|---|---|---|---|---|
| A1 | vLLM 文档 + Qwen2.5-VL HF 模型卡 | OpenAI 兼容 `/v1`、多模态图像输入 | 3090 起 Qwen2.5-VL-7B，验证传图推理 | 本地 endpoint 跑通 ☐ |
| A2 | vLLM 多模态 / 量化文档 | `--max-model-len`、`--gpu-memory-utilization`、FP8 / AWQ | A800 起 Qwen3-VL-30B-A3B 或 Qwen2.5-VL-32B | 主力 VLM 服务 ☐ |
| A3 | — | provider 抽象、模型可切换 | agent 加一层 model 配置，一行切 Gemini / 本地 Qwen | 可切换配置 + 同图双模型对比笔记 ☐ |

### Week 6 · 接入 IMDL-BenCo SoTA 模型作为「重武器」
> 目标：把高精度 IML 模型也变成工具，做分层成本感知路由。

| 天 | 阅读材料 | 核心知识点 | 项目任务 | 产出 ☐ |
|---|---|---|---|---|
| D1 | IMDL-BenCo github + arXiv:2406.10580 | 模块化 codebase、评测协议 | 跑通一个预训练 SoTA IML 模型推理 | benco 推理脚本 ☐ |
| D2 | IMDL-BenCo 模型库文档 | pixel-level mask 输出 | 把一个 SoTA IML 模型封成 MCP tool | `detectors/benco_tool` ☐ |
| D3 | 成本感知路由资料 | 轻量信号工具 vs 重型模型 | agent 分层调用（先轻后重） | 路由 v2 ☐ |
| D4 | region grounding 资料 | 解释绑定具体区域 | reasoning 引用 mask 证据 | reasoning v3 ☐ |
| D5 | — | 中期演示 | 整周联调 + 录 demo | demo 视频/gif + README v5 ☐ |

---

## Phase 3 · 可观测性与可靠性

### Week 7 · 可观测性（招聘硬信号）
> 目标：全链路 trace，README 能放真实执行图。

| 天 | 阅读材料 | 核心知识点 | 项目任务 | 产出 ☐ |
|---|---|---|---|---|
| D1 | LangSmith 或 Langfuse 接入文档 | tracing、span、session | 接一个可观测平台，跑出全链路 trace | trace 接入 ☐ |
| D2 | 平台 agent 可视化文档 | 执行图、state diff | 可视化 agent 执行图 | trace 截图入 README ☐ |
| D3 | 自定义 span / metadata 文档 | 自定义埋点 | 记录 tool 耗时、token、调用次数 | metrics ☐ |
| D4 | annotation / dataset 文档 | 失败用例归集 | 收集失败 case 建错误集 | failure set ☐ |
| D5 | — | 文档化 | 整理可观测说明 | `docs/observability.md` ☐ |

### Week 8 · 可靠性 / guardrails
> 目标：从「研究 demo」升级为「工程系统」。

| 天 | 阅读材料 | 核心知识点 | 项目任务 | 产出 ☐ |
|---|---|---|---|---|
| D1 | 重试 / 降级模式资料 | tool 失败 fallback、重试 | 工具失败时降级处理 | retry 逻辑 ☐ |
| D2 | Pydantic 校验 + 修复 | 结构化输出强校验 | schema 守卫 + 失败重试 | validator ☐ |
| D3 | 「CoT 不忠实」资料（unfaithful reasoning） | 幻觉、证据可溯源 | evidence 必须可溯源到 tool 输出 | grounding check ☐ |
| D4 | 输入安全资料 | 恶意 / 超大输入处理 | input guard | `guards.py` ☐ |
| D5 | — | 文档化 | 可靠性测试集 + 文档 | `docs/reliability.md` + README v6 ☐ |

---

## Phase 4 · 服务化与部署

### Week 9 · FastAPI 服务化
| 天 | 阅读材料 | 核心知识点 | 项目任务 | 产出 ☐ |
|---|---|---|---|---|
| D1 | FastAPI 官方教程 | async、Pydantic models、依赖注入 | `POST /analyze` 骨架 | `app.py` ☐ |
| D2 | FastAPI 响应模型文档 | 响应模型、错误码 | 接入 agent，返回结果 + 推理轨迹 | 可调用 API ☐ |
| D3 | SSE / streaming 文档 | 流式返回 | 流式返回推理步骤 | streaming ☐ |
| D4 | 简单前端资料 | 上传 / 展示 | demo 页（上传图 → 看证据） | static demo ☐ |
| D5 | — | 文档化 | API 文档 + curl 示例 | `docs/api.md` ☐ |

### Week 10 · Docker 部署
| 天 | 阅读材料 | 核心知识点 | 项目任务 | 产出 ☐ |
|---|---|---|---|---|
| D1 | Dockerfile 最佳实践 | 镜像分层、依赖固定 | 容器化 | `Dockerfile` ☐ |
| D2 | docker-compose 文档 | 多服务编排 | api + MCP server + 可观测 一起编排 | `compose` ☐ |
| D3 | 配置 / secrets 资料 | env、密钥管理 | 配置化 | config ☐ |
| D4 | HF Spaces / Render / Fly 部署文档 | 部署目标选型 | 上线一个公开实例 | 公开 URL ☐ |
| D5 | — | 冒烟测试 | 端到端测试 + 架构图 | 架构图 + 可访问 demo + README v7 ☐ |

---

## Phase 5 · 双层评测（研究与求职核心）

### Week 11 · 第一层 · 检测性能
| 天 | 阅读材料 | 核心知识点 | 项目任务 | 产出 ☐ |
|---|---|---|---|---|
| D1 | IMDL-BenCo 评测协议文档 | pixel F1、AUC、image-level | batch 评测脚本 | `eval_detection.py` ☐ |
| D2 | 标准数据集（CASIA / NIST16 等）文档 | 协议一致性 | agent vs 单模型 baseline | 结果表 v0 ☐ |
| D3 | 鲁棒性评测资料 | JPEG / resize / noise 扰动 | robustness 评测 | 鲁棒性表 ☐ |
| D4 | 绘图（matplotlib / seaborn） | 结果可视化 | 画表与图 | figures ☐ |
| D5 | 实验管理资料 | seed、config、版本 | 实验记录规范 | `experiments/` + 记录 ☐ |

### Week 12 · 第二层 · Agent 轨迹与解释忠实度
| 天 | 阅读材料 | 核心知识点 | 项目任务 | 产出 ☐ |
|---|---|---|---|---|
| D1 | agent 评测资料 | 工具选择正确率、步数、路由效率 | trajectory 指标 | `eval_agent.py` ☐ |
| D2 | 解释忠实度 / faithfulness 资料 | 解释是否 grounded 在工具输出与真实 region | faithfulness metric | faithfulness eval ☐ |
| D3 | LLM-as-judge 资料 | judge prompt、与人工对齐 | LLM-as-judge 评解释质量 | judge pipeline ☐ |
| D4 | 回归测试资料 | prompt / 模型变更回归 | 回归测试集 | regression suite ☐ |
| D5 | — | 分析 | 汇总全部实验 → 结果分析 | 完整结果 + 分析笔记 ☐ |

---

## Phase 6 · 论文与求职物料

### Week 13 · 论文初稿
| 天 | 阅读材料 | 核心知识点 | 项目任务 | 产出 ☐ |
|---|---|---|---|---|
| D1 | FakeShield / ForgeryGPT / ForgerySleuth / Agent4FaceForgery | 差异点定位 | related work + gap 表 | gap 表 ☐ |
| D2 | — | 方法呈现 | 方法章：编排 + MCP 工具层 + 证据化推理 | method draft ☐ |
| D3 | — | 实验呈现 | 实验章：两层评测 | experiments draft ☐ |
| D4 | — | 动机与贡献 | 引言 + 贡献点 + 摘要 | intro / abstract ☐ |
| D5 | — | 作图 | 系统架构图 + 主图 | figures ☐ |

### Week 14 · 打磨 · 开源 · 求职
| 天 | 阅读材料 | 核心知识点 | 项目任务 | 产出 ☐ |
|---|---|---|---|---|
| D1 | — | 自查 | 论文 internal review | 论文 v2 ☐ |
| D2 | 目标 workshop / 期刊 CFP | 格式化、投稿要求 | 确定投稿目标并格式化 | 投稿版 ☐ |
| D3 | 优秀 repo README 范例 | 可复现性、demo、badges | repo 最终打磨 | 发布 v1.0 ☐ |
| D4 | — | 技术叙事 | 简历项目描述 + 技术博客 | 简历段 + 博客 ☐ |
| D5 | — | 面试准备 | agent / MCP / eval / RAG 八股 + 项目深问 | 面试笔记 ☐ |

---

## 第 4 到 6 个月 · 收尾与求职（粗粒度）

- 论文返修与补实验，按 reviewer / 自评意见迭代。
- 可选扩展，提升话题度：multi-agent 编排、A2A 协议、更多数据集与跨域泛化。
- 系统性刷 agent 方向面试题，按周做 mock。
- 海投 + 复盘，每次面试后回填面试笔记。

---

## 资源附录（已核对）

**MCP**
- Build an MCP server: https://modelcontextprotocol.io/docs/develop/build-server
- 官方 Python SDK: https://github.com/modelcontextprotocol/python-sdk

**LangChain / LangGraph**
- LangGraph 官方文档与 LangChain Academy（免费课程）
- LangChain LCEL 文档

**你领域的基准与相关工作**
- IMDL-BenCo（NeurIPS'24 Spotlight）: https://github.com/scu-zjz/IMDLBenCo ｜ arXiv:2406.10580
- FakeShield（ICLR'25）: https://github.com/zhipeixu/FakeShield
- ForgeryGPT: arXiv:2410.10238
- ForgerySleuth: arXiv:2411.19466
- Agent4FaceForgery: arXiv:2509.12546

**可观测 / 评测**
- LangSmith（与 LangGraph 原生集成最省事）｜ Langfuse / Arize Phoenix（开源自托管）

**工程**
- FastAPI 官方教程 ｜ Pydantic 文档 ｜ Docker 最佳实践

**本地模型服务**
- vLLM 官方文档（OpenAI 兼容服务 + 多模态）
- Qwen2.5-VL / Qwen3-VL Hugging Face 模型卡（Apache 2.0，含官方 FP8 版本）
- 选型实时参考：Artificial Analysis 开源榜（每月变动，钉版本保可复现）

---

## 风险与调整

- 14 周排满偏紧，尤其你同时在做研究。卡壳时优先保 **评测 > MCP > 可观测 > RAG**。
- RAG 若做成玩具反而减分，W2-D4 要诚实决定保留还是砍。
- 论文别撞「又一个会解释的 MLLM」，守住「agentic 编排 + 忠实度评测」这个差异点。
- 每周末来对一次进度，我据此调整后面的安排与补讲知识点。
