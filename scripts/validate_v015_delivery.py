"""Verify v015 files, timeline, original source integrity, and local links."""
import json,hashlib
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
root=Path(__file__).resolve().parents[1]
def read(p):return json.loads((root/p).read_text(encoding='utf8'))
old=read('镜头设计/shot-plan-v0.14.json')
new=read('镜头设计/shot-plan-v0.15.json')
choices=read('镜头设计/生成记录/动作收尾-v015/采用映射.json')
script=(root/new['story_script']).read_text(encoding='utf8')
oldby={s['id']:s for s in old['shots']}
assert [s['id'] for s in new['shots'] if s['id']!='CY022A1']==list(oldby)
assert len(new['shots'])==90 and new['total_seconds']==289
assert len(choices)==17
ids=[s['id'] for s in new['shots']]
assert ids[ids.index('CY021B'):ids.index('CY022')+1]==['CY021B','CY021A','CY022A','CY022A1','CY022']
elapsed=0;unchanged=0
for s in new['shots']:
 assert s['source_quote'] in script,s['id']
 assert s['panel_rect_pixels']==[0,0,*s['page_size']]
 assert s['start_second']==elapsed
 elapsed+=s['seconds']
 assert s['end_second']==elapsed
 assert (root/s['presentation']['path']).is_file()
 if s['id'] in oldby:
  assert s['seconds']==oldby[s['id']]['seconds']
 if s['id'] not in choices:
  assert s['presentation']['path']==oldby[s['id']]['presentation']['path'];unchanged+=1
 else:
  assert s['generation_request'].endswith(f"-v{choices[s['id']]:03d}.json")
assert elapsed==289 and unchanged==73
records=read('镜头设计/生成记录/动作收尾-v015/结果映射.json')
for r in records:
 assert hashlib.sha256((root/r['destination']).read_bytes()).digest()==hashlib.sha256(Path(r['original']).read_bytes()).digest()
checked=[]
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ('href','src') and v:
    link=urlsplit(v)
    if link.scheme or not link.path:continue
    p=(self.page.parent/unquote(link.path)).resolve()
    assert p.exists(),(self.page,v)
    checked.append(str(p))
for rel in ('00_打开项目.html','镜头设计/带图分镜.html','资产/资产图册.html'):
 parser=Links();parser.page=root/rel;parser.feed(parser.page.read_text(encoding='utf8'))
result=dict(version='v015',shots=90,seconds=elapsed,changed_shots=17,unchanged_images=unchanged,source_quotes_verified=90,full_frame_images=90,checked_local_links=len(checked),archived_images_verified=len(records),old_music_roughcut='v002 unchanged',dynamic_review='not performed')
(root/'镜头设计/生成记录/交付核验-v015.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(result,ensure_ascii=False))
