"""Versioned CPU-only static storyboard music audition; no source edits."""
import argparse, hashlib, json, subprocess, wave, html
from pathlib import Path
import numpy as np

p=argparse.ArgumentParser(); p.add_argument('--root',type=Path,required=True)
p.add_argument('--version',default='v001',choices=['v001','v002'])
p.add_argument('--manifest',default='镜头设计/shot-plan-v0.5.json'); args=p.parse_args()
root=args.root.resolve(); out=root/f'后期/静帧配乐-{args.version}'; out.mkdir(parents=True,exist_ok=True)
final=out/f'穿云-全片静帧配乐-{args.version}.mp4'
if final.exists(): raise SystemExit('Preserve completed version; choose a new version')
plan_path=root/args.manifest
plan=json.loads(plan_path.read_text(encoding='utf-8')); shots=plan['shots']; total=plan['total_seconds']
assert shots and total>0
assert all(s['end_second']-s['start_second']==s['seconds'] for s in shots)
assert all(a['end_second']==b['start_second'] for a,b in zip(shots,shots[1:]))
def run(cmd): subprocess.run(cmd,check=True,cwd=out)
def probe(f): return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height,sample_rate,channels,nb_frames','-of','json',str(f)]))
def sha(f): return hashlib.sha256(f.read_bytes()).hexdigest()
def write_json(f,d): f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sources={
 'Hobbits':'资产/声音/BGM/B站-BV1Ay4y1J7q6_p2.m4a',
 'Knife':'资产/声音/BGM/B站-BV1Ay4y1J7q6_p7.m4a',
 'Courage':'资产/声音/BGM/B站-BV1Eu4y1L7qz.m4a',
 'Victory':'资产/声音/参考/Victory-BV1Qs411J71S.m4a'}
# title, timeline in/out, source in, target loudness, fade in/out
specs=[('Hobbits',2,18,0,-23,1,3),('Knife',18,90,0,-25,1.5,1.5),
 ('Knife',94,133,72,-20,.4,.25),('Victory',133,146,127.28,-17,.015,.5),
 ('Courage',146,171,45,-19,.35,.5),('Victory',171,184,140.28,-18,.25,.12),
 ('Courage',186,213,0,-25,1.3,1.5),('Hobbits',213,237,0,-22,1,3)]
by_id={s['id']:s for s in shots}
at=lambda id:by_id[id]['start_second']
duck_at=171;duck_len=6
if args.version=='v002':
 assert plan['revision']=='v006'
 # Derive cue boundaries from stable shot IDs after the visual revision.
 # Short overlaps only at flashback/epilogue transitions; the entrance attack stays exact.
 specs=[('Hobbits',2,at('CY004')+.4,0,-23,1,2.4),
  ('Knife',at('CY004'),at('CY016B'),0,-25,1.2,1.2),
  ('Knife',at('CY016C'),at('CY023'),at('CY016B')-at('CY004'),-20,.4,.20),
  ('Victory',at('CY023'),at('CY026A')+.3,127.28,-17,.015,.5),
  ('Courage',at('CY026A')-.2,at('CY027A'),45,-19,.5,.5),
  ('Victory',at('CY027A'),at('CY027E1'),140.28,-18,.25,.12),
  ('Courage',at('CY027F'),at('CY031')+.4,0,-25,1.3,1.2),
  ('Hobbits',at('CY031')-.4,total,0,-22,1.2,3)]
 duck_at=at('CY027A');duck_len=at('CY027C')-duck_at
cue_record=[]; sr=48000; mix=np.zeros((round(total*sr),2),np.float32)
for n,(name,start,end,src,lufs,fi,fo) in enumerate(specs):
 duration=end-start; f=root/sources[name]; assert src+duration<=float(probe(f)['format']['duration'])
 pcm=subprocess.check_output(['ffmpeg','-v','error','-ss',str(src),'-i',str(f),'-t',str(duration),'-af',f'loudnorm=I={lufs}:TP=-2:LRA=11','-f','f32le','-ar',str(sr),'-ac','2','-'])
 data=np.frombuffer(pcm,dtype='<f4').reshape(-1,2).copy()[:round(duration*sr)]
 envelope=np.ones(len(data),np.float32)
 for count,reverse in [(int(fi*sr),False),(int(fo*sr),True)]:
  count=min(count,len(data)); ramp=np.linspace(0,1,count,dtype=np.float32)
  if reverse: envelope[-count:]*=ramp[::-1]
  else: envelope[:count]*=ramp
 # Let the treaty and GPT's reply breathe; resume strength at takeoff.
 if name=='Victory' and start==duck_at:
  quiet=round((duck_len-.3)*sr);resume=round(duck_len*sr)
  envelope[:quiet]*=.35
  envelope[quiet:resume]*=np.linspace(.35,1,resume-quiet)
 data*=envelope[:,None]; base=round(start*sr); mix[base:base+len(data)]+=data
 cue_record.append(dict(music=name,path=sources[name],timeline_in=start,timeline_out=end,source_in=src,source_out=src+duration,target_lufs=lufs,fade_in=fi,fade_out=fo,source_sha256=sha(f)))
peak=float(np.max(np.abs(mix))); assert peak<1,peak
wav=out/f'全片-BGM-{args.version}.wav'
with wave.open(str(wav),'wb') as w:
 w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((mix*32767).astype('<i2').tobytes())
print('Music bed saved',flush=True)

def ast(t):
 cs=round(t*100);return f'{cs//360000}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}'
ass='''[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 0
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Dialogue,Microsoft YaHei,30,&H00FFFFFF,&H00FFFFFF,&H00101010,&H90000000,0,0,0,0,100,100,0,0,1,2,1,2,45,45,28,1
Style: Time,Microsoft YaHei,30,&H00FFFFFF,&H00FFFFFF,&H00101010,&H90000000,0,0,0,0,100,100,0,0,1,2,1,7,36,36,65,1
Style: Shot,Microsoft YaHei,16,&H00DDDDDD,&H00FFFFFF,&H00202020,&H90000000,0,0,0,0,100,100,0,0,1,1,0,7,20,20,16,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
events=[]
def event(start,end,style,text):
 events.append(dict(start=start,end=end,style=style,text=text));return f'Dialogue: 0,{ast(start)},{ast(end)},{style},,0,0,0,,{text}\n'
for s in shots:
 ass+=event(s['start_second'],s['end_second'],'Shot',f"{s['id']} · 静帧配乐试听")
 cap=s.get('time_caption')
 if cap: ass+=event(s['start_second']+cap['offset'],s['start_second']+cap['offset']+cap['duration'],'Time',cap['text'])
 for i,c in enumerate(s.get('dialogue_cues',[])):
  start=s['start_second']+c['offset']; dur=float(probe(root/c['file'])['format']['duration'])+.65
  nxt=s['dialogue_cues'][i+1]['offset']+s['start_second'] if i+1<len(s['dialogue_cues']) else total
  ass+=event(start,min(start+dur,nxt),'Dialogue',c['speaker']+'：'+c['text'])
(out/'subtitles.ass').write_text(ass,encoding='utf-8-sig')
write_json(out/'字幕与提示.json',events)
segments=[]
for index,s in enumerate(shots):
 part=out/(s['id']+'.mp4'); x,y,w,h=s['panel_rect_pixels']
 vf=f'crop={w}:{h}:{x}:{y},scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p'
 if s.get('split_screen_reveal'):
  reveal=s['split_screen_reveal']; display_w=min(1280,720*w/h); left=(1280-display_w)/2
  for col,offset in enumerate(reveal['offsets'][1:],1):
   px=round(left+display_w*col/5); right=round(left+display_w*(col+1)/5)
   vf+=f",drawbox=x={px}:y=0:w={right-px}:h=720:color=black:t=fill:enable='lt(t,{offset})'"
 if args.version=='v002':
  # Brief fades mark elapsed time, never conceal a same-action mismatch.
  if s['id'] in ['CY004B','CY010A','CY031']:
   vf+=',fade=t=in:st=0:d=0.20'
  if s['id'] in ['CY004A','CY010','CY030']:
   vf+=f",fade=t=out:st={s['seconds']-.20}:d=0.20"
 if not part.exists():
  run(['ffmpeg','-v','error','-n','-loop','1','-i',str(root/s['presentation']['path']),'-t',str(s['seconds']),'-vf',vf,'-r','24','-an','-c:v','libx264','-threads','2','-preset','veryfast','-tune','stillimage','-crf','20',str(part)])
 segments.append(part)
 if (index+1)%10==0: print(f'Shots {index+1}/{len(shots)}',flush=True)
(out/'concat.txt').write_text(''.join(f"file '{f.name}'\n" for f in segments),encoding='utf-8')
run(['ffmpeg','-v','error','-n','-f','concat','-safe','0','-i','concat.txt','-i',wav.name,'-vf','ass=subtitles.ass','-map','0:v','-map','1:a','-c:v','libx264','-threads','2','-preset','veryfast','-crf','20','-c:a','aac','-b:a','192k','-t',str(total),'-movflags','+faststart',final.name])
run(['ffmpeg','-v','error','-i',str(final),'-f','null','-'])
report=dict(version=args.version,shot_plan=plan_path.relative_to(root).as_posix(),shot_plan_sha256=sha(plan_path),duration=total,shot_count=len(shots),video=final.relative_to(root).as_posix(),audio=wav.relative_to(root).as_posix(),probe=probe(final),sha256=sha(final),decode_ok=True,sample_peak=peak,cues=cue_record,shots=[dict(id=s['id'],start=s['start_second'],end=s['end_second'],image=s['presentation']['path'],image_sha256=sha(root/s['presentation']['path']),crop=s['panel_rect_pixels']) for s in shots],notes=[f'{len(shots)}镜、{total}秒；五格按0.6秒依次显露。','对白仅字幕；无临时读稿、正式配音或拟音。','援军登场Victory按CY023定位；条约对白处压低，开场/被发现前/落尘保留留白。','各乐段in/out为本轮试听方案，未实际听审；响度/解码不等于听感通过。','CPU静帧渲染；未启动Resolve，未创建Resolve工程。'])
write_json(out/'粗剪记录.json',report)
print(json.dumps({'video':str(final),'seconds':total,'peak':peak},ensure_ascii=False),flush=True)
