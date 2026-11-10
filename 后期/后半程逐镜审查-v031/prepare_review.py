import json, subprocess, importlib.util
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
def normalize(path):
    a=json.loads(path.read_text('utf8'));a.sort(key=lambda x:float(x['left'][:-2]))
    k=float(a[0]['width'][:-2])/234
    return [{'name':x['name'],'start':round(float(x['left'][:-2])/k),'frames':round(float(x['width'][:-2])/k)} for x in a]
a=normalize(OUT/'当前工程DOM.json')
b=normalize(ROOT/'后期/小鱼脱手与二维统一-v030/重新加载DOM.json')
assert a==b,'User changed timeline; re-evaluate source trims'
def tc(f):return f'{f//1440:02d}:{(f//24)%60:02d}:{f%24:02d}'
rows=[]
for x in a:
    shot=int(x['name'].split('_')[0])
    if shot<42:continue
    path=ROOT/'后期/OpenCut后续画面-v018/逐镜视频'/x['name']
    assert path.exists(),path
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(path)]))['streams'][0]
    assert int(info['nb_frames'])==x['frames'],(x,info)
    rows.append(dict(x,shot=f'{shot:03d}',source=str(path),start_tc=tc(x['start']),end_tc=tc(x['start']+x['frames']),duration=x['frames']/24))
(OUT/'镜头索引.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
spec=importlib.util.spec_from_file_location('qc','E:/projects/内容创作/创作工具库/scripts/media/clip_qc.py')
qc=importlib.util.module_from_spec(spec);spec.loader.exec_module(qc)
def png_frames(path,temporary,n=3):
    duration=qc.probe(path);result=[]
    for i in range(n):
        moment=duration*(0.08+0.84*i/max(1,n-1))
        frame=int(moment*24)
        dest=OUT/'抽帧'/Path(path).stem/f'{frame:04d}.png'
        dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists():
            subprocess.run(['ffmpeg','-v','error','-i',str(path),'-vf',f'select=eq(n\\,{frame})','-frames:v','1','-pix_fmt','rgb24','-y',str(dest)],check=True)
        assert dest.exists(),(path,frame)
        result.append((moment,dest))
    return result
qc.frames=png_frames
qc.build([Path(x['source']) for x in rows],OUT/'概览',columns=3,cell_width=448,per_sheet=6)
print(json.dumps({'baseline_unchanged':True,'shots':len(rows),'start':rows[0]['start_tc'],'end':rows[-1]['end_tc'],'all_source_lengths_match':True},ensure_ascii=False))
