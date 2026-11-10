"""Pitch-preserving chant timing candidates; keep every chosen original intact."""
from pathlib import Path
import json,subprocess,hashlib
R=Path(__file__).resolve().parents[1];O=R/'后期/导演重构-v003';D=O/'声音/咏唱速度候选';D.mkdir(parents=True,exist_ok=True)
P=json.loads((R/'后期/声画重构-v002/后期执行计划.json').read_text(encoding='utf8'))
rows=[]
for v in P['voice']:
 if v['role']!='GPT' or not v['id'].startswith('VO-CY024A') or not 25<=v['batch']<=31:continue
 if v['id']=='VO-CY024A5-02':continue
 rate=1.12 if v['batch']<=27 else (1.06 if v['batch']==31 else 1.08)
 out=D/(v['id']+f'-tempo{rate:.2f}.wav')
 subprocess.run(['ffmpeg','-v','error','-y','-i',v['path'],'-af',f'apad=pad_dur=0.08,atempo={rate}','-ar','48000','-c:a','pcm_s24le',str(out)],check=True)
 dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(out)]))
 rows.append({**v,'original_path':v['path'],'path':str(out),'original_duration':v['duration'],'duration':dur,'rate':rate,'original_sha256':hashlib.sha256(Path(v['path']).read_bytes()).hexdigest(),'processing':'ffmpeg atempo保持音高，原文件尾补80ms保护后再变速；完整文字不删','status':'candidate_pending_in_context_review'})
(O/'咏唱速度候选.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps([{'id':v['id'],'rate':v['rate'],'seconds':v['duration']} for v in rows]))
