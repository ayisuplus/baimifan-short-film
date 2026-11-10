"""Check the scoped storyboard revision and frozen requests."""
import json,hashlib,re,subprocess
from pathlib import Path
from urllib.parse import unquote,urlsplit
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
o=load('镜头设计/shot-plan-v0.33.json');d=load('镜头设计/shot-plan-v0.34.json')
by={s['id']:s for s in d['shots']}
assert [s['id'] for s in o['shots']]==[s['id'] for s in d['shots']]
changed=[s['id'] for s in o['shots'] if s!=by[s['id']]]
assert set(changed)=={'CY024A10','CY024A11','CY024A12'},changed
assert d['music_direction']==o['music_direction']
for s in o['shots']:
    n=by[s['id']]
    for key in ['seconds','start_second','end_second','dialogue','subtitle_cues','dialogue_cues']:
        assert s.get(key)==n.get(key),(s['id'],key)
assert len(d['shots'])==109 and d['total_seconds']==359
assert len({s['id'] for s in d['shots']})==109
idx=load(d['source_manifest']);active=[x for x in idx['records'] if x['status']=='candidate_pending_author_review']
assert len(active)==2 and len(idx['records'])==4
for row in idx['records']:
    assert sha(R/row['destination'])==row['sha256']
    assert sha(R/row['request'])==row['request_sha256']
    for inp in row['inputs']:assert sha(inp['path'])==inp['sha256']
for row in active:assert by[row['shot_id']]['presentation']['path']==row['destination']
for p in ['镜头设计/shot-plan-v0.33.json','剧本/穿云-场景剧本-v0.33.md','镜头设计/生成记录/生成索引-v033.json']:
    committed=subprocess.check_output(['git','show','b28323c:'+p],cwd=R)
    assert committed.replace(b'\r\n',b'\n')==(R/p).read_bytes().replace(b'\r\n',b'\n'),p
assert subprocess.check_output(['git','show','b28323c:镜头设计/带图分镜.html'],cwd=R).replace(b'\r\n',b'\n')==(R/'镜头设计/带图分镜-v0.33.html').read_bytes().replace(b'\r\n',b'\n')
lock=load('归档/画面封版-v016-20261022.json')
for x in lock['shots']+lock['documents']:assert sha(R/x['path'])==x['sha256']
script=(R/d['story_script']).read_text(encoding='utf-8')
assert all(s['source_quote'] in script for s in d['shots'])
links=set()
for path in [R/'镜头设计/带图分镜.html',R/'00_打开项目.html']:
    for href in re.findall(r'(?:src|href)=["\']([^"\']+)',path.read_text(encoding='utf-8')):
        if href.startswith(('#','https:','http:','data:','javascript:')):continue
        p=unquote(urlsplit(href).path)
        if p:
            target=(path.parent/p).resolve();assert target.exists(),target;links.add(str(target))
report=dict(shots=109,total_seconds=359,modified_shots=changed,image_replacements=[r['shot_id'] for r in active],attempts_preserved=4,unaffected_shots_identical=106,timing_and_dialogue_unchanged=True,approved_chant_and_music_plan_unchanged=True,previous_version_unchanged=True,old_html_snapshot_content_matches=True,git_comparison_normalizes_line_endings=True,picture_lock_files_verified=len(lock['shots'])+len(lock['documents']),local_links_verified=len(links),source_quotes_verified=109,visual_review='主代理实际查看：上行方向、飞行单叶无术光、飞行纵深与撞击侧面构图区分；仍待作者审阅。',video_produced=False,audio_produced=False,browser_playback='not_verified')
(R/'镜头设计/生成记录/扇叶上行与换机位-v034/一致性核验.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))

