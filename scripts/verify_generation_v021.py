"""Check audio conservation and every authored clock in the current deliverable."""
import json,re,hashlib
from pathlib import Path
from prepare_generation_v021 import ROOT,OUT,FIX,SOURCE,BASE,load,write,sha

def near(a,b):assert abs(a-b)<.00003,(a,b)
def main():
 src=load(SOURCE);old=load(BASE);sm={s['id']:s for s in src['shots']}
 board=load(OUT+'/展开数据.json');vp=load(FIX+'/配音对位方案.json');mix=load(FIX+'/实际BGM剪辑.json')
 facts={x['cue_id']:x for x in load(FIX+'/音频实测.json')};tc={c['id']:c for c in vp['cues']};ev={e['cue_id']:e for e in vp['mix_events']}
 assert len(tc)==len(ev)==len(facts)==63
 assert board['source_sha256']==vp['source_sha256']==mix['source_sha256']==sha(SOURCE)
 assert [s['id'] for s in src['shots']]==[s['id'] for s in old['shots']]
 assert all(a['presentation']==b['presentation'] and a['refs']==b['refs'] for a,b in zip(old['shots'],src['shots']))
 assert [s for b in board['batches'] for s in b['shot_ids']]==list(sm)
 seen=[]
 for b in board['batches']:
  assert b['used_seconds']<=15+.00001 and b['models'][b['selected_model']]['capacity_ok']
  for m,text in b['prompts'].items():assert (ROOT/OUT/'提示词'/f'{b["id"]}-{m}.txt').read_text('utf-8').strip()==text.strip()
  for ref in b['references']:assert sha(ref['path'])==ref['sha256']
  for d in b['dialogue']:
   a=d['returned_audio'];cid=a['cue_id'];seen.append(cid);c=tc[cid];e=ev[cid];f=facts[cid]
   near(b['film_start']+d['start'],c['timeline_start']);near(b['film_start']+d['end'],c['timeline_end'])
   near(e['timeline_start'],c['timeline_start']);near(e['timeline_end'],c['timeline_end'])
   near(c['file_out'],f['seconds']);assert c['file_in']==e['file_in']==0
   assert c['sha256']==a['sha256']==f['sha256']==sha(e['file']);assert c['file']==a['path']==e['file']==f['path']
   assert e['rate']==c['rate']==1
   assert round((e['file_out']-e['file_in'])*48000)==f['decoded_frames_48k']
   assert round((e['timeline_end']-e['timeline_start'])*48000)==f['decoded_frames_48k']
   near(a['budget_seconds'],f['seconds']);assert c['text_ja']==a['text']==d['text']
   sub=next(x for x in sm[c['shot_id']]['subtitle_cues'] if x['cue_id']==cid)
   near(sm[c['shot_id']]['start_second']+sub['offset'],c['timeline_start']);near(sub['duration'],f['seconds'])
 assert len(seen)==len(set(seen))==63
 ordered=sorted(ev.values(),key=lambda e:e['timeline_start'])
 assert all(a['timeline_end']<=b['timeline_start']+.00001 for a,b in zip(ordered,ordered[1:]))
 near(sm['CY024K00']['seconds'],4)
 near(tc['VO-CY029E1-01']['timeline_start']-tc['VO-CY028C-01']['timeline_end'],6)
 assert tc['VO-CY029-01']['timeline_start']>=tc['VO-CY028C-01']['timeline_end']
 assert tc['VO-CY029-01']['timeline_end']<=tc['VO-CY029E1-01']['timeline_start']
 near(tc['VO-CY024A5-02']['timeline_start']-tc['VO-CY024A5-01']['timeline_end'],.8)
 assert tc['VO-CY024A5-02']['timeline_end']<sm['CY024A5B']['start_second']
 assert tc['VO-CY029B1-01']['timeline_end']<sm['CY029B2']['start_second']
 assert len(mix['cues'])==13 and len(mix['silences'])==8 and len(mix['action_points'])==46
 near(mix['silences'][-1]['duration'],4)
 assert mix['status']=='rendered_candidate_not_audition_approved'
 for name,v in mix['output_assets'].items():assert sha(FIX+'/'+name)==v['sha256']
 for v in mix['render_decode_checks'].values():near(v['decoded_seconds'],src['total_seconds']);assert v['all_finite']
 assert all(v==0 for v in mix['render_decode_checks']['BGM试听.wav']['silence_max_abs'])
 assert all(sha(p)==v['sha256'] for p,v in mix['input_assets'].items())
 assert len(list((ROOT/OUT/'提示词').glob('*.txt')))==len(board['batches'])*2
 report=dict(status='passed',seconds=src['total_seconds'],shots=len(sm),batches=len(board['batches']),cues=63,full_original_files_once=True,no_voice_overlap=True,all_clocks_same_source=True,images_unchanged=True,source_sha256=sha(SOURCE),bgm_segments=13,silences=8,action_points=46,protected_beats_verified=True,render_decode_checks=mix['render_decode_checks'],video_generated=False,limits=['文件边界和实测瞬态不等于逐词发音或音乐乐句听审','静帧预览不能证明动态口型和动作实现'])
 write(FIX+'/验证结果.json',report);print(json.dumps({k:v for k,v in report.items() if k!='render_decode_checks'},ensure_ascii=False))

if __name__=='__main__':main()
