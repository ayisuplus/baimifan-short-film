"""Render the complete v0.68 review script from its JSON; no media calls."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / '剧本/白米饭-日语对白-v0.68.json'
d = json.loads(DATA.read_text(encoding='utf-8'))
rows = d['lines']
by_id = {r['id']: r for r in rows}
active = [r for r in rows if r['ja']]
assert len(by_id) == len(rows) == 64
assert len(active) == 54
assert all(r['zh_back_translation'] for r in active)
for r in rows:
    if r['status'] == 'merged_not_spoken':
        assert by_id[r['merged_into']]['ja']
assert sum(len(r['ja']) for r in active) == d['statistics']['active_characters']

out = ['# 《白米饭》完整日语台词稿 v0.68', '',
       '**情境、魔法救场与Kimi呼唤修改已合入，整稿待作者复看。日语为主稿，中文为回译。未生成配音，未替换正片。**', '',
       '相对v0.66：开场感谢改由动作截断，教徒改为交接命令；GPT拒绝体现守约选择，内心争执缩短；Kimi呼唤古老意志并恢复完整醒来反应。教堂以魔法处决与水击救场替代列队展示，不增加教主刀具。完整动作见[场景剧本v0.68](白米饭-场景剧本-v0.68.md)。', '',
       '全稿54句可朗读台词。原63个ID全部保留，新增1个ID；9条历史台词合并、1条路线说明不再朗读。下文只展示当前可朗读台词，历史停用记录列在文末。批次沿旧片定位，不代表新配音剪点。', '',
       '主数据：同目录 `白米饭-日语对白-v0.68.json`。本阅读稿由主数据生成；表演、动作和读音说明不属于朗读正文。', '',
       '## 完整台词（影片叙事顺序）', '']
last_batch = None
for r in active:
    batch = r.get('batch', r['previous_batch'])
    if batch != last_batch:
        out += [f'### 第{batch}批', '']
        last_batch = batch
    state = '新增' if r['status'] == 'new_draft' else ('修订' if r['status'] == 'revised_draft' else '保留')
    out += [f"**{r['role']}** · `{r['id']}` · {state}", '',
            '> ' + r['ja'], '', '中文回译：' + r['zh_back_translation'], '']
    if r['direction'] != '沿场景意图表演；停顿以新试听为准，不沿用旧录音速度或硬套原剪点。':
        out += ['表演／动作：' + r['direction'], '']
    if r['reading_hints']:
        out += ['读音：' + '；'.join(f'{k}＝{v}' for k, v in r['reading_hints'].items()) + '。', '']
    for bridge in d['action_bridges']:
        if bridge['after_id'] == r['id']:
            out += ['*无台词过渡：' + bridge['action_zh'] + '*', '']

out += ['## 咏唱节奏说明（非朗读正文）', '']
for role, group in d['groups'].items():
    budget = group['spoken_budget_seconds']
    label = f'口播目标约{budget[0]}–{budget[1]}秒，只是表演预算，未经新配音实测。' if budget else '新呼唤的口播时长待试读。'
    out += [f'**{role}**：' + label + group['scene_budget_note'], '']
out += ['Kimi：举刃蓄力、投刃破窗、明刃钉稳后报术名，再瞬移与回收；护罩为之后的独立动作。', '',
        'GPT：「炎を鎮め、」「罪なき者に、救いを――」作为连续祈愿，不能各自拉成长停顿。术名后释放主龙；敌方金罩与水龙攻击的动作仍保留。', '',
        'Claude：父亲在首句后打断。她选择继续，才说「この手に、宿れ。」；不从头起咏。束具已解，光屑、火种、空刑架起火、脱力依次发生。', '',
        '## 历史停用台词（不朗读）', '', '| ID | 处理 | 原因 |', '|---|---|---|']
for r in rows:
    if r['ja'] is None:
        target = '合并至 ' + r['merged_into'] if r.get('merged_into') else '删除口播；保留原文与ID追踪'
        out += [f"| {r['id']} | {target} | {r['direction']} |"]
out += ['', '## 审阅状态', '',
        '作者已同意情境与救场方向，并明确教主改用魔法；完整稿仍待本次整体复看。未调用ElevenLabs、本地克隆或任何配音生成，也未修改选声、画面、达芬奇时间线。语速、声线、口型和连续听感尚不能由文字稿验收。', '',
        '配音前按角色统一声线，按场景与表演段组织；逐句ID保留。显示正文字符统计仅供参考，不等于服务计费字符或实际录音时长。', '']
DATA.with_suffix('.md').write_text('\n'.join(out), encoding='utf-8')
print(f"Rendered {len(active)} spoken cues from {len(rows)} stable records.")

# Both review documents use the same Japanese and Chinese source.
import re
template = (ROOT / d['source_scene_template']).read_text(encoding='utf-8')
cue_ids = re.findall(r'\{\{cue:([^}]+)\}\}', template)
assert cue_ids == [r['id'] for r in active], 'Scene and dialogue cue order differs'
def render_cue(match):
    row = by_id[match.group(1)]
    return f"**{row['role']}** · `{row['id']}`\n\n> {row['ja']}\n\n中文回译：{row['zh_back_translation']}"
scene = re.sub(r'\{\{cue:([^}]+)\}\}', render_cue, template)
assert '{{cue:' not in scene
(ROOT / d['source_script']).write_text(scene, encoding='utf-8')
print('Rendered complete six-scene script from the same 54 dialogue records.')
