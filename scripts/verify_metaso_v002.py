"""Verify media without mutating the live submission queue."""
from pathlib import Path
import json,hashlib,subprocess,argparse
ap=argparse.ArgumentParser();ap.add_argument('--revision',choices=['v002','v003'],default='v002');args=ap.parse_args()
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/('视频制作/Metaso-H3-'+args.revision)
q=json.loads((OUT/'执行队列.json').read_text(encoding='utf-8'))
p=OUT/'视频核验.json';records=json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
for b in q['items']:
 if not b.get('local_path') or b['attempt_id'] in records:continue
 path=ROOT/b['local_path'];digest=hashlib.sha256(path.read_bytes()).hexdigest();assert digest==b['sha256']
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],encoding='utf-8'))
 r=subprocess.run(['ffmpeg','-hide_banner','-v','error','-i',str(path),'-f','null','-'],capture_output=True,text=True);assert r.returncode==0 and not r.stderr,r.stderr
 sheet=OUT/'审查'/(b['attempt_id']+'-半秒采样.jpg');sheet.parent.mkdir(exist_ok=True)
 subprocess.run(['ffmpeg','-hide_banner','-v','error','-y','-i',str(path),'-vf','fps=2,scale=320:-1,tile=5x6','-frames:v','1',str(sheet)],check=True)
 records[b['attempt_id']]={'file':b['local_path'],'sha256':digest,'probe':probe,'decode':'passed','task_id':b['task_id'],'sheet':sheet.relative_to(ROOT).as_posix(),'visual_review':'pending'}
 p.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8');print(b['attempt_id'],'verified',flush=True)
