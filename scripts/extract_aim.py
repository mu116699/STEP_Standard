# -*- coding: utf-8 -*-
"""从 steptools AIM 页面 SVG 中提取全部实体框（定义框 + 引用框）。"""
import re
import json
import os
import collections
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "aim.html")
OUT_DIR = os.path.dirname(HERE)
PAGE = "https://www.steptools.com/stds/stp_expg/aim.html"
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

defs = {}
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
        continue
    url = href
    if url.startswith("../"):
        url = "https://www.steptools.com/stds/" + url[3:]
    elif url.startswith("http"):
        pass
    else:
        url = BASE + url
    schema = ""
    frag = ""
    if "#" in url:
        url, frag = url.split("#", 1)
    if frag:
        schema = frag.split(".")[0]
    defs[rid] = {
        "name": name,
        "id": rid,
        "schema": schema,
        "fragment": frag,
        "url": url,
        "link": url + ("#" + frag if frag else ""),
        "dash": 'class="dash"' in rect_attrs,
        "title": "definition" if 'xlink:title="definition"' in a_attrs else "",
    }

# 未加链接的匿名框（如 INTEGER / REAL 等基础类型）
plain_pat = re.compile(
    r'<rect\s+x="[^"]*"\s+y="[^"]*"\s+width="[^"]*"\s+height="[^"]*"\s*/>\s*'
    r'<text class="box"[^>]*>([^<]*)</text>',
    re.S,
)
plain = collections.Counter(t.strip() for t in plain_pat.findall(raw))

entities = sorted(defs.values(), key=lambda d: d["name"])
json.dump(
    {"entities": entities, "references": refs, "plain": dict(plain)},
    open(os.path.join(OUT_DIR, "aim_entities.json"), "w", encoding="utf-8"),
    ensure_ascii=False,
    indent=1,
)

print("definition boxes :", len(entities))
print("reference boxes  :", len(refs))
print("plain boxes      :", len(plain), sorted(plain)[:20])
print("schemas          :", len({e["schema"] for e in entities}))
print("no schema        :", sum(1 for e in entities if not e["schema"]))
print("dash (defined ty):", sum(1 for e in entities if e["dash"]))
print("no url           :", sum(1 for e in entities if not e["url"]))
for e in entities[:5]:
    print("  ", e["name"], "|", e["schema"], "|", e["link"])