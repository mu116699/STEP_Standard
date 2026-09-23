# -*- coding: utf-8 -*-
"""提取 AIM 图中的虚线框：DEFINED TYPE 与 SELECT / 抽象超类型。"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "aim.html")
OUT = os.path.join(HERE, "aim_dashtypes.json")

raw = open(SRC, encoding="utf-8", errors="replace").read()
pat = re.compile(r'<rect\s+id="([^"]+)"[^>]*class="dash"')

sel, dt = [], []
for m in pat.finditer(raw):
    head = raw[m.end():m.end() + 260].split("<text")[0]
    (sel if "<line" in head else dt).append(m.group(1))

json.dump({"select": sel, "defined_type": dt},
          open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("SELECT/抽象超类型:", len(sel), "| DEFINED TYPE:", len(dt))