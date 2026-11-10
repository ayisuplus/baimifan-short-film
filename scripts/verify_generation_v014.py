"""Check persisted exports against actual sources, timing, and rendered sample evidence."""
import hashlib,json,re
from pathlib import Path
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'视频制作/生成板-v014';FIX=ROOT/'后期/生成前修正-v014'
def load(p):return json.loads((ROOT/p).read_text('utf-8-sig'))
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def near(a,b):assert abs(a-b)<1e-5,(a,b)
def main():
    b=load(OUT/'展开数据.json');p=load(OUT/'批次计划.json');s=load(b['source']);v=load(FIX/'配音对位方案.json');mix=load(FIX/'实际BGM剪辑.json');am=load(OUT/'日语音频映射.json')
    assert len(s['shots'])==133 and len(b['batches'])==41 and len(am['cues'])==len(v['cues'])==63
    near(s['total_seconds'],464.4);near(mix['film_seconds'],464.4)
    assert b['source_sha256']==sha(b['source'])==v['source_sha256']==mix['source_sha256']
    assert b['assets_sha256']==sha(p['assets'])
    assert all(sha(f)==h for f,h in b['review_hashes'].items())
    assert mix['voice_plan_sha256']==sha(FIX/'配音对位方案.json')
    assert mix['bgm_plan_sha256']==sha(FIX/'BGM剪辑方案.json')
    assert [r['id'] for batch in b['batches'] for r in batch['rows']]==[x['id'] for x in s['shots']]
    cursor=0
    for x in s['shots']:near(x['start_second'],cursor);near(x['end_second']-x['start_second'],x['seconds']);cursor=x['end_second']
    near(cursor,464.4)
    page=(OUT/'生成板.html').read_text('utf-8');embedded=json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>',page,re.S)[1]);assert embedded==b
    references=0;h3=[];seed=[]
    for batch in b['batches']:
        assert 0<batch['used_seconds']<=15.000001
        assert len({r['path'] for r in batch['references']})==len(batch['references'])
        for r in batch['references']:assert sha(r['path'])==r['sha256'];references+=1
        for model,prompt in batch['prompts'].items():
            exported=(OUT/'提示词'/f"{batch['id']}-{model}.txt").read_text('utf-8')
            assert exported.rstrip('\n')==prompt.rstrip('\n')
            pattern=r'@图片(\d+)' if model=='seedance25' else r'<Picture (\d+)>'
            assert set(map(int,re.findall(pattern,prompt)))==set(range(1,len(batch['references'])+1))
            assert 'そうかいてんけい' not in prompt and '沧海天倾' not in prompt
            assert not re.search(r'CY\d|VO-@|VO-<Picture',prompt),batch['id']
            assert '不拖音填满' in prompt
            for c in batch['dialogue']:assert c['text'] in prompt
        model=batch['selected_model'];contract=p['model_contracts'][model]
        assert len(batch['references'])<=contract['max_images']
        assert len(batch['prompts'][model])<=contract.get('max_chars',10**9)
        (h3 if model=='minimax-h3' else seed).append(batch['id'])
    assert 'disabled=!m.capacity_ok' in page and 'hidden=!m.capacity_ok' in page
    tm={c['id']:c for c in v['cues']};mapping={c['cue_id']:c for c in am['cues']}
    for batch in b['batches']:
        for c in batch['dialogue']:
            a=c['returned_audio'];t=tm[a['cue_id']]
            assert a['text']==t['text_ja']==c['text'];assert sha(a['path'])==a['sha256']
            near(batch['film_start']+c['start'],t['timeline_start']);near(batch['film_start']+c['end'],t['timeline_end'])
    assert [(tm[k]['timeline_start'],tm[k]['timeline_end']) for k in ['VO-CY008M-01','VO-CY008M-02','VO-CY009-01']]==[(53.6,57.18),(57.53,65.33),(66.5,68.2)]
    spell=tm['VO-CY024A5-02'];near(spell['timeline_start'],309.43);near(spell['timeline_end'],311.46);assert not any(k.startswith('master_') for k in spell)
    near(v['protected_beats']['claude_pause'][1]-v['protected_beats']['claude_pause'][0],6)
    sm={x['id']:x for x in s['shots']};near(sm['CY024K00']['seconds'],4)
    events={e['id']:e for e in mix['voice_events']};near(events['MASTER-GPT-3']['timeline_start']-events['MASTER-GPT-2']['timeline_end'],.8)
    assert len(events)==48
    byfile={}
    for e in events.values():
        assert e['rate']==1;near(e['timeline_end']-e['timeline_start'],e['file_out']-e['file_in'])
        byfile.setdefault(e['file'],[]).append((e['file_in'],e['file_out']))
    for path,ranges in byfile.items():
        ordered=sorted(ranges)
        assert all(x[1]<=y[0]+1e-6 for x,y in zip(ordered,ordered[1:])),path
    gpt=next(m for m in v['masters'] if m['id']=='GPT');assert byfile[gpt['path']]==[(0,31.72),(31.72,47.54)]
    assert [(r['file_in'],r['file_out']) for r in gpt['retired_segments']]==[(47.54,53.0)]
    spans=sorted((x['timeline_start'],x['timeline_end']) for x in mix['cues']+mix['silences']);cursor=0
    for a,z in spans:near(a,cursor);assert z>a;cursor=z
    near(cursor,464.4)
    sources={x['id']:x for x in load(FIX/'BGM剪辑方案.json')['sources']}
    for c in mix['cues']:assert 0<=c['source_in']<c['source_out']<=sources[c['music_id']]['measured_duration'];near(c['playback_rate'],1)
    assert len({c['music_id'] for c in mix['cues']})==7
    assert mix['status']=='rendered_candidate_not_audition_approved'
    assert all(sha(path)==info['sha256'] for path,info in mix['input_assets'].items())
    assert all(sha(FIX/path)==info['sha256'] for path,info in mix['output_assets'].items())
    assert all(x['decoded_seconds']==464.4 and x['all_finite'] for x in mix['render_decode_checks'].values())
    assert all(x['max_gain_db']<=x['target_db']+.0001 for x in mix['mix']['scene_duck_checks'])
    # Verify linked local pages/assets, ignoring UI fragments and media loaded dynamically.
    missing=[]
    for pagepath in [ROOT/'00_打开项目.html',OUT/'生成板.html',FIX/'修正交接.html',FIX/'全片声音预览.html']:
        text=pagepath.read_text('utf-8')
        for path in re.findall(r'(?:src|href)="([^"$]+)"',text):
            if path.startswith(('http:','https:','#','data:')) or '__' in path:continue
            path=unquote(path.split('#')[0]);absolute=(pagepath.parent/path).resolve()
            if absolute==FIX/'验证结果.json':continue  # This successful run creates that linked report.
            if path and not absolute.exists():missing.append(str(absolute))
    assert not missing,missing
    report=dict(status='passed',source_sha256=b['source_sha256'],shots=133,cues=63,batches=41,seconds=464.4,reference_slots=references,h3_batches=h3,seedance_batches=seed,all_selected_models_fit=True,exported_prompts=82,input_audio_assets=len(mix['input_assets']),output_audio_assets=3,mix_events=48,images_and_hashes_verified=True,timing_and_source_samples_verified=True,links_verified=True,explicit_limits=['静帧候选待作者审阅；未生成视频','解码与时码通过不代表实听或动态口型验收'])
    (FIX/'验证结果.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
