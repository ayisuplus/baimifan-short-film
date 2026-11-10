"""Encode an explicitly reviewed source window and update the adoption ledger."""
import argparse,hashlib,json,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent;N=Path('G:/comfyui/ComfyUI/ComfyUI/output/Baimifan/v034')
def read(p):return json.loads(p.read_text('utf8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),'utf8')
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]))
a=argparse.ArgumentParser();a.add_argument('job');a.add_argument('--id',required=True);a.add_argument('--start',type=int,default=0);a.add_argument('--end',type=int,required=True);a.add_argument('--frames',type=int,required=True);a.add_argument('--note',required=True);a.add_argument('--crop',help='w:h:x:y');args=a.parse_args()
files=list(N.glob(args.job+'_*.mp4'));assert len(files)==1
src=files[0];v=next(s for s in probe(src)['streams'] if s['codec_type']=='video')
assert 0<=args.start<args.end<=int(v['nb_frames']) and args.frames>0
out=P/'edits'/(args.id+'_'+args.job+'_adopted.mp4');out.parent.mkdir(exist_ok=True)
assert not out.exists(),'Preserve existing adoption; use a new versioned source job'
vf=[f'trim=start_frame={args.start}:end_frame={args.end}',f'setpts=(PTS-STARTPTS)*{args.frames}/{args.end-args.start}','fps=24:round=near']
if args.crop:vf.append('crop='+args.crop)
vf+=['scale=1344:768:force_original_aspect_ratio=decrease:force_divisible_by=2','pad=1344:768:(ow-iw)/2:(oh-ih)/2','setsar=1','tpad=stop_mode=clone:stop_duration=1']
subprocess.run(['ffmpeg','-y','-v','error','-i',str(src),'-vf',','.join(vf),'-frames:v',str(args.frames),'-an','-c:v','libx264','-preset','fast','-crf','17','-threads','4','-pix_fmt','yuv420p','-color_range','tv','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-chroma_sample_location','left','-movflags','+faststart',str(out)],check=True)
pv=probe(out);vv=next(s for s in pv['streams'] if s['codec_type']=='video')
assert vv['width']==1344 and vv['height']==768 and vv['r_frame_rate']=='24/1' and int(vv['nb_frames'])==args.frames
assert not any(s['codec_type']=='audio' for s in pv['streams'])
subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
record=dict(id=args.id,name=args.id+'_二维修订_v034',source=str(out),source_in=0,source_out_exclusive=args.frames,target_frames=args.frames,review='pass',note=args.note,provenance=dict(job=args.job,source=str(src),source_in=args.start,source_out_exclusive=args.end,crop=args.crop,workflow=str(P/'workflows'/(args.job+'.api.json')),sha256=hashlib.sha256(out.read_bytes()).hexdigest()),probe=pv)
ledger=read(P/'adopted.json') if (P/'adopted.json').exists() else {}
history=read(P/'adoption-history.json') if (P/'adoption-history.json').exists() else []
if args.id in ledger:history.append(ledger[args.id])
ledger[args.id]=record;save(P/'adopted.json',ledger);save(P/'adoption-history.json',history)
print(args.id,args.frames,str(out))
