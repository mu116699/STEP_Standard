"""校验《step-NURBS.md》中引用的实体名是否都存在于解析数据中。

判定为「合法」的名称来源：
  1. aim_entities.json 中的实体定义（1461 个）
  2. aim_dash_types.csv 中的虚线框（DEFINED TYPE / SELECT / 抽象超类型）
其余（属性名、枚举值、函数名、数学符号）不计入实体名。
"""
import csv
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOC = os.path.join(ROOT, "step-NURBS.md")
JSON = os.path.join(ROOT, "aim_entities.json")
DASH = os.path.join(ROOT, "aim_dash_types.csv")

d = json.load(open(JSON, encoding="utf-8"))
names = {e["name"] for e in d["entities"]}
with open(DASH, encoding="utf-8-sig") as f:
    names |= {r["名称"] for r in csv.DictReader(f)}

txt = open(DOC, encoding="utf-8").read()

tbl = set(re.findall(r"^\|\s*`([a-z][a-z0-9_]+)`\s*\|", txt, re.M))
mm = set(re.findall(r"^\s*\w+\[([a-z][a-z0-9_]+)\]", txt, re.M))
mm |= set(re.findall(r"-->\s*([a-z][a-z0-9_]+)", txt))
cand = tbl | mm
miss = sorted(c for c in cand if c not in names)
print("表格/图 中实体名:", len(cand), " 缺失:", len(miss))
for m in miss:
    print("  ?", m)

