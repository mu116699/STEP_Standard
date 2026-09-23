# STEP ARM / AIM 中文速查资料集

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

> **本目录是一个完全独立的资料集，与任何宿主项目无关。**
> 目录内所有脚本、数据、文档均自包含（仅依赖 Python 标准库），
> 可整体复制到任意位置、任意仓库或独立仓库中运行，无需任何外部依赖或配置。

本目录保存对 STEP Tools 官方 **ARM（应用参考模型）概念图** 与 **AIM（应用解释模型）集成定义图** 的完整解析结果。

* ARM 来源页面：<https://www.steptools.com/stds/stp_expg/arm.html>（Updated 2022-02-23 with SMRLv9 update）
* AIM 来源页面：<https://www.steptools.com/stds/stp_expg/aim.html>（Updated 2022-02-25 with SMRLv9 updates）
* AIM EXPRESS 源码：<https://www.steptools.com/stds/stp_aim/html/>（`step_merged_ap_schema`，含 TYPE / ENTITY / RULE / FUNCTION）
* 抓取/生成日期：2026-09-22（AIM）/ 2026-09-23（ARM）

---

## 一、STEP 是什么？ARM 与 AIM 又是什么？

### 1.1 STEP（ISO 10303）

STEP（**St**andard for the **E**xchange of **P**roduct model data，产品模型数据交换标准）是国际标准化组织（ISO）发布的 **ISO 10303** 系列标准，用于**数字化地表示和交换产品信息**。

* **目标**：让不同 CAD / CAM / CAE / PDM 系统之间能够无损地交换三维模型、装配结构、公差标注（PMI）、制造工艺等信息，摆脱对特定厂商私有格式的依赖。
* **核心应用协议（AP）**：
  * **AP203**：面向航空航天 / 国防的配置控制三维设计数据交换（已被 AP242 取代）。
  * **AP214**：面向汽车行业的机械设计数据交换（已被 AP242 取代）。
  * **AP242**：**Managed Model-Based 3D Engineering**，2014 年发布，是当前 CAD 数据导入 / 导出的首选协议，整合了 AP203e2 与 AP214，并新增 PMI、装配、增材制造等能力。
  * **AP238**：**STEP-NC**，面向数控加工的工艺信息模型，描述刀具路径、加工特征、工步等。
* **文件格式**：最常用的是 **Part 21**（`.stp` / `.step` 文本文件），另有 Part 28（XML）、Part 21 Edition 3（支持压缩与 UTF-8）等。
* **数据访问接口**：**SDAI**（Standard Data Access Interface，ISO 10303-22）。

### 1.2 ARM 与 AIM：同一标准的两种视图

STEP 用 **EXPRESS** 语言定义数据模型。同一个应用协议（如 AP242）通常提供两种互补的模型视图：

| 视图 | 全称 | 面向对象 | 特点 |
| --- | --- | --- | --- |
| **ARM** | Application Reference Model（应用参考模型） | **工程人员** | 用「工件、工作计划、产品形状」等**高层业务概念**描述需求，贴近人的理解 |
| **AIM** | Application Interpreted Model（应用解释模型） | **软件实现者** | 把 ARM 概念**映射 / 解释**为可实现的 EXPRESS 实体与属性，是文件实际存储的结构 |

* **ARM → AIM 的映射**由标准中的「解释（interpretation）」规则定义；一个 ARM 概念往往对应多个 AIM 实体。
* 本目录同时收录两者的官方图解析结果：
  * **ARM 概念图**（`STEP-ARM-概念全表-中文速查.md`）：**1523** 个高层概念，按 **182** 个应用模块组织。
  * **AIM 集成定义图**（`STEP-AIM-实体全表-中文速查.md`）：**1461** 个 EXPRESS 实体，按 schema 分组。

> 简单记：**ARM 是「人话」，AIM 是「机器话」**；ARM 便于沟通需求，AIM 决定文件里到底存了什么。

### 1.3 STEP Tools 官方提供的三种资料

STEP Tools 在 AP242 页面（<https://www.steptools.com/stds/step/index.html>）上并列提供了三种互补的资料，分别面向不同读者、解决不同问题：

| 资料 | 链接 | 面向对象 | 内容与用途 |
| --- | --- | --- | --- |
| **ARM: Concepts Diagram**<br>（应用参考模型 · 概念图） | <https://www.steptools.com/stds/stp_expg/arm.html> | 工程人员、需求方 | 用**高层业务概念**（工件、工作计划、产品形状、加工特征……）及其关系描述「这个标准能表达什么」。适合**理解业务语义、沟通需求、做数据映射规划**。本目录解析为 `STEP-ARM-概念全表-中文速查.md`。 |
| **AIM: Integrated Definitions Diagrams**<br>（应用解释模型 · 集成定义图） | <https://www.steptools.com/stds/stp_expg/aim.html> | 软件实现者、数据工程师 | 把 ARM 概念**解释为可实现的 EXPRESS 实体与属性**，并画出实体之间的引用关系（定义框 + 属性引用框）。适合**理解文件实际结构、编写读写器、排查数据问题**。本目录解析为 `STEP-AIM-实体全表-中文速查.md`。 |
| **AIM EXPRESS Text**<br>（AIM 的 EXPRESS 源码文本） | <https://www.steptools.com/stds/stp_aim/html/> | 编译器 / 工具开发者 | 由 STEP Tools 的 **EXPRESS to HTML Converter** 生成的**完整 EXPRESS schema 源码**（`step_merged_ap_schema`），逐条列出 `TYPE` / `ENTITY` / `RULE` / `FUNCTION` 定义。适合**生成代码、做 schema 校验、精确查阅某实体的属性与约束**。 |

**三者关系一句话总结**：

```
ARM（概念图）  ──解释/映射──▶  AIM（集成定义图）  ──序列化──▶  AIM EXPRESS Text（源码）
   人话                          结构图                        可编译的正式定义
```

* **ARM 概念图**回答「**要表达什么**」；
* **AIM 集成定义图**回答「**这些概念在数据模型里长什么样、彼此怎么引用**」；
* **AIM EXPRESS Text** 回答「**精确的语法定义是什么**」（属性类型、可选性、WHERE 规则、函数体）。

> 本目录目前完整解析了前两种（ARM 概念图、AIM 集成定义图）。
> 第三种（EXPRESS 源码）是纯文本 schema，可直接在浏览器中按实体名检索，无需额外解析。

---

## 二、目录内容

| 文件 | 内容 |
| --- | --- |
| `STEP-ARM-概念全表-中文速查.md` | **ARM 主文档**。总览、182 个 ARM 模块索引、按模块分类的 1523 个概念（含中文名与官方定义链接）、**按应用领域 / 使用者 / 产品生命周期功能环节三维分类**、STEP-NC（AP238）应用对象、引用次数 Top 30 |
| `STEP-AIM-实体全表-中文速查.md` | **AIM 主文档**。统计总览、尺寸/公差/基准专题、**按工业用途 / 软件模块 / 产品生命周期功能环节三维分类**、1461 个实体（按 EXPRESS schema 分组，含中文名与官方定义链接）、虚线框附录、术语表 |
| `step-NURBS.md` | **专题文档**。曲线 / 曲面 / 体实体全解，NURBS 在 STEP 中的定义、裁剪（trimming）机制、T-spline 与局部细化样条 |
| `STEP-ARM-概念全表-中文速查.pdf` | ARM 主文档的 **PDF 版**（240 页），已内置 **210 个目录书签**（按标题层级） |
| `STEP-AIM-实体全表-中文速查.pdf` | AIM 主文档的 **PDF 版**（262 页），已内置 **287 个目录书签**（按标题层级） |
| `step-NURBS.pdf` | NURBS 专题文档的 **PDF 版**（26 页），已内置 **65 个目录书签**（按标题层级） |
| `arm_concepts.csv` | 1523 个 ARM 概念的精简表（中文名、英文名、模块、来源、引用次数、定义链接） |
| `arm_modules.csv` | 182 个 ARM 模块索引（模块名 + 概念数） |
| `arm_industry.csv` | 1302 个 AP242 概念的**应用领域分类索引**（航空 / 汽车 / 造船 / 机械 / 电气 / 通用） |
| `arm_users.csv` | 1302 个 AP242 概念的**使用者分类索引**（领域专家 / 工程师 / 标准制定者） |
| `arm_lifecycle.csv` | 1302 个 AP242 概念的**产品生命周期功能环节分类索引**（CAD / CAM / CAE / PDM / CAPP / 检测质量） |
| `arm_concepts.json` | ARM 原始解析结果（概念、引用框） |
| `aim_boxes_all_3974.csv` | AIM 图上全部 **3974** 个框的明细（1461 实体定义框 + 2513 属性引用框） |
| `aim_entities.csv` | 1461 个实体定义的精简表（含「图中引用次数」） |
| `aim_dash_types.csv` | 328 个虚线框：95 个 DEFINED TYPE + 233 个 SELECT / 抽象超类型 |
| `aim_domains.csv` | 1461 个实体的**领域分类索引**（工业用途 13 类 / 软件模块 14 类） |
| `aim_lifecycle.csv` | 1461 个实体的**产品生命周期功能环节分类索引**（CAD / CAM / CAE / CAPP / PDM / CMM / 工程图 / 通用） |
| `aim_entities.json` | AIM 原始解析结果（实体、引用框索引、匿名框） |
| `LICENSE` | **MIT 许可证**（本目录的脚本、文档、数据均适用） |
| `scripts/` | 可复现的生成脚本（见下） |

### `scripts/` 脚本清单

| 脚本 | 作用 | 输入 | 输出 |
| --- | --- | --- | --- |
| `extract_arm.py` | 解析 ARM 概念图 SVG，提取全部概念框 | `scripts/arm.html`（缺失时自动下载） | `arm_concepts.json` |
| `gen_arm_doc.py` | 生成 ARM 主文档与 CSV | `arm_concepts.json` | `STEP-ARM-概念全表-中文速查.md` + 5 个 CSV |
| `extract_aim.py` | 解析 AIM 页面 SVG，提取全部实体框 | `scripts/aim.html`（缺失时自动下载） | `aim_entities.json` |
| `extract_dash_types.py` | 提取虚线框（DEFINED TYPE / SELECT） | `scripts/aim.html` | `scripts/aim_dashtypes.json` |
| `glossary.py` | 构词术语表（842 条）+ 人工译名覆盖 | — | 被 `gen_aim_doc.py` / `gen_arm_doc.py` 导入 |
| `domains.py` | AIM 分类规则（工业用途 13 类 / 软件模块 14 类 / 功能环节 7 类） | — | 被 `gen_aim_doc.py` 导入；可独立自检 |
| `arm_domains.py` | ARM 三维分类规则（应用领域 5 类 / 使用者 3 类 / 功能环节 6 类） | — | 被 `gen_arm_doc.py` 导入；可独立自检 |
| `gen_aim_doc.py` | 生成 AIM 主文档与全部 CSV | `aim_entities.json`、`aim_dashtypes.json` | `STEP-AIM-实体全表-中文速查.md` + 5 个 CSV |
| `check_geom_doc.py` | 校验专题文档引用的实体名 | `step-NURBS.md`、`aim_entities.json`、`aim_dash_types.csv` | 控制台报告 |
| `add_pdf_bookmarks.py` | 为 PDF 添加目录书签（outline）：从同名 Markdown 解析标题层级，按**行**（y 坐标聚类）+ 行内最大字号在 PDF 中定位标题所在页，写入书签树 | `<markdown>`、`<pdf>` | 就地更新 `<pdf>`（重建书签） |

---

## 三、运行环境

* **Python 3.8+**（脚本仅使用标准库：`re` / `json` / `os` / `csv` / `collections` / `urllib`，**无需 pip 安装任何第三方包**）。
* 首次运行 `extract_arm.py` / `extract_aim.py` 需要**联网**下载对应页面（各约 1.7 MB）；之后离线即可。
* 若在 Windows 控制台运行且需正确显示中文，建议设置 `PYTHONIOENCODING=utf-8`。

> 本目录**不依赖**任何虚拟环境、任何宿主项目路径或任何配置文件。
> 使用系统 `python` 或任意 Python 解释器均可。

---

## 四、完整运行流程（从零重建全部产物）

在**本目录**（`STEP_Standard/`）下执行：

```powershell
# ===== ARM（应用参考模型）=====
# 1) 解析 ARM 概念图 → arm_concepts.json（首次会自动下载 arm.html）
python scripts/extract_arm.py

# 2) （可选）ARM 三维分类自检：打印各维度未命中概念数
python scripts/arm_domains.py

# 3) 生成 ARM 主文档 + 5 个 CSV
python scripts/gen_arm_doc.py

# ===== AIM（应用解释模型）=====
# 4) 解析 AIM 页面 → aim_entities.json（首次会自动下载 aim.html）
python scripts/extract_aim.py

# 5) 提取虚线框 → scripts/aim_dashtypes.json
python scripts/extract_dash_types.py

# 6) （可选）领域分类自检：打印未命中实体数
python scripts/domains.py

# 7) 生成 AIM 主文档 + 全部 CSV
python scripts/gen_aim_doc.py

# 8) （可选）校验 step-NURBS.md 专题文档中的实体名
python scripts/check_geom_doc.py

# 9) （可选）为三个 PDF 添加目录书签（需先安装 pypdf）
python scripts/add_pdf_bookmarks.py "STEP-ARM-概念全表-中文速查.md" "STEP-ARM-概念全表-中文速查.pdf"
python scripts/add_pdf_bookmarks.py "STEP-AIM-实体全表-中文速查.md" "STEP-AIM-实体全表-中文速查.pdf"
python scripts/add_pdf_bookmarks.py "step-NURBS.md" "step-NURBS.pdf"
```

Linux / macOS 下把 `python` 换成 `python3` 即可，命令完全相同。

### 一键脚本（可选）

Windows PowerShell：

```powershell
$env:PYTHONIOENCODING = "utf-8"
python scripts/extract_arm.py
python scripts/gen_arm_doc.py
python scripts/extract_aim.py
python scripts/extract_dash_types.py
python scripts/gen_aim_doc.py
```

Linux / macOS：

```bash
export PYTHONIOENCODING=utf-8
python3 scripts/extract_arm.py
python3 scripts/gen_arm_doc.py
python3 scripts/extract_aim.py
python3 scripts/extract_dash_types.py
python3 scripts/gen_aim_doc.py
```

### PDF 目录书签

三个 PDF（`STEP-ARM-概念全表-中文速查.pdf`、`STEP-AIM-实体全表-中文速查.pdf`、`step-NURBS.pdf`）已内置**目录书签（PDF outline）**，在阅读器侧边栏可直接按标题层级跳转。

书签由 `scripts/add_pdf_bookmarks.py` 生成，原理：

1. 从同名 Markdown 解析 1~4 级标题（得到干净的标题文本与层级）；
2. 在 PDF 中按**行**识别标题：先按 y 坐标把文本片段聚成行，再取该行**最大字号**判定层级
   （`36`=一级、`28`=二级、`24`=三级、`20`=四级），得到每个标题所在页；
3. 两者按顺序对齐后，用 `pypdf` 写入书签树。

> **为何按行而不是按字号连续段**：标题里可能含行内代码（如 `5.1 曲线裁剪：`trimmed_curve``），
> 行内代码字号是正文的 0.85 倍（h3 标题里为 `20.4`、h4 标题里为 `17.0`），
> 会把一个标题拆成多个不同字号的片段；按行聚类后取最大字号即可正确还原。
>
> 该脚本需要第三方库 `pypdf`（其余脚本仅用标准库）：`pip install pypdf`。
> 脚本会先丢弃 PDF 已有书签再重建，因此**可重复运行**，不会叠加。
> 若 Markdown 重新生成后 PDF 也重新导出，重跑上述命令即可刷新书签。
> 注意：运行前请先关闭正在阅读该 PDF 的程序，否则 Windows 下会因文件被占用而写入失败。

---

## 五、刷新 / 更新

### 5.1 官方页面更新后刷新

当 STEP Tools 更新 ARM / AIM 页面（页面版本号变化）时：

1. **删除旧缓存**：删除 `scripts/arm.html` / `scripts/aim.html`（强制重新下载最新页面）。
2. 重新执行第四节的完整流程。
3. 用 `check_geom_doc.py` 校验专题文档，若报出「缺失」实体名，说明官方新增/改名了实体，需同步更新 `step-NURBS.md`。

### 5.2 只改译名（不动数据）

中文名由 `scripts/glossary.py` 的 `TOKENS`（构词表）与 `OVERRIDES`（人工覆盖）组合生成：

* **AIM**：编辑 `scripts/glossary.py` 的 `OVERRIDES`，重跑 `python scripts/gen_aim_doc.py`。
* **ARM**：编辑 `scripts/gen_arm_doc.py` 的 `ARM_TOKENS` / `ARM_OVERRIDES`，重跑 `python scripts/gen_arm_doc.py`。

两者均无需重新抓取。

### 5.3 只改分类规则（AIM）

分类规则集中在 `scripts/domains.py` 的 `INDUSTRY` / `SOFTWARE` / `LIFECYCLE`（正则规则）
与 `EXTRA_INDUSTRY` / `EXTRA_SOFTWARE` / `EXTRA_LIFECYCLE`（精确名补充）：

1. 编辑 `scripts/domains.py`。
2. 运行 `python scripts/domains.py` 自检，查看各维度「未命中」数量。
3. 重跑 `python scripts/gen_aim_doc.py`。

### 5.4 只改分类规则（ARM）

ARM 的三维分类规则集中在 `scripts/arm_domains.py` 的 `INDUSTRY` / `USERS` / `LIFECYCLE`（正则规则）：

1. 编辑 `scripts/arm_domains.py`。
2. 运行 `python scripts/arm_domains.py` 自检，查看各维度「未分类」数量。
3. 重跑 `python scripts/gen_arm_doc.py`。

### 5.5 只改排版 / 章节结构

编辑 `scripts/gen_aim_doc.py` 或 `scripts/gen_arm_doc.py` 后重跑即可。

---

## 六、数量关系

```
【ARM 概念图】
概念定义框 1523  +  概念引用框 1999  =  3522
其中：AP242 ARM 模块概念 1302（182 个模块）
      AP238 STEP-NC 应用对象 220
      其他资源概念 1

【AIM 集成定义图】
实体定义框 1461  +  属性引用框 2513  =  3974   ← 页面上「3974 个实体框」
另有虚线框 328（DEFINED TYPE 95 + SELECT/抽象超类型 233）
```

---

## 七、ARM 模块分类体系

ARM 主文档按 **182 个应用模块（module）** 对 1302 个 AP242 概念分类，概念数最多的模块：

| 模块 | 概念数 | 说明 |
| --- | ---: | --- |
| `machining_features` | 147 | 加工特征（孔、槽、倒角、阵列等） |
| `kinematic_structure` | 54 | 运动学结构（关节、连杆、轴） |
| `numeric_expression` | 42 | 数值表达式 |
| `value_with_unit_extension` | 37 | 带单位量值扩展 |
| `geometric_tolerance` | 35 | 几何公差 |
| `tessellated_geometry` | 25 | 网格化几何 |
| `basic_geometry` | 24 | 基本几何 |
| `characteristic` | 23 | 特性 |
| `mechanical_design_features_and_requirements` | 23 | 机械设计特征与要求 |
| `dimension_tolerance` | 22 | 尺寸公差 |

完整模块索引见 `STEP-ARM-概念全表-中文速查.md` 第二节与 `arm_modules.csv`。

### 7.1 三维分类（应用领域 / 使用者 / 功能环节）

除按模块分类外，ARM 主文档第四~六节还从三个正交维度对 1302 个 AP242 概念细分：

* **应用领域（5 类 + 通用）**：航空 / 航天、汽车 / 车辆、造船 / 船舶、机械 / 装备制造、电气 / 电子 / 物理量；未命中者归入「通用 / 跨行业」。
* **使用者（3 类）**：领域专家（业务 / 管理）、工程师（几何 / 工艺 / 公差）、标准制定者（元模型 / 表达 / 库）。
* **产品生命周期功能环节（6 类 + 通用）**：CAD（设计 / 建模 / 制图）、CAM（制造 / 加工）、CAE（分析 / 仿真）、PDM（产品数据管理）、CAPP（工艺规划）、检测 / 质量（PMI / 计量）；未命中者归入「通用 / 基础」。

分类规则集中在 `scripts/arm_domains.py`，一个概念可同时命中多个类别（多标签），故各类别计数之和大于概念总数。对应索引见 `arm_industry.csv` / `arm_users.csv` / `arm_lifecycle.csv`。

---

## 八、AIM 分类体系

AIM 主文档第三部分按三个维度对全部实体分类，便于按用途查找：

* **工业用途 / 工科分类（13 类）**：NC 数控加工、机械/运动学、电力/物理量、渲染/外观、几何/拓扑、公差/尺寸/基准（PMI）、制图/标注、产品/配置/数据管理、表达式/数学、增材制造、扫描/点云、材料/表面条件、特征/加工特征。
* **软件模块 / 设计理念（14 类）**：2D 绘图/草图、3D 建模/实体造型、制图/工程图、渲染/可视化、装配/结构、运动学/仿真、制造/工艺规划、检测/PMI、数据管理/配置、元模型/表示框架、类型系统/选择机制、外部引用/代理机制、属性/特征化、有效性/版本。
* **产品生命周期功能环节（7 类 + 通用）**：CAD（设计 / 建模 / 实体造型）、CAM（制造 / 加工 / 数控）、CAE（分析 / 仿真 / 运动学）、CAPP（工艺规划 / 工序 / 资源）、PDM（产品数据管理 / 配置）、CMM（检测 / 计量 / PMI）、工程图（制图 / 标注 / 图纸）；未命中者归入「通用 / 基础」。

分类规则集中在 `scripts/domains.py`，对 1461 个实体实现 **100% 覆盖**（无遗漏）。一个实体可同时命中多个类别（多标签），故各类别计数之和大于实体总数。对应索引见 `aim_domains.csv`（工业用途 / 软件模块）与 `aim_lifecycle.csv`（功能环节）。

---

## 九、关于中文名

* 中文名由 `scripts/glossary.py` 中的 **842 条构词术语表** 自动组合生成，并对尺寸/公差/基准、几何、度量、表达式函数等重点概念做了人工译名覆盖。
* ARM 概念名（如 `Unary_function_call`）按下划线切分后查表拼接，另有 `gen_arm_doc.py` 的 ARM 专用补充译名。
* 自动组合结果**仅作检索提示**，工程使用请以英文实体名 / 概念名与 SMRL 官方定义为准。
* 若发现译名不妥，直接修改 `glossary.py` 的 `OVERRIDES`（AIM）或 `gen_arm_doc.py` 的 `ARM_OVERRIDES`（ARM）后重跑对应生成脚本即可。

---

## 十、关于「空间尺寸标注」

AIM 图中**没有**名为「空间尺寸标注」的实体。与尺寸相关的内容分两族：

* **3D 空间尺寸（语义尺寸 / PMI）** → `shape_dimension_schema` 族（`dimensional_size`、`dimensional_location`、`shape_dimension_representation` 等）；
* **2D 图纸尺寸标注** → `draughting_*` / `aic_draughting_elements` 族（`dimension_callout`、`linear_dimension`、`radius_dimension` 等）。

注意 `coordinate_space_dimension` **不是实体**，它是 `geometric_representation_context.dimension_count` 的属性名（坐标空间维数）。

---

## 十一、校验与质量保证

| 校验项 | 方法 | 期望结果 |
| --- | --- | --- |
| AIM 领域分类覆盖 | `python scripts/domains.py` | 未命中工业用途 = 0，未命中软件模块 = 0 |
| AIM 主文档内部锚点 | 见下方脚本片段 | 失效链接 = 0，重复锚点 = 0 |
| ARM 主文档内部锚点 | 见下方脚本片段（改文件名） | 失效链接 = 0，重复锚点 = 0 |
| 专题文档实体名 | `python scripts/check_geom_doc.py` | 报出的「缺失」项应全部是属性名 / 枚举值 / 函数名（非实体），无真正的实体名缺失 |

主文档内部跳转锚点采用与 GitHub 完全一致的算法
（小写 → 去标点 → 每个空格替换为 `-` → URL 编码）：

* AIM 主文档：已校验 261 条内部链接全部有效、无重复锚点。
* ARM 主文档：已校验 182 条内部链接全部有效、无重复锚点。

锚点自检脚本片段（可另存为 `scripts/check_anchors.py`，把文件名换成目标文档即可）：

```python
import re, urllib.parse, collections

def anchor(t):
    t = t.strip().lower()
    t = re.sub(r"[^\w\s\-]", "", t)
    return urllib.parse.quote(t.replace(" ", "-"))

txt = open("STEP-AIM-实体全表-中文速查.md", encoding="utf-8").read()
heads = collections.Counter(anchor(m.group(2))
                            for m in re.finditer(r"^(#{1,6})\s+(.*)$", txt, re.M))
links = re.findall(r"\]\(#([^)]+)\)", txt)
bad = [l for l in links if l not in heads]
print("标题数:", len(heads), "内部链接数:", len(links), "失效:", len(bad))
print("重复锚点:", [k for k, v in heads.items() if v > 1])
```

---

## 十二、常见问题

**Q：脚本报 `FileNotFoundError: aim.html` / `arm.html`？**
A：`extract_aim.py` / `extract_arm.py` 会自动下载；若下载失败（网络/SSL 问题），手动把
<https://www.steptools.com/stds/stp_expg/aim.html> 保存为 `scripts/aim.html`、
<https://www.steptools.com/stds/stp_expg/arm.html> 保存为 `scripts/arm.html` 后重跑。

**Q：`extract_dash_types.py` 报找不到 `aim.html`？**
A：它依赖 `extract_aim.py` 下载的 `scripts/aim.html`，请先运行 `extract_aim.py`。

**Q：`gen_aim_doc.py` / `gen_arm_doc.py` 报找不到 JSON？**
A：请先运行对应的 `extract_aim.py` / `extract_arm.py`。

**Q：ARM 和 AIM 有什么区别？**
A：ARM 是面向工程人员的高层概念模型（人话），AIM 是面向软件实现的 EXPRESS 实体模型（机器话），
详见第一节。

**Q：ARM 概念图、AIM 集成定义图、AIM EXPRESS Text 三者该看哪个？**
A：想理解「标准能表达什么业务概念」看 **ARM 概念图**；想理解「数据模型里实体怎么组织、怎么互相引用」看 **AIM 集成定义图**；
想查「某实体的精确属性类型、可选性、WHERE 规则、函数体」看 **AIM EXPRESS Text**。详见第 1.3 节。

**Q：控制台中文乱码？**
A：设置 `PYTHONIOENCODING=utf-8`（仅影响控制台显示，文件本身始终为 UTF-8）。

**Q：能否把本目录整体搬到别处？**
A：可以。所有脚本使用相对路径（基于脚本自身位置），目录整体移动后无需任何修改即可运行。

---

## 十三、许可（License）

本目录采用 **MIT 许可证**，完整文本见 [`LICENSE`](./LICENSE)。

```
MIT License

Copyright (c) 2026 tianheju

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**中文要点**（仅供参考，以英文原文为准）：

* 允许**自由使用、复制、修改、合并、发布、分发、再许可、销售**本目录内容；
* 唯一条件是**保留版权声明与许可声明**；
* 软件按「**原样**」提供，**不提供任何担保**，作者不承担任何索赔或损害责任。

> ⚠️ **适用范围说明**：MIT 许可仅覆盖**本目录作者原创的部分**（解析脚本、生成的中文文档、
> CSV / JSON 数据、PDF 排版与书签等）。
> 目录中引用的 **ISO 10303（STEP）标准文本、EXPRESS schema 定义、STEP Tools 官方图表**
> 版权归各自权利人所有，不在本许可授权范围内；引用时请遵守原权利人的使用条款。

---

*本目录依据 ISO 10303（STEP）系列标准、STEP Tools 官方 ARM 概念图与 AIM 集成定义图整理。*
*自动组合的中文名仅作检索提示，工程使用请以英文实体名 / 概念名与标准定义为准。*
