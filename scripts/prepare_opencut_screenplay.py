"""Upgrade the existing three native manuscripts to one scene, without media work."""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT.parents[1] / 'OpenCut/toolkit/compat/creative-workbench/app'
sys.path.insert(0, str(APP))
from store import Store
from screenplay import initialize_scenes


def prepare():
    out = ROOT / '后期/OpenCut导演台原型-v001'
    manifest = json.loads((out/'package/manifest.json').read_text(encoding='utf-8'))
    source = ROOT / '剧本/白米饭-场景剧本-v0.69.md'
    if hashlib.sha256(source.read_bytes()).hexdigest() != manifest['sources'][source.relative_to(ROOT).as_posix()]:
        raise ValueError('剧本来源已经变化，请先核对并更新资料包，避免混用不同版本的前后文')
    script = source.read_text(encoding='utf-8-sig')
    s02 = script.split('## S02｜',1)[1].split('## S03｜',1)[0]
    before = s02.split('\n',1)[1].split('**小鱼** · `VO-CY006-01`',1)[0].strip()
    after = '### 王宫内心戏（作者已采用）'+s02.split('### 王宫内心戏（作者已采用）',1)[1]
    sections = {}
    pattern = re.compile(r'\*\*(.+?)\*\* · `(VO-[\w-]+)`\s*\n\n> ([^\n]+)\s*\n\n中文回译：([^\n]+)')
    expected = {s['id']:s['story'] for s in manifest['shots']}
    for shot in manifest['shots']:
        blocks, position, index = [], 0, 0
        def actions(text):
            nonlocal index
            for paragraph in text.strip().split('\n\n'):
                if paragraph.strip():
                    index += 1
                    blocks.append(dict(id=shot['id']+'-action-'+str(index),type='action',text=paragraph.strip()))
        for match in pattern.finditer(shot['story']):
            actions(shot['story'][position:match.start()])
            speaker,cue,text,translation = match.groups()
            blocks.append(dict(id=cue,type='dialogue',speaker=speaker,text=text,
                               translation=translation,parenthetical='',cue_id=cue))
            position=match.end()
        actions(shot['story'][position:])
        if shot['id']=='CY007':
            blocks[0]['text']='ChatGPT看着小鱼，目光迟疑。片刻后，她认真开口。'
        sections[shot['id']]=blocks
    scene = dict(id='S02',heading='S02｜宫殿 · 黄昏 · 外转内',
        scope='本次编辑：王座厅内的求救、拒绝与追问（CY006–CY008）。前后文保留 v0.69 原文。',
        source={'path':source.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(source.read_bytes()).hexdigest()},
        before=before,after=after.strip(),sections=sections)
    store=Store(out/'导演台')
    if (store.directory / 'opencut-owner.json').exists():
        raise ValueError('本作品已迁入 OpenCut Rust，请在 OpenCut 场次面板修改；旧稿保持只读')
    p=initialize_scenes(store,manifest['id'],[scene],expected)
    return dict(revision=p['revision'],scene='S02',shots=list(sections),root=str(store.root))

if __name__=='__main__':
    print(json.dumps(prepare(),ensure_ascii=False))
