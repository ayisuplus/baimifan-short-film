"""Add audition alternatives for S03 and Kimi's entrance; preserve story and marks."""
import argparse, copy, hashlib, json, shutil
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True)
    root=ap.parse_args().root.resolve();folder=root/'后期/BGM重选-v006'
    old_plan=root/'镜头设计/shot-plan-v0.48.json'
    plan=json.loads(old_plan.read_text(encoding='utf-8-sig'))
    config=json.loads((root/plan['audio_arrangement']).read_text(encoding='utf-8-sig'))
    old=copy.deepcopy(config)
    target=root/'镜头设计/shot-plan-v0.48-bgm-v006.json'
    if (folder/'预演编排.json').exists():raise SystemExit('Round 6 already prepared; preserve history.')
    snapshot=root/'镜头设计/带图分镜-月影渡-v048.html'
    if not snapshot.exists():shutil.copy2(root/'镜头设计/带图分镜.html',snapshot)
    plan['audio_arrangement']='后期/BGM重选-v006/预演编排.json'
    plan['title']='《穿云》带图分镜 v0.48 · 第六轮秘密行动与月影渡选曲'
    target.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    config['version']='bgm-v006-on-picture-v048'
    config['previous']='后期/目光与入场-v048/预演编排.json'
    config['shot_plan']=target.relative_to(root).as_posix()
    config['shot_plan_sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
    config['music_manifests'].append('资产/生成记录/BGM重选-音频-v006.json')
    config['audition_note']='第六轮：S03秘密行动与Kimi月影渡新增6首。每镜3首新候选并保留对应旧曲对照；仅供作者试听，不自动选定或切曲。'
    config['round6_author_feedback']='神秘潜行中有史诗分量，结合Kimi新出场找曲；其他已选不变。'
    # Each frame receives a small relevant set, never the entire library.
    rows={
      'CY010A':('HP7-02,FZ-16,FZ-01','等取柴队离开：比较秘密行动的张力和仪式规模；第三首作史诗感更强的对照。'),
      'CY011':('FZ-16,HP7-02,FZ-18','鲸帽卡住：保持小心和危险感；暗杀者作偏阴暗对照，避免喜剧偷窃感。'),
      'CY011A':('HP7-02,FZ-16,FZ-01','挤进空堂：动作悄悄发生，空间和使命感逐渐展开。'),
      'CY012':('FZ-01,HP7-02,FZ-18','空教堂大景：比较魔术仪式的规模与隐藏威胁；史诗感优先从空间而来。'),
      'CY013':('HP7-01,FZ-01,FZ-16','发现宝宝：一忘皆空作为含情感重量的对照，另外两首检查是否更能保持紧张。'),
      'CY013A':('HP7-02,FZ-18,FZ-01','看见踝链：压迫与未知，避免配成即将战胜敌人的宣告。'),
      'CY015':('HP7-01,FZ-01,FZ-16','偷偷保证：比较救人的决心与隐秘气氛，低声对白必须清楚。'),
      'CY016':('FZ-16,HP7-02,FZ-18','反复试锁：比较持续行动的悬念；保留锁链和呼吸。'),
      'CY016A1':('FZ-01,FZ-16,HP7-02','烛泪落下：时间压力与仪式纵深，不给滴蜡硬配爆点。'),
      'CY016A':('HP7-01,FZ-01,HP7-02','失败后坚持：比较情感分量与压住不发的紧迫。'),
      'CY016B':('FZ-18,HP7-02,FZ-16','小手停住：门外脚步先被听到，音乐不能替代实际来人的提示。'),
      'CY016B1':('HP7-02,FZ-18,FZ-01','快走：神秘感向危险倾斜，给短台词和脚步留位置。'),
      'CY016C':('HP7-02,FZ-18,FZ-01','教徒抱柴回来：秘密行动被打断；交给S04已选曲继续，勿提前堆满高潮。'),
      'CY024R':('FZ-01,HP7-02,FZ-16','敌人转向正门，Kimi画外呼唤：压低音乐、留清人声；不是敌人发现了窗外。'),
      'CY024K0':('FZ-01,FZ-02,HP7-02','月下举刃：比较暗处仪式、星月降临和隐秘突入三种方向；咏唱优先，人声织体若冲突则避开。'),
      'CY024K1':('FZ-02,FZ-01,HP7-02','明刃破窗：先保留玻璃爆裂与刃鸣的独立重音；可连续听上镜同曲，不必每镜换。'),
      'CY024K1A':('FZ-01,FZ-02,HP7-02','明刃钉柴、月影渡：术名读完再释放力量，别让配乐抢先揭晓瞬移。'),
      'CY024K2':('FZ-02,FZ-01,HP7-02','瞬临震柴：允许史诗规模在此展开；比较爆发是否带救援感而非反派降临。'),
      'CY024K2A':('FZ-02,FZ-01,FZ-18','教徒转身攻击：沿用出场曲维持连贯，暗杀者仅作危险侧对照。'),
      'CY024K3':('FZ-02,FZ-01,HP7-02','暗刃闭罩：力量落在抵挡敌法和保护Claude，音乐延续前镜，避免像与GPT对抗。'),
      'CY024K4':('HP7-01,FZ-01,FZ-16','罩内试镣见痛收刀：力量收住，比较关切与仍未脱险的紧张。'),
    }
    for sid,(shorts,note) in rows.items():
        prev=copy.deepcopy(config['shot_overrides'][sid]);new=['BGM-CY-'+s for s in shorts.split(',')]
        # One old S03 reference, both existing entrance references for continuity.
        retained=prev['candidates'][:1] if sid.startswith('CY01') else prev['candidates']
        config['shot_overrides'][sid]=dict(candidates=list(dict.fromkeys(new+retained)),previous_candidates=prev['candidates'],note='第六轮 · '+note+' 新曲排在前，旧曲留作对照。',status='新候选 · 待作者试听',audition_question=note)
    config['author_marks_record']='后期/BGM重选-v006/作者已选记录.json'
    (folder/'预演编排.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert plan['shots']==json.loads(old_plan.read_text(encoding='utf-8-sig'))['shots']
    assert config['effects']==old['effects'] and config['sections']==old['sections']
    unchanged=[s['id'] for s in plan['shots'] if s['id'] not in rows]
    assert all(config['shot_overrides'].get(s)==old['shot_overrides'].get(s) for s in unchanged)
    (folder/'结构核验.json').write_text(json.dumps(dict(shots=len(plan['shots']),seconds=plan['total_seconds'],changed=list(rows),unchanged_candidates=len(unchanged),story_images_dialogue_timing_unchanged=True,effects_unchanged=True,source_plan_sha256=hashlib.sha256(old_plan.read_bytes()).hexdigest(),new_plan_sha256=config['shot_plan_sha256']),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Added music to',len(rows),'shots; untouched',len(unchanged),'shots.')

if __name__=='__main__':main()
