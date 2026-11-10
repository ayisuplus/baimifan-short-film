"""Validate v016 scope, continuity, timings, images and local links."""
import json,hashlib
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
root=Path(__file__).resolve().parents[1]
def read(p):return json.loads((root/p).read_text(encoding='utf8'))
old=read('镜头设计/shot-plan-v0.15.json');new=read('镜头设计/shot-plan-v0.16.json')
before={s['id']:s for s in old['shots']}
assert [s['id'] for s in new['shots'] if s['id']!='CY022B1']==list(before)
assert len(new['shots'])==91 and new['total_seconds']==292
ids=[s['id'] for s in new['shots']];i=ids.index('CY022B')
assert ids[i:i+5]==['CY022B','CY022B1','CY026','CY022C','CY023']
script=(root/new['story_script']).read_text(encoding='utf8')
unchanged=0;elapsed=0
for s in new['shots']:
 assert s['source_quote'] in script
 assert (root/s['presentation']['path']).is_file()
 assert s['panel_rect_pixels']==[0,0,*s['page_size']]
 assert s['start_second']==elapsed
 elapsed+=s['seconds'];assert s['end_second']==elapsed
 if s['id'] in before:
  assert s['seconds']==before[s['id']]['seconds']
  if s['id']!='CY027D':
   assert s['presentation']['path']==before[s['id']]['presentation']['path'];unchanged+=1
assert unchanged==89 and elapsed==292
records=read('镜头设计/生成记录/收工补镜-v016/结果映射.json')
assert len(records)==2
for r in records:
 assert hashlib.sha256((root/r['destination']).read_bytes()).digest()==hashlib.sha256(Path(r['original']).read_bytes()).digest()
checked=[]
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ('href','src') and v:
    u=urlsplit(v)
    if u.scheme or not u.path:continue
    p=(self.page.parent/unquote(u.path)).resolve();assert p.exists(),(self.page,v)
    checked.append(str(p))
for rel in ('00_打开项目.html','镜头设计/带图分镜.html','资产/资产图册.html'):
 parser=Links();parser.page=root/rel;parser.feed(parser.page.read_text(encoding='utf8'))
result=dict(version='v016',shots=91,seconds=elapsed,added_shots=['CY022B1'],revised_images=['CY027D'],unchanged_images=89,source_quotes_verified=91,checked_local_links=len(checked),archived_images_verified=2,dynamic_review='pending',old_music_roughcut='v002 unchanged')
(root/'镜头设计/生成记录/交付核验-v016.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(result,ensure_ascii=False))
