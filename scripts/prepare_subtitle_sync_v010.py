"""Use existing native-speed dialogue as the subtitle clock; move only opening cue."""
from pathlib import Path
import json,math,hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'后期/对白字幕同步-v010';OUT.mkdir(exist_ok=True)
p=json.loads((ROOT/'后期/对白补齐-v009/对白装配计划.json').read_text(encoding='utf8'))
p['baseline']='v009_Selected_Voices_Assembly';p['timeline']='v010_Dialogue_Subtitle_Sync'
p['baseline_snapshot']=str(ROOT/'后期/对白补齐-v009/v009-装配后快照.json')
cue=next(x for x in p['lines'] if x['id']=='VO-CY003B-01')
cue['previous_v009_record']=cue['record'];cue['record']=441;cue['end']=441+cue['duration_frames']
p['opening_sync']={'id':cue['id'],'old_record':396,'new_record':441,'shift_frames':45,'fps':24,'end_frame':cue['end'],'slap_segment_start_frame':472,'gap_seconds':(472-cue['end'])/24,'rationale':'Finish the short thanks within the eye close-up immediately before the existing slap segment; preserve voice speed and all picture/SFX edit positions.'}
p['subtitle_cues']=[]
for i,x in enumerate(p['lines']):
 start=int(x['record']);end=max(math.ceil(x['end'])+6,start+20)
 if i+1<len(p['lines']):end=min(end,int(p['lines'][i+1]['record'])-2)
 if x['id']==cue['id']:end=472
 assert end>start
 p['subtitle_cues'].append({'index':i+1,'id':x['id'],'role':x['role'],'start_frame':start,'end_frame_exclusive':end,'zh':x['zh'],'ja':x['ja']})
def time(f):
 ms=round(f*1000/24);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
for lang,name in [('zh','白米饭-v010-中文.srt'),('ja','白米饭-v010-日语校对.srt')]:
 text='\n\n'.join(f'{c["index"]}\n{time(c["start_frame"])} --> {time(c["end_frame_exclusive"])}\n{c[lang]}' for c in p['subtitle_cues'])+'\n'
 (OUT/name).write_text(text,encoding='utf-8-sig')
p['subtitle_policy']='Chinese display subtitles, Japanese reference SRT with the same timecodes. Native speech spans plus six-frame reading tail/minimum20 frames, clipped before next cue; opening ends at slap segment cut.'
(OUT/'同步计划.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'timeline':p['timeline'],'opening':p['opening_sync'],'subtitle_cues':len(p['subtitle_cues'])},ensure_ascii=False))
