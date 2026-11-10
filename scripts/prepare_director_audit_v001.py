"""Freeze the actual board selection and create timestamped visual evidence; no generation."""
from pathlib import Path
import json, hashlib, subprocess, math
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'后期/导演全片审查-v001';OUT.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
audio_events={e['cue_id']:e for b in read(ROOT/'视频制作/Metaso-H3-v003/声音修订.json').values() for e in b.get('events',[])}
def cue(c):
 opt=c.get('aligned_option') or {};rev=c.get('revision') or {}
 result={**{k:v for k,v in c.items() if k in ['id','shot','role','start','end','current_path']},'legacy_ja':c['ja'],'ja':opt.get('text_ja') or rev.get('ja') or c['ja'],'zh':opt.get('text_zh') or rev.get('zh') or c.get('zh',''),'text_source':'v025 aligned_option.text优先，revision次之；保留legacy_ja，仅作数据核对，未实听。'}
 delta=audio_events.get(c['id'],{}).get('delta_seconds',0)
 if delta:result.update(original_start=c['start'],original_end=c['end'],start=c['start']+delta,end=c['end']+delta,actual_override='v003声音修订.json：合扇后入声')
 return result
w=read(ROOT/'后期/制作工作台-v025/工作台数据.json')
history=[]
for name in ['LibTV-H3-v001/H3节约余量执行队列.json','Metaso-H3-v001/执行队列.json','Metaso-H3-v002/执行队列.json','Metaso-H3-v003/执行队列.json']:
 for x in read(ROOT/'视频制作'/name)['items']:
  if x.get('local_path'):history.append(x)
selection={**read(ROOT/'视频制作/Metaso-H3-v002/剪辑候选.json'),**read(ROOT/'视频制作/Metaso-H3-v003/剪辑候选.json')}
records=[]
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
for i,b in enumerate(w['batches'],1):
 main=selection.get(b['id']) or [x for x in history if x['batch_id']==b['id']][-1]
 source=ROOT/main['local_path'];digest=hashlib.sha256(source.read_bytes()).hexdigest()
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(source)],encoding='utf8'))
 duration=float(next(x for x in probe['streams'] if x['codec_type']=='video')['duration'])
 rec={'batch_number':i,'id':b['id'],'title':b['title'],'path':main['local_path'],'sha256':digest,'video_duration':duration,'planned_duration':b['used_seconds'],'film_start':b['film_start'],'composite':b['id'] in selection,'audio_state':main.get('audio','模型原生音频，尚未替换最终配音/BGM'),'shots':[s for s in w['shots'] if s['id'] in b['shot_ids']],'cues':[cue(c) for c in w['cues'] if c.get('shot') in b['shot_ids']],'sheets':[]}
 folder=OUT/'证据'/f'{i:02d}-{b["id"]}';folder.mkdir(parents=True,exist_ok=True)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-vf','fps=2,scale=400:226:force_original_aspect_ratio=decrease,pad=400:226:(ow-iw)/2:(oh-ih)/2','-q:v','3',str(folder/'frame-%04d.jpg')],check=True)
 frames=sorted(folder.glob('frame-*.jpg'))
 for start in range(0,len(frames),20):
  subset=frames[start:start+20];canvas=Image.new('RGB',(1600,math.ceil(len(subset)/4)*250),(18,22,30));draw=ImageDraw.Draw(canvas)
  for j,p in enumerate(subset):
   x=j%4*400;y=j//4*250;canvas.paste(Image.open(p),(x,y+24));draw.text((x+6,y+3),f'Batch {i} | local {(start+j)/2:.2f}s',fill='white',font=font)
  dest=folder/f'sheet-{start//20+1:02d}.jpg';canvas.save(dest,quality=88);rec['sheets'].append(dest.relative_to(ROOT).as_posix())
 records.append(rec);save(OUT/'当前44批审查清单.json',records);print(i,b['id'],len(frames),'frames',flush=True)
save(OUT/'审查边界.json',{'selection':'与v003工作台相同：v003合成覆盖v002合成，其余用当前列表最后可用回片','base_sampling':'全时长2fps顺序抽帧，标签为0.5秒名义网格；问题处另作密采样/原尺寸查看','not_proven':['实时连续观看','完整声音听审','逐字口型同步'],'source_preserved':True,'paid_generation':False})
