"""Record source integrity and derive non-destructive panel display regions from sheet gutters."""
import argparse,hashlib,json,math
from pathlib import Path
from PIL import Image
ap=argparse.ArgumentParser()
ap.add_argument("--root",type=Path,required=True)
ap.add_argument("--manifest",default="镜头设计/shot-plan-v0.5.json")
args=ap.parse_args()
root=args.root.resolve()
manifest=root/args.manifest
data=json.loads(manifest.read_text(encoding="utf-8"))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def groups(vals):
    out=[]
    for v in vals:
        if not out or v>out[-1][-1]+2: out.append([v])
        else: out[-1].append(v)
    return [(r[0],r[-1]+1) for r in out]
def boundaries(im,axis,count):
    w,h=im.size; n=w if axis=="x" else h; other=h if axis=="x" else w
    if count == 1:
        return [(0,n)]
    ratios=[]
    sample=range(0,other,3)
    for k in range(n):
        ratios.append(sum(min(im.getpixel((k,j) if axis=="x" else (j,k)))>235 for j in sample)/len(sample))
    whites=groups([i for i,v in enumerate(ratios) if v>.92])
    inner=[]
    for k in range(1,count):
        expected=n*k/count
        options=[g for g in whites if abs((g[0]+g[1])/2-expected)<n/count*.16]
        if not options: raise ValueError(f"No clear {axis} gutter near {expected}")
        inner.append(min(options,key=lambda g:abs((g[0]+g[1])/2-expected)))
    left=0;right=n
    if whites and whites[0][0]==0 and whites[0][1]<12:left=whites[0][1]
    if whites and whites[-1][1]==n and n-whites[-1][0]<12:right=whites[-1][0]
    cuts=[(left,inner[0][0])]
    cuts.extend((inner[i-1][1],inner[i][0]) for i in range(1,len(inner)))
    cuts.append((inner[-1][1],right))
    return [(a+1,b-1) for a,b in cuts]
pages=[]
for layout in data["page_layouts"]:
    path=root/layout["path"]
    with Image.open(path) as original:
        original.verify()
    im=Image.open(path).convert("RGB")
    w,h=im.size
    xs=layout.get('x_intervals') or boundaries(im,"x",layout["cols"])
    ys=layout.get('y_intervals') or boundaries(im,"y",layout["rows"])
    for intervals,count,limit in [(xs,layout['cols'],w),(ys,layout['rows'],h)]:
        assert len(intervals)==count and all(0<=a<b<=limit for a,b in intervals)
        assert all(intervals[i][1]<=intervals[i+1][0] for i in range(count-1))
    ss=[s for s in data["shots"] if s["presentation"]["path"]==layout["path"]]
    assert ss, f"Unused page layout: {layout['path']}"
    cell_count=layout["cols"]*layout["rows"]
    indices=[s["panel_index"] for s in ss]
    assert len(set(indices))==len(indices), f"Repeated source cell: {layout['path']}"
    assert all(isinstance(i,int) and 0<=i<cell_count for i in indices)
    for s in ss:
        i=s["panel_index"]
        a,b=xs[i%layout["cols"]];c,d=ys[i//layout["cols"]]
        # A shot can select a closer, non-destructive view of its own source cell.
        if s.get("display_crop_normalized"):
            cx,cy,cw,ch=s["display_crop_normalized"]
            assert 0<=cx<1 and 0<=cy<1 and 0<cw<=1-cx and 0<ch<=1-cy
            cell_w,cell_h=b-a,d-c
            a,c=a+round(cx*cell_w),c+round(cy*cell_h)
            b,d=a+round(cw*cell_w),c+round(ch*cell_h)
        s["page_size"]=[w,h]
        s["panel_rect_pixels"]=[a,c,b-a,d-c]
        s["panel_region"]={"x":a/w,"y":c/h,"w":(b-a)/w,"h":(d-c)/h}
        assert 1.5<(b-a)/(d-c)<layout.get("max_panel_aspect",2.1),(s["id"],"Unexpected panel aspect; review source sheet before using it")
    pages.append({"scenes":list(dict.fromkeys(s["scene"] for s in ss)),"path":layout["path"],"size":[w,h],"sha256":sha(path),"x_intervals":xs,"y_intervals":ys,"panel_count":cell_count,"referenced_cells":indices,"unused_cells_preserved":[i for i in range(cell_count) if i not in indices],"raster_modified":False})
records=[]
for p in sorted((root/"镜头设计/生成记录").rglob("*请求*.json")):
    doc=json.loads(p.read_text(encoding="utf-8-sig"))
    inputs=set()
    def crawl(obj):
        if isinstance(obj,dict):
            for k,v in obj.items():
                if k=="referenced_image_paths":inputs.update(v)
                else:crawl(v)
        elif isinstance(obj,list):
            for item in obj:crawl(item)
    crawl(doc)
    records.append({"file":str(p.relative_to(root)).replace("\\","/"),"sha256":sha(p),"input_integrity_at_archive":[{"path":v,"sha256":sha(Path(v)),"size_bytes":Path(v).stat().st_size} for v in sorted(inputs)]})
index={"version":data["version"],"engine":"built-in imagegen","purpose":"rough storyboard","input_hash_note":"Hashes verified at archive time against local inputs; frozen request files precede each submitted batch.","script":{"path":data["story_script"],"sha256":sha(root/data["story_script"])},"requests":records,"current_pages":pages,"failed_requests":[{"scene":s,"request":"镜头设计/生成记录/六场粗分镜-请求-v001.json","error":"referenced_image_paths must contain at most 5 paths"} for s in ["S03","S04","S05"]],"media_policy":"Source files preserved; no raster editing or cropping; panel windows are display metadata only.","video_produced":False}
(root/("镜头设计/生成记录/生成索引-"+data.get("revision","v001")+".json")).write_text(json.dumps(index,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
data["source_manifest"]="镜头设计/生成记录/生成索引-"+data.get("revision","v001")+".json"
manifest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"pages":pages,"request_records":len(records)},ensure_ascii=False))
