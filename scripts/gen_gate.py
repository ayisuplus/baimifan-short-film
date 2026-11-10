"""One gate for every ComfyUI/GPU submission path.

`当前制作状态.json` 的 `status` 决定是否允许提交生成任务：
只有显式写成 `active` 才放行，其余取值（`paused`、`archived`、缺失、写错）一律拒绝——缺省即拒绝。

2026-11-03 起本项目为 `archived`（定档）：任何生成、回装、导出都必须由作者重新开口，
并先按 `交接/定档说明.md` 第五节改状态与记录，再运行提交脚本。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / '当前制作状态.json'
ALLOWED_STATUS = 'active'


def current_status():
    if not STATE.exists():
        return None
    return json.loads(STATE.read_text('utf8')).get('status')


def assert_generation_allowed():
    status = current_status()
    assert status == ALLOWED_STATUS, (
        'Generation blocked: 当前制作状态.json status=%r, only %r permits submission. '
        'Resume explicitly first (see 交接/定档说明.md 第五节).' % (status, ALLOWED_STATUS))
    return True
