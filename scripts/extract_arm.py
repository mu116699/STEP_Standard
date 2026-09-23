# -*- coding: utf-8 -*-
"""从 steptools ARM（Application Reference Model）概念图页面 SVG 中提取全部概念框。

ARM 页面（STEP Concepts / Application Objects）与 AIM 页面结构不同：

* **定义框**：`<rect id="<concept>">` + `<text>Concept_name</text>`，
  链接指向 SMRL 模块定义页
  `../smrl/data/modules/<module>/sys/4_info_reqs.htm#<module>_arm.<concept>`。
  模块名即 ARM 的天然分类。
* **引用框**：`<rect id="refXXXX">` + `<text>N, M, Concept_name</text>`，
  链接为页内锚点 `#<concept>`，表示该概念在图中被引用的位置。

输出：`arm_concepts.json`
"""
import re
import json
import os
import collections
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "arm.html")
OUT_DIR = os.path.dirname(HERE)
PAGE = "https://www.steptools.com/stds/stp_expg/arm.html"
BASE = "https://www.steptools.com/stds/stp_expg/"

os.makedirs(OUT_DIR, exist_ok=True)
if not os.path.exists(SRC):
    print("下载", PAGE)
    urllib.request.urlretrieve(PAGE, SRC)
raw = open(SRC, encoding="utf-8", errors="replace").read()

anchor_pat = re.compile(
    r'<a\s+xlink:href="([^"]+)"([^>]*)>\s*'
    r'<rect\s+id="([^"]+)"([^>]*?)/>\s*'
    r'<text class="box"[^>]*>([^<]*)</text>\s*</a>',
    re.S,
)

concepts = {}
refs = []
for m in anchor_pat.finditer(raw):
    href, a_attrs, rid, rect_attrs, text = m.groups()
    text = text.strip()
    is_ref = bool(re.match(r"^\d+,\s*\d+,\s*", text))
    name = re.sub(r"^\d+,\s*\d+,\s*", "", text).strip()
    if is_ref:
        refs.append({"id": rid, "name": name, "href": href})
        continue
    if href.startswith("#"):
        # 无外部定义链接的定义框（极少见），跳过
        continue
    url = href
    if url.startswith("../"):
        url = "https://www.steptools.com/stds/" + url[3:]
    elif not url.startswith("http"):
        url = BASE + url
    frag = ""
    if "#" in url:
        url, frag = url.split("#", 1)
    # 模块名：/modules/<module>/sys/
    mm = re.search(r"/modules/([^/]+)/sys/", url)
    module = mm.group(1) if mm else ""
    # 概念名：<module>_arm.<concept> 或 ao-<concept>
    if "." in frag:
        concept = frag.split(".", 1)[1]
    elif frag.startswith("ao-"):
        concept = frag[3:]
    else:
        concept = rid
    # 来源：AP242 ARM 模块 / AP238 STEP-NC / PDF 资源
    if module:
        source = "ap242"
    elif "stepmfg.github.io" in url:
        source = "ap238"
    elif url.lower().endswith(".pdf"):
        source = "pdf"
    else:
        source = "other"
    concepts[rid] = {
        "name": name,
        "id": rid,
        "concept": concept,
        "module": module,
        "source": source,
        "fragment": frag,
        "url": url,
        "link": url + ("#" + frag if frag else ""),
    }

# 统计每个概念被引用的次数
ref_count = collections.Counter()
for r in refs:
    if r["href"].startswith("#"):
        ref_count[r["href"][1:]] += 1

items = sorted(concepts.values(), key=lambda d: (d["source"], d["module"], d["name"]))
for it in items:
    it["ref_count"] = ref_count.get(it["id"], 0)

json.dump(
    {"concepts": items, "references": refs},
    open(os.path.join(OUT_DIR, "arm_concepts.json"), "w", encoding="utf-8"),
    ensure_ascii=False,
    indent=1,
)

print("definition boxes :", len(items))
print("reference boxes  :", len(refs))
print("modules          :", len({c["module"] for c in items if c["module"]}))
print("by source        :", dict(collections.Counter(c["source"] for c in items)))
print("no url           :", sum(1 for c in items if not c["url"]))
for c in items[:5]:
    print("  ", c["name"], "|", c["source"], "|", c["module"], "|", c["link"])
