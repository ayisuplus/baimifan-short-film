"""Freeze per-shot audition hypotheses; preserve approved-direction late scenes."""
import argparse,json
from pathlib import Path

ROWS='''
CY001|MT-03,MT-15,NA-03|阳光与饭碗，比较童话日常、亲近感和轻柔幻想；仍可选择只留街声
CY002|MT-39,NA-03,LR-15|回望尚未求救，比较内心距离与神秘感，避免提前悲壮
CY003|TIME,MT-15,NA-03|第一次邀请，保留首尾呼应并比较更轻的陌生人善意
CY003A|MT-15,MT-39,NA-03|饭碗悬着无人接，比较温暖的等待与微小失落，不催情
CY003B|TIME,MT-20,MT-39|眼底映出小鱼，比较克制感谢与压住的悲伤
CY003C|MT-18,MT-84,LR-04|掀饭是突变，比较短促惊愕、危险预感；拍碗声必须先到
CY004|MT-13,MT-84,LR-04|听见火祭消息，比较恐惧与危机，不把教徒对白盖住
CY004A|NA-02,MT-63,MT-15|放下空碗去求援，比较紧迫、主动选择与善意驱动
CY004B|NA-02,MT-63,MT-84|跑上长阶，比较赶时间与意志推动，不能提前进入胜利高潮
CY004C|MT-69,MT-41,NA-06|长枪拦路，比较宫廷秩序与权威压迫，避免直接演成反派登场
CY004D|MT-41,MT-69,MT-15|让她进来，比较权威松动与一线希望，不用盛大救援感
CY005|MT-69,MT-41,LR-15|空殿拉开距离，比较空间庄严与人物孤小
CY006|MT-39,MT-20,NA-02|请求救人，比较真切恳求、忍住的悲伤与时间压力；对白优先
CY007|MT-18,MT-39,LR-04|收住迟疑的拒绝，比较现实落差、内心犹豫与阴影；不要直接定性GPT冷酷
CY008|MT-20,MT-13,NA-03|她会死的，比较无助、恐惧与孩子般的脆弱，留出追问后的空白
CY009|MT-15,MT-63,NA-02|那我自己去，比较柔软的勇气与向前的决心，不能提前像战胜了
CY010|MT-39,MT-18,LR-04|扶手上的迟疑，比较内心冲突；手指和钟声承担转折
CY009A|MT-39,MT-69,NA-05|目送远处蓝点，比较留下的人、空殿距离和下一场未知感
CY010A|MT-70,LR-07,MT-42|等灯离开再潜入，比较轻巧行动与被发现的悬念
CY011|MT-70,NA-05,MT-84|帽子卡住，比较小动作悬念与受阻，不把危险演成滑稽段子
CY011A|MT-70,NA-05,LR-07|挤进空堂，比较短暂松气与仍需屏息的危险
CY012|MT-89,LR-13,NA-05|空教堂显露刑架，比较宗教空间、黑暗纵深与童话未知
CY013|MT-39,MT-20,NA-03|Claude发现宝宝，比较担忧与相互关心，别过早抒情释放
CY013A|MT-13,LR-04,NA-11|赤足与锁链，比较处境危险与献祭预感；先听稀薄部分是否足够
CY015|MT-15,MT-39,NA-03|我带你出去，比较小小保证与保护欲；对白前景清楚
CY016|MT-70,MT-84,LR-07|试锁拉链，比较行动尝试与时间流失，链响要可辨
CY016A1|MT-39,MT-13,LR-13|烛泪与时间，比较等待、绝望和空间压力，不给每滴烛泪硬配重拍
CY016A|MT-20,MT-15,MT-13|再试一下，比较疲惫不放弃、善意与无力；不要浪漫化苦难
CY016B|MT-42,LR-07,MT-84|脚步先到小手停住，比较被发现前的警觉，音乐不替代脚步
CY016B1|MT-84,MT-75,LR-04|快走，比较急迫警告与压倒性威胁，留清短台词
CY016C|LR-13,MT-42,NA-06|提灯从门口回来，比较空间逼近、计谋与权力压迫
CY016D|MT-63,NA-02,MT-84|冲下长阶阻火，比较冒险行动与焦急，不用已经得救的旋律结论
CY017|NA-06,MT-75,MT-89|神明在等你，比较父权威胁、力量差与宗教秩序；不替教主歌颂
CY018|MT-84,MT-63,LR-05|撞偏火把，比较局部反抗与危险升级；撞击火星先由音效落点
CY019|MT-15,MT-75,NA-06|小小身体挡路，比较从孩子或施压者出发的两个视角
CY020|MT-20,MT-63,NA-11|别碰她，比较心痛与保护性反抗，喊声必须清楚
CY020B|MT-75,NA-06,LR-05|仰视教主逼近，比较力量差与步步施压，不抢后段援军登场
CY020A|MT-18,MT-13,NA-11|被推倒失守，比较突变后无力与牺牲感，落地声后可留白
CY021|MT-20,MT-39,NA-11|求父亲放过孩子，比较痛苦、哀求与仪式悲剧，避免煽情过满
CY021B|MT-15,MT-20,MT-13|攥住袍尾，比较仅剩的一点坚持与即将失去的力量
CY021A|MT-42,NA-06,LR-05|第二支火把递来，比较冷酷决定与危机升级
CY022A|MT-20,MT-13,NA-11|衣摆滑脱，比较努力落空；允许这一瞬只留衣料与呼吸
CY022A1|MT-89,NA-11,LR-13|持火登阶，比较宗教仪式与逐步逼近的死亡感
CY022|MT-04,LR-05,NA-11|黑焰初起，比较咏唱仪式、破坏性转折与献祭；这不是英雄施法
CY022B|MT-13,MT-20,NA-11|火隙痛苦，比较无法逃离与人物受难，不能被宏大音乐美化
CY022B2|NA-11,MT-89,LR-05|黑焰吞没祭坛，比较献祭规模与仪式压迫；配乐人声不能冒充教徒现场吟唱
'''

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);args=ap.parse_args();root=args.root.resolve()
    out=root/'后期/BGM重选-v002/预演编排.json'
    if out.exists():raise SystemExit('Round 2 bindings already exist; preserve history.')
    config=json.loads((root/'后期/BGM重选-v001/预演编排.json').read_text(encoding='utf-8'))
    plan=json.loads((root/config['shot_plan']).read_text(encoding='utf-8-sig'))
    config['version']='v002';config.pop('music_manifest')
    config['music_manifests']=['资产/生成记录/BGM重选-音频-v001.json','资产/生成记录/BGM重选-音频-v002.json']
    config['author_feedback']={'S05_S06':'作者认为当前选曲可以，保持候选和留白；尚未锁定具体原曲区间。','S02_S04':'旧候选不合适，本轮逐镜扩充重选。','method':'逐镜候选独立比较，不自动每镜切换音乐。'}
    config['shot_overrides']={}
    for line in ROWS.strip().splitlines():
        sid,shorts,note=line.split('|');ids=['BGM-CY-TIME-001' if x=='TIME' else 'BGM-CY-'+x for x in shorts.split(',')]
        config['shot_overrides'][sid]={'candidates':ids,'note':note,'status':'新候选 · 待作者试听','audition_question':note}
    expected={s['id'] for s in plan['shots'] if s['scene'] in ['S01','S02','S03','S04']}
    assert set(config['shot_overrides'])==expected
    config['audition_note']='S01–S04逐镜各3首候选，按画面筛选；S05/S06保留作者认可方向。曲目身份与解码已核对，音乐效果为待作者比较的假设；未锁定原曲in/out，不自动切曲。'
    out.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Per-shot auditions:',len(expected))
if __name__=='__main__':main()
