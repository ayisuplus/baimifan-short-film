from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];O=R/'后期/截图定点修正-v004'
notice='作者最新纠偏：少数镜头仍有3D建模感，画风未通过。当前时间线为 v004_Screenshot_2D_Style_Rework。以下为技术装配记录，不能当作画风采用；正在按片中标准二维动漫逐镜返修。'
p=O/'修订说明.md';s=p.read_text(encoding='utf8')
if not s.startswith('> 作者最新纠偏'):p.write_text('> '+notice+'\n\n'+s,encoding='utf8')
p=O/'工程内审阅.html';s=p.read_text(encoding='utf8')
if 'id="style-rework"' not in s:s=s.replace('<h1>','<aside id="style-rework" style="border:2px solid #ff9d9d;padding:20px">'+notice+'</aside><h1>',1);p.write_text(s,encoding='utf8')
p=O/'验证结果.json';v=json.loads(p.read_text(encoding='utf8'));v['status']='技术结构检查通过；作者拒绝3D建模画风，正在二维纠偏';v['native_timeline']='v004_Screenshot_2D_Style_Rework';p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
