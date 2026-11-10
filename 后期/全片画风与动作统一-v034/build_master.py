"""Combine adopted segments only; fail on missing reviews rather than fill with old shots."""
import json,re
from pathlib import Path
P=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text('utf-8-sig'))
baseline=read(P.parent/'迁回达芬奇-v033/迁移剪辑清单.json')
adopted=read(P/'adopted.json') if (P/'adopted.json').exists() else {}
early=read(P/'early-video-planning.json')+read(P/'early-extra-video-planning.json')
replace={}
for x in early:replace.setdefault(x['source_shot'],[]).append(x['id'])
replace['019']=['019a','019b']
source19=next(x for x in baseline if x['name'].startswith('019_'))
adopted['019b']=dict(id='019b',source=source19['source'],source_in=64,source_out_exclusive=163,target_frames=99,review='pass',name='019b_等待与试锁_保留',note='只重绘前64帧蜡烛，原后99帧保留。')
sequence=[]
for x in baseline:
 id=f"{int(re.match(r'\d+',x['name']).group()):03}"
 if int(id)>50:continue
 if id=='033':continue
 if id in replace:
  for sub in replace[id]:sequence.append(dict({'id':sub},**adopted.get(sub,{'review':'pending'})))
 else:
  sequence.append(dict(id=id,name=x['name'],source=x['source'],source_in=x['source_in'],source_out_exclusive=x['source_out_exclusive'],target_frames=x['frames'],review='pass',note='保留此前采用剪点和表演。'))
installed=read(P/'edits/install-manifest.json')
for group in [2,3,4]:
 for x in installed[str(group)]:
  id=x['id']
  if id in adopted:row=adopted[id]
  elif id=='069':row=dict(x,review='pending',note='原升空镜需二维化并收紧为48帧；不得沿用旧102帧假称统一完成。')
  elif x['status']=='ready':row=dict(x,review='pass',name=id+'_二维修订_v034')
  else:row=dict(x,review='pending')
  sequence.append(row)
for group in [5,6,7]:
 draft=P/f'edit-group-{group:02}-draft.json'
 rows=read(draft) if draft.exists() else read(P.parent/f'后半程逐段修订-v032/group-{group:02}.json')
 for x in rows:
  id=x['id'];sequence.append(adopted.get(id,dict(id=id,review='pending')))
pending=[x['id'] for x in sequence if x.get('review')!='pass' or not x.get('source')]
(P/'master-pending.json').write_text(json.dumps(pending,ensure_ascii=False,indent=2),'utf8')
assert not pending,'Pending visual/motion review: '+', '.join(pending)
pos=0;manifest=[]
for x in sequence:
 assert Path(x['source']).is_file(),x['source']
 frames=x['target_frames'];start=x['source_in'];end=x['source_out_exclusive']
 assert end-start==frames,'Must encode retiming before Resolve import: '+x['id']
 manifest.append(dict(id=x['id'],name=x.get('name',x['id']+'_二维修订_v034'),source=x['source'],source_in=start,source_out_exclusive=end,frames=frames,start=pos,review='pass',note=x.get('note','')))
 pos+=frames
chapters={'001':'入殿与求助','010':'潜入与受阻','031':'堆柴与点火','042':'援手抵达','051':'Kimi潜入','063':'召集同伴','069':'水龙压制','086a':'化龙与决胜','093a':'解锁与选择','107':'承托与离开','114':'数日之后'}
for x in manifest:
 if x['id'] in chapters:x['chapter_start']=chapters[x['id']]
(P/'master-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),'utf8')
print(json.dumps(dict(clips=len(manifest),frames=pos,fps=24),ensure_ascii=False))
