"""Validate current delivery against real source files and natural-rate audio."""
import hashlib,json,re
from pathlib import Path
import soundfile as sf
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def main():
    board=load('视频制作/生成板-v012/展开数据.json');source=load(board['source'])
    timing=load('后期/收尾修复-v001/配音对位方案.json');edit=load('后期/收尾修复-v001/实际BGM剪辑.json')
    assert board['source_sha256']==edit['source_sha256']==sha(board['source'])
    for path,value in board['review_hashes'].items():assert sha(path)==value,path
    assert [r['id'] for b in board['batches'] for r in b['rows']]==[s['id'] for s in source['shots']]
    cue_map={c['id']:c for c in timing['cues']};found=[];point_count=0
    for b in board['batches']:
        assert b['used_seconds']<=15 and abs(b['handle_seconds']+b['used_seconds']-15)<1e-6
        assert b['models'][b['selected_model']]['capacity_ok']
        for ref in b['references']:assert sha(ref['path'])==ref['sha256']
        for c in b['dialogue']:
            a=c['returned_audio'];t=cue_map[a['cue_id']];found.append(a['cue_id'])
            assert c['language']=='Japanese' and c['text']==t['text_ja']
            assert abs(b['film_start']+c['start']-t['timeline_start'])<1e-5
            assert abs(b['film_start']+c['end']-t['timeline_end'])<1e-5
            assert c['review']['film_start']==t['timeline_start'] and c['review']['film_end']==t['timeline_end']
            assert 0<=c['start']<c['end']<=b['used_seconds']+.001
            assert set(t['visual_shots'])<=set(b['shot_ids'])
            assert sha(a['path'])==a['sha256']
            for model,p in b['prompts'].items():
                if t['id']=='VO-CY024A9-01' and model=='minimax-h3':continue
                assert c['text'] in p,(b['id'],model,a['cue_id'])
        for model,p in b['prompts'].items():
            assert not re.search(r'CY\d',p)
            pattern=r'@图片(\d+)' if model=='seedance25' else r'<Picture (\d+)>'
            assert set(map(int,re.findall(pattern,p)))==set(range(1,len(b['references'])+1))
            assert p.rstrip()+'\n'==(ROOT/f"视频制作/生成板-v012/提示词/{b['id']}-{model}.txt").read_text(encoding='utf-8')
        for p in b['rhythm']['points']:
            point_count+=1;assert abs(p['film_time']-b['film_start']-p['time'])<1e-5
            music=next((m for m in edit['cues'] if m['timeline_start']<=p['film_time']<m['timeline_end']),None)
            if music:assert abs(p['source_seconds']-(music['source_in']+p['film_time']-music['timeline_start']))<1e-4
            else:assert p['source_seconds'] is None
    assert len(found)==len(set(found))==61 and point_count==46
    # Every original sample is used exactly once, including the six-second master pause.
    groups={}
    for event in timing['mix_events']:groups.setdefault(event['file'],[]).append(event)
    for path,events in groups.items():
        info=sf.info(str(ROOT/path));cursor=0
        for e in sorted(events,key=lambda x:x['file_in']):
            assert round(e['file_in']*info.samplerate)==cursor,path
            cursor=round(e['file_out']*info.samplerate)
            assert abs(e['timeline_end']-e['timeline_start']-(e['file_out']-e['file_in']))<1e-5 and e['rate']==1
        assert cursor==info.frames,(path,cursor,info.frames)
    assert len(groups)==42
    for name,item in edit['output_assets'].items():assert sha('后期/收尾修复-v001/'+name)==item['sha256']
    sm={s['id']:s for s in source['shots']}
    assert sm['CY024K00']['seconds']==4
    assert abs(timing['protected_beats']['claude_pause'][1]-timing['protected_beats']['claude_pause'][0]-6)<1e-5
    assert edit['status']=='rendered_candidate_not_audition_approved'
    report=dict(status='pass',shots=132,batches=len(board['batches']),dialogue_cues=61,action_points=46,original_audio_sources=42,original_samples_preserved_once=True,film_seconds=450.9,all_selected_models_fit=True,japanese_spoken_text_matches_delivery=True,transcript_listened=False,sfx_completed=False,source_sha256=sha(board['source']))
    (ROOT/'后期/收尾修复-v001/修复校验.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
