#!/usr/bin/env python3
"""Rewrite a .excalidraw file so it conforms to the prettier-excalidraw style.

Usage:
    python3 fix.py in.excalidraw out.excalidraw [--font comic|nunito] [--arrowhead outline|filled]

Fixes: font family, snapped font sizes, roughness, fill style, rounded
rectangles, arrowhead type, arrows moved to the end of the z-order, child
rectangles moved after their container. It never changes positions, colors
or text, so the diagram keeps its meaning; run lint.py afterwards to see what
still needs a human (dark fills, icon sizes, unbound arrows).
Standard library only.
"""
import json, sys
from exstyle import ARROWHEADS, FONT_IDS, FONT_SIZES, area, bbox, inside
from lint import icon_groups


def snap(fs):
    return min(FONT_SIZES, key=lambda s: abs(s - fs))


def fix(doc, font="comic", arrowhead="outline"):
    want_font, want_head = FONT_IDS[font], ARROWHEADS[arrowhead]
    els = [e for e in doc["elements"] if not e.get("isDeleted")]
    icons = icon_groups(els)
    changed = 0
    for e in els:
        in_icon = any(g in icons for g in e.get("groupIds", []))
        t = e["type"]
        if t in ("rectangle", "ellipse", "diamond", "arrow", "line", "text") and not in_icon and e.get("roughness"):
            e["roughness"] = 0; changed += 1
        if t in ("rectangle", "ellipse", "diamond") and e.get("fillStyle") != "solid":
            e["fillStyle"] = "solid"; changed += 1
        if t == "rectangle" and e.get("roundness") is not None and not in_icon:
            e["roundness"] = None; changed += 1
        if t == "text":
            if e.get("fontFamily") != want_font:
                e["fontFamily"] = want_font; changed += 1
            fs = e.get("fontSize", 20)
            if abs(fs - snap(fs)) > 0.01:
                e["fontSize"] = snap(fs); changed += 1
            e["lineHeight"] = 1.25
        if t == "arrow":
            if e.get("endArrowhead") not in (None, want_head):
                e["endArrowhead"] = want_head; changed += 1
            if e.get("startArrowhead") not in (None, want_head):
                e["startArrowhead"] = want_head; changed += 1
    # z-order: containers before children, arrows last
    rects = [e for e in els if e["type"] == "rectangle" and e.get("backgroundColor") not in (None, "transparent")]
    order = {e["id"]: i for i, e in enumerate(els)}
    moved = True
    while moved:
        moved = False
        for c in rects:
            for p in rects:
                if p is c: continue
                if inside(bbox(c), bbox(p)) and area(bbox(p)) > area(bbox(c)) * 1.1 and order[p["id"]] > order[c["id"]]:
                    # move c (and its bound text) right after p
                    bound_ids = {b["id"] for b in c.get("boundElements") or [] if b.get("type") == "text"}
                    block = [c] + [e for e in els if e["id"] in bound_ids]
                    for b in block: els.remove(b)
                    pi = els.index(p)
                    for k, b in enumerate(block): els.insert(pi + 1 + k, b)
                    order = {e["id"]: i for i, e in enumerate(els)}
                    changed += 1; moved = True
                    break
            if moved: break
    arrows = [e for e in els if e["type"] == "arrow" and (e.get("endArrowhead") or e.get("startArrowhead"))]
    if arrows:
        arrow_text = {b["id"] for a in arrows for b in a.get("boundElements") or [] if b.get("type") == "text"}
        tail = arrows + [e for e in els if e["id"] in arrow_text]
        head = [e for e in els if e not in tail]
        if head + tail != els:
            changed += 1
        els = head + tail
    for i, e in enumerate(els):
        e["index"] = "a" + format(i, "04d")
        e["version"] = e.get("version", 1) + 1
    doc["elements"] = els
    return changed


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__); sys.exit(2)
    font = args[args.index("--font") + 1] if "--font" in args else "comic"
    head = args[args.index("--arrowhead") + 1] if "--arrowhead" in args else "outline"
    doc = json.load(open(args[0]))
    n = fix(doc, font, head)
    json.dump(doc, open(args[1], "w"), indent=1)
    print(f"wrote {args[1]}: {n} changes")


if __name__ == "__main__":
    main()
