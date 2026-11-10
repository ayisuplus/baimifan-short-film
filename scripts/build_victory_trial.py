"""Render a short existing-storyboard music trial; never change shot timings."""
import argparse, hashlib, json, subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--root', type=Path, required=True)
a = p.parse_args()
root = a.root.resolve()
outdir = root / '资产/声音/试配'
outdir.mkdir(parents=True, exist_ok=True)
output = outdir / 'Victory-援军登场-v001.mp4'
record_path = root / '资产/生成记录/Victory-援军试配-v001.json'
if output.exists() or record_path.exists():
    raise SystemExit('Preserve existing trial; use a new version for revisions')

plan_path = root / '镜头设计/shot-plan-v0.5.json'
plan = json.loads(plan_path.read_text(encoding='utf-8'))
ids = ['CY023', 'CY024', 'CY027', 'CY025']
shots = [s for s in plan['shots'] if s['id'] in ids]
assert [s['id'] for s in shots] == ids
assert sum(s['seconds'] for s in shots) == 13
source = root / '资产/声音/参考/Victory-BV1Qs411J71S.m4a'
start = 127.28
music = outdir / 'Victory-援军登场-v001.m4a'
subprocess.run(['ffmpeg', '-v', 'error', '-n', '-ss', str(start), '-i', str(source),
                '-t', '13', '-af', 'volume=0.55,afade=t=in:d=0.015,afade=t=out:st=11:d=2',
                '-c:a', 'aac', '-b:a', '192k', str(music)], check=True)
segments = []
for shot in shots:
    image = root / shot['presentation']['path']
    x, y, w, h = shot['panel_rect_pixels']
    part = outdir / (shot['id'] + '-victory-v001.mp4')
    vf = f'crop={w}:{h}:{x}:{y},scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p'
    subprocess.run(['ffmpeg', '-v', 'error', '-n', '-loop', '1', '-i', str(image),
                    '-t', str(shot['seconds']), '-vf', vf, '-r', '24', '-an',
                    '-c:v', 'libx264', '-preset', 'fast', '-crf', '20', str(part)], check=True)
    segments.append(part)
listing = outdir / 'victory-v001-concat.txt'
listing.write_text(''.join(f"file '{v.name}'\n" for v in segments), encoding='utf-8')
subprocess.run(['ffmpeg', '-v', 'error', '-n', '-f', 'concat', '-safe', '0', '-i', str(listing),
                '-i', str(music), '-map', '0:v', '-map', '1:a', '-c', 'copy', '-t', '13',
                '-movflags', '+faststart', str(output)], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-i', str(output), '-f', 'null', '-'], check=True)
probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
                    'format=duration:stream=codec_name,width,height,sample_rate,channels', '-of', 'json', str(output)]))
sha = lambda v: hashlib.sha256(v.read_bytes()).hexdigest()
record = dict(title='Victory · 援军登场试配 v001', path=output.relative_to(root).as_posix(),
    audio_path=music.relative_to(root).as_posix(), source_path=source.relative_to(root).as_posix(),
    source_url='https://www.bilibili.com/video/BV1Qs411J71S/',
    official_source='https://www.youtube.com/watch?v=hKRUPYrAQoE',
    source_kind='公开转载；上传者 AG认证男妹妹，非官方发行账号；原官方 YouTube 获取遇登录验证，未绕过',
    source_range_seconds=[start, start+13], timeline_range_seconds=[133,146],
    shots=[dict(id=s['id'],seconds=s['seconds'],image=s['presentation']['path'],crop=s['panel_rect_pixels']) for s in shots],
    edit='原分镜顺序与 2/4/4/3 秒时长不变；静帧硬切；音乐不变速不变调，音量0.55，末尾2秒淡出；无新增对白、拟音或动态动作',
    selection_evidence='在源音频125–150秒测量短时RMS上升沿，127.34秒附近有强瞬态，提前60毫秒起剪。此为试切点，不将波形判断冒称主旋律或听审结果。',
    review_status='文件解码已核验；乐句完整性、熟悉感、听感与画面同步冲击力待作者试听',
    rights='仅本地试配候选；未取得公开发布用同步授权，不代表版权已清理',
    sha256=sha(output),source_sha256=sha(source),shot_plan_sha256=sha(plan_path),probe=probe)
record_path.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,ensure_ascii=False))
