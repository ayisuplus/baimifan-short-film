"""Fetch author-linked MP3s with the source-page referrer; freeze a new record."""
import argparse, concurrent.futures, hashlib, json, subprocess, urllib.request
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--root',type=Path,required=True); args=p.parse_args(); root=args.root.resolve()
out=root/'资产/生成记录/声音候选-v002.json'
if out.exists(): raise SystemExit('Preserve v002')
data=json.loads((root/'资产/生成记录/声音候选-v001.json').read_text(encoding='utf-8'))
data['version']='v002'; data['previous']='资产/生成记录/声音候选-v001.json'
def fetch(m):
    path=root/'资产/声音/BGM'/(m['id']+'.mp3')
    try:
        if path.exists(): raise RuntimeError('Refusing overwrite')
        req=urllib.request.Request(m['url'],headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36','Referer':m['source'],'Accept':'*/*'})
        with urllib.request.urlopen(req,timeout=45) as r: blob=r.read()
        tmp=path.with_suffix('.part.mp3'); tmp.write_bytes(blob)
        probe=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,sample_rate,channels','-of','json',str(tmp)],capture_output=True,text=True,check=True)
        subprocess.run(['ffmpeg','-v','error','-i',str(tmp),'-f','null','-'],capture_output=True,check=True)
        tmp.rename(path)
        m.update(path=path.relative_to(root).as_posix(),sha256=hashlib.sha256(blob).hexdigest(),bytes=len(blob),probe=json.loads(probe.stdout),decode_ok=True)
        m['acquisition_history']=[m.pop('acquisition_error',None),'Success with source-page Referer']
    except Exception as ex: m['acquisition_error']=str(ex)
    return m
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: data['music']=list(pool.map(fetch,data['music']))
data['voice_references'].append(dict(id='VOICE-REF-DS-03',title='Let me go大肥鱼和用户深情对唱',creator='星落落_oi',url='https://www.bilibili.com/video/BV13SYr6dEiQ/',role='DeepSeek',finding='原页简介标注作曲为谱乐 AI，并提到谱乐及剪映会员；未标明可调用的独立对白声线。',evidence='内置浏览器实际读取原页简介；播放器连播到此页。未进行听审。',reusable=False))
out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assets=root/'资产/assets.json'; a=json.loads(assets.read_text(encoding='utf-8')); a['sound_manifest']=out.relative_to(root).as_posix(); assets.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps([{'id':m['id'],'path':m.get('path'),'duration':m.get('probe',{}).get('format',{}).get('duration'),'error':m.get('acquisition_error')} for m in data['music']],ensure_ascii=False))
