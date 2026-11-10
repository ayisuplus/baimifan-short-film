"""Fetch explicitly selected public video AAC tracks with resumable per-track records."""
import argparse, hashlib, json, subprocess, urllib.request, concurrent.futures, re
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True)
    ap.add_argument('--round',default='v002');ap.add_argument('--date',default='2026-10-23');args=ap.parse_args()
    if not re.fullmatch(r'v\d{3}',args.round):ap.error('Expected round vNNN')
    root=args.root.resolve();folder=root/('后期/BGM重选-'+args.round)
    choices=json.loads((folder/'候选提取清单.json').read_text(encoding='utf-8'))['music']
    output=root/('资产/声音/BGM/重选-'+args.round);output.mkdir(parents=True,exist_ok=True)
    records=folder/'提取记录';records.mkdir(exist_ok=True)
    def fetch(c):
        rid=records/(c['id']+'.json');target=output/(c['id']+'.m4a')
        if rid.exists():
            old=json.loads(rid.read_text(encoding='utf-8'))
            if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()==old['sha256']:return old
            raise RuntimeError('Existing record integrity mismatch: '+c['id'])
        base='https://www.bilibili.com/video/'+c['bvid']+'/'
        headers={'User-Agent':'Mozilla/5.0','Referer':base}
        def get(url):
            with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=60) as r:return r.read()
        source=json.loads((folder/(c['bvid']+'-来源.json')).read_text(encoding='utf-8'))
        page=source['pages'][c['part']-1];assert page['part']==c['source_page_title']
        extraction='Public video DASH AAC saved without re-encoding, cuts, pitch, speed or gain changes.'
        source_media=None
        if not target.exists():
            data=json.loads(get(f'https://api.bilibili.com/x/player/playurl?bvid={c["bvid"]}&cid={page["cid"]}&fnval=16&qn=64'))
            if data['code']:raise RuntimeError('Play API '+str(data['code']))
            streams=[a for a in data['data'].get('dash',{}).get('audio',[]) if a.get('codecs','').startswith('mp4a')]
            temp=target.with_suffix('.part.m4a')
            if streams:
                stream=max(streams,key=lambda a:a.get('bandwidth',0))
                temp.write_bytes(get(stream.get('baseUrl') or stream['base_url']))
            else:
                segments=data['data'].get('durl',[])
                if len(segments)!=1:raise RuntimeError('No DASH audio or single public muxed video')
                source_video=output/(c['id']+'-source.mp4')
                if not source_video.exists():
                    source_video.write_bytes(get(segments[0]['url']))
                subprocess.run(['ffmpeg','-v','error','-y','-i',str(source_video),'-map','0:a:0','-vn','-c:a','copy',str(temp)],check=True,capture_output=True)
            subprocess.run(['ffmpeg','-v','error','-i',str(temp),'-f','null','-'],check=True,capture_output=True)
            temp.rename(target)
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,sample_rate,channels,bit_rate','-of','json',str(target)]))
        subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True,capture_output=True)
        duration=float(probe['format']['duration']);assert abs(duration-page['duration'])<2
        source_video=output/(c['id']+'-source.mp4')
        if source_video.exists():
            source_media=dict(path=source_video.relative_to(root).as_posix(),bytes=source_video.stat().st_size,sha256=hashlib.sha256(source_video.read_bytes()).hexdigest())
            extraction='AAC stream copied from retained public muxed video with ffmpeg -vn -c:a copy; no re-encoding, cuts, pitch, speed or gain changes.'
        item=dict(c,cid=page['cid'],source=base+'?p='+str(c['part']),uploader=source['owner']['name'],video_title=source['title'],path=target.relative_to(root).as_posix(),bytes=target.stat().st_size,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),duration=duration,probe=probe,decode_ok=True,status='候选 · 作者试听比较',heard=False,source_in=None,source_out=None,extraction=extraction)
        if source_media:item['source_media']=source_media
        rid.write_text(json.dumps(item,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'id':c['id'],'title':c['title'],'seconds':duration,'decode_ok':True},ensure_ascii=False),flush=True)
        return item
    done=[];errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        futures={ex.submit(fetch,c):c for c in choices}
        for f in concurrent.futures.as_completed(futures):
            try:done.append(f.result())
            except Exception as err:errors.append({'id':futures[f]['id'],'error':str(err)})
    if errors:
        print(json.dumps(errors,ensure_ascii=False));raise SystemExit(1)
    by_id={m['id']:m for m in done}
    manifest={'version':args.round,'date':args.date,'music':[by_id[c['id']] for c in choices],'listening_status':'Technical decoding validated; shot assignments are audition hypotheses for author comparison.'}
    (root/('资产/生成记录/BGM重选-音频-'+args.round+'.json')).write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
