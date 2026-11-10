"""Validate the versioned movie's provenance, local review links and preservation of v001."""
import hashlib,json,subprocess
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
root=Path(__file__).resolve().parents[1];out=root/'后期/静帧配乐-v002'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
plan=read(root/'镜头设计/shot-plan-v0.6.json');record=read(out/'粗剪记录.json')
assert record['shot_plan_sha256']==sha(root/record['shot_plan'])
assert record['sha256']==sha(root/record['video'])
assert record['decode_ok'] and record['sample_peak']<1
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,width,height,r_frame_rate','-of','json',str(root/record['video'])]))
assert abs(float(probe['format']['duration'])-239)<.05
vs=next(s for s in probe['streams'] if s['codec_type']=='video')
assert (vs['width'],vs['height'],vs['r_frame_rate'])==(1280,720,'24/1')
assert sum(s['codec_type']=='audio' for s in probe['streams'])==1
old=read(root/'后期/静帧配乐-v001/粗剪记录.json')
assert old['sha256']==sha(root/old['video'])
assert old['shot_plan_sha256']==sha(root/old['shot_plan'])
assert set(s['id'] for s in old['shots']).issubset(s['id'] for s in plan['shots'])
class Links(HTMLParser):
    def __init__(self):super().__init__();self.urls=[]
    def handle_starttag(self,tag,attrs):
        self.urls += [v for k,v in attrs if k in ['src','href','poster'] and v]
checked=[]
for path in [root/'00_打开项目.html',root/'镜头设计/带图分镜.html',out/'试听.html']:
    parser=Links();parser.feed(path.read_text(encoding='utf-8'))
    for u in parser.urls:
        part=urlsplit(u)
        if part.scheme or not part.path:continue
        dest=(path.parent/unquote(part.path)).resolve()
        assert dest.exists(),(path,u)
        checked.append(str(dest))
for s,r in zip(plan['shots'],record['shots']):
    assert s['id']==r['id'] and s['panel_rect_pixels']==r['crop']
    assert sha(root/r['image'])==r['image_sha256']
assert (out/'核验帧/CY028.jpg').exists()
report=dict(shots=69,cuts=68,seconds=239,video_probe=probe,all_source_hashes_match=True,previous_v001_video_and_v005_plan_unchanged=True,local_link_count=len(checked),decode_ok=True,visual_review='All 69 midpoint frames viewed in two contact sheets; new image pages and selected rescue windows independently inspected.',independent_review='C two hands, B/E basin, F last cuff and platform, final D2 close-up accepted as static candidates.',browser_storyboard='69 cards, 21 dialogue metadata, controls, split reveal and responsive checks passed; see 浏览器核验-v006.json.',preview_browser='Not tested: in-app browser blocked file protocol; no bypass attempted.',actual_continuous_watch='not performed',actual_audio_listening='pending author audition',dynamic_motion='not produced')
(out/'核验记录.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['video_probe']},ensure_ascii=False))
