"""Project entrypoint; shared generation-board implementation stays in the toolkit."""
import runpy, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
if len(sys.argv)==1 or ('--plan' in sys.argv and sys.argv[sys.argv.index('--plan')+1]=='视频制作/生成板-v012/批次计划.json'):
    runpy.run_path(str(root/'scripts/build_repaired_generation_board.py'),run_name='__main__')
    raise SystemExit(0)
shared=root.parent.parent/'OpenCut/toolkit/plugins/film-studio/skills/generation-board/scripts/build_multiref_board.py'
sys.argv=[str(shared),'--root',str(root),'--plan','视频制作/生成板-v011/批次计划.json',*sys.argv[1:]]
runpy.run_path(str(shared),run_name='__main__')
from enrich_japanese_board import enrich
plan_path=Path(sys.argv[max(i for i,v in enumerate(sys.argv) if v=='--plan')+1])
import json
plan=json.loads((root/plan_path).read_text(encoding='utf-8-sig'))
enrich(root,root/plan['output'])
