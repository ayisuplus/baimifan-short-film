import json, subprocess, pathlib, concurrent.futures

ROOT=pathlib.Path(__file__).resolve().parent
V034=ROOT.parent
PROJECT=V034.parent.parent
def read(p): return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def write(p,obj): pathlib.Path(p).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def run(args): subprocess.run(args,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]))

def group4():
    audit=read(V034/'审查-水龙.json')
    plan={r['id']:r for r in read(PROJECT/'后期/后半程逐段修订-v032/group-04.json')}
    idx={r['shot']:r for r in read(PROJECT/'后期/后半程逐镜审查-v031/镜头索引.json')}
    rows=[]
    for r in sorted(audit['rows'],key=lambda x:x['id']):
        i=r['id']
        if i in ['076','084']: continue
        if i=='069':
            s=idx[i]
            rows.append(dict(name=i+'-v034-preserve',id=i,source=s['source'].replace('\\','/'),source_in=0,source_out_exclusive=s['frames'],target_frames=s['frames'],status='pass',note='原升空建立镜保留；新剪辑小节另抽帧检查。'))
        elif r['kind']=='video' and r['usable_source_range_exclusive']:
            a,b=r['usable_source_range_exclusive']
            rows.append(dict(name=i+'-v034-edit',id=i,source=r['source'].replace('\\','/'),source_in=a,source_out_exclusive=b,target_frames=r['target_frames'],status='trim',note=r['reason']+' '+r['fix']))
        else:
            rows.append(dict(name=i+'-v034-pending',id=i,source=None,source_in=None,source_out_exclusive=None,target_frames=plan[i]['target_frames'],status='pending',note='等待动态审查通过。'+r['reason']+' '+r['fix']))
    write(V034/'edit-group-04-draft.json',rows)

def encode(r):
    out=ROOT/(r['name']+'.mp4')
    p=probe(r['source']); v=next(s for s in p['streams'] if s['codec_type']=='video')
    a,b,t=r['source_in'],r['source_out_exclusive'],r['target_frames']
    assert 0<=a<b<=int(v['nb_frames'])
    vf=f'trim=start_frame={a}:end_frame={b},setpts=(PTS-STARTPTS)*{t}/{b-a},fps=24:round=near,scale=1344:768:force_original_aspect_ratio=decrease:force_divisible_by=2,pad=1344:768:(ow-iw)/2:(oh-ih)/2,setsar=1,tpad=stop_mode=clone:stop_duration=1'
    run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',r['source'],'-vf',vf,'-frames:v',str(t),'-an','-c:v','libx264','-preset','fast','-crf','17','-threads','4','-pix_fmt','yuv420p','-color_range','tv','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-chroma_sample_location','left','-movflags','+faststart',str(out)])
    q=probe(out); streams=q['streams']; w=next(s for s in streams if s['codec_type']=='video')
    assert w['width']==1344 and w['height']==768 and w['r_frame_rate']=='24/1' and int(w['nb_frames'])==t and not any(s['codec_type']=='audio' for s in streams)
    return dict(id=r['id'],output=str(out),source=r['source'],source_in=a,source_out_exclusive=b,target_frames=t,source_dimensions=[v['width'],v['height']],output_dimensions=[1344,768],fps=24,audio_streams=0,verified=True,note=r['note'])

def make_flash():
    p=ROOT/'055to056-cold-white-flash-2f.mp4'
    run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','lavfi','-i','color=c=0xe9f5ff:s=1344x768:r=24','-frames:v','2','-an','-c:v','libx264','-preset','fast','-crf','17','-threads','2','-pix_fmt','yuv420p','-color_range','tv','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-chroma_sample_location','left',str(p)])
    return p

def preview(group,number,rows,flash):
    label=f'preview-g{group:02d}-part{number:02d}'
    entries=[]; cuts=[]; pos=0
    for r in rows:
        if r['id']=='056' and entries and rows[rows.index(r)-1]['id']=='055':
            entries.append(f"file '{flash.as_posix()}'")
            cuts.append(dict(id='055to056-flash',start=pos,frames=2));pos+=2
        entries.append(f"file '{(ROOT/(r['name']+'.mp4')).as_posix()}'")
        cuts.append(dict(id=r['id'],start=pos,frames=r['target_frames']));pos+=r['target_frames']
    listing=ROOT/(label+'.ffconcat'); listing.write_text('\n'.join(entries)+'\n',encoding='utf-8')
    out=ROOT/(label+'.mp4')
    run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-c','copy','-an','-movflags','+faststart',str(out)])
    vp=next(s for s in probe(out)['streams'] if s['codec_type']=='video')
    assert int(vp['nb_frames'])==pos
    # Dense sequential overview: one frame per six source frames at 24 fps.
    n=(pos+5)//6; columns=6; lines=(n+columns-1)//columns
    sheet=ROOT/(label+'.jpg')
    run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(out),'-vf',f"select=not(mod(n\\,6)),scale=320:-1,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='%{{pts\\:hms}}':fontsize=14:fontcolor=white:box=1:boxcolor=black@0.7:x=4:y=h-20,tile={columns}x{lines}",'-frames:v','1',str(sheet)])
    return dict(name=label,source_ids=[r['id'] for r in rows],frames=pos,cuts=cuts,output=str(out),sheet=str(sheet),complete_group=False)

def main():
    if not (V034/'edit-group-04-draft.json').exists(): group4()
    groups={n:read(V034/f'edit-group-{n:02d}-draft.json') for n in [2,3,4]}
    rows=[r for g in groups.values() for r in g if r['source'] is not None and r['status']!='pending']
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(encode,rows))
    flash=make_flash()
    previews=[]
    for n,rows in groups.items():
        chunks=[];current=[]
        for r in rows:
            if r['status']=='pending' or r['source'] is None:
                if current:chunks.append(current);current=[]
            else:current.append(r)
        if current:chunks.append(current)
        for j,chunk in enumerate(chunks,1): previews.append(preview(n,j,chunk,flash))
    report=dict(codec='libx264',crf=17,fps=24,size=[1344,768],audio=False,retiming='frame sampling only; no optical flow',fit='uniform fit and centered pad; no aspect crop or stretching',color_tags='BT.709 limited range, left chroma location, consistent across original and generated clips',clips=results,previews=previews,executed_effect=dict(file=str(flash),frames=2,color='#E9F5FF',position='055 -> 056, inserted only into group02 part01 preview; standalone source for parent to insert',executed=True),pending={str(n):[r['id'] for r in g if r['status']=='pending'] for n,g in groups.items()},complete=False)
    for part in previews:
        run(['ffmpeg','-hide_banner','-loglevel','error','-i',part['output'],'-f','null','-'])
        part['full_decode_check']='pass'
    write(ROOT/'validation.json',report)
    install={}
    for n,group in groups.items():
        seq=[]
        for r in group:
            if r['id']=='056':
                seq.append(dict(id='055to056-flash',source=str(flash),source_in=0,source_out_exclusive=2,target_frames=2,status='ready',note='实际执行的2帧冷白闪；原055/056源镜不改。'))
            ready=r['source'] is not None and r['status']!='pending'
            seq.append(dict(id=r['id'],source=str(ROOT/(r['name']+'.mp4')) if ready else None,source_in=0 if ready else None,source_out_exclusive=r['target_frames'] if ready else None,target_frames=r['target_frames'],status='ready' if ready else 'pending',note=r['note']))
        install[str(n)]=seq
    write(ROOT/'install-manifest.json',install)
    print(json.dumps(dict(clips=len(results),previews=len(previews),pending=report['pending']),ensure_ascii=False))

if __name__=='__main__': main()
