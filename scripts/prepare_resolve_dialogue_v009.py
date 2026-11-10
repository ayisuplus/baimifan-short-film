"""Create traceable native-speed dialogue edits for Resolve; preserve source files."""
from pathlib import Path
import json, subprocess, hashlib, math
import numpy as np
import soundfile as sf

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'后期/对白补齐-v009'
AUDIO=OUT/'装配音频';AUDIO.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inv=read('声音/正式配音准备-v006/正式配音清单.json')
split=read('声音/逐句切分审阅-v007/切分清单.json')
before=read('后期/对白补齐-v009/v008-装配前快照.json')
old={x['name']:x for x in before['tracks'][1]['items']}
candidates={c['id']:c for c in split['candidates'] if c['take']==(2 if c['voice_role'] in ['Kimi','教主'] else 1)}
existing={c['id']:c for c in split['existing_lines']}
new={}
for p in (ROOT/'声音/缺口补齐-v008').glob('VO-*-结果.json'):
    d=json.loads(p.read_text(encoding='utf8'))
    if d['status']=='saved_pending_review' and d.get('generation_revision',1)==1:new[d['line_id']]=d
repaired=ROOT/'声音/缺口补齐-v008/修正采用映射.json'
if repaired.exists():
    for ident,receipt in json.loads(repaired.read_text(encoding='utf8'))['receipts'].items():
        d=json.loads((repaired.parent/receipt).read_text(encoding='utf8'))
        assert d['status']=='saved_pending_review' and d['line_id']==ident
        new[ident]=d
rows=[];missing=[]
for l in inv['lines']:
    ident=l['id'];take=None
    if ident in new and new[ident].get('generation_revision',1)>1:
        c=new[ident];src=ROOT/c['file'];sha=c['sha256'];kind='selected_voice_reading_repair'
    elif ident in candidates:
        c=candidates[ident];src=ROOT/c['file'];sha=c['sha256'];kind='selected_master_split';take=c['take']
    elif ident in existing:
        c=existing[ident]['existing_audio'];src=ROOT/c['file'];sha=c['sha256'];kind='existing_selected'
    elif ident in new:
        c=new[ident];src=ROOT/c['file'];sha=c['sha256'];kind='new_selected_voice_completion'
    else:missing.append({'id':ident,'role':l['role'],'ja':l['ja']});continue
    assert digest(src)==sha,ident+' source hash changed'
    meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','a:0','-show_entries','stream=sample_rate,channels','-of','json',str(src)]))['streams'][0]
    sr=int(meta['sample_rate']);channels=int(meta['channels'])
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-f','f32le','-acodec','pcm_f32le','-'])
    y=np.frombuffer(raw,np.float32).copy().reshape(-1,channels)
    a=0;b=len(y)
    # Only outer quiet handles, never internal pauses or spoken duration.
    if kind!='existing_selected':
        hop=max(1,round(sr*.01))
        rms=np.array([np.sqrt(np.mean(y[k:k+hop]**2)) for k in range(0,len(y),hop)])
        on=np.flatnonzero(rms>10**(-45/20))
        assert len(on),ident+' silent output'
        a=max(0,int(on[0]*hop-sr*.10));b=min(len(y),int((on[-1]+1)*hop+sr*.14))
    crop=y[a:b].copy()
    # Eight milliseconds at the outer handles suppress edit clicks, with spoken content retained.
    fade=min(round(sr*.008),len(crop)//4)
    crop[:fade]*=np.linspace(0,1,fade)[:,None];crop[-fade:]*=np.linspace(1,0,fade)[:,None]
    revision=new.get(ident,{}).get('generation_revision',1)
    suffix='-r'+str(revision) if revision>1 else ''
    file=AUDIO/(ident+'__'+l['voice_role']+suffix+'.wav')
    sf.write(file,crop,sr,subtype='PCM_24')
    peak=float(np.max(np.abs(crop)));peakdb=20*math.log10(max(peak,1e-12))
    record=l.get('previous_record_frame')
    if ident=='VO-CY019-02':record=3640
    assert record is not None,ident
    rows.append({'id':ident,'role':l['role'],'voice_role':l['voice_role'],'ja':l['ja'],'zh':l['zh_back_translation'],'direction':l['performance_direction_v004'],'source':str(src),'source_sha256':sha,'source_kind':kind,'repeat_take':take,'trim_start_sample':a,'trim_end_sample_exclusive':b,'source_sample_rate':sr,'file':str(file),'sha256':digest(file),'samples':len(crop),'sample_rate':sr,'duration_seconds':len(crop)/sr,'duration_frames':len(crop)*24/sr,'peak_dbfs':peakdb,'record':record,'previous_record_frame':l.get('previous_record_frame'),'speed':100.0,'selected_identity_reference_approved':True,'author_performance_accepted':False})
# Keep each role's dynamics: one gain per role, not per-sentence normalization.
role_peaks={role:max(x['peak_dbfs'] for x in rows if x['voice_role']==role and x['source_kind']!='existing_selected') for role in {x['voice_role'] for x in rows if x['source_kind']!='existing_selected'}}
for x in rows:
    if x['source_kind']=='existing_selected':x['gain_db']=float(old.get(x['id'],{}).get('properties',{}).get('AudioVolume',-3.0))
    else:x['gain_db']=round(min(3.0,-3.0-role_peaks[x['voice_role']]),2)
rows.sort(key=lambda x:x['record'])
adjustments=[]
for i,x in enumerate(rows):
    if i:
        prev=rows[i-1];minimum=math.ceil(prev['record']+prev['duration_frames'])+6
        if x['record']<minimum:
            prior=x['record'];x['record']=minimum
            adjustments.append({'id':x['id'],'old_frame':prior,'new_frame':minimum,'reason':'retain full native-speed dialogue plus six-frame turn-taking gap'})
    x['end']=x['record']+x['duration_frames']
assert len({x['id'] for x in rows})==len(rows)
active={x['id'] for x in inv['lines']}
old_ids=set()
for v in read('后期/局部收口-v008/后期执行计划.json')['voice']:old_ids.add(v['native_id'].split('-part')[0])
plan={'timeline':'v009_Selected_Voices_Assembly','baseline':'v008_Local_Continuity_Fixes','fps':24,'frames':before['end'],'status':'ready_for_assembly' if not missing else 'partial_preparation_pending_engine_choice','script':inv['script'],'script_sha256':inv['script_sha256'],'baseline_snapshot':'后期/对白补齐-v009/v008-装配前快照.json','lines':rows,'missing':missing,'removed_or_merged_old_ids':sorted(old_ids-active),'record_adjustments':adjustments,'repeat_take_policy':'Kimi and leader use middle repeat 2 as technical assembly candidate; author voice candidate1 is a different selection; all repetitions retained. This is not auditory performance approval.','processing':'Original speed; outer -45 dBFS 10 ms RMS silence trim only with 100/140ms handles, 8ms fades; PCM24; role-consistent gain peak capped at -3 dBFS; original independent dialogue gain preserved.','export_allowed':False,'limitations':['Picture remains v008 baseline; lip sync, new rescue action and shorter spell picture rhythm remain separate picture work.','ASR and signal checks are not listening/performance acceptance.']}
(OUT/'对白装配计划.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'prepared':len(rows),'missing':missing,'adjustments':adjustments,'role_peaks':role_peaks},ensure_ascii=False))
