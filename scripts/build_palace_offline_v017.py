"""Independent CPU-only edit from saved readback; never connects to Resolve."""
from pathlib import Path
import json,subprocess,hashlib,shutil
import numpy as np
import soundfile as sf
R=Path(__file__).resolve().parents[1];O=R/'后期/独立剪辑-v017';W=O/'工作';W.mkdir(parents=True,exist_ok=True)
D=json.loads((R/'后期/宫殿调色-v014/after.json').read_text(encoding='utf8'))
FPS=24;SR=48000
def run(args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-threads','2','-filter_threads','2',*args],cwd=W,check=True)
def render(path,start,n,rate,out,lut=None):
 filters=f'trim=start_frame={start},setpts=(PTS-STARTPTS)/{rate},fps=24'
 if lut:filters+=',lut3d=file='+lut
 run(['-i',str(path),'-an','-vf',filters,'-frames:v',str(n),'-c:v','libx264','-threads','2','-preset','fast','-crf','17','-pix_fmt','yuv420p',str(out)])
manifest=[];groups={'01_登阶与守卫放行':[],'02_俯拍行进与亮灯':[],'03_接小鱼与GPT对话':[]}
for key in ['stair','gate','dialogue']:
 shutil.copyfile(R/f'后期/宫殿调色-v014/LUT/Baimifan_v014_{key}_r1.cube',W/f'{key}.cube')
for c in D['tracks'][0]['items']:
 f=int(c['start'])
 if not (682<=f<916 or 946<=f<1282):continue
 group='01_登阶与守卫放行' if f<916 else '03_接小鱼与GPT对话'
 n=int(c['end']-c['start']);name=f'part-{f}.mp4';path=W/name;key='stair' if f==682 else 'gate' if f<916 else 'dialogue'
 render(Path(c['path']),c['source_start'],n,c['speed']['Percentage']/100,path,key+'.cube')
 groups[group].append((name,n));manifest.append(dict(source=c['path'],source_start=c['source_start'],frames=n,speed=c['speed']['Percentage'],baseline_start=f,group=group,lut=key))
lamp=R/'视频制作/Metaso-H3-v016/产物/CY005L-v016-high-angle-r2.mp4'
render(lamp,0,96,1,W/'part-lamps.mp4');groups['02_俯拍行进与亮灯']=[('part-lamps.mp4',96)]
manifest.append(dict(source=str(lamp),source_start=0,frames=96,speed=100,group='02_俯拍行进与亮灯',note='cut before final deeper stair ascent; omit old 30-frame approach to avoid duplicate arrival'))
def decoded(path):
 data=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-f','f32le','-ac','2','-ar',str(SR),'-'])
 return np.frombuffer(data,dtype='<f4').reshape(-1,2)
def mix_interval(start,n):
 out=np.zeros((n*2000,2),np.float32)
 for t in D['tracks']:
  if t['type']!='audio' or not t['enabled'] or not (t['index'] in [5,6] or t['name'].startswith('VO_v009')):continue
  for c in t['items']:
   a=max(start,c['start']);b=min(start+n,c['end'])
   if b<=a or not c['enabled']:continue
   assert abs(c['speed']['Percentage']-100)<1e-6
   samples=decoded(c['path']);src=round((c['source_start']+a-c['start'])*2000);dst=round((a-start)*2000);count=min(round((b-a)*2000),len(samples)-src,len(out)-dst)
   if count>0:out[dst:dst+count]+=samples[src:src+count]*10**(c['properties'].get('AudioVolume',0)/20)
 return out
audio={'01_登阶与守卫放行':mix_interval(682,234),'03_接小鱼与GPT对话':mix_interval(946,336)}
# The insert uses only the established room ambience, not the generated soundtrack.
amb=next(t for t in D['tracks'] if t['type']=='audio' and t['index']==5)['items'][0]
samples=decoded(amb['path']);audio['02_俯拍行进与亮灯']=samples[916*2000:1012*2000]*10**(amb['properties'].get('AudioVolume',0)/20)
outputs=[]
for group,parts in groups.items():
 listing=W/(group+'.txt');listing.write_text('\n'.join("file '"+name+"'" for name,n in parts),encoding='utf8')
 pic=W/(group+'-picture.mp4');run(['-f','concat','-safe','0','-i',str(listing),'-c','copy',str(pic)])
 wav=W/(group+'.wav');sf.write(wav,audio[group],SR,subtype='PCM_24')
 dest=O/(group+'.mp4');run(['-i',str(pic),'-i',str(wav),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart','-shortest',str(dest)])
 outputs.append(dict(file=dest.name,frames=sum(n for _,n in parts),sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
listing=W/'review.txt';listing.write_text('\n'.join("file '"+str(O/x['file']).replace('\\','/')+"'" for x in outputs),encoding='utf8')
run(['-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(O/'宫殿亮灯-独立粗剪-v017.mp4')])
result=dict(fps=24,frames=666,duration=27.75,segments=outputs,edits=manifest,source_snapshot='后期/宫殿调色-v014/after.json',resolve_accessed=False,bgm_and_subtitle_originals_untouched=True,preview_contains_bgm=False,preview_contains_subtitles=False,voice_source_speed_preserved=True,note='Independent shot review, not a final film export; original timeline not touched.')
(O/'剪辑清单.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'output':str(O),'frames':666,'duration':27.75},ensure_ascii=True))
