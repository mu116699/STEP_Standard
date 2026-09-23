# -*- coding: utf-8 -*-
"""生成 STEP ARM（Application Reference Model）概念全表文档（Markdown + CSV）。

ARM 概念名采用「首字母大写 + 下划线分词」形式（如 `Unary_function_call`），
因此中文名 = 按下划线切分 -> 小写 -> 查 `glossary.TOKENS` -> 拼接。
"""
import json
import os
import re
import sys
import csv
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glossary import TOKENS, OVERRIDES
from arm_domains import classify, INDUSTRY, USERS, LIFECYCLE

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.dirname(HERE)
DATA = os.path.join(OUT_DIR, "arm_concepts.json")
SRC_PAGE = "https://www.steptools.com/stds/stp_expg/arm.html"
PAGE_VER = "Updated 2022-02-23 with SMRLv9 update"

# ARM / STEP-NC 专用补充译名
ARM_TOKENS = {
    "am": "增材制造",
    "ao": "应用对象",
    "nc": "数控",
    "stepnc": "STEP-NC",
    "p21": "Part 21",
    "sda": "SDA",
    "plib": "PLIB",
    "pmi": "PMI",
    "gd": "几何尺寸",
    "t": "T",
    "iso": "ISO",
    "id": "标识",
    "ids": "标识",
    "uuid": "UUID",
    "url": "URL",
    "uri": "URI",
    "xml": "XML",
    "json": "JSON",
    "html": "HTML",
    "pdf": "PDF",
    "cad": "CAD",
    "cam": "CAM",
    "cnc": "CNC",
    "b": "B",
    "d": "D",
    "v": "V",
    "x": "X",
    "y": "Y",
    "z": "Z",
    "2d": "二维",
    "3d": "三维",
    "n": "N",
    "m": "M",
    "k": "K",
    "r": "R",
    "c": "C",
    "s": "S",
    "u": "U",
    "w": "W",
    "e": "E",
    "a": "A",
    "i": "I",
    "o": "O",
    "p": "P",
    "q": "Q",
    "g": "G",
    "h": "H",
    "j": "J",
    "l": "L",
    "f": "F",
}
ARM_TOKENS.update(TOKENS)

# 补充：ARM / STEP-NC 概念名中出现的其余词
ARM_TOKENS.update({
    "part": "零件", "activity": "活动", "md": "机械设计", "axis": "轴", "axes": "轴",
    "finish": "精加工", "rough": "粗加工", "work": "工作", "drill": "钻", "contour": "轮廓",
    "mill": "铣", "plunge": "下刀", "nominal": "名义", "numerical": "数值",
    "catalogue": "目录", "ap": "接近", "trajectory": "轨迹", "bidirectional": "双向",
    "hierarchy": "层次", "lift": "抬刀", "endmill": "立铣刀", "const": "常量",
    "complete": "完整", "tolerances": "公差", "predefined": "预定义", "straight": "直线",
    "additional": "附加", "dictionary": "字典", "collection": "集合", "bevel": "锥",
    "cutout": "切口", "through": "通", "heterogenuous": "异质", "center": "中心",
    "combined": "组合", "reamer": "铰刀", "connect": "连接", "cutter": "刀具",
    "exchange": "交换", "pallet": "托盘", "five": "五", "tilt": "倾斜", "yaw": "偏航",
    "statement": "语句", "multistep": "多步", "stop": "停止", "profiled": "成型",
    "program": "程序", "reaming": "铰孔", "mark": "标记", "tapered": "锥形",
    "three": "三", "two5d": "2.5D", "unidirectional": "单向", "alternative": "备选",
    "replication": "复制", "implicit": "隐式", "extruded": "拉伸", "attributes": "属性",
    "coordinate": "坐标", "thickness": "厚度", "toleranced": "带公差", "median": "中位",
    "categories": "类别", "curved": "曲线", "distance": "距离", "detailed": "详细",
    "otd": "OTD", "affected": "受影响", "frame": "框架", "helical": "螺旋",
    "test": "测试", "gradient": "梯度", "infill": "填充", "oned": "一维", "twod": "二维",
    "ballnose": "球头", "bullnose": "圆鼻", "chamfered": "倒角", "channel": "通道",
    "tap": "攻丝", "direct": "直接", "secplane": "截面", "connector": "连接器",
    "spiral": "螺旋", "counter": "反向", "sinking": "下沉", "normal": "法向",
    "display": "显示", "dovetail": "燕尾", "facemill": "面铣刀", "feedstop": "进给停止",
    "var": "变量", "if": "如果", "last": "最后", "timestamp": "时间戳",
    "leading": "前导", "load": "装载", "travel": "行程", "optional": "可选",
    "parameterised": "参数化", "cc": "CC", "cl": "CL", "ramp": "斜坡",
    "toolaxis": "刀轴", "zigzag": "之字形", "return": "返回", "home": "原点",
    "rotating": "旋转", "selective": "选择性", "shouldermill": "肩铣刀", "spade": "扁钻",
    "spotdrill": "定心钻", "tilted": "倾斜", "probe": "测头", "twist": "螺旋",
    "unload": "卸载", "uv": "UV", "wait": "等待", "while": "当", "platform": "平台",
    "alias": "别名", "supplier": "供应商", "technical": "技术", "approving": "批准",
    "correlated": "相关", "statistical": "统计", "symmetrical": "对称", "typical": "典型",
    "characterizable": "可特征化", "mapping": "映射", "contextual": "上下文",
    "rectangle": "矩形", "draft": "草图", "decimal": "十进制", "places": "位",
    "significant": "有效", "digits": "数字", "limitation": "限制", "undefined": "未定义",
    "measurement": "测量", "radial": "径向", "digital": "数字", "suffix": "后缀",
    "iso15926": "ISO 15926", "4": "4", "rdl": "RDL", "hardcopy": "硬拷贝",
    "validation": "验证", "incomplete": "不完整", "assembled": "装配", "controlled": "受控",
    "attachment": "附件", "structuring": "结构化", "blind": "盲", "countersunk": "锥形沉孔",
    "diagonal": "对角", "diamond": "菱形", "first": "第一", "groove": "槽",
    "shoulder": "台肩", "radiused": "圆角", "recess": "凹槽", "base": "基础",
    "spur": "直齿", "woodruff": "半圆", "translation": "平移", "indication": "指示",
    "collected": "收集", "initial": "初始", "output": "输出", "market": "市场",
    "quantity": "数量", "selected": "选定", "substitution": "替换", "supplied": "供应",
    "precedence": "优先级", "tracing": "追踪", "period": "周期", "replaced": "替换",
    "influence": "影响", "fabrication": "制造", "manual": "手动", "allocation": "分配",
    "coating": "涂层", "treatment": "处理", "duration": "持续时间",
})

# 整名人工覆盖（ARM 概念名 -> 中文）
ARM_OVERRIDES = {
    "Abs_function": "绝对值函数",
    "Acos_function": "反余弦函数",
    "Asin_function": "反正弦函数",
    "Atan_function": "反正切函数",
    "Cos_function": "余弦函数",
    "Sin_function": "正弦函数",
    "Tan_function": "正切函数",
    "Exp_function": "指数函数",
    "Log_function": "对数函数",
    "Sqrt_function": "平方根函数",
    "Plus_function": "加法函数",
    "Minus_function": "减法函数",
    "Times_function": "乘法函数",
    "Divide_function": "除法函数",
    "Power_function": "幂函数",
    "Modulo_function": "取模函数",
    "Length_function": "长度函数",
    "Value_function": "取值函数",
    "Generic_expression": "通用表达式",
    "Unary_generic_expression": "一元通用表达式",
    "Binary_generic_expression": "二元通用表达式",
    "Multiple_arity_generic_expression": "多元通用表达式",
    "Unary_numeric_expression": "一元数值表达式",
    "Binary_numeric_expression": "二元数值表达式",
    "Multiple_arity_numeric_expression": "多元数值表达式",
    "Unary_function_call": "一元函数调用",
    "Binary_function_call": "二元函数调用",
    "Multiple_arity_function_call": "多元函数调用",
    "Value_with_unit": "带单位的量值",
    "Am_compound_feature": "增材制造复合特征",
    "Am_construction": "增材制造构造",
    "Am_feature": "增材制造特征",
    "Am_operation": "增材制造操作",
    "Am_part": "增材制造零件",
    "Am_process": "增材制造工艺",
    "Am_setup": "增材制造装夹",
    "Am_workpiece": "增材制造工件",
    "Adaptive_control": "自适应控制",
    "Air_strategy": "空行程策略",
    "Along_path": "沿路径",
    "Axis_placement_3d": "三维轴系布置",
    "Cartesian_point": "笛卡儿点",
    "Plane_angle_measure": "平面角度量",
    "Length_measure": "长度量",
    "Product_view_definition": "产品视图定义",
    "Initial_view_definition_context": "初始视图定义上下文",
    "Additional_view_definition_context": "附加视图定义上下文",
    "Constructive_geometry": "构造几何",
    "Document_type": "文档类型",
    "Digital_file": "数字文件",
    "External_geometric_model": "外部几何模型",
    "Work_request": "工作请求",
    "Work_plan": "工作计划",
    "Workpiece": "工件",
    "Kinematic_joint": "运动副",
    "Kinematic_pair": "运动副对",
    "Actuated_kinematic_pair": "受驱动运动副对",
    "Detailed_topological_model_element": "详细拓扑模型元素",
    "Function_application": "函数应用",
    "Blind_bottom_condition": "盲孔底部条件",
    "Blind_hole_bottom": "盲孔底部",
    "Through_bottom_condition": "通孔底部条件",
    "Ap_lift_path_angle": "接近抬刀路径角",
    "Ap_lift_path_tangent": "接近抬刀路径相切",
    "Ap_retract_angle": "接近退回角",
    "Ap_retract_tangent": "接近退回相切",
    "Catalogue_gear": "标准齿轮",
    "Catalogue_knurl": "标准滚花",
    "Catalogue_marking": "标准标记",
    "Catalogue_thread": "标准螺纹",
}
ARM_OVERRIDES.update(OVERRIDES)


def tr(name):
    """ARM 概念名 -> 中文名。"""
    if name in ARM_OVERRIDES:
        return ARM_OVERRIDES[name]
    parts = re.split(r"[_]", name)
    out = []
    for p in parts:
        key = p.lower()
        out.append(ARM_TOKENS.get(key, p))
    s = "".join(out)
    s = s.replace("的的", "的")
    return s or name


def gh_anchor(text):
    """按 GitHub 规则生成标题锚点。"""
    import urllib.parse
    t = text.strip().lower()
    t = re.sub(r"[^\w\s\-]", "", t)
    t = t.replace(" ", "-")
    return urllib.parse.quote(t)


def build_groups(concepts, dim, order, fallback_label):
    """按某一维度把概念分组；未命中任何类别的归入 fallback_label。

    一个概念可能同时命中多个类别（多标签），因此各类别计数之和会大于概念总数。
    """
    groups = collections.OrderedDict((k, []) for k in order)
    groups[fallback_label] = []
    for c in concepts:
        labels = classify(c["name"], c["module"]).get(dim, [])
        if not labels:
            groups[fallback_label].append(c)
        else:
            for lb in labels:
                groups[lb].append(c)
    for v in groups.values():
        v.sort(key=lambda d: d["name"])
    return groups


def main():
    data = json.load(open(DATA, encoding="utf-8"))
    concepts = data["concepts"]
    refs = data["references"]

    ap242 = [c for c in concepts if c["source"] == "ap242"]
    ap238 = [c for c in concepts if c["source"] == "ap238"]
    other = [c for c in concepts if c["source"] not in ("ap242", "ap238")]

    # 模块 -> 概念列表
    by_mod = collections.defaultdict(list)
    for c in ap242:
        by_mod[c["module"]].append(c)
    for v in by_mod.values():
        v.sort(key=lambda d: d["name"])
    mod_order = sorted(by_mod, key=lambda m: (-len(by_mod[m]), m))

    # 引用次数排行
    top_ref = sorted(concepts, key=lambda c: -c["ref_count"])[:30]

    # 三维分类（仅对 AP242 概念）
    ind_groups = build_groups(ap242, "industry", list(INDUSTRY.keys()), "通用 / 跨行业")
    usr_groups = build_groups(ap242, "users", list(USERS.keys()), "通用 / 基础")
    lc_groups = build_groups(ap242, "lifecycle", list(LIFECYCLE.keys()), "通用 / 基础")

    lines = []
    A = lines.append

    def render_dim(title, intro, groups):
        """渲染一个分类维度小节（含类别计数表 + 各类别概念表）。"""
        A("## %s" % title)
        A("")
        A(intro)
        A("")
        A("| 类别 | 概念数 |")
        A("| --- | ---: |")
        for k, v in groups.items():
            A("| %s | %d |" % (k, len(v)))
        A("")
        A("> 一个概念可能同时属于多个类别，故各类别计数之和大于概念总数。")
        A("")
        for k, v in groups.items():
            A("### %s（%d）" % (k, len(v)))
            A("")
            A("| 中文名 | 英文名 | 模块 | 引用 | 官方定义 |")
            A("| --- | --- | --- | ---: | --- |")
            for c in v:
                A("| %s | `%s` | %s | %d | [定义](%s) |" % (
                    tr(c["name"]), c["name"], c["module"] or "—", c["ref_count"], c["link"]))
            A("")
        A("---")
        A("")

    A("# STEP ARM 概念全表（中文速查）")
    A("")
    A("> **本目录是一个完全独立的资料集，与任何宿主项目无关。**")
    A("> 目录内所有脚本、数据、文档均自包含（仅依赖 Python 标准库），")
    A("> 可整体复制到任意位置、任意仓库或独立仓库中运行，无需任何外部依赖或配置。")
    A("")
    A("本目录保存对 STEP Tools 官方 **ARM（Application Reference Model，应用参考模型）概念图** 的完整解析结果。")
    A("")
    A("* 来源页面：<%s>" % SRC_PAGE)
    A("* 页面版本：%s" % PAGE_VER)
    A("* 抓取/生成日期：2026-09-23")
    A("")
    A("---")
    A("")
    A("## 一、总览")
    A("")
    A("| 项目 | 数量 |")
    A("| --- | --- |")
    A("| 概念定义框 | **%d** |" % len(concepts))
    A("| 概念引用框 | %d |" % len(refs))
    A("| AP242 ARM 模块 | %d |" % len(by_mod))
    A("| AP242 概念 | %d |" % len(ap242))
    A("| AP238（STEP-NC）应用对象 | %d |" % len(ap238))
    A("| 其他资源概念 | %d |" % len(other))
    A("")
    A("> ARM 概念是**面向工程人员的高层概念**（如工件、工作计划、产品形状），")
    A("> 与 AIM 的底层 EXPRESS 实体一一对应但更易理解。")
    A("")
    A("---")
    A("")
    A("## 二、ARM 模块索引")
    A("")
    A("AP242 的 ARM 概念按 **%d 个应用模块（module）** 组织，下表按概念数降序排列：" % len(by_mod))
    A("")
    A("| # | 模块 | 概念数 |")
    A("| --- | --- | --- |")
    for i, m in enumerate(mod_order, 1):
        A("| %d | [`%s`](#%s) | %d |" % (i, m, gh_anchor("模块 " + m), len(by_mod[m])))
    A("")
    A("---")
    A("")
    A("## 三、按模块分类的概念全表")
    A("")
    A("每个模块一节，列出该模块全部概念：**中文名**、英文名、图中引用次数、官方定义链接。")
    A("")
    for m in mod_order:
        A("### 模块 %s" % m)
        A("")
        A("> 共 %d 个概念。" % len(by_mod[m]))
        A("")
        A("| 中文名 | 英文名 | 引用 | 官方定义 |")
        A("| --- | --- | ---: | --- |")
        for c in by_mod[m]:
            A("| %s | `%s` | %d | [定义](%s) |" % (tr(c["name"]), c["name"], c["ref_count"], c["link"]))
        A("")
    A("---")
    A("")
    render_dim(
        "四、按应用领域分类（航空 / 汽车 / 造船 / 机械 / 电气 / 通用）",
        "按概念所服务的**应用领域**归类。同一概念可能跨多个领域；"
        "未命中任何领域关键词的概念归入「通用 / 跨行业」，"
        "它们通常是几何、拓扑、文档、活动等各行业共用的基础概念。",
        ind_groups)
    render_dim(
        "五、按使用者分类（领域专家 / 工程师 / 标准制定者）",
        "按概念的**主要使用者角色**归类：领域专家关注业务与管理概念，"
        "工程师关注几何、工艺与公差概念，标准制定者关注元模型、表达与库概念。",
        usr_groups)
    render_dim(
        "六、按产品生命周期功能环节分类（CAD / CAM / CAE / PDM / CAPP / 检测质量）",
        "按概念在产品生命周期中所处的**功能环节**归类："
        "CAD（设计 / 建模 / 制图）、CAM（制造 / 加工）、CAE（分析 / 仿真）、"
        "PDM（产品数据管理）、CAPP（工艺规划）、检测 / 质量（PMI / 计量）。"
        "未命中任何环节的概念归入「通用 / 基础」。",
        lc_groups)
    A("## 七、STEP-NC（AP238）应用对象")
    A("")
    A("以下 %d 个概念来自 STEP-NC（ISO 10303-238）应用对象定义，用于数控加工工艺描述：" % len(ap238))
    A("")
    A("| 中文名 | 英文名 | 引用 | 官方定义 |")
    A("| --- | --- | ---: | --- |")
    for c in sorted(ap238, key=lambda d: d["name"]):
        A("| %s | `%s` | %d | [定义](%s) |" % (tr(c["name"]), c["name"], c["ref_count"], c["link"]))
    A("")
    if other:
        A("### 其他资源概念")
        A("")
        A("| 中文名 | 英文名 | 引用 | 官方定义 |")
        A("| --- | --- | ---: | --- |")
        for c in other:
            A("| %s | `%s` | %d | [定义](%s) |" % (tr(c["name"]), c["name"], c["ref_count"], c["link"]))
        A("")
    A("---")
    A("")
    A("## 八、图中引用次数最多的概念（Top 30）")
    A("")
    A("引用次数反映该概念在 ARM 概念图中的「枢纽」程度：")
    A("")
    A("| # | 中文名 | 英文名 | 模块 | 引用次数 |")
    A("| --- | --- | --- | --- | ---: |")
    for i, c in enumerate(top_ref, 1):
        A("| %d | %s | `%s` | %s | %d |" % (i, tr(c["name"]), c["name"], c["module"] or "—", c["ref_count"]))
    A("")
    A("---")
    A("")
    A("## 九、关于中文名")
    A("")
    A("* 中文名由 `scripts/glossary.py` 的构词术语表 + 本脚本的 ARM 专用补充译名自动组合生成。")
    A("* 自动组合结果**仅作检索提示**，工程使用请以英文概念名与 SMRL 官方定义为准。")
    A("* 若发现译名不妥，修改 `scripts/gen_arm_doc.py` 的 `ARM_OVERRIDES` 后重跑即可。")
    A("")
    A("---")
    A("")
    A("*本目录依据 STEP Tools ARM 概念图与 SMRL 官方定义整理。")
    A("自动组合的中文名仅作检索提示，工程使用请以英文概念名与标准定义为准。*")
    A("")
    A("本目录采用 **MIT 许可证**，完整文本见 [`LICENSE`](./LICENSE)。")

    doc = "\n".join(lines) + "\n"
    open(os.path.join(OUT_DIR, "STEP-ARM-概念全表-中文速查.md"), "w", encoding="utf-8").write(doc)

    # CSV 1：概念全表
    with open(os.path.join(OUT_DIR, "arm_concepts.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["中文名", "英文名", "概念名", "模块", "来源", "引用次数", "官方定义链接"])
        for c in concepts:
            w.writerow([tr(c["name"]), c["name"], c["concept"], c["module"], c["source"], c["ref_count"], c["link"]])

    # CSV 2：模块索引
    with open(os.path.join(OUT_DIR, "arm_modules.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["模块", "概念数"])
        for m in mod_order:
            w.writerow([m, len(by_mod[m])])

    # CSV 3~5：三维分类
    def write_dim_csv(fname, groups):
        with open(os.path.join(OUT_DIR, fname), "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["类别", "中文名", "英文名", "模块", "来源", "引用次数", "官方定义链接"])
            for k, v in groups.items():
                for c in v:
                    w.writerow([k, tr(c["name"]), c["name"], c["module"], c["source"], c["ref_count"], c["link"]])

    write_dim_csv("arm_industry.csv", ind_groups)
    write_dim_csv("arm_users.csv", usr_groups)
    write_dim_csv("arm_lifecycle.csv", lc_groups)

    print("概念总数 :", len(concepts))
    print("模块数   :", len(by_mod))
    print("AP242    :", len(ap242))
    print("AP238    :", len(ap238))
    print("其他     :", len(other))
    print("应用领域 :", " / ".join("%s=%d" % (k, len(v)) for k, v in ind_groups.items()))
    print("使用者   :", " / ".join("%s=%d" % (k, len(v)) for k, v in usr_groups.items()))
    print("功能环节 :", " / ".join("%s=%d" % (k, len(v)) for k, v in lc_groups.items()))
    print("已写出   : STEP-ARM-概念全表-中文速查.md, arm_concepts.csv, arm_modules.csv,")
    print("           arm_industry.csv, arm_users.csv, arm_lifecycle.csv")


if __name__ == "__main__":
    main()
