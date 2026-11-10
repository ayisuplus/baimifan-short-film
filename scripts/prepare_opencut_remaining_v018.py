"""Prepare individual silent editing clips from the saved v014 readback. No Resolve connection."""
from pathlib import Path
import json, subprocess, hashlib

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'后期/OpenCut后续画面-v018'
CLIPS=OUT/'逐镜视频'
CLIPS.mkdir(parents=True,exist_ok=True)
source=ROOT/'后期/宫殿调色-v014/after.json'
data=json.loads(source.read_text(encoding='utf8'))
shots=[s for s in data['tracks'][0]['items'] if s['start']>=1282]
assert len(shots)==116 and all(a['end']==b['start'] for a,b in zip(shots,shots[1:]))
rows=[]
for index,s in enumerate(shots,4):
    n=round(s['end']-s['start']);p=s['properties'];rate=s['speed']['Percentage']/100
    dest=CLIPS/f"{index:03d}_{s['name']}.mp4"
    filters=[f"trim=start_frame={s['source_start']}",f"setpts=(PTS-STARTPTS)/{rate}","fps=24","scale=1344:768:force_original_aspect_ratio=decrease","pad=1344:768:(ow-iw)/2:(oh-ih)/2","setsar=1"]
    if p['ZoomX']!=1 or p['Pan']!=0 or p['Tilt']!=0:
        w=round(1344*p['ZoomX']/2)*2;h=round(768*p['ZoomY']/2)*2
        x=(w-1344)/2-p['Pan'];y=(h-768)/2+p['Tilt']
        assert -1<=x<=w-1344+1 and -1<=y<=h-768+1,(s['name'],x,y,w,h)
        x=max(0,min(x,w-1344));y=max(0,min(y,h-768))
        filters += [f'scale={w}:{h}',f'crop=1344:768:{x}:{y}']
    filters += ['tpad=stop_mode=clone:stop_duration=1']
    if not dest.exists():
        subprocess.run(['ffmpeg','-v','error','-y','-threads','2','-filter_threads','2','-i',s['path'],'-an','-sn','-dn','-vf',','.join(filters),'-frames:v',str(n),'-c:v','libx264','-threads','2','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],check=True)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,nb_frames,r_frame_rate,width,height','-of','json',str(dest)]))
    assert len(probe['streams'])==1 and probe['streams'][0]['codec_type']=='video'
    assert int(probe['streams'][0]['nb_frames'])==n,(dest,n,probe)
    rows.append(dict(file=dest.name,path=str(dest),frames=n,start_frame=round(s['start']-1282+666),end_frame=round(s['end']-1282+666),original=s,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),retime_method='frame sampling; Resolve optical flow not transferred' if rate!=1 else 'original rate'))
    print(f'{index-3}/116 {dest.name} {n} frames',flush=True)
    (OUT/'迁移清单.json').write_text(json.dumps(dict(source_snapshot=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),resolve_accessed=False,video_only=True,clips=rows,total_new_frames=sum(r['frames'] for r in rows),target_total_frames=9538,finished=len(rows)==116),ensure_ascii=False,indent=2),encoding='utf8')
print('DONE',len(rows),sum(r['frames'] for r in rows),flush=True)
