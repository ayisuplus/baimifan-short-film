"""Retain unchanged audio design and matching Kimi response after the v041 rewrite."""
import copy,json,hashlib,wave,shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text('utf-8-sig'))
def save(p,d):(R/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p='镜头设计/shot-plan-v0.41.json';d=load(p);old=load('镜头设计/shot-plan-v0.40.json')
by={s['id']:s for s in d['shots']};ob={s['id']:s for s in old['shots']}
rec='镜头设计/生成记录/月刃救援-v041/'
img='镜头设计/图像/月刃救援-v041/'
target=img+'CY024A4-v041-r2.png'
if not (R/target).exists():
 shutil.copy2(Path('C:/Users/36322/.codex/generated_images/01a16925-a797-71a2-9c39-4f481f8b65a6/exec-14b4b47b-c2b3-41aa-95fa-98d7dac41b96.png'),R/target)
index=load(d['source_manifest'])
for sid,request in [('CY024A4','固定脚托修正请求.json'),('CY024K0','护罩与试镣实际请求-站姿约束.json'),('CY024K2','护罩与试镣实际请求-站姿约束.json')]:
 s=by[sid];rows=load(rec+request)
 if isinstance(rows,dict):rows=[rows]
 row=next(x for x in rows if x['id']==sid)
 path=target if sid=='CY024A4' else s['presentation']['path']
 prior=s['presentation']['path']
 if prior!=path:s['refs'].append(dict(path=prior,role='历史修订候选，固定脚托结构已修正'))
 s['presentation']['path']=path
 s['refs']=[x for x in s['refs'] if x['role'] not in ['当前修订候选','实际生成请求']]
 s['refs'][:0]=[dict(path=path,role='当前修订候选'),dict(path=rec+request,role='实际生成请求')]
 s.update(visual_prompt=row['prompt'],generation_request=rec+request)
 with Image.open(R/path) as im:w,h=im.size
 s.update(page_size=[w,h],panel_rect_pixels=[0,0,w,h])
 ix=next(x for x in index['images'] if x['id']==sid)
 ix.update(path=path,sha256=hashlib.sha256((R/path).read_bytes()).hexdigest(),size=[w,h],request=rec+request,
           inputs=[dict(path=q,sha256=hashlib.sha256((R/q).read_bytes()).hexdigest()) for q in row['refs']])
note='CY024A4r1独立凳腿错误，改r2固定脚托'
if note not in index['not_used']:index['not_used'].append(note)
save(d['source_manifest'],index)
script=(R/d['story_script']).read_text('utf-8-sig')
before='再打开最后一个腕扣；符纹没有被暴力触发。'
after='再依次打开两只腕扣；最后一扣解除前GPT已经扶稳，符纹没有被暴力触发。'
for field in ['action','source_quote']:by['CY027G'][field]=by['CY027G'][field].replace(before,after)
(R/d['story_script']).write_text(script.replace(before,after),encoding='utf-8')
for sc in d['scenes']:
 ss=[s for s in d['shots'] if s['scene']==sc['id']]
 sc['pages']=list(dict.fromkeys(s['presentation']['path'] for s in ss))
d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
cues=copy.deepcopy(ob['CY026D']['dialogue_cues'])
for c in cues:
 c['offset']=5.7
 with wave.open(str(R/c['file'])) as w:assert c['offset']+w.getnframes()/w.getframerate()<=7
by['CY026D']['dialogue_cues']=cues
by['CY026D']['sound']='新增GPT分路交代待配音；沿用Kimi同一句“嗯”的既有临时读稿，移至5.7秒；月背微风。'
d['continuity']['audio']='保留19段既有临时读稿；Kimi“嗯”移至CY026D的5.7秒，新增GPT分路对白与Kimi画外短咏仅有字幕，配音待制作。未将旧音轨冒用为新台词；正式声音与实际听审待完成。'
# Keep unaffected shots free of unrelated new global ritual rules.
for s in d['shots']:
 if s['scene'] in ['S01','S02','S06']:s['invariants']=copy.deepcopy(ob[s['id']]['invariants'])
save(p,d)
a=load(d['audio_arrangement']);oa=load(old['audio_arrangement'])
changed=set(d['revision_notes']['modified_image_ids'])|{'CY026D','CY027F1','CY027G','CY024A0','CY024A5'}
for s in d['shots']:
 a['effects'][s['id']]=s['sound'] if s['id'] in changed or s['id'] not in ob else oa['effects'][s['id']]
a['shot_plan_sha256']=hashlib.sha256((R/p).read_bytes()).hexdigest();save(d['audio_arrangement'],a)
print('Retained matching response audio and unaffected sound designs.')
