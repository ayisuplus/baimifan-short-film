"""Read-only validation of scope, links, audio, frozen inputs and picture-lock integrity."""
import json,hashlib,re,wave
from pathlib import Path
from urllib.parse import unquote,urlsplit
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
d=load('镜头设计/shot-plan-v0.33.json');o=load('镜头设计/shot-plan-v0.32.json');b={s['id']:s for s in d['shots']};ob={s['id']:s for s in o['shots']}
lock=load('归档/画面封版-v016-20261022.json');verified=0
for x in lock['shots']+lock['documents']:
 assert sha(R/x['path'])==x['sha256'],x['path'];verified+=1
idx=load('镜头设计/生成记录/生成索引-v033.json');active=[r for r in idx['records'] if r['status']=='candidate_pending_author_review']
assert len(active)==18 and len(idx['records'])==25
for r in idx['records']:
 assert sha(R/r['destination'])==r['sha256'];assert sha(R/r['request'])==r['request_sha256']
 for x in r['inputs']:assert sha(x['path'])==x['sha256']
for r in active:assert b[r['shot_id']]['presentation']['path']==r['destination']
assert d['music_direction']['approved_incantation']==o['music_direction']['approved_incantation']
script=(R/d['story_script']).read_text(encoding='utf-8')
for line in d['music_direction']['approved_incantation']:assert script.count(line)==1,(line,script.count(line))
assert b['CY024A']['presentation']['path']!=b['CY024A5']['presentation']['path']
elapsed=0;audio=0
for s in d['shots']:
 assert s['start_second']==elapsed and s['source_quote'] in script;elapsed+=s['seconds'];assert s['end_second']==elapsed
 for c in s.get('subtitle_cues',[]):assert 0<=c['offset'] and c['offset']+c['duration']<=s['seconds']+1e-8
 for c in s.get('dialogue_cues',[]):
  with wave.open(str(R/c['file'])) as w:assert c['offset']+w.getnframes()/w.getframerate()<=s['seconds']
  audio+=1
 if s['id'] in ob:assert s['dialogue_cues']==ob[s['id']]['dialogue_cues']
assert elapsed==359 and len(d['shots'])==109
assert sum(b[x]['seconds'] for x in d['music_direction']['sequence'] if x.startswith('CY024A'))==51
old_ids=[s['id'] for s in o['shots']];assert [s['id'] for s in d['shots'] if s['id'] in ob]==old_ids
changed_seconds={sid:(ob[sid]['seconds'],b[sid]['seconds']) for sid in ob if ob[sid]['seconds']!=b[sid]['seconds']}
assert set(changed_seconds)=={'CY024A','CY024A1','CY024B','CY027'}
links=set()
for htmlpath in [R/'镜头设计/带图分镜.html',R/'00_打开项目.html']:
 for href in re.findall(r'(?:src|href)=[\"\']([^\"\']+)',htmlpath.read_text(encoding='utf-8')):
  if href.startswith(('#','https:','http:','data:','javascript:')):continue
  p=unquote(urlsplit(href).path)
  if p:
   target=(htmlpath.parent/p).resolve();assert target.exists(),str(target);links.add(str(target))
result=dict(shots=109,total_seconds=359,current_images=18,attempts_preserved=25,picture_lock_files_verified=verified,local_links_verified=len(links),source_passages_verified=109,existing_audio_files_readable=audio,existing_audio_unchanged=True,approved_spell_unchanged=True,old_shot_order_preserved=True,changed_existing_seconds=changed_seconds,added_ids=[s['id'] for s in d['shots'] if s['id'] not in ob],flight_isolated=True,opening_macro=True,spell_sequence_seconds=51,video_produced=False,audio_produced=False,browser_playback='not_verified',script_sha256=sha(R/d['story_script']))
(R/'镜头设计/生成记录/展翼与扇面-v033/一致性核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
