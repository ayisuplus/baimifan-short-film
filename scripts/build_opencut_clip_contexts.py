"""Compile audited, read-only source references; never rewrite browser editing data.

Run with --snapshot <complete-backup/browser.json> --target <staging-package>.
The staging package must be a copy of the current project package.
"""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

FILM = Path(__file__).resolve().parents[1]
AUDIT = FILM / '后期/全片剧本关联-v036'

def read(path):
    return json.loads(Path(path).read_text('utf-8-sig'))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--snapshot', type=Path, required=True)
    parser.add_argument('--target', type=Path, required=True)
    args = parser.parse_args()
    snapshot = read(args.snapshot)
    package = read(args.target / 'manifest.json')
    audit = read(AUDIT / 'source-audit.json')
    excerpts = read(AUDIT / 'script-excerpts.json')
    excerpt_rows = {r['element_id']: r for r in excerpts['clips']}
    evidence = {r['element_id']: r for r in read(FILM / '后期/迁回OpenCut-v035/source-media-evidence.json')}
    scene = next(s for s in snapshot['project']['scenes'] if s['id'] == snapshot['project']['currentSceneId'])
    elements = {e['id']: e for e in scene['tracks']['main']['elements']}
    assert len(elements) == len(audit['clips']) == 118
    project_id = snapshot['project']['metadata']['id']
    screenplay = read(sorted((args.snapshot.parent / 'creative/versions').glob('*.json'))[-1])
    contexts, bindings, registered = {}, [], {}

    def register(path):
        source = Path(path)
        if not source.is_absolute(): source = FILM / source
        if str(source) in registered: return registered[str(source)]
        sha = hashlib.file_digest(source.open('rb'), 'sha256').hexdigest()
        key = sha[:24]
        relative = f'media/{key}{source.suffix.lower()}'
        destination = args.target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists(): shutil.copy2(source, destination)
        assert hashlib.file_digest(destination.open('rb'), 'sha256').hexdigest() == sha
        package['media'][key] = {'path': relative, 'sha256': sha, 'source': str(source), 'label': source.name}
        registered[str(source)] = key
        return key

    for index, row in enumerate(audit['clips'], 1):
        eid = row['element_id']; element = elements[eid]; source = evidence[eid]
        assert element['name'] == row['name']
        assert element['startTime'] == row['timeline_start_frame'] * 5000
        assert element['duration'] == (row['timeline_end_frame'] - row['timeline_start_frame']) * 5000
        assert 'directorBinding' not in element
        context_id = f'CUT{index:03d}'
        prompts, seen = [], set()
        for group in row['execution_groups']:
            prompt_file = group.get('prompt_file')
            if prompt_file in seen: continue
            seen.add(prompt_file)
            if prompt_file:
                frozen = read(FILM / prompt_file)
                locator = group.get('prompt_locator')
                if isinstance(locator, list):
                    parts = []
                    for item in locator:
                        value = frozen
                        for key in item.split('.'): value = value[key]
                        if value.strip() and value not in parts: parts.append(value)
                    text = '\n\n'.join(parts)
                elif locator.startswith('payload.'):
                    text = '\n\n'.join(c['text'] for c in frozen['payload']['content'] if c.get('type') == 'text')
                elif locator.startswith('request'):
                    text = frozen['request']['prompt']
                else: raise ValueError(f'Unknown prompt locator {locator}')
                assert text.strip()
                prompts.append({'label': Path(prompt_file).stem, 'status': '实际执行提示词 · 批次范围，不等同于当前剪点', 'source': prompt_file, 'text': text})
            else:
                record = '视频制作/Metaso-H3-v003/火种主观-本地摄影记录.json'
                prompts.append({'label': '火种主观 · 本地摄影推进', 'status': '本地制作记录 · 无生视频提示词', 'source': record, 'text': json.dumps(read(FILM / record), ensure_ascii=False, indent=2)})
        references = [{'media': register(p), 'label': Path(p).name, 'status': '实际执行参考 · 历史版本', 'source': p}
                      for p in row['actual_reference_paths'] if Path(p).suffix.lower() in {'.png','.jpg','.jpeg','.webp','.mp4','.webm','.mov'}]
        for ref in references:
            if Path(ref['source']).suffix.lower() in {'.mp4','.webm','.mov'}: ref['kind']='motion-video'
        clip = {'media': register(source['source']), 'sourceIn': source['source_in']/24,
                'duration': element['duration']/120000, 'sourceDuration':source['frames']/24,
                'width':source['width'], 'height':source['height'], 'fps':24}
        title = element['name'].removesuffix('.mp4')
        script = [{'page_id':f"import-{int(s['scene_id'][1:])}", 'label':s['label'], 'quote':s['quote']}
                  for s in excerpt_rows[eid]['excerpts']]
        # A restored native manuscript contains the author's later CY007 edit.
        # Quote that saved revision rather than overwriting it with the older Markdown.
        if index == 3:
            script = []
            for sid in ['CY006','CY007','CY008']:
                blocks = screenplay['scenes']['S02']['sections'][sid]
                quote = '\n\n'.join(b['text'] if b['type']=='action' else
                    f"**{b['speaker']}** · `{b['cue_id']}`\n\n> {b['text']}\n\n中文回译：{b['translation']}" for b in blocks)
                script.append({'page_id':'import-2','label':f'{sid} · 当前保存剧本', 'quote':quote})
        # A source excerpt can cross the S03/S04 page boundary; retain two actual pages.
        split_script = []
        for ref in script:
            parts = re.split(r'\n\n## (S\d+)｜[^\n]+\n\n', ref['quote'])
            split_script.append({**ref,'quote':parts[0]})
            for at in range(1,len(parts),2):
                split_script.append({'page_id':f'import-{int(parts[at][1:])}','label':ref['label']+' · 后续场次','quote':parts[at+1]})
        script = split_script
        contexts[context_id] = {'title': title, 'shot_ids': row['proposed_context_cy_ids'],
            'script': script, 'prompts': prompts,
            'notes': row['ambiguity'] + excerpt_rows[eid]['notes'] + ['CY编号是叙事或执行批次范围，不是新增分镜或逐帧对白同步。当前剧本与历史生成可能有版本差异。'],
            'evidence': row['evidence_paths']}
        bindings.append({'context_id': context_id, 'element': element})
        assert not any(s['id']==context_id for s in package['shots'])
        package['shots'].append({'id':context_id,'title':title,'references':references,'sounds':[],
            'clip':clip,'action':'','camera':'','story':'','storySource':'现有完整剧本引用',
            'prompt':'','promptSource':'原执行快照','dialogue':[],'soundDesign':''})
    package['clipContexts'] = {'schema_version':1,'project_id':project_id,'package_id':package['id'],
        'bindings':bindings,'contexts':contexts}
    (args.target / 'manifest.json').write_text(json.dumps(package,ensure_ascii=False,indent=2)+'\n','utf-8')
    result = {'count':len(contexts),'references':len(registered),'project_id':project_id,
        'snapshot':str(args.snapshot),'package_manifest_sha256':hashlib.sha256((args.target/'manifest.json').read_bytes()).hexdigest()}
    (AUDIT/'build-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps(result,ensure_ascii=False))

if __name__ == '__main__': main()
