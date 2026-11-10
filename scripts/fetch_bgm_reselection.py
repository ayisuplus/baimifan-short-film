"""Extract the six selected public video audio streams, preserving source bytes."""
import argparse, hashlib, json, subprocess, urllib.request
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--root', type=Path, required=True)
args = p.parse_args()
root = args.root.resolve()
record = root / '资产/生成记录/BGM重选-音频-v001.json'
if record.exists():
    raise SystemExit('Completed record exists; preserve it.')
bvid = 'BV1U6BfBCE5o'
base = 'https://www.bilibili.com/video/' + bvid + '/'
headers = {'User-Agent': 'Mozilla/5.0', 'Referer': base}
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=50) as r:
        return r.read()
def api(url):
    d = json.loads(get(url))
    if d.get('code') != 0:
        raise RuntimeError('Bilibili API: ' + str(d.get('code')) + ' ' + d.get('message',''))
    return d['data']
view = api('https://api.bilibili.com/x/web-interface/view?bvid=' + bvid)
pages = {p['page']: p for p in view['pages']}
choices = [(9,'TIME','Time Flows Ever Onward'),(28,'FEAR','Fear Brought Me This Far'),
           (30,'LIFT','Lift My Head From Shadow'),(35,'ZOLTRAAK','Zoltraak'),
           (39,'SCHEME','Things That Scheme in the Dark'),(52,'MAGIC','Ancient Magic')]
folder = root / '资产/声音/BGM/重选-v001'
folder.mkdir(parents=True, exist_ok=True)
music = []
for part, short, title in choices:
    page = pages[part]
    assert title in page['part'], (part, page['part'])
    name = f'BGM-CY-{short}-001'
    target = folder / (name + '.m4a')
    stream = api(f'https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={page["cid"]}&fnval=16&qn=64')
    tracks = [a for a in stream.get('dash',{}).get('audio',[]) if a.get('codecs','').startswith('mp4a')]
    if not tracks:
        raise RuntimeError('No public AAC audio stream: ' + title)
    selected = max(tracks, key=lambda a:a.get('bandwidth',0))
    if not target.exists():
        blob = get(selected.get('baseUrl') or selected['base_url'])
        temp = target.with_suffix('.part.m4a')
        temp.write_bytes(blob)
        subprocess.run(['ffmpeg','-v','error','-i',str(temp),'-f','null','-'],check=True,capture_output=True)
        temp.rename(target)
    probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,sample_rate,channels,bit_rate','-of','json',str(target)]))
    subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True,capture_output=True)
    duration = float(probe['format']['duration'])
    assert abs(duration-page['duration']) < 2, (title, duration, page['duration'])
    item = dict(id=name,title=title,composer='Evan Call',part=part,cid=page['cid'],source=base+f'?p={part}',
                uploader=view['owner']['name'],video_title=view['title'],path=target.relative_to(root).as_posix(),
                bytes=target.stat().st_size,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),probe=probe,
                duration=duration,decode_ok=True,status='候选 · 待听审',heard=False,
                extraction='Video DASH AAC audio stream saved directly; no re-encoding, speed, pitch, gain or cuts.',
                source_in=None,source_out=None)
    music.append(item)
    print(json.dumps({'title':title,'seconds':duration,'bytes':item['bytes'],'decode_ok':True},ensure_ascii=False),flush=True)
record.write_text(json.dumps(dict(version='v001',date='2026-10-23',music=music,source_bvid=bvid,
    listening_status='technical validation only; actual listening pending'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
