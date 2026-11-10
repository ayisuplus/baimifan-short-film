"""Preserve native PCM and phrase pauses in review-only dialogue candidates."""
from pathlib import Path
import json, re, subprocess, hashlib, io
import numpy as np
import soundfile as sf

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'声音/逐句切分审阅-v007'
CLIPS=OUT/'逐句候选'
CLIPS.mkdir(exist_ok=True)
inventory=json.loads((ROOT/'声音/正式配音准备-v006/正式配音清单.json').read_text(encoding='utf8'))
logs=json.loads((OUT/'静音检测原始日志.json').read_text(encoding='utf8'))
byid={x['id']:x for x in inventory['lines']}
# Boundaries are chosen at sentence gaps, NOT every detected pause.
# Indices address paired silence_start/end intervals in the retained raw log.
layout={
 'Claude':([0,1,2,3,4,6,7,8,10,12,13],['CY003B-01','CY015-01','CY016A-01','CY016B1-01','CY020-01','CY021-01','CY028A-02','CY028B-01','CY029E1-01','CY029E4-01','CY029B1-01','CY031A-02']),
 'GPT':([1,2,4,6,7,9,10,11,13,14],['CY024-01','CY024A-01','CY024A2-01','CY024A3-01','CY024A4-01','CY024A5-01','CY024A5-02','CY028A-01','CY028A2-01','CY008M-01','CY008M-02']),
 'Kimi':([1,3,4,5,7,9,10,11,13,15,16],['CY024R-01','CY024K0-01','CY024K1A-01','CY026D-02']*3),
 '教主':([1,2,3,5,7,8,9,11,13,14,15],['CY021A-01','CY019-01','CY027A-01','CY029-01']*3),
 '千问':([0],['CY026A1-01','CY024A0-01']),
 '教徒':([1],['CY004-01','CY010A-01']),
}
records=[]
sources=[]
for role,(gap_indices,cues) in layout.items():
    src=ROOT/inventory['voice_assets'][role]['file']
    source_sha=hashlib.sha256(src.read_bytes()).hexdigest()
    assert source_sha==inventory['voice_assets'][role]['sha256']
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-c:a','pcm_f32le','-f','wav','-'])
    pcm,sr=sf.read(io.BytesIO(raw),dtype='float32',always_2d=True)
    starts=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',logs[role])]
    ends=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',logs[role])]
    assert len(starts)==len(ends)
    gaps=list(zip(starts,ends))
    cuts=[0]+[round((sum(gaps[k])/2)*sr) for k in gap_indices]+[len(pcm)]
    assert len(cuts)==len(cues)+1 and all(a<b for a,b in zip(cuts,cuts[1:]))
    sources.append(dict(role=role,path=src.relative_to(ROOT).as_posix(),sha256=source_sha,sample_rate=sr,channels=pcm.shape[1],samples=len(pcm),split_gap_indices=gap_indices,cuts_samples=cuts,method='sentence order + whole-master ASR + midpoint of measured silence'))
    for i,cue in enumerate(cues):
        cid='VO-'+cue
        row=byid[cid]
        take=i//4+1 if role in ['Kimi','教主'] else 1
        a,b=cuts[i:i+2]
        dst=CLIPS/f'{cid}__{role}__take{take}.wav'
        sf.write(dst,pcm[a:b],sr,subtype='FLOAT')
        decoded,actual_sr=sf.read(dst,dtype='float32',always_2d=True)
        assert actual_sr==sr and np.array_equal(decoded,pcm[a:b])
        records.append(dict(id=cid,role=row['role'],voice_role=role,take=take,ja=row['ja'],reading_text=row['tts_reading_text'],zh=row['zh_back_translation'],direction=row['performance_direction_v004'],source=src.relative_to(ROOT).as_posix(),source_sha256=source_sha,start_sample=a,end_sample_exclusive=b,sample_rate=sr,start_seconds=a/sr,end_seconds=b/sr,duration_seconds=(b-a)/sr,file=dst.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),pcm_exact=True,peak_dbfs=float(20*np.log10(max(float(np.max(np.abs(decoded))),1e-10))),status='segmented_candidate_pending_listening',author_selected_take=None,timeline_adopted=False))
expected={x['id'] for x in inventory['lines'] if x['audio_state']=='selected_master_contains_text'}
assert {x['id'] for x in records}==expected and len(expected)==35 and len(records)==51
result=dict(version='v007',source_inventory='声音/正式配音准备-v006/正式配音清单.json',status='review_candidates_not_adopted',method='Manual sentence grouping based on supplied text and unprompted ASR, cut only at measured silence midpoints. Original rate, gain, internal pauses and every decoded master sample retained across candidate partitions.',summary=dict(unique_lines=35,candidate_files=51,repeated_roles=['Kimi','教主'],existing_individual_lines=7,missing_lines=12),sources=sources,candidates=records,missing_lines=[x for x in inventory['lines'] if x['audio_state']=='needs_recording'],existing_lines=[x for x in inventory['lines'] if x['audio_state']=='exact_existing_line'],limitations=['ASR is fallible; not listening or Japanese pronunciation acceptance.','All repeated takes retained for comparison; none automatically adopted.','Whole-master ASR timestamps are coarse; boundaries use observed silent intervals.','No timeline, selected voice, script or original audio changed.'])
(OUT/'切分清单.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result['summary'],ensure_ascii=False))
