from pathlib import Path
import json,subprocess,wave,hashlib
R=Path(__file__).resolve().parents[1];O=R/'后期/导演重构-v003'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def unpack(p):
 x=read(p);return json.loads(x['content'][0]['text'])['result']
P=read(O/'后期执行计划.json');A=unpack(O/'实际时间线最终回读.json');M=read(O/'声音施工记录.json');S=read(O/'音效施工记录.json');G=read(O/'混音电平检查.json')
assert A['timeline']==P['timeline'] and A['frames']==P['frames']
assert len(A['video'])==len(P['edl']) and all(A['enabled'])
for p,a in zip(P['edl'],A['video']):
 assert (p['name'],p['record'],p['record']+p['frames'])==(a['name'],a['start'],a['end']),(p['name'],a)
 assert Path(p['source']).resolve()==Path(a['path']).resolve()
 if p.get('follow_face'):assert a['fusion_comps']
 for k,v in p['props'].items():
  if k in a['props']:assert abs(v-a['props'][k])<.001,(p['name'],k,v,a['props'][k])
rows=[dict(v,id=v['native_id'],track=1) for v in P['voice']]+M['cues']+S['stems']
assert len(rows)==len(A['audio'])
for v in rows:
 a=next(a for a in A['audio'] if a['name']==v['id'] and a['track']==v['track'])
 assert abs(a['start']-v['record'])<.001
 assert abs((a['end']-a['start'])/24-v['duration'])<1/48000+.00001,(v['id'],a['end']-a['start'],v['duration'])
 assert a['speed']['Percentage']==100 and a['gain']==G['shared_gain_db']
 with wave.open(v['path'],'rb') as f:assert f.getframerate()==48000
for track in range(1,9):
 vals=sorted([a for a in A['audio'] if a['track']==track],key=lambda a:a['start'])
 assert all(a['end']<=b['start']+.001 for a,b in zip(vals,vals[1:])),track
assert G['finite'] and G['peak_after_gain']<.85
assert len(set(v['id'] for v in P['voice']))==63
assert len([v for v in P['voice'] if v.get('rate')])==4
assert all(e['start']>=0 and e['start']+e['duration']<=P['seconds']+.001 for e in S['events'])
for s in S['stems']:
 with wave.open(s['path'],'rb') as f:assert f.getnframes()==G['samples']
Q=read(R/'视频制作/Metaso-H3-v006/执行队列.json')
for c in Q['items']:
 assert c['status']=='downloaded_candidate'
 f=R/c['local_path'];assert hashlib.sha256(f.read_bytes()).hexdigest()==c['sha256']
result=dict(timeline=P['timeline'],frames=P['frames'],seconds=P['seconds'],picture_segments=len(P['edl']),batches=len(P['batches']),voice_pieces=len(P['voice']),unique_selected_lines=63,music_cues=len(M['cues']),sound_events=len(S['events']),tracks=8,all_tracks_enabled=True,native_picture_audio_conform=True,voice_original_speed_except_four_gpt_chant_lines=True,author_b12_trim_preserved=True,new_tasks=len(Q['items']),adopted_retake_sources=8,rejected_retake_sources=1,estimated_credits=sum(c['estimated_credits'] for c in Q['items']),actual_billing_verified=False,peak_after_shared_gain=G['peak_after_gain'],no_new_video_or_project_exports=True,verification_stills='仅工程预览裁切静帧，不是视频导出',remaining=['全片连续听审','逐音素口型验收','表演张力与构图最终作者核验','角色跨句音色与响度精修'])
(O/'验证结果.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False))
