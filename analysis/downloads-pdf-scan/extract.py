import os, json
from pypdf import PdfReader

SRC = "/Users/tangzw119/Downloads"
OUT = "/Users/tangzw119/Documents/GitHub/auto-research/analysis/downloads-pdf-scan/first_pages.json"

results = []
for fn in sorted(os.listdir(SRC)):
    if not fn.lower().endswith(".pdf"):
        continue
    path = os.path.join(SRC, fn)
    size = os.path.getsize(path)
    entry = {"file": fn, "size_mb": round(size/1e6,1), "pages": None, "text": None, "error": None}
    try:
        r = PdfReader(path)
        n = len(r.pages)
        entry["pages"] = n
        take = 1 if size > 20e6 else min(2, n)
        parts = []
        for i in range(take):
            try:
                t = r.pages[i].extract_text() or ""
            except Exception as e:
                t = f"[page {i} extract error: {e}]"
            parts.append(t)
        entry["text"] = "\n===PAGE BREAK===\n".join(parts)[:6000]
        if r.metadata:
            md = {k: str(v)[:200] for k, v in r.metadata.items() if v}
            entry["metadata"] = md
    except Exception as e:
        entry["error"] = str(e)[:300]
    results.append(entry)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
ok = sum(1 for r in results if r["text"])
err = [r["file"] for r in results if r["error"]]
empty = [r["file"] for r in results if not r["error"] and not (r["text"] or "").strip()]
print(f"total={len(results)} ok={ok} error={len(err)} empty_text={len(empty)}")
print("ERRORS:", err)
print("EMPTY:", empty)
