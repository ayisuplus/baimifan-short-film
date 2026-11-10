"""分析 OpenCut 全片工程：时间线绑定 / 媒体文件 / 分镜板覆盖。"""
import json
import pathlib
import re
from collections import defaultdict

P = pathlib.Path(r"E:\projects\内容创作\OpenCut\.local\project-backups\baimifan-fullfilm-v035-20261101-r2\creative\legacy\history\000012.json")
d = json.loads(P.read_text(encoding="utf-8"))

files = d.get("files", [])
print(f"files 条目: {len(files)}")
if files:
    print("file[0] keys:", list(files[0].keys()))
    print("file[0]:", json.dumps(files[0], ensure_ascii=False)[:400])

names = defaultdict(list)
for f in files:
    for k in ("name", "path", "source_path", "url", "file_name", "filename"):
        v = f.get(k)
        if isinstance(v, str) and v:
            names[v].append(f)
            break

hits = [f for f in files if "登阶与守卫放行" in json.dumps(f, ensure_ascii=False)]
print("\n匹配 '登阶与守卫放行':")
for h in hits[:3]:
    print(json.dumps(h, ensure_ascii=False)[:600])

board = d["presentation"]["board"]
shots = board["shots"]
print(f"\n分镜板镜头数: {len(shots)}")
print("前 12 镜 id/title:")
for s in shots[:12]:
    print(f"  {s['id']:>8} {s.get('title','')[:24]:<26} {s.get('start')}-{s.get('end')}")

# 分镜板 id 数字 vs 时间线文件名前缀
ids = [s["id"] for s in shots]
nums = sorted(int(m.group(1)) for i in ids if (m := re.search(r"(\d+)$", i)))
print(f"\n分镜编号范围: {nums[0]}..{nums[-1]}  共 {len(nums)}，缺号:",
      [n for n in range(nums[0], nums[-1] + 1) if n not in nums])
