import json, subprocess, hashlib
from pathlib import Path
OUT=Path(__file__).resolve().parent
NATIVE=Path('G:/comfyui/ComfyUI/ComfyUI/output/Baimifan/v030')
PARTS=[('041a',5,73,68),('041b',20,90,70),('041c',0,107,84),('041d',7,73,66)]
adopted=[]
for shot,start,end,target in [('037',5,73,68)]+PARTS:
    source=NATIVE/f'{shot}-2d-i2v-r1-no-upscale_00001_.mp4'
    dest=OUT/('037_小鱼推离撑地_二维_v030.mp4' if shot=='037' else f'{shot}-采用片段.mp4')
    factor=target/(end-start)
    vf=f'trim=start_frame={start}:end_frame={end},setpts=(PTS-STARTPTS)*{factor:.12f},fps=24,setsar=1'
    subprocess.run(['ffmpeg','-v','error','-i',str(source),'-vf',vf,'-frames:v',str(target),'-an','-c:v','libx264','-crf','17','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart','-y',str(dest)],check=True)
    adopted.append({'shot':shot,'source':str(source),'source_start':start,'source_end_exclusive':end,'frames':target,'speed':(end-start)/target,'output':str(dest)})
join=OUT/'041-concat.txt'
join.write_text(''.join(f"file '{shot}-采用片段.mp4'\n" for shot,*_ in PARTS),encoding='utf-8')
full=OUT/'041_小鱼脱手与点火_二维_v030.mp4'
subprocess.run(['ffmpeg','-v','error','-f','concat','-safe','0','-i',str(join),'-c','copy','-an','-movflags','+faststart','-y',str(full)],check=True)
checks=[]
for path,expected in [(OUT/'037_小鱼推离撑地_二维_v030.mp4',68),(full,288)]:
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    streams=info['streams'];s=streams[0]
    assert len(streams)==1 and s['codec_type']=='video'
    assert s['r_frame_rate']=='24/1' and int(s['nb_frames'])==expected
    assert (s['width'],s['height'])==(1344,768)
    assert abs(float(info['format']['duration'])-expected/24)<0.001
    checks.append({'file':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'frames':expected,'duration':info['format']['duration'],'resolution':[1344,768],'fps':'24/1','audio':False})
r={'adopted':adopted,'final_checks':checks,'041_parts_frames':[68,70,84,66],'041_cuts_local':[0,68,138,222,288],'upscale':False}
(OUT/'采用素材核验.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False))
