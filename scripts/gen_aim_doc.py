# -*- coding: utf-8 -*-
"""生成 STEP AIM 实体全表文档（Markdown + CSV）。"""
import json
import os
import re
import sys
import csv
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glossary import TOKENS, OVERRIDES
from domains import (INDUSTRY, SOFTWARE, LIFECYCLE,
                     industry_of, software_of, lifecycle_of)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.dirname(HERE)
DATA = os.path.join(OUT_DIR, "aim_entities.json")
SRC_PAGE = "https://www.steptools.com/stds/stp_expg/aim.html"

TOKENS.setdefault("extruded", "拉伸")
TOKENS.setdefault("extrusion", "拉伸")

PDF_GROUP = {
    "ISO_13584-20": "ISO 13584-20 通用表达式逻辑模型",
    "ISO_10303-50": "ISO 10303-50 数学构造",
    "ISO_10303-49": "ISO 10303-49 加工特征",
}
PDF_FALLBACK = "ISO 10303-5xx 应用解释模型"


def gh_anchor(text):
    """按 GitHub 规则生成标题锚点（保留中日韩字符，去掉 ASCII 标点）。

    GitHub 的算法：转小写 -> 删除除「字母/数字/下划线/连字符/空格」外的字符
    -> 每个空格替换为一个连字符（**不合并**连续连字符）。
    """
    import urllib.parse
    t = text.strip().lower()
    t = re.sub(r"[^\w\s\-]", "", t)
    t = t.replace(" ", "-")
    return urllib.parse.quote(t)


def tr(name):
    """实体名 -> 中文名"""
    if name in OVERRIDES:
        return OVERRIDES[name]

    parts = name.split("_")
    if len(parts) == 1:
        return TOKENS.get(name, name)

    for sep, fmt in (
        ("_with_", lambda l, r: "带%s的%s" % (tr(r), tr(l))),
        ("_and_", lambda l, r: "%s与%s" % (tr(l), tr(r))),
        ("_in_", lambda l, r: "%s中的%s" % (tr(r), tr(l))),
        ("_on_", lambda l, r: "%s上的%s" % (tr(r), tr(l))),
        ("_to_", lambda l, r: "%s到%s" % (tr(l), tr(r))),
        ("_for_", lambda l, r: "用于%s的%s" % (tr(r), tr(l))),
        ("_about_", lambda l, r: "绕%s的%s" % (tr(r), tr(l))),
    ):
        i = name.rfind(sep)
        if i > 0:
            return fmt(name[:i], name[i + len(sep):])

    if name.endswith("_defined_by_curves"):
        return "由曲线定义的%s" % tr(name[:-len("_defined_by_curves")])
    if name.endswith("_defined_by_nodes"):
        return "由节点定义的%s" % tr(name[:-len("_defined_by_nodes")])
    if "_of_" in name:
        i = name.rfind("_of_")
        return "%s的%s" % (tr(name[i + 4:]), tr(name[:i]))

    out = "".join(TOKENS.get(p, p) for p in parts)
    out = out.replace("的的", "的").strip("的")
    return out or name


SPECIAL_OVERRIDES = {
    "amount_of_substance_measure_with_unit": "物质的量（带单位）",
    "amount_of_substance_unit": "物质的量单位",
    "centre_of_symmetry": "对称中心",
    "surface_of_linear_extrusion": "线性拉伸曲面",
    "surface_of_revolution": "回转曲面",
    "class_by_extension": "按外延定义的类",
    "class_by_intension": "按内涵定义的类",
    "presentation_style_by_context": "由上下文决定的表示样式",
    "integer_interval_from_min": "以最小值为界的整数区间",
    "integer_interval_to_max": "以最大值为界的整数区间",
    "real_interval_from_min": "以最小值为界的实数区间",
    "real_interval_to_max": "以最大值为界的实数区间",
    "make_from_usage_option": "由用法选项确定的制造",
    "single_property_is_definition": "单一属性即定义",
    "comparison_not_equal": "不等于比较",
    "context_dependent_over_riding_styled_item": "上下文相关的覆盖样式项",
    "hidden_element_over_riding_styled_item": "隐藏元素的覆盖样式项",
    "link_motion_representation_along_path": "沿路径的链接运动表示",
    "all_around_shape_aspect": "全周形状要素",
    "characterized_item_within_representation": "表示内的被特征化项",
    "product_as_planned": "计划产品（product as planned）",
    "right_to_usage_association": "权限到用法关联",
    "product_planned_to_realized": "计划产品到已实现产品",
    "product_design_to_individual": "产品设计到个体",
    "product_design_version_to_individual": "产品设计版本到个体",
    "annotation_to_annotation_leader_line": "标注到标注的指引线",
}
OVERRIDES.update(SPECIAL_OVERRIDES)

# 尺寸 / 公差 / 基准 专题分组
TOPIC = collections.OrderedDict([
    ("专题 1：3D 空间尺寸（shape_dimension_schema 族）", [
        "dimensional_size", "dimensional_size_with_path", "dimensional_size_with_datum_feature",
        "dimensional_location", "dimensional_location_with_path", "dimensional_location_with_datum_feature",
        "directed_dimensional_location", "dimensional_characteristic_representation",
        "shape_dimension_representation", "shape_dimension_representation_item",
    ]),
    ("专题 2：2D 图纸尺寸标注（draughting / aic_draughting_elements 族）", [
        "dimension_callout", "dimension_callout_relationship", "dimension_callout_component_relationship",
        "structured_dimension_callout", "angular_dimension", "linear_dimension", "ordinate_dimension",
        "radius_dimension", "diameter_dimension", "curve_dimension", "leader_directed_dimension",
        "dimension_curve", "dimension_curve_directed_callout", "dimension_curve_terminator",
        "dimension_curve_terminator_to_projection_curve_associativity", "dimension_text_associativity",
        "dimension_pair", "dimension_count", "dimension_extent_usage", "pre_defined_dimension_symbol",
        "externally_defined_dimension_definition", "dimension_tolerance",
    ]),
    ("专题 3：公差（shape_tolerance_schema）", [
        "geometric_tolerance", "geometric_tolerance_relationship", "geometric_tolerance_with_datum_reference",
        "geometric_tolerance_with_modifiers", "geometric_tolerance_with_defined_unit",
        "geometric_tolerance_with_defined_area_unit", "geometric_tolerance_with_maximum_tolerance",
        "geometric_tolerance_auxiliary_classification", "modified_geometric_tolerance",
        "unequally_disposed_geometric_tolerance", "flatness_tolerance", "straightness_tolerance",
        "roundness_tolerance", "cylindricity_tolerance", "line_profile_tolerance",
        "surface_profile_tolerance", "angularity_tolerance", "parallelism_tolerance",
        "perpendicularity_tolerance", "position_tolerance", "concentricity_tolerance",
        "symmetry_tolerance", "circular_runout_tolerance", "total_runout_tolerance",
        "plus_minus_tolerance", "tolerance_value", "tolerance_value_or_limits_and_fits",
        "tolerance_zone", "tolerance_zone_form", "tolerance_zone_definition",
        "tolerance_zone_with_datum", "directed_tolerance_zone", "oriented_tolerance_zone",
        "geometrical_tolerance_callout", "pre_defined_geometrical_tolerance_symbol",
        "dimension_related_tolerance_zone_element",
    ]),
    ("专题 4：基准（shape_aspect_definition_schema / datum_and_datum_systems_mim）", [
        "datum", "datum_feature", "datum_system", "datum_target", "datum_reference",
        "datum_reference_compartment", "datum_reference_element",
        "datum_reference_modifier_with_value", "general_datum_reference",
        "referenced_modified_datum", "datum_feature_callout", "datum_target_callout",
        "common_datum", "placed_datum_target_feature", "feature_for_datum_target_relationship",
    ]),
])

data = json.load(open(DATA, encoding="utf-8"))
entities = data["entities"]
refs = data["references"]
dash = json.load(open(os.path.join(HERE, "aim_dashtypes.json"), encoding="utf-8"))
SELECT_TYPES = set(dash["select"])
DEFINED_TYPES = set(dash["defined_type"])
MODULE_NAMES = {"dimension_tolerance": "模块名（ISO 10303 dimension_tolerance 模块），非实体"}


def kind_of(name):
    if name in MODULE_NAMES:
        return MODULE_NAMES[name]
    if name in DEFINED_TYPES:
        return "DEFINED TYPE（图中虚线框）"
    if name in SELECT_TYPES:
        return "SELECT / 抽象超类型（图中虚线框）"
    return "图中仅作为选择列表成员出现，无独立定义框"

ref_count = collections.Counter(r["name"] for r in refs)
by_name = collections.OrderedDict()
for e in entities:
    by_name.setdefault(e["name"], e)

topic_names = {n for _, lst in TOPIC.items() for n in lst}

# 分组：schema -> [entity]
groups = collections.defaultdict(list)
for name, e in sorted(by_name.items()):
    key = e["schema"]
    if not key:
        pdf = e["url"].rsplit("/", 1)[-1]
        key = next((v for k, v in PDF_GROUP.items() if pdf.startswith(k)), PDF_FALLBACK)
    groups[key].append(e)

# ---------- 校验 ----------
untr = sorted({p for n in by_name for p in n.split("_")
               if p not in TOKENS and n not in OVERRIDES and len(n.split("_")) > 1})
print("未覆盖 token:", untr)
print("定义实体:", len(by_name), "| 引用框:", len(refs), "| 分组:", len(groups))


def link(e):
    return "[定义](%s)" % e["link"]


def row(i, e):
    cn = tr(e["name"])
    star = " ⭐" if e["name"] in topic_names else ""
    return "| %d | `%s` | %s%s | %d | %s |" % (
        i, e["name"], cn, star, ref_count.get(e["name"], 0), link(e))


lines = []
A = lines.append

A("# STEP AIM 集成定义实体全表（中文速查）")
A("")
A("> **本目录为完全独立的资料集，与任何宿主项目无关。** 所有脚本仅依赖 Python 标准库，")
A("> 可整体复制到任意位置独立运行。运行与刷新方法见同目录 `README.md`。")
A("")
A("> **数据来源**：STEP Integrated Definitions（AIM 图） — <https://www.steptools.com/stds/stp_expg/aim.html>  ")
A("> **页面版本**：Updated 2022-02-25 with SMRLv9 updates  ")
A("> **文档生成日期**：2026-09-22  ")
A("> **解析方式**：直接解析该页内嵌 SVG（1.73 MB），提取全部带超链接的实体框与引用框。")
A("")
A("## 一、统计总览")
A("")
A("| 项目 | 数量 | 说明 |")
A("| --- | ---: | --- |")
A("| 图上实体/引用框总数 | **%d** | 页面 SVG 中所有带超链接的方框 |" % (len(entities) + len(refs)))
A("| 实体定义框（唯一实体） | **%d** | 带 `xlink:title=\"definition\"`，链接到 SMRL 定义页 |" % len(entities))
A("| 属性引用框（`4, 82, xxx` 形式） | **%d** | 上级实体的属性槽指向某实体的引用，含 %d 个唯一实体名 |"
  % (len(refs), len(set(ref_count))))
A("| EXPRESS schema 分组 | **%d** | 含 PDF 形式链接的 ISO 分部 |" % len(groups))
A("| 尺寸/公差/基准相关实体 ⭐ | **%d** | 见第二节专题 |" % len(topic_names & set(by_name)))
A("| 虚线框：DEFINED TYPE | **%d** | 附录 A |" % len(DEFINED_TYPES))
A("| 虚线框：SELECT / 抽象超类型 | **%d** | 附录 B |" % len(SELECT_TYPES))
A("")
A("> 读写约定：`实体定义框 + 属性引用框 = %d + %d = %d`，即页面上「3974 个实体框」的全部内容；"
  % (len(entities), len(refs), len(entities) + len(refs)))
A("> 另有 %d 个虚线框（DEFINED TYPE / SELECT 类型），见附录。" % (len(DEFINED_TYPES) + len(SELECT_TYPES)))
A("")

A("## 二、专题：空间尺寸标注 / 公差 / 基准")
A("")
A("> 图里**没有**名为「空间尺寸标注」的实体。AIM 中与尺寸相关的内容分两族：")
A("> * **3D 空间尺寸（语义尺寸 / PMI）** → `shape_dimension_schema` 族；")
A("> * **2D 图纸尺寸标注** → `draughting_*` / `aic_draughting_elements` 族。")
A("> 注意 `coordinate_space_dimension` 不是实体，它是 `geometric_representation_context.dimension_count` 的**属性名**（坐标空间维数）。")
A(">")
A("> 自动组合的中文名仅作检索提示，工程使用请以英文实体名与标准定义为准。")
A("")

for title, names in TOPIC.items():
    A("### %s" % title)
    A("")
    A("| # | 实体名 | 中文名 | 图中引用 | 链接 |")
    A("| ---: | --- | --- | ---: | --- |")
    k = 0
    for n in names:
        e = by_name.get(n)
        if e:
            k += 1
            A(row(k, e))
        else:
            A("| %d | `%s` | — | 0 | %s |" % (k + 1, n, kind_of(n)))
            k += 1
    A("")

# ---------- 领域分类索引 ----------
ind_index = collections.defaultdict(list)
sw_index = collections.defaultdict(list)
lc_index = collections.defaultdict(list)
for name, e in sorted(by_name.items()):
    for k in industry_of(name):
        ind_index[k].append(e)
    for k in software_of(name):
        sw_index[k].append(e)
    for k in lifecycle_of(name):
        lc_index[k].append(e)

A("## 三、全部实体（按工业用途 / 软件模块 / 功能环节分类）")
A("")
A("> 同一实体可同时属于多个类别（多标签）。分类依据实体名关键词 + 精确名补充表，")
A("> 定义见 `scripts/domains.py`。⭐ = 属于第二节的尺寸/公差/基准专题。")
A("")
A("### 3.1 按工业用途 / 工科分类")
A("")
A("| 类别 | 实体数 | 跳转 |")
A("| --- | ---: | --- |")
for k in INDUSTRY:
    A("| %s | %d | [查看](#%s) |" % (k, len(ind_index.get(k, [])), gh_anchor("3.1 " + k)))
A("")
for k in INDUSTRY:
    items = ind_index.get(k, [])
    A("#### 3.1 %s" % k)
    A("")
    A("共 %d 个实体。" % len(items))
    A("")
    A("| # | 实体名 | 中文名 | 图中引用 | 链接 |")
    A("| ---: | --- | --- | ---: | --- |")
    for i, e in enumerate(sorted(items, key=lambda x: x["name"]), 1):
        A(row(i, e))
    A("")

A("### 3.2 按软件模块 / 设计理念")
A("")
A("| 类别 | 实体数 | 跳转 |")
A("| --- | ---: | --- |")
for k in SOFTWARE:
    A("| %s | %d | [查看](#%s) |" % (k, len(sw_index.get(k, [])), gh_anchor("3.2 " + k)))
A("")
for k in SOFTWARE:
    items = sw_index.get(k, [])
    A("#### 3.2 %s" % k)
    A("")
    A("共 %d 个实体。" % len(items))
    A("")
    A("| # | 实体名 | 中文名 | 图中引用 | 链接 |")
    A("| ---: | --- | --- | ---: | --- |")
    for i, e in enumerate(sorted(items, key=lambda x: x["name"]), 1):
        A(row(i, e))
    A("")

A("### 3.3 按产品生命周期功能环节分类")
A("")
A("> 按实体在产品生命周期中所处的**功能环节**归类，覆盖从设计到检测的全过程：")
A("> **CAD**（设计 / 建模 / 实体造型）→ **CAE**（分析 / 仿真 / 运动学）→ "
  "**CAPP**（工艺规划 / 工序 / 资源）→ **CAM**（制造 / 加工 / 数控）→ "
  "**CMM**（检测 / 计量 / PMI）→ **PDM**（产品数据管理 / 配置）；"
  "**工程图**（制图 / 标注 / 图纸）贯穿设计—制造—检测全过程。")
A("> 未命中任何环节的实体（数学表达式、计量单位、类型系统等）归入「通用 / 基础」。")
A("")
LC_ORDER = list(LIFECYCLE.keys()) + ["通用 / 基础"]
A("| 环节 | 实体数 | 跳转 |")
A("| --- | ---: | --- |")
for k in LC_ORDER:
    A("| %s | %d | [查看](#%s) |" % (k, len(lc_index.get(k, [])), gh_anchor("3.3 " + k)))
A("")
for k in LC_ORDER:
    items = lc_index.get(k, [])
    A("#### 3.3 %s" % k)
    A("")
    A("共 %d 个实体。" % len(items))
    A("")
    A("| # | 实体名 | 中文名 | 图中引用 | 链接 |")
    A("| ---: | --- | --- | ---: | --- |")
    for i, e in enumerate(sorted(items, key=lambda x: x["name"]), 1):
        A(row(i, e))
    A("")

A("## 四、全部实体（按 EXPRESS schema 分组）")
A("")
A("> ⭐ = 属于第二节的尺寸/公差/基准专题；「图中引用」= 该实体在图中被上级实体属性框引用的次数（可粗略视为重要度）。")
A("")

A("### 4.1 分组导航")
A("")
nav = sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))
for key, items in nav:
    A("* [`%s`](#%s) — %d 个" % (key, gh_anchor(key), len(items)))
A("")

for key, items in nav:
    A("### %s" % key)
    A("")
    A("共 %d 个实体。" % len(items))
    A("")
    A("| # | 实体名 | 中文名 | 图中引用 | 链接 |")
    A("| ---: | --- | --- | ---: | --- |")
    for i, e in enumerate(sorted(items, key=lambda x: x["name"]), 1):
        A(row(i, e))
    A("")

A("## 五、附录：虚线框（DEFINED TYPE / SELECT 类型）")
A("")
A("### 附录 A：DEFINED TYPE（%d 个）" % len(DEFINED_TYPES))
A("")
A("| # | 名称 | 中文名 |")
A("| ---: | --- | --- |")
for i, n in enumerate(sorted(DEFINED_TYPES), 1):
    A("| %d | `%s` | %s |" % (i, n, tr(n)))
A("")
A("### 附录 B：SELECT / 抽象超类型（%d 个）" % len(SELECT_TYPES))
A("")
A("| # | 名称 | 中文名 |")
A("| ---: | --- | --- |")
for i, n in enumerate(sorted(SELECT_TYPES), 1):
    A("| %d | `%s` | %s |" % (i, n, tr(n)))
A("")
A("## 六、术语表（构词 token 中英对照）")
A("")
A("> 用于自动组合中文名，%d 条。" % len(TOKENS))
A("")
A("| 英文 token | 中文 | 英文 token | 中文 | 英文 token | 中文 |")
A("| --- | --- | --- | --- | --- | --- |")
items = sorted(TOKENS.items())
for i in range(0, len(items), 3):
    cells = []
    for j in range(3):
        if i + j < len(items):
            cells += ["`%s`" % items[i + j][0], items[i + j][1]]
        else:
            cells += ["", ""]
    A("| " + " | ".join(cells) + " |")
A("")
A("## 七、附件与数据文件")
A("")
A("* `aim_boxes_all_3974.csv` — 图上全部 %d 个框的明细（序号 / 框类型 / 实体名 / 中文名 / schema / 链接）"
  % (len(entities) + len(refs)))
A("* `aim_entities.csv` — %d 个实体定义的精简表" % len(by_name))
A("* `aim_dash_types.csv` — %d 个虚线框（DEFINED TYPE / SELECT 类型）"
  % (len(DEFINED_TYPES) + len(SELECT_TYPES)))
A("* `aim_domains.csv` — 领域分类索引（实体名 / 工业用途 / 软件模块）")
A("* `aim_lifecycle.csv` — 产品生命周期功能环节分类索引（实体名 / 功能环节）")
A("* `aim_entities.json` — 原始解析结果（含引用框索引）")
A("")
A("---")
A("")
A("生成脚本：`scripts/extract_aim.py`（抓取解析）、`scripts/gen_aim_doc.py` + `scripts/glossary.py`（翻译与排版）、`scripts/domains.py`（领域分类）。")
A("")
A("> 本目录为完全独立的资料集，与任何宿主项目无关；完整运行、刷新与校验方法见同目录 `README.md`。")
A("")
A("本目录采用 **MIT 许可证**，完整文本见 [`LICENSE`](./LICENSE)。")
A("")

md_path = os.path.join(OUT_DIR, "STEP-AIM-实体全表-中文速查.md")
open(md_path, "w", encoding="utf-8").write("\n".join(lines))

# ---------- CSV ----------
with open(os.path.join(OUT_DIR, "aim_boxes_all_3974.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["序号", "框类型", "实体名", "中文名", "EXPRESS schema", "说明链接"])
    i = 0
    for e in entities:
        i += 1
        w.writerow([i, "实体定义框", e["name"], tr(e["name"]), e["schema"], e["link"]])
    for r in refs:
        i += 1
        e = by_name.get(r["name"], {})
        w.writerow([i, "属性引用框", r["name"], tr(r["name"]),
                    e.get("schema") or kind_of(r["name"]), e.get("link", "")])

with open(os.path.join(OUT_DIR, "aim_entities.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["序号", "实体名", "中文名", "EXPRESS schema", "图中引用次数", "说明链接"])
    for i, e in enumerate(sorted(by_name.values(), key=lambda x: x["name"]), 1):
        w.writerow([i, e["name"], tr(e["name"]), e["schema"], ref_count.get(e["name"], 0), e["link"]])

with open(os.path.join(OUT_DIR, "aim_dash_types.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["序号", "框类型", "名称", "中文名"])
    i = 0
    for n in sorted(DEFINED_TYPES):
        i += 1
        w.writerow([i, "DEFINED TYPE", n, tr(n)])
    for n in sorted(SELECT_TYPES):
        i += 1
        w.writerow([i, "SELECT/抽象超类型", n, tr(n)])

with open(os.path.join(OUT_DIR, "aim_domains.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["序号", "实体名", "中文名", "工业用途分类", "软件模块分类", "EXPRESS schema", "说明链接"])
    for i, e in enumerate(sorted(by_name.values(), key=lambda x: x["name"]), 1):
        w.writerow([i, e["name"], tr(e["name"]),
                    " / ".join(industry_of(e["name"])),
                    " / ".join(software_of(e["name"])),
                    e["schema"], e["link"]])

with open(os.path.join(OUT_DIR, "aim_lifecycle.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["序号", "实体名", "中文名", "功能环节分类", "EXPRESS schema", "图中引用次数", "说明链接"])
    for i, e in enumerate(sorted(by_name.values(), key=lambda x: x["name"]), 1):
        w.writerow([i, e["name"], tr(e["name"]),
                    " / ".join(lifecycle_of(e["name"])),
                    e["schema"], ref_count.get(e["name"], 0), e["link"]])

print("写出:", md_path)
print("md 行数:", len(lines))
print("md 大小:", os.path.getsize(md_path))