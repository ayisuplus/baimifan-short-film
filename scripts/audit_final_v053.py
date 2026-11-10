"""Read-only audit of current adopted storyboard and source audio; never resets choices."""
import argparse,concurrent.futures,hashlib,json,re,subprocess
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];OUT=R/'后期/最终审查-v053';OUT.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ap=argparse.ArgumentParser();ap.add_argument('--manifest',default='镜头设计/shot-plan-v0.53.json');ap.add_argument('--reuse-audio',action='store_true');args=ap.parse_args()
path=args.manifest;p=read(path);cfg=read(p['audio_arrangement']);adopt=read(p['music_adoption'])
assert cfg['shot_plan_sha256']==sha(R/path)==adopt['source_plan_sha256']
music={m['id']:m for mf in cfg['music_manifests'] for m in read(mf)['music']}
shots=p['shots'];ids=[s['id'] for s in shots];marks=adopt['marks'];assert set(marks)==set(ids) and len(ids)==len(set(ids))
script=(R/p['story_script']).read_text(encoding='utf-8-sig');elapsed=0;images={};voices=[];flags=[];subtitles=0
for s in shots:
 assert s['start_second']==elapsed;elapsed+=s['seconds'];assert s['end_second']==elapsed
 assert s['source_quote'] in script,s['id']
 f=R/s['presentation']['path'];assert f.is_file(),str(f)
 if str(f) not in images:
  with Image.open(f) as im:w,h=im.size;im.verify()
  images[str(f)]=dict(path=s['presentation']['path'],size=[w,h],sha256=sha(f))
 for c in s.get('subtitle_cues',[]):
  subtitles+=1;assert c['offset']>=0 and c['offset']+c['duration']<=s['seconds']+.001
  units=len(re.findall(r'[\u4e00-\u9fff]|[A-Za-z]+',c['text']))
  if units/c['duration']>5:flags.append(dict(id=s['id'],text=c['text'],units_per_second=units/c['duration'],note='跨镜连读需要结合整句，非实际听审结论'))
 for c in s['dialogue_cues']:
  f=R/c['file'];d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(f)]));dur=float(d['format']['duration']);assert c['offset']+dur<=s['seconds']+.03
  voices.append(dict(shot=s['id'],file=c['file'],duration=dur,sha256=sha(f)))
assert elapsed==p['total_seconds']
for m in music.values():assert sha(R/m['path'])==m['sha256'],m['id']
runs=[]
for s in shots:
 mid=marks[s['id']]
 if runs and runs[-1]['music_id']==mid:runs[-1].update(last_shot=s['id'],end=s['end_second'],shots=runs[-1]['shots']+1)
 else:runs.append(dict(first_shot=s['id'],last_shot=s['id'],start=s['start_second'],end=s['end_second'],shots=1,music_id=mid,title=music[mid]['title']))
for r in runs:r.update(timeline_seconds=r['end']-r['start'],source_seconds=music[r['music_id']]['duration'],shortfall_if_full_bed=max(0,r['end']-r['start']-music[r['music_id']]['duration']))
def measure(mid):
 m=music[mid];f=R/m['path'];result=subprocess.run(['ffmpeg','-v','info','-nostats','-i',str(f),'-af','loudnorm=I=-23:TP=-2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,encoding='utf-8',errors='replace',check=True)
 log=result.stderr;v=json.loads(log[log.rfind('{'):log.rfind('}')+1])
 return dict(id=mid,title=m['title'],path=m['path'],sha256=sha(f),duration=m['duration'],decode_ok=True,lufs=float(v['input_i']),true_peak_db=float(v['input_tp']),loudness_range_lu=float(v['input_lra']))
if args.reuse_audio:
 measured=read('后期/最终审查-v053/全片结构与音频核验.json')['selected_music']
 assert {m['id'] for m in measured}==set(marks.values())
 for m in measured:assert m['sha256']==sha(R/m['path'])
else:
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:measured=list(ex.map(measure,sorted(set(marks.values()))))
record=dict(plan=path,plan_sha256=sha(R/path),shots=len(shots),seconds=elapsed,source_quotes_verified=len(shots),subtitle_count=subtitles,subtitle_overflow=0,subtitle_reading_flags=flags,voice_clips=voices,image_files=list(images.values()),all_candidate_hashes_verified=len(music),adopted_runs=runs,selected_music=measured,full_music_listening=False,continuous_video_viewing=False,formal_mix=False,method='Current files probed/hashed and selected audio fully decoded with FFmpeg loudness analysis; not listening approval')
(OUT/'全片结构与音频核验.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:record[k] for k in ['shots','seconds','subtitle_count','subtitle_reading_flags','all_candidate_hashes_verified','adopted_runs','selected_music']},ensure_ascii=False))
