"""统计铺片后的全片时间线：镜头覆盖、空缺、总长。

OpenCut 时间刻度为 1/120000 秒。
"""
import json
import re
import sys
from pathlib import Path

TICK = 120000.0
P = Path(sys.argv[1] if len(sys.argv) > 1 else r"E:\projects\内容创作\故事短片\白米饭\后期\全片画风与动作统一-v034\风格审查\timeline-live.json")
d = json.loads(P.read_text(encoding="utf-8"))
val = d.get("value", d)

tracks = val.get("tracks") or {}
main = (tracks.get("main") or {}).get("elements") or []
els = val.get("elements") or main
if isinstance(els, dict):
    els = els.get("elements", [])
print(f"轨道元素数: {len(els)}")

rows = []
for e in els:
    st = e.get("startTime", 0) / TICK
    dur = e.get("duration", 0) / TICK
    src = e.get("sourceDuration", 0) / TICK
    te = e.get("trimEnd", 0) / TICK
    ts = e.get("trimStart", 0) / TICK
    rows.append((e.get("id", ""), st, dur, src, ts, te, e.get("name", ""), e.get("mediaId", "")))

rows.sort(key=lambda r: r[1])
end = max(r[1] + r[2] for r in rows)
print(f"总长: {end:.2f} 秒 = {int(end//60)}分{end%60:04.1f}秒")
gaps = []
for a, b in zip(rows, rows[1:]):
    delta = b[1] - (a[1] + a[2])
    if delta > 0.02:
        gaps.append((a[6], b[6], delta))
print(f"时间线空隙: {len(gaps)} 处")
for g in gaps[:10]:
    print("   ", g)

# 源镜号覆盖
nums = []
for r in rows:
    m = re.match(r"^(\d{3})_", r[6]) or re.match(r"^(\d{1,3})[_-]", r[6])
    if m:
        nums.append(int(m.group(1)))
nums = sorted(set(nums))
print(f"\n源镜号范围: {nums[0]}..{nums[-1]}  覆盖 {len(nums)} 个")
missing = [n for n in range(1, nums[-1] + 1) if n not in nums]
print(f"时间线上没有的镜号({len(missing)}): {missing}")

print("\n逐条(镜号 | 起点 | 时长 | 裁剪 | 文件):")
for cid, st, dur, src, ts, te, name, mid in rows:
    m = re.match(r"^(\d{3})_", name) or re.match(r"^(\d{1,3})[_-]", name)
    shot = m.group(1) if m else "???"
    trim = f"裁{ts:.1f}+{te:.1f}" if (ts or te) else ""
    print(f"{shot:>4} | {st:7.2f} | {dur:5.2f} | {trim:<10} | {name}")
