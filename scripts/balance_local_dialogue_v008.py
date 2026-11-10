"""Bounded, per-line gain only. Preserve source, timbre, timing and acting contrast."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];O=R/'后期/局部收口-v008'
def read(p):return json.loads(p.read_text(encoding='utf8'))
P=read(R/'后期/二维动漫纠偏-v005/后期执行计划.json');S=read(O/'对白电平复核.json')['items'];B=read(O/'修前实际状态.json')
targets={'VO-CY009-01':-28,'VO-CY015-02':-28,'VO-CY024A-01':-25,'VO-CY024A6-01':-25,'VO-CY028A-01':-30,'VO-CY028A-02':-30,'VO-CY028B-01':-29,'VO-CY028C-01':-29,'VO-CY029E1-01':-20,'VO-CY029E2-01':-20,'VO-CY029E4-01':-20,'VO-CY031A-01':-28,'VO-CY031A-02':-30}
rows=[]
for v,s in zip(P['voice'],S):
 name=v['id_display']
 if name not in targets:continue
 before=next(x for x in B['audio'] if x['name']==name and x['track']==1)
 g=round(targets[name]-s['active_rms_db'],2)
 assert -12<=g<=18 and s['sample_peak_db']+g-3<-6
 rows.append(dict(name=name,role=v['role'],zh=v['zh'],path=before['path'],start=before['start'],end=before['end'],old_volume=before['props']['AudioVolume'],gain_delta_db=g,new_volume=round(before['props']['AudioVolume']+g,2),active_rms_before=s['active_rms_db'],active_rms_target=targets[name],reason='校正源录音电平差异，保留战后低声与施法强句的差距；不压缩、不改音色、不改时长'))
out=dict(method='按语义分组的有声段RMS辅助增益，非LUFS规范化；低声-30/-29、普通轻声-28、起咏-25、强施法-20，其他句不动',adjustments=rows,preserved_silent_author_cut='VO-CY021A-01-part2保留；作者删帧后剩余尾静音不回填词句',continuous_listening_verified=False,source_files_changed=False)
(O/'对白增益修正.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print('Prepared',len(rows),'per-clip gain adjustments; no source audio changed')
