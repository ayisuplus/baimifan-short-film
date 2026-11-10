"""Controlled two-second push toward bare wood; no generated scene additions."""
from pathlib import Path
import subprocess,json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'视频制作/Metaso-H3-v003'
source=OUT/'修订参考/GB030-1-CY029B2-cold-pov-firstframe-r002.png'
dest=OUT/'产物/CY029B2-local-push-v003.mp4'
# Imagegen-authored clean plate; this is a video camera move, not a new still edit.
# The optical centre moves to the bare wood below the metal brace while zoom accelerates.
vf="scale=3344:1882,zoompan=z='1+0.8*on/47+1.2*pow(on/47,3)':x='iw*0.5-iw/zoom/2':y='ih*(0.5+0.10*on/47)-ih/zoom/2':d=48:s=1344x756:fps=24,pad=1344:768:0:6,setsar=1"
cmd=['ffmpeg','-v','error','-y','-i',str(source),'-vf',vf,'-frames:v','48','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)]
subprocess.run(cmd,check=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
record=dict(method='本地二维摄影推进，不冒充AI空间重建',source=source.relative_to(ROOT).as_posix(),source_sha256=sha(source),output=dest.relative_to(ROOT).as_posix(),sha256=sha(dest),duration=2,frames=48,frame_rate=24,reason='两次生成均擅自添加背景燃烛；已纠正的冷木纹起态保留全部内容，仅做连续渐快推进。镜末硬切现有外部腾燃，不重复释放。',command=cmd)
(OUT/'火种主观-本地摄影记录.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
print('local POV rendered: 48 frames / 2 seconds')
