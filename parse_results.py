#!/usr/bin/env python3
import csv, glob, os, re, sys

FOLDER = sys.argv[1] if len(sys.argv) > 1 else "results"

def roi_part(text):
    i = text.find("Region of Interest Statistics")
    return text[i:] if i >= 0 else ""

def num(pat, text, cast=float):
    m = re.search(pat, text, re.M)
    return cast(m.group(1)) if m else None

rows = []
for path in sorted(glob.glob(os.path.join(FOLDER, "*__*.txt"))):
    trace, mode = os.path.basename(path)[:-4].rsplit("__", 1)
    roi = roi_part(open(path, errors="ignore").read())
    if not roi:
        continue
    r = {"trace": trace, "mode": mode}
    r["ipc"] = num(r"CPU 0 cumulative IPC:\s*([\d.]+)", roi)
    for c in ("DTLB", "STLB", "L1D", "L2C", "LLC"):
        r[f"{c}_mpki"] = num(rf"^{c} TOTAL\s+ACCESS:.*MPKI:\s*([\d.]+)", roi)
    r["stlb_pf_access"] = num(r"^STLB TRANSLATION FROM L1D PREFETCHER ACCESS:\s*(\d+)", roi, int)
    r["stlb_pf_miss"] = num(r"^STLB TRANSLATION FROM L1D PREFETCHER ACCESS:.*?MISS:\s*(\d+)", roi, int)
    r["l1d_pf_issued"] = num(r"^L1D PREFETCH\s+REQUESTED:.*ISSUED:\s*(\d+)", roi, int)
    r["l1d_pf_useful"] = num(r"^L1D PREFETCH\s+REQUESTED:.*USEFUL:\s*(\d+)", roi, int)
    r["l1d_pf_useless"] = num(r"^L1D PREFETCH\s+REQUESTED:.*USELESS:\s*(\d+)", roi, int)
    r["l1d_pf_late"] = num(r"^L1D TIMELY PREFETCHES:.*LATE PREFETCHES:\s*(\d+)", roi, int)
    r["cross_page_pf"] = num(r"^L1D Cross Page Prefetch Requests:\s*(\d+)", roi, int)
    r["same_page_pf"] = num(r"^L1D Same Page Prefetch Requests:\s*(\d+)", roi, int)
    rows.append(r)


ipc = {(r["trace"], r["mode"]): r["ipc"] for r in rows}
for r in rows:
    base = ipc.get((r["trace"], "discard"))
    r["speedup_vs_discard"] = round(r["ipc"] / base, 6) if base and r["ipc"] else None

keys = list(rows[0].keys())
with open(os.path.join(FOLDER, "summary.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys)
    w.writeheader()
    w.writerows(rows)
