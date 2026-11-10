from pathlib import Path
import json,hashlib,subprocess,urllib.request
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'视频制作/LibTV-H3-v001'
def read(n): return json.loads((OUT/n).read_text(encoding='utf-8'))
def write(n,d): (OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
delivery=read('续生成-交付清单.json')
queue=read('H3节约余量执行队列.json')
verified=read('已交付视频核验.json')
for f in delivery['files']:
 name=Path(f['filename']).name
 assert name==f['filename'] and name.endswith('.mp4')
 b=next(b for b in queue['items'] if b.get('node_id')==f['nodeId'])
 out=OUT/'产物'/name
 if not out.exists(): urllib.request.urlretrieve(f['url'],out)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)],encoding='utf-8'))
 digest=hashlib.sha256(out.read_bytes()).hexdigest()
 result=subprocess.run(['ffmpeg','-hide_banner','-v','error','-i',str(out),'-f','null','-'],capture_output=True,text=True)
 assert result.returncode==0 and not result.stderr,result.stderr
 rel=out.relative_to(ROOT).as_posix()
 record={'file':rel,'bytes':out.stat().st_size,'sha256':digest,'probe':probe,'decode':'passed','visual_review':'pending','task_id':f['taskId']}
 verified=[v for v in verified if v['file']!=rel]+[record]
 b.update(status='generated_candidate',local_path=rel,sha256=digest,actual_duration=float(probe['format']['duration']),task_id=f['taskId'],accepted=False,review='文件与完整解码通过，待视听审片。')
 sheet=OUT/'审查'/(b['batch_id']+'-半秒采样.jpg')
 if not sheet.exists(): subprocess.run(['ffmpeg','-hide_banner','-v','error','-y','-i',str(out),'-vf','fps=2,scale=320:-1,tile=5x6','-frames:v','1',str(sheet)],check=True)
 print(b['batch_id'],f['taskId'],probe['format']['duration'],digest[:12])
 write('H3节约余量执行队列.json',queue)
 write('已交付视频核验.json',verified)
