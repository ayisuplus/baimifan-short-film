"""Validate the v022 candidate ledger and an isolated local choice service."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text('utf-8-sig'))
def digest(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
manifest=read('后期/配音挑选-v022/候选索引.json')
old=read('视频制作/生成板-v021/日语音频映射.json')['cues']
cues={c['id']:c for c in manifest['cues']}
assert len(cues)==len(old)==63
for x in old:
    c=cues[x['cue_id']]
    assert c['shot']==x['shot_id'] and c['ja']==x['text'] and c['visual_shots']==x['visual_shots']
    assert c['start']==x['timeline_start'] and c['end']==x['timeline_end']
    assert c['current_path']==x['path'] and sum(o['path']==x['path'] for o in c['options'])==1
    for o in c['options']:
        assert (ROOT/o['path']).is_file() and digest(o['path'])==o['sha256'] and o['seconds']>0
for g in manifest['groups']:
    assert all(c in cues for c in g['members'])
    for o in g['options']: assert (ROOT/o['path']).is_file() and digest(o['path'])==o['sha256']
spell=cues['VO-CY024A5-02']
assert any('v002 沧龙出海' in o['label'] and o['selectable'] for o in spell['options'])
assert any('v001' in o['label'] and not o['selectable'] and '旧版术名' in o['note'] for o in spell['options'])
assert len(cues['VO-CY008M-01']['options'])>=2 and len(cues['VO-CY008M-02']['options'])>=2
assert len(cues['VO-CY024K1A-01']['options'])>=4
assert len(cues['VO-CY021-01']['visual_shots'])==2 and len(cues['VO-CY024A9-01']['visual_shots'])==5
oldboard=(ROOT/'视频制作/生成板-v021/生成板.html').read_text('utf-8')
newboard=(ROOT/'视频制作/生成板-v022/生成板.html').read_text('utf-8')
def data(s):
    marker='<script id="data" type="application/json">';a=s.index(marker)+len(marker);return json.loads(s[a:s.index('</script>',a)])
o,n=data(oldboard),data(newboard)
assert len(o['batches'])==len(n['batches'])==43
for a,b in zip(o['batches'],n['batches']):
    assert a['id']==b['id'] and a['prompts']==b['prompts'] and a['film_start']==b['film_start'] and a['film_end']==b['film_end']
    assert all('returned_audio' not in d for d in b['dialogue'])
    for name in a['prompts']:
        f=a['id']+'-'+name+'.txt'
        assert (ROOT/'视频制作/生成板-v021/提示词'/f).read_bytes()==(ROOT/'视频制作/生成板-v022/提示词'/f).read_bytes()
assert '<audio controls' not in newboard and '在预演版比较这句配音' in newboard
print('Ledger: 63 cues,',sum(len(x['options']) for x in cues.values()),'single-line candidates,',sum(len(g['options']) for g in manifest['groups']),'whole-take candidates; hashes and v021 inputs preserved')

if len(sys.argv)>1:
    port=int(sys.argv[1]);base=f'http://127.0.0.1:{port}';api=base+'/api/voice-choices-v022'
    def post(kind,key,opt,origin=True):
        headers={'Content-Type':'application/json'}
        if origin:headers['Origin']=base
        req=Request(api,data=json.dumps(dict(kind=kind,key=key,option_id=opt)).encode(),headers=headers,method='POST')
        try:
            with urlopen(req,timeout=5) as r:return r.status,json.load(r)
        except HTTPError as e:return e.code,json.load(e)
    assert post('cue','VO-CY003-01',cues['VO-CY003-01']['options'][0]['id'],False)[0]==403
    assert post('cue','VO-CY003-01','forged')[0]==400
    bad=next(o for o in spell['options'] if not o['selectable'])
    assert post('cue',spell['id'],bad['id'])[0]==400
    targets=list(cues.values())[:12]
    with ThreadPoolExecutor(max_workers=6) as pool:
        responses=list(pool.map(lambda c:post('cue',c['id'],next(o for o in c['options'] if o['selectable'])['id']),targets))
    assert all(code==200 for code,_ in responses)
    with urlopen(api,timeout=5) as r: state=json.load(r)
    assert all(c['id'] in state['cue_choices'] for c in targets)
    group=manifest['groups'][0];assert post('group',group['id'],group['options'][1]['id'])[0]==200
    with urlopen(api,timeout=5) as r:state=json.load(r)
    assert state['group_choices'][group['id']]['option_id']==group['options'][1]['id']
    for c in targets: assert post('cue',c['id'],None)[0]==200
    assert post('group',group['id'],None)[0]==200
    print('Isolated server: origin/choice rejection, concurrent save and group/clear passed')
