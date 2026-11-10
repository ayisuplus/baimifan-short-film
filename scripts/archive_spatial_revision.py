"""Verify originals/copies and record accepted display windows, without changing media."""
import hashlib,json
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
base=root/'镜头设计/生成记录/空间修订-v006'
rows=json.loads((base/'输出路径.json').read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
plan=json.loads((root/'镜头设计/shot-plan-v0.6.json').read_text(encoding='utf-8'))
for r in rows:
    source=Path(r['source']);dest=root/r['copy']
    assert sha(source)==sha(dest),r['key']
    im=Image.open(dest);im.verify()
    r.update(sha256=sha(dest),size_bytes=dest.stat().st_size,size=list(Image.open(dest).size),request_sha256=sha(base/r['request']))
    req=json.loads((base/r['request']).read_text(encoding='utf-8'))
    r['inputs']=[dict(path=p,sha256=sha(Path(p))) for p in req['referenced_image_paths']]
    r['current_views']=[dict(shot=s['id'],cell=s['panel_index'],crop=s['panel_rect_pixels']) for s in plan['shots'] if s['presentation']['path']==r['copy']]
    r['status']='used_as_candidate' if r['current_views'] else 'preserved_not_selected'
report=dict(engine='built-in imagegen',requests=len(rows),outputs=rows,notes=['原图与项目副本逐字节哈希一致；所有实际请求保留。','B初稿右下盆、C初稿第三手、F初稿后方楼梯已修订。','D整页未采用，第二格后方台阶再作局部修正后，仅使用两人近景；第一和第三格不采用。','来源与显示窗核验不替代作者审美、实际听审或动态验收。'])
(base/'输出归档.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'outputs':len(rows),'copies_identical':True,'selected_pages':sum(bool(r['current_views']) for r in rows)},ensure_ascii=False))
