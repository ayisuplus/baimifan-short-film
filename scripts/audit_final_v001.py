"""Freeze author-approved music assignments and audit current local production evidence."""
import argparse, hashlib, json, subprocess, re, concurrent.futures
from pathlib import Path
from PIL import Image

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True)
    root=ap.parse_args().root.resolve();out=root/'后期/终极审查-v001';out.mkdir(exist_ok=True)
    def read(p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
    def save(p,v):(out/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
    path='镜头设计/shot-plan-v0.48-bgm-v006.json';plan=read(path);config=read(plan['audio_arrangement']);shots=plan['shots']
    assert config['shot_plan_sha256']==sha(root/path)
    music={m['id']:m for mf in config['music_manifests'] for m in read(mf)['music']}
    original=read('后期/终极审查-v001/浏览器原始选曲.json')
    scene_map={x['scene'].split(' · ')[0]:x['music_id'] for x in original['choices']}
    ids=[s['id'] for s in shots];kimi=ids[ids.index('CY024R'):ids.index('CY024K4')+1]
    marks={s['id']:('BGM-CY-FZ-02' if s['id'] in kimi else scene_map[s['scene']]) for s in shots}
    rows=[dict(scene=s['scene'],shot=s['id'],title=s['title'],start=s['start_second'],end=s['end_second'],music_id=marks[s['id']],music=music[marks[s['id']]]['title']) for s in shots]
    frozen={'version':'v001','date':'2026-10-25','status':'作者确认用曲，非原曲剪辑点/混音定稿','confirmation':'作者确认六段用曲已定，Kimi另用let the stars fall down；出场范围CY024R–CY024K4，之后恢复S05主题。','scene_defaults':scene_map,'overrides':{sid:'BGM-CY-FZ-02' for sid in kimi},'marks':marks,'shots':rows,'source_plan':path,'source_plan_sha256':sha(root/path),'music_sources':{k:music[k] for k in sorted(set(marks.values()))},'source_in_out_status':'未锁定；需要按乐句剪辑并实际听审','playback_policy':'音乐独立试听；逐镜选择不自动等于逐镜重启曲目'}
    save('作者确认选曲-v001.json',frozen)
    images=[];seen=set();script=(root/plan['story_script']).read_text(encoding='utf-8-sig');elapsed=0;cue_flags=[];clip_count=0
    for s in shots:
        assert s['start_second']==elapsed;elapsed+=s['seconds'];assert s['end_second']==elapsed
        assert s['source_quote'] in script,s['id']
        reg=s['panel_region'];assert all(0<=reg[k]<=1 for k in ('x','y','w','h')) and reg['x']+reg['w']<=1.00001 and reg['y']+reg['h']<=1.00001
        p=root/s['presentation']['path'];assert p.exists(),p
        if p not in seen:
            with Image.open(p) as im:im.verify()
            with Image.open(p) as im:size=im.size
            images.append(dict(path=p.relative_to(root).as_posix(),dimensions=size,sha256=sha(p)));seen.add(p)
        for c in s.get('subtitle_cues',[]):
            assert 0<=c['offset'] and c['offset']+c['duration']<=s['seconds']+.001
            units=len(re.findall(r'[\u4e00-\u9fff]|[A-Za-z]+',c['text']))
            if units/c['duration']>5:cue_flags.append(dict(shot=s['id'],text=c['text'],duration=c['duration'],units=units,units_per_second=round(units/c['duration'],2),status='阅读/表演预算提示，非实际听审失败'))
        for c in s['dialogue_cues']:
            p=root/c['file'];assert p.exists();clip_count+=1
            d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(p)]))
            assert c['offset']+float(d['format']['duration'])<=s['seconds']+.03
    assert elapsed==plan['total_seconds'] and len(set(ids))==len(ids)
    for m in music.values():assert sha(root/m['path'])==m['sha256'],m['id']
    runs=[]
    for row in rows:
        if runs and runs[-1]['music_id']==row['music_id'] and runs[-1]['end']==row['start']:
            runs[-1]['end']=row['end'];runs[-1]['last_shot']=row['shot']
        else:runs.append(dict(first_shot=row['shot'],last_shot=row['shot'],start=row['start'],end=row['end'],music_id=row['music_id']))
    for run in runs:
        run['timeline_duration']=run['end']-run['start'];run['source_duration']=music[run['music_id']]['duration'];run['whole_track_shortfall']=max(0,run['timeline_duration']-run['source_duration'])
    def audio_audit(mid):
        m=music[mid];p=root/m['path'];log=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(p),'-af','loudnorm=I=-23:TP=-2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,encoding='utf-8',errors='replace',check=True).stderr
        measurement=json.loads(log[log.rfind('{'):log.rfind('}')+1])
        return dict(id=mid,title=m['title'],path=m['path'],sha256=m['sha256'],duration=m['duration'],probe=m['probe'],decode_ok=True,input_integrated_lufs=measurement['input_i'],input_true_peak_db=measurement['input_tp'],input_loudness_range_lu=measurement['input_lra'],method='FFmpeg loudnorm analysis; original file unchanged; numbers are not listening approval')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:audios=list(ex.map(audio_audit,sorted(set(marks.values()))))
    save('全片结构与音频核验.json',dict(plan=path,plan_sha256=sha(root/path),shot_count=len(shots),seconds=elapsed,source_quotes_verified=len(shots),subtitle_overflow=0,subtitle_rate_flags=cue_flags,temporary_dialogue_cues=clip_count,image_files=images,all_music_hashes_verified=len(music),selected_music=audios,adopted_runs=runs,continuous_viewing=False,actual_music_listening=False,formal_mix_exists=False))
    print(json.dumps(dict(shots=len(shots),seconds=elapsed,images=len(images),music=len(audios),subtitle_flags=cue_flags,runs=runs,audio=audios),ensure_ascii=False))

if __name__=='__main__':main()
