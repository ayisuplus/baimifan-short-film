"""Build the v025 board and actual full-audio preview from reconciled clocks."""
from pathlib import Path
import subprocess,sys,json
from prepare_generation_v025 import ROOT,OUT,FIX,SOURCE,load,write

def renderer(name,entry='main'):
 path=ROOT/'scripts'/name
 code=path.read_text('utf-8').replace('视频制作/生成板-v014',OUT).replace('后期/生成前修正-v014',FIX).replace('镜头设计/shot-plan-v0.59.json',SOURCE)
 code=code.replace("p['music_intent']='本镜5.74–6.54秒收声留白0.8秒，后期保留水流'", "p['music_intent']='按新版祈愿词尾至术名起声收音乐0.8秒，后期保留水流'")
 code=code.replace('连续咏唱的句界是估算定位，不代表逐词识别验收。','每句边界依据完整新版干声实测；文件内部停顿原样保留，未做逐词识别验收。')
 code=code.replace('t.toFixed(2)','t.toFixed(6)')
 ns={'__file__':str(path),'__name__':'v025_adapter'}
 exec(compile(code,str(path),'exec'),ns)
 return ns[entry](ROOT) if entry=='build' else ns[entry]()

def main():
 subprocess.run([sys.executable,str(ROOT/'scripts/build_repaired_audio_preview.py'),'--root',str(ROOT),'--source',SOURCE,'--bgm-plan',FIX+'/BGM剪辑方案.json','--voice-plan',FIX+'/配音对位方案.json','--out',FIX],check=True)
 renderer('build_generation_v014.py')
 renderer('build_previs_v014.py','build')
 valid={b['id']+'-'+m+'.txt' for b in load(OUT+'/展开数据.json')['batches'] for m in b['prompts']}
 for p in (ROOT/OUT/'提示词').glob('*.txt'):
  if p.name not in valid:
   archive=ROOT/FIX/'中间稿提示词'/p.name
   archive.parent.mkdir(exist_ok=True);p.replace(archive)
 print('v025 board and preview built')

if __name__=='__main__':main()
