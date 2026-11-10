from pathlib import Path
import json,math,hashlib
import numpy as np
import soundfile as sf
R=Path(__file__).resolve().parents[3];D=Path(__file__).resolve().parent;P=D.parent
load=lambda n:json.loads((P/n).read_text(encoding='utf8'))
a=load('修前实际状态.json');b=load('修后实际状态.json');ed=load('剪辑施工增量.json');au=load('声音施工增量.json');ga=load('对白增益修正.json')
allowed={(x['name'],x['start'],x['end']) for x in ed['affected']}
lookup={(x['start'],x['end']):x for x in b['video']}
vf=['name','start','end','path','source_in','source_out','speed','props']
unexpected=[];unchanged=[]
for x in a['video']:
 if (x['name'],x['start'],x['end']) in allowed:continue
 y=lookup.get((x['start'],x['end']))
 differences={k:[x.get(k),y.get(k) if y else None] for k in vf if not y or x.get(k)!=y.get(k)}
 if differences:unexpected.append({'name':x['name'],'differences':differences})
 else:unchanged.append(x['name'])
def audio(n,rows):return next(x for x in rows if x['name']==n)
voice_differences=[];endpoint_semantics=[];gain_differences=[];gains={x['name']:x for x in ga['adjustments']};voices=[x for x in a['audio'] if x['track']==1]
for x in voices:
 y=next((z for z in b['audio'] if z['track']==1 and z['name']==x['name'] and z['start']==x['start']),None)
 if y is None:voice_differences.append({'name':x['name'],'missing':True});continue
 # Before snapshot uses integer frames; after uses fractional timeline frames and source seconds.
 expected={'path':x['path'],'start':x['start'],'end':x['end'],'source_in':x['source_in'],'source_out':x['source_out'],'enabled':x['enabled']}
 actual={'path':y['path'],'start':y['start'],'end':math.floor(y['end']+1e-6),'source_in':math.floor(y['source_in']*24+1e-6),'source_out':math.floor(y['source_out']*24+1e-6),'enabled':y['enabled']}
 dif={k:[expected[k],actual[k]] for k in expected if expected[k]!=actual[k]}
 if set(dif)=={'source_out'} and actual['source_out']==expected['source_out']+1 and abs(y['source_out']*24-(y['end']-y['start']+actual['source_in']))<1e-6:
  endpoint_semantics.append({'name':x['name'],'old_last_source_frame':expected['source_out'],'new_exclusive_source_seconds':y['source_out'],'unchanged_timeline':[x['start'],x['end']]})
  dif={}
 if dif:voice_differences.append({'name':x['name'],'differences':dif})
 expected_gain=gains.get(x['name'],{}).get('new_volume',x['props']['AudioVolume'])
 if abs(y['volume']-expected_gain)>1e-6:gain_differences.append({'name':x['name'],'expected':expected_gain,'actual':y['volume']})
def pcm_compare(oldpath,newpath,old_offset,new_offset,frames):
 oi=sf.info(oldpath);ni=sf.info(newpath)
 assert oi.samplerate==ni.samplerate==48000
 old=sf.read(oldpath,start=round(old_offset*2000),frames=round(frames*2000),dtype='int32',always_2d=True)[0]
 new=sf.read(newpath,start=round(new_offset*2000),frames=round(frames*2000),dtype='int32',always_2d=True)[0]
 delta=int(np.max(np.abs(old.astype(np.int64)-new.astype(np.int64)))) if old.shape==new.shape else None
 return {'samples':len(old),'same_shape':old.shape==new.shape,'sample_exact_equal':bool(np.array_equal(old,new)),'max_abs_int32_delta':delta,'max_abs_24bit_lsb_delta':delta/256 if delta is not None else None,'max_abs_delta_dbfs':20*math.log10(delta/2**31) if delta else None,'within_3_lsb_24bit':delta is not None and delta<=768}
checks={}
for n in ['Foley','Action']:
 old=audio(n,a['audio']);new=audio(n,b['audio'])
 checks[n+'_kimi_4922_6303']=pcm_compare(old['path'],new['path'],4922,4922,6303-4922)
old=audio('M09',a['audio']);new=audio('M09',b['audio']);checks['M09_tail_6409_8007']=pcm_compare(old['path'],new['path'],6409-old['start'],6409-new['start'],8007-6409)
oldn=audio('N01_flashback',a['audio']);newn=audio('N01_flashback',b['audio']);checks['N01_prefix_5696_6285']=pcm_compare(oldn['path'],newn['path'],0,0,6285-5696)
b17=lookup[(4778,4838)];b17pass=b17['source_in']==24 and b17['source_out']==84 and b17['speed']['Percentage']==100 and 'Metaso-H3-v010' in b17['path']
middle_unchanged=[x['name'] for x in a['video'] if 4922<=x['start'] and x['end']<=8218 and x['name'] in unchanged]
prefix_a=next(x for x in a['video'] if x['start']==10368);prefix_b=next(x for x in b['video'] if x['start']==10368)
prefix_pass=prefix_b['end']==10641 and prefix_b['path']==prefix_a['path'] and prefix_b['source_in']==0 and prefix_b['source_out']==273 and prefix_b['props']==prefix_a['props'] and prefix_b['speed']==prefix_a['speed']
report={'reviewer':'style_audit_middle independent','verdict':'pass_structural_readback_with_scope_limits' if not unexpected and not voice_differences and not gain_differences and b17pass and prefix_pass and all(x['within_3_lsb_24bit'] for x in checks.values()) else 'needs_review',
 'inputs':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['修前实际状态.json','修后实际状态.json','剪辑施工增量.json','声音施工增量.json','对白增益修正.json']},
 'baseline':a['timeline'],'applied':b['timeline'],'frames_before':a['end'],'frames_after':b['frames'],'video_count_before':len(a['video']),'video_count_after':len(b['video']),
 'unmodified_video_count':len(unchanged),'unmodified_video_checked_fields':vf,'unexpected_video_differences':unexpected,
 'all_middle_B18_to_B32_unchanged_count':len(middle_unchanged),'all_middle_unchanged':middle_unchanged,
 'B17':{'pass':b17pass,'source_in':b17['source_in'],'source_out':b17['source_out'],'timeline':[4778,4838],'source':b17['path'],'speed':b17['speed'],'note':'RetimeProcess由0变1是新片默认值；本镜100%原速且源/时间线长度均60，其他变换仍Zoom1/Pan0/Tilt0，不导致变速。'},
 'B40_unchanged_prefix_10368_10641_preserved':prefix_pass,
 'voice_count':len(voices),'voice_selection_and_integer_timeline_differences':voice_differences,'source_endpoint_schema_differences':endpoint_semantics,'voice_gain_adjustment_count':len(gains),'voice_gain_unexpected_differences':gain_differences,
 'audio_readback_unit_note':'修前GetEnd为整数帧/GetSourceEndFrame为帧；修后GetEnd(True)含小数帧/GetSourceEndTime为秒。按24fps转换并向下取整数后比较，不能将schema差异误报为对白被挪。修后未记录GetSpeed/全部音频props，故不宣称仅凭两快照验证所有音频属性完全相同。',
 'music_bridge':{'declared':au['music_bridge'],'M09_actual':[new['start'],new['end']],'N01_actual':[newn['start'],newn['end']],'crossfade_window':[6285,6321],
  'note':'前20帧原入场淡入随新桥改变；6409之后至8007的工作WAV与原段对应样本最大差1个24bit LSB，证明后段内容映射与卡点保持，但不是字节/样本完全原样。淡入/淡出曲线已烘焙到工作WAV，不替代听觉过渡验收。'},
 'PCM_checks':checks,'timeline_contiguous':all(x['end']==y['start'] for x,y in zip(b['video'],b['video'][1:])),
 'saved':b.get('save'),'exported':b.get('exported'),'old_timeline_preserved':b.get('old_timeline_preserved'),
 'limits':['这是独立文件回读及PCM比较，未调用或修改Resolve。','未执行完整连续听审，不宣称逐音素口型、音色或最终张力通过。','修后video未记track/enabled字段，不以此证明这些未记录属性；source/speed/所有已记录props已逐项核对。']}
(D/'施工回读复核.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:report[k] for k in ['verdict','unmodified_video_count','unexpected_video_differences','all_middle_B18_to_B32_unchanged_count','B17','voice_count','voice_selection_and_integer_timeline_differences','voice_gain_unexpected_differences','PCM_checks','B40_unchanged_prefix_10368_10641_preserved']},ensure_ascii=False,indent=2))
