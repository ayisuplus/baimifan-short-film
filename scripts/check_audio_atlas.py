"""Check local audition playback and references; this is not a listening review."""
import argparse,json
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--report-version',default='v001');a=p.parse_args();root=a.root.resolve()
report=root/f'资产/生成记录/声音图册核验-{a.report_version}.json'
if report.exists(): raise SystemExit('Preserve earlier verification report; select a new version')
assets=json.loads((root/'资产/assets.json').read_text(encoding='utf-8'))
sound=json.loads((root/assets['sound_manifest']).read_text(encoding='utf-8'))
voices=json.loads((root/assets['voice_auditions']).read_text(encoding='utf-8'))
expected=len([m for m in sound['music'] if m.get('path')])+len([v for v in voices['results'] if v.get('path')])
expected+=sum(bool(v.get(k)) for v in voices['results'] if v.get('path') for k in ['reference_path','previous_path'])
expected+=sum(len(v.get('alternatives',[])) for v in voices['results'] if v.get('path'))
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',args=['--allow-file-access-from-files'])
    page=browser.new_page(viewport={'width':1440,'height':1000})
    errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
    page.goto((root/'资产/资产图册.html').as_uri(),wait_until='load')
    assert page.locator('audio').count()==expected
    page.wait_for_function('Array.from(document.querySelectorAll("audio")).every(a=>a.readyState>=1 && Number.isFinite(a.duration))')
    durations=page.locator('audio').evaluate_all('(els)=>els.map(a=>({src:a.getAttribute("src"),duration:a.duration}))')
    for index in range(expected):
        player=page.locator('audio').nth(index)
        player.evaluate('(a)=>a.play()');page.wait_for_timeout(120)
        assert player.evaluate('(a)=>!a.paused&&a.currentTime>0')
        player.evaluate('(a)=>a.pause()')
    video_results=[]
    for player in page.locator('video').all():
        player.evaluate('(v)=>v.play()');page.wait_for_timeout(150)
        assert player.evaluate('(v)=>!v.paused && v.currentTime>0 && v.videoWidth>0')
        video_results.append(player.evaluate('(v)=>({src:v.getAttribute("src"),duration:v.duration,width:v.videoWidth,height:v.videoHeight})'))
        player.evaluate('(v)=>v.pause()')
    page.locator('#search').fill('ChatGPT')
    assert page.locator('article:visible').count()>=1
    page.locator('#search').fill('')
    page.set_viewport_size({'width':390,'height':844})
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth+2')
    assert not errors,errors
    browser.close()
result={'local_audio_players':expected,'playback_progressed':True,'durations':durations,'videos':video_results,'mobile_overflow':False,'javascript_errors':errors,'listening_review':'pending; browser decoding and playback are not human listening'}
report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
