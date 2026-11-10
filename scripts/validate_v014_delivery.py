"""Validate the v014 delivery links, continuity metadata and preservation."""
import json, hashlib
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
root=Path(__file__).resolve().parents[1]
def read(p):return json.loads((root/p).read_text(encoding='utf-8'))
old=read('镜头设计/shot-plan-v0.13.json')
new=read('镜头设计/shot-plan-v0.14.json')
choices=read('镜头设计/生成记录/天瀑空间-v014/采用映射.json')
script=(root/new['story_script']).read_text(encoding='utf-8')
assert [s['id'] for s in old['shots']]==[s['id'] for s in new['shots']]
assert [s['seconds'] for s in old['shots']]==[s['seconds'] for s in new['shots']]
assert len(new['shots'])==89 and sum(s['seconds'] for s in new['shots'])==286
unchanged=[]
for a,b in zip(old['shots'],new['shots']):
 assert b['source_quote'] in script,b['id']
 assert b['panel_rect_pixels']==[0,0,*b['page_size']],b['id']
 assert (root/b['presentation']['path']).is_file(),b['id']
 if b['id'] not in choices:
  assert a['presentation']['path']==b['presentation']['path']
  unchanged.append(b['id'])
 else:
  assert b['generation_request'].endswith(f"-v{choices[b['id']]:03d}.json")
checked=[]
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ('href','src') and v:
    link=urlsplit(v)
    if link.scheme or not link.path:continue
    p=(self.page.parent/unquote(link.path)).resolve()
    assert p.exists(),(self.page,v)
    checked.append({'page':str(self.page.relative_to(root)),'target':str(p)})
for rel in ('00_打开项目.html','镜头设计/带图分镜.html','资产/资产图册.html'):
 parser=Links();parser.page=root/rel;parser.feed(parser.page.read_text(encoding='utf-8'))
records=read('镜头设计/生成记录/天瀑空间-v014/结果映射.json')
for r in records:
 assert hashlib.sha256((root/r['destination']).read_bytes()).digest()==hashlib.sha256(Path(r['original']).read_bytes()).digest()
result={'version':'v014','shots':89,'seconds':286,'changed_shots':len(choices),'unchanged_images':len(unchanged),'source_quotes_verified':89,'full_frame_images':89,'checked_local_links':len(checked),'archived_images_verified':len(records),'dynamic_review':'not performed','old_music_roughcut':'v002 unchanged'}
(root/'镜头设计/生成记录/交付核验-v014.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
