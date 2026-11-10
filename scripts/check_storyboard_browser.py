"""Read-only browser checks for the actual storyboard, including media and playback controls."""
import json, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(sys.argv[1]).resolve()
out=root/"镜头设计/核验截图"
out.mkdir(parents=True,exist_ok=True)
plan=json.loads((root/(sys.argv[2] if len(sys.argv)>2 else "镜头设计/shot-plan-v0.5.json")).read_text(encoding="utf-8"))
total=plan["total_seconds"]; count=len(plan["shots"]); revision=plan["revision"]
errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",args=["--allow-file-access-from-files"])
    page=browser.new_page(viewport={"width":1440,"height":1080},device_scale_factor=1)
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.goto((root/"镜头设计/带图分镜.html").as_uri(),wait_until="load",timeout=60000)
    page.locator("img").evaluate_all("(els)=>els.forEach(e=>e.loading='eager')")
    page.wait_for_function("Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)",timeout=60000)
    assert page.locator(".shot").count()==count
    assert page.locator(".scene").count()==6
    assert page.locator(".scene-jump").count()==6
    page.locator("#previs").scroll_into_view_if_needed()
    page.screenshot(path=str(out/f"desktop-{revision}.png"),full_page=False)
    media=page.evaluate("""async()=>{
      const clips=window.__storyboard.shots.flatMap(s=>s.audio);
      const results=[];
      for(const c of clips){
        const a=new Audio(c.url);
        const duration=await new Promise((resolve,reject)=>{a.onloadedmetadata=()=>resolve(a.duration);a.onerror=()=>reject(new Error(c.url));});
        results.push({file:c.file,duration});
      }
      return results;
    }""")
    page.locator("#play").click()
    page.wait_for_timeout(1250)
    assert page.evaluate("window.__storyboard.playing")
    assert page.evaluate("window.__storyboard.position")>1
    page.locator("#play").click()
    paused=page.evaluate("window.__storyboard.position")
    assert "已暂停" in page.locator("#audio-status").inner_text()
    page.wait_for_timeout(200)
    assert abs(page.evaluate("window.__storyboard.position")-paused)<0.01
    refusal=next(s for s in plan["shots"] if s["id"]=="CY007")
    page.evaluate("t=>{window.__storyboard.seek(t);window.__storyboard.setPlaying(true)}",refusal["start_second"]+0.1)
    page.wait_for_timeout(350)
    assert "CY007" in page.locator("#stage-title").inner_text()
    page.evaluate("window.__storyboard.setPlaying(false)")
    last_scene_start=next(s["start_second"] for s in plan["shots"] if s["scene"]=="S06")
    page.locator(f".scene-jump[data-start='{last_scene_start}']").click()
    assert "CY031" in page.locator("#stage-title").inner_text()
    page.locator("#next").click()
    first_ending_index=next(i for i,s in enumerate(plan["shots"]) if s["id"]=="CY031")
    assert plan["shots"][first_ending_index+1]["id"] in page.locator("#stage-title").inner_text()
    page.locator("#prev").click()
    assert "CY031" in page.locator("#stage-title").inner_text()
    page.evaluate(f"window.__storyboard.seek({total-0.2});window.__storyboard.setPlaying(true)")
    page.wait_for_timeout(500)
    assert not page.evaluate("window.__storyboard.playing")
    assert page.evaluate("window.__storyboard.position")==total
    page.locator("#play").click()
    assert page.evaluate("window.__storyboard.position")<1
    page.locator("#play").click()
    page.locator("#voice").uncheck()
    assert not page.locator("#voice").is_checked()
    assert "已关闭" in page.locator("#audio-status").inner_text()
    split=next(s for s in plan["shots"] if "split_screen_reveal" in s)
    reveal_counts=[]
    for local in [0,0.7,1.3,1.9,2.5]:
        page.evaluate("t=>window.__storyboard.seek(t)",split["start_second"]+local)
        count_revealed=int(page.locator("#stage").get_attribute("data-revealed"))
        reveal_counts.append(count_revealed)
        if local in (0.7,2.5):
            page.screenshot(path=str(out/f"split-{count_revealed}-{revision}.png"),full_page=False)
    assert reveal_counts==[1,2,3,4,5]
    page.evaluate("t=>window.__storyboard.seek(t)",split["end_second"])
    assert page.locator("#stage").evaluate("e=>e.style.clipPath")=="none"
    page.evaluate("t=>window.__storyboard.seek(t)",split["start_second"])
    assert page.locator("#stage").get_attribute("data-revealed")=="1"
    captions=[]
    for s in [s for s in plan["shots"] if "time_caption" in s]:
        cap=s["time_caption"]
        page.evaluate("t=>window.__storyboard.seek(t)",s["start_second"]+cap["offset"]+0.1)
        assert page.locator("#time-caption").inner_text()==cap["text"]
        page.screenshot(path=str(out/f"caption-{s['id']}-{revision}.png"),full_page=False)
        page.evaluate("t=>window.__storyboard.seek(t)",s["start_second"]+cap["offset"]+cap["duration"]+0.01)
        assert page.locator("#time-caption").inner_text()==""
        captions.append({"shot":s["id"],"text":cap["text"],"show_and_clear":True})
    for shot_id in [s["id"] for s in plan["shots"] if s["id"] in ["CY003B","CY016B1","CY021A","CY027","CY025","CY026A1","CY027D","CY027F","CY028","CY028A","CY029A","CY031A","CY032A"]]:
        shot=next(s for s in plan["shots"] if s["id"]==shot_id)
        page.evaluate("t=>window.__storyboard.seek(t)",shot["start_second"])
        page.wait_for_function("document.getElementById('stage-image').complete && document.getElementById('stage-image').naturalWidth>0")
        page.screenshot(path=str(out/f"{shot_id}-{revision}.png"),full_page=False)
    mobile=browser.new_page(viewport={"width":390,"height":844},device_scale_factor=1)
    mobile.goto((root/"镜头设计/带图分镜.html").as_uri(),wait_until="load")
    mobile.locator("#previs").scroll_into_view_if_needed()
    mobile.wait_for_timeout(300)
    assert mobile.evaluate("document.documentElement.scrollWidth<=window.innerWidth+1")
    mobile.screenshot(path=str(out/f"mobile-{revision}.png"),full_page=False)
    atlas=browser.new_page(viewport={"width":1440,"height":1080})
    atlas.goto((root/"资产/资产图册.html").as_uri(),wait_until="load")
    atlas.locator("img").evaluate_all("els=>els.forEach(e=>e.loading='eager')")
    atlas.wait_for_function("Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)")
    asset_count=len(json.loads((root/"资产/assets.json").read_text(encoding="utf-8"))["assets"])
    visual_cards=atlas.locator('main > .grid').first.locator('article')
    assert visual_cards.count()==asset_count
    atlas.locator("#search").fill("Llama")
    assert atlas.locator('main > .grid').first.locator('article:visible').count()==1
    browser.close()
assert not errors,errors
report={"renderer":"headless local Edge via Playwright","cards":count,"scenes":6,"image_decode_in_browser":"all loaded","audio_metadata":media,"controls":["play/pause","advance across cut","scene jump","previous/next shot","seek","end stop","restart","voice toggle"],"mobile_width":390,"overflow":False,"page_errors":errors,"actual_audio_listening":"pending; metadata and playback control only"}
report.update(split_screen_reveal_counts=reveal_counts,split_reset_on_exit_and_seek=True,time_captions=captions,asset_cards=asset_count,asset_search="Llama returns one card")
(root/f"镜头设计/生成记录/浏览器核验-{revision}.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False))
