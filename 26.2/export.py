import json, pathlib
root = pathlib.Path("generated/data/minecraft")
reg = json.load(open("generated/reports/registries.json"))
items = sorted(k.replace("minecraft:", "") for k in reg["minecraft:item"]["entries"])

def ing(x):
    if isinstance(x, str): return x.replace("minecraft:", "")
    if isinstance(x, list): return "|".join(ing(i) for i in x)
    if isinstance(x, dict):
        return ing(x["item"]) if "item" in x else "#" + x.get("tag", "?").replace("minecraft:", "")
    return "?"

def res(r):
    if isinstance(r, str): return r.replace("minecraft:", ""), 1
    return (r.get("id") or r.get("item")).replace("minecraft:", ""), r.get("count", 1)

lines = []
for f in sorted((root / "recipe").glob("*.json")):
    d = json.load(open(f))
    if "result" not in d: continue
    t = d["type"].replace("minecraft:", "")
    if t == "crafting_shaped": ins = list(d["key"].values())
    elif "ingredients" in d: ins = d["ingredients"]
    else: ins = [d[k] for k in ("ingredient", "template", "base", "addition", "input", "material") if k in d]
    r, c = res(d["result"])
    lines.append(f"{r} x{c} <- {t}: " + ", ".join(ing(i) for i in ins))

tags = []
tdir = root / "tags" / "item"
for f in sorted(tdir.rglob("*.json")):
    name = "#" + f.relative_to(tdir).with_suffix("").as_posix()
    vals = [v if isinstance(v, str) else v["id"] for v in json.load(open(f))["values"]]
    tags.append(f"{name}: " + ", ".join(v.replace("minecraft:", "") for v in vals))

with open("items_und_rezepte.txt", "w", encoding="utf-8") as out:
    out.write("## ITEMS\n" + "\n".join(items))
    out.write("\n\n## REZEPTE (ergebnis <- typ: zutaten, '|' = eins davon, '#' = Tag)\n" + "\n".join(lines))
    out.write("\n\n## TAGS\n" + "\n".join(tags))