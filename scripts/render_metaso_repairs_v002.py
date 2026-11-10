"""Non-destructive picture edits plus the fixed v025 voice/BGM reference mix.

Never retime speech. Native generated audio remains in original candidates.
"""
from pathlib import Path
import json,subprocess,hashlib,argparse
parser=argparse.ArgumentParser();parser.add_argument('--revision',choices=['v002','v003'],default='v002');args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/('视频制作/Metaso-H3-'+args.revision)
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
w=read(ROOT/'后期/制作工作台-v025/工作台数据.json');batches={b['id']:b for b in w['batches']}
plan=read(OUT/'剪辑执行计划.json');sp=OUT/'剪辑候选.json';records=read(sp) if sp.exists() else {}
audio_overrides=read(OUT/'声音修订.json') if (OUT/'声音修订.json').exists() else {}
for bid,segments in plan.items():
 b=batches[bid];assert abs(sum(s['target_duration'] for s in segments)-b['used_seconds'])<.002,(bid,segments)
 override=audio_overrides.get(bid,{})
 audio=ROOT/override.get('path','后期/生成收口-v025/全片声音预览.mp3');audio_start=override.get('source_start',b['film_start'])
 spec={'segments':segments,'audio_sha256':sha(audio),'audio_start':audio_start,'film_start':b['film_start'],'used_seconds':b['used_seconds']}
 for s in segments:
  assert (ROOT/s['source']).exists();s['source_sha256']=sha(ROOT/s['source'])
  assert s['out']>s['in'] and s['target_duration']>0
  source_probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=duration','-of','json',str(ROOT/s['source'])],encoding='utf8'))
  assert s['out']<=float(source_probe['streams'][0]['duration'])+.002,(bid,'source out beyond video',s)
  assert s['target_duration']/(s['out']-s['in'])<=2.201,(bid,'excessive slow motion')
 fingerprint=hashlib.sha256(json.dumps(spec,sort_keys=True).encode()).hexdigest()
 if bid in records and records[bid].get('fingerprint')==fingerprint:continue
 dest=OUT/'剪辑候选'/(bid+'-'+args.revision+'.mp4');dest.parent.mkdir(exist_ok=True)
 if dest.exists():
  oldhash=sha(dest)[:10];dest.rename(dest.with_name(dest.stem+'-history-'+oldhash+'.mp4'))
 cmd=['ffmpeg','-hide_banner','-v','error','-y'];filters=[]
 for i,s in enumerate(segments):
  cmd+=['-ss',str(s['in']),'-t',str(s['out']-s['in']),'-i',str(ROOT/s['source'])]
  chain=f'[{i}:v]setpts={s["target_duration"]/(s["out"]-s["in"]):.10f}*(PTS-STARTPTS),'
  if s.get('crop'):chain+=s['crop']+','
  chain+=f'scale=1344:768:force_original_aspect_ratio=decrease,pad=1344:768:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,trim=duration={s["target_duration"]},setpts=PTS-STARTPTS[v{i}]'
  filters.append(chain)
 n=len(segments);cmd+=['-ss',str(audio_start),'-i',str(audio)]
 filters.append(''.join(f'[v{i}]' for i in range(n))+f'concat=n={n}:v=1:a=0[v]')
 cmd+=['-filter_complex',';'.join(filters),'-map','[v]','-map',f'{n}:a:0','-t',str(b['used_seconds']),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(dest)]
 subprocess.run(cmd,check=True)
 p=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(dest)],encoding='utf8'))
 assert abs(float(p['format']['duration'])-b['used_seconds'])<.1
 r=subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],capture_output=True,text=True);assert not r.stderr and r.returncode==0
 records[bid]={'local_path':dest.relative_to(ROOT).as_posix(),'sha256':sha(dest),'fingerprint':fingerprint,'segments':segments,'probe':p,'decode':'passed','audio':override.get('note','v025固定原速声音+BGM试听；未通过口型验收'),'accepted':False}
 save(sp,records);print(bid,'rendered',flush=True)
