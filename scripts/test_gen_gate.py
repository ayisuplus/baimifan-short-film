"""Self-check for the generation gate. Run: python scripts/test_gen_gate.py

无外部依赖，只用临时文件模拟状态，不改动真实的 当前制作状态.json。
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_gate

FAILS = []


def check(label, ok):
    print(('PASS  ' if ok else 'FAIL  ') + label)
    if not ok:
        FAILS.append(label)


def blocks(label, value):
    """Write a temp state file with `value` as status; the gate must refuse."""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / '当前制作状态.json'
        if value is not None:
            p.write_text(json.dumps({'status': value}, ensure_ascii=False), 'utf8')
        gen_gate.STATE = p
        try:
            gen_gate.assert_generation_allowed()
        except AssertionError:
            check(label + ' -> rejected', True)
        else:
            check(label + ' -> rejected', False)
        finally:
            gen_gate.STATE = gen_gate.ROOT / '当前制作状态.json'


def allows(label, value):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / '当前制作状态.json'
        p.write_text(json.dumps({'status': value}, ensure_ascii=False), 'utf8')
        gen_gate.STATE = p
        try:
            gen_gate.assert_generation_allowed()
            check(label + ' -> allowed', True)
        except AssertionError:
            check(label + ' -> allowed', False)
        finally:
            gen_gate.STATE = gen_gate.ROOT / '当前制作状态.json'


# 1. Real project state must be archived and must block generation.
real = json.loads((gen_gate.ROOT / '当前制作状态.json').read_text('utf8'))
check('真实状态 status=archived', real.get('status') == 'archived')
try:
    gen_gate.assert_generation_allowed()
    check('真实状态被闸门拒绝', False)
except AssertionError as e:
    check('真实状态被闸门拒绝', 'archived' in str(e))

# 2. Only an explicit opt-in passes; everything else fails closed.
allows('status=active', 'active')
blocks('status=paused', 'paused')
blocks('status=archived', 'archived')
blocks('status 缺失', None)
blocks('status 拼错', 'Active')

print('\n%d checks failed' % len(FAILS))
sys.exit(1 if FAILS else 0)
