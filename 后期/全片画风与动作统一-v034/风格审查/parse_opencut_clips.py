"""解析 OpenCut 全片工程的片段清单，输出铺片概览。"""
import json
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else r"E:\projects\内容创作\故事短片\白米饭\后期\全片画风与动作统一-v034\风格审查\opencut-clips.json")
data = json.loads(P.read_text(encoding="utf-8"))
val = data.get("value", data)
binds = val.get("bindings", [])
print(f"片段数: {len(binds)}")

ms = 0
rows = []
for b in binds:
    e = b["element"]
    dur = e["duration"] / 1_000_000
    st = e["startTime"] / 1_000_000
    src = e.get("sourceDuration", 0) / 1_000_000
    trim_s = e.get("trimStart", 0) / 1_000_000
    trim_e = e.get("trimEnd", 0) / 1_000_000
    rows.append((b["context_id"], st, dur, src, trim_s, trim_e, e.get("name", ""), e.get("mediaId", "")))
    ms = max(ms, st + dur)
print(f"时间线总长: {ms:.1f} 秒 = {ms/60:.2f} 分钟")

print("\n镜号 | 起点(s) | 时长(s) | 源长(s) | 裁头 | 裁尾 | 文件")
for cid, st, dur, src, ts, te, name, mid in rows:
    print(f"{cid} | {st:7.1f} | {dur:6.1f} | {src:7.1f} | {ts:5.1f} | {te:5.1f} | {name}")

# 媒体库
for key in ("media", "assets", "mediaLibrary"):
    if key in val:
        print(f"\n{key}: {len(val[key])} 项")
        break
else:
    print("\n本文件不含媒体库")
