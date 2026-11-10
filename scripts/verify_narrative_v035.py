"""Validate v035 scope, source quotations, lineage and audio preservation."""
import json,hashlib,subprocess,re,wave
from pathlib import Path
from urllib.parse import unquote,urlsplit
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
d=load('镜头设计/shot-plan-v0.35.json');o=load('镜头设计/shot-plan-v0.34.json')
by={s['id']:s for s in d['shots']};ob={s['id']:s for s in o['shots']}
assert len(by)==114 and d['total_seconds']==379
assert [s['id'] for s in d['shots'] if s['id'] in ob]==[s['id'] for s in o['shots']]
assert set(by)-set(ob)=={'CY027D0','CY029E1','CY029E2','CY029E3','CY029E4'}
assert d['music_direction']==o['music_direction']
for sid in ['CY024A10','CY024A11','CY024A12']:
    for k in ob[sid]:
        if k not in ['start_second','end_second']:assert by[sid][k]==ob[sid][k],(sid,k)
changed_durations={sid:(s['seconds'],by[sid]['seconds']) for sid,s in ob.items() if s['seconds']!=by[sid]['seconds']}
assert changed_durations=={'CY022B':(2,3),'CY029B1':(2,3)},changed_durations
for sid,s in ob.items():
    assert by[sid]['dialogue_cues']==s['dialogue_cues']
    if sid!='CY029B1':
        assert by[sid]['dialogue']==s['dialogue'],sid
        assert by[sid].get('subtitle_cues',[])==s.get('subtitle_cues',[]),sid
script=(R/d['story_script']).read_text(encoding='utf-8')
elapsed=0;audio=0
for s in d['shots']:
    assert s['source_quote'] in script,s['id']
    assert s['start_second']==elapsed;elapsed+=s['seconds'];assert s['end_second']==elapsed
    for c in s.get('subtitle_cues',[]):assert c['offset']>=0 and c['offset']+c['duration']<=s['seconds']
    for c in s['dialogue_cues']:
        with wave.open(str(R/c['file'])) as w:assert c['offset']+w.getnframes()/w.getframerate()<=s['seconds']
        audio+=1
assert elapsed==379
seq=d['star_incantation']['sequence']
assert sum(by[sid]['seconds'] for sid in seq)==18
assert ''.join(c['text'] for sid in seq for c in by[sid]['subtitle_cues'])==d['star_incantation']['text']
assert all(script.count(c['text'])==1 for sid in seq[:-1] for c in by[sid]['subtitle_cues'])
idx=load(d['source_manifest']);active=[r for r in idx['records'] if r['status']=='candidate_pending_author_review']
assert len(active)==15 and len(idx['records'])==16
for r in idx['records']:
    assert sha(R/r['destination'])==r['sha256'];assert sha(R/r['request'])==r['request_sha256']
    for x in r['inputs']:assert sha(x['path'])==x['sha256']
for r in active:assert by[r['shot_id']]['presentation']['path']==r['destination']
lock=load('归档/画面封版-v016-20261022.json')
for x in lock['shots']+lock['documents']:assert sha(R/x['path'])==x['sha256']
for p in ['镜头设计/shot-plan-v0.34.json','剧本/穿云-场景剧本-v0.34.md','镜头设计/生成记录/生成索引-v034.json']:
    data=subprocess.check_output(['git','show','b6b96dc:'+p],cwd=R)
    assert data.replace(b'\r\n',b'\n')==(R/p).read_bytes().replace(b'\r\n',b'\n')
links=set()
for hp in [R/'镜头设计/带图分镜.html',R/'00_打开项目.html']:
    for url in re.findall(r'(?:src|href)=["\']([^"\']+)',hp.read_text(encoding='utf-8')):
        if url.startswith(('#','https:','http:','data:','javascript:')):continue
        p=unquote(urlsplit(url).path)
        if p:
            path=(hp.parent/p).resolve();assert path.exists(),path;links.add(str(path))
report=dict(shots=114,total_seconds=379,star_incantation_seconds=18,star_incantation_single_read=True,added_ids=sorted(set(by)-set(ob)),changed_old_durations=changed_durations,old_order_preserved=True,gpt_chant_and_music_unchanged=True,fan_sequence_unchanged=True,existing_audio_unchanged=True,existing_audio_readable=audio,source_quotes_verified=114,current_images=15,attempts_preserved=16,picture_lock_files_verified=len(lock['shots'])+len(lock['documents']),local_links_verified=len(links),previous_version_content_unchanged=True,line_endings_normalized_for_git_comparison=True,video_produced=False,audio_produced=False,browser_playback='not_verified')
(R/'镜头设计/生成记录/末轮叙事优化-v035/一致性核验.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))

