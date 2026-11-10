import json,subprocess,argparse,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
N=Path('G:/comfyui/ComfyUI/ComfyUI/output/Baimifan/v032')
index={r['shot']:r for r in json.loads((P.parent/'后半程逐镜审查-v031/镜头索引.json').read_text('utf8'))}
a=argparse.ArgumentParser();a.add_argument('group',type=int);a.add_argument('--skip-missing',action='store_true');args=a.parse_args()
rows=json.loads((P/f'edit-group-{args.group:02}.json').read_text('utf8'))
receipts=[]
for r in rows:
 src=Path(index[r['id']]['source']) if r.get('original') else N/f"{r['id']}-video-r{r.get('revision',1)}-no-upscale_00001_.mp4"
 if not src.exists() and args.skip_missing:continue
 assert src.exists(),src
 target=P/'edits'/r['name'];target.parent.mkdir(exist_ok=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,nb_frames','-of','json',str(src)]))['streams'][0]
 assert r['end']<=int(probe['nb_frames']),r
 crop='crop=1344:756,' if probe['width']==1344 and probe['height']==768 else ''
 ratio=r['frames']/(r['end']-r['start'])
 vf=f"trim=start_frame={r['start']}:end_frame={r['end']},setpts=(PTS-STARTPTS)*{ratio},{crop}fps=24,setsar=1"
 subprocess.run(['ffmpeg','-v','error','-i',str(src),'-vf',vf,'-frames:v',str(r['frames']),'-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-y',str(target)],check=True)
 out=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(target)]))['streams']
 assert len(out)==1 and out[0]['codec_type']=='video' and int(out[0]['nb_read_frames'])==r['frames'],(r,out)
 receipts.append(dict(**r,path=str(target),source=str(src),sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
(P/f'edit-group-{args.group:02}-verified.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2),encoding='utf8')
print('assembled',len(receipts),'/',len(rows),flush=True)
