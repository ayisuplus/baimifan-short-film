"""Prepare project-specific reference policies; shared renderer owns compilation."""
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
out=root/'视频制作/生成板-v003';out.mkdir(exist_ok=True)
plan=json.loads((root/'视频制作/生成板-v001/批次计划.json').read_text('utf-8'))
cast=json.loads((root/plan['cast_review']).read_text('utf-8'))
plan.update(version='v003',output='视频制作/生成板-v003',title='白米饭 · 全片生成板',
    direction_reviews=['视频制作/生成板-v003/动态审查-首批.json','视频制作/生成板-v003/动态审查-前半.json','视频制作/生成板-v003/动态审查-后半.json'],
    pilot_prompts={m:f'视频制作/生成板-v002-试写/GB001-{m}.txt' for m in ['seedance25','minimax-h3']})
ids={'DeepSeek':'CHAR-DEEPSEEK','Claude':'CHAR-CLAUDE','ChatGPT':'CHAR-GPT','圣骑士':'CHAR-PALADIN'}
names_en={'DeepSeek':'DeepSeek','Claude':'Claude','ChatGPT':'ChatGPT','Qwen':'Qwen','Kimi':'Kimi','Grok':'Grok','Gemini':'Gemini','混元':'Hunyuan','Llama':'Llama','智谱':'Zhipu','Mistral':'Mistral','Perplexity':'Perplexity','圣骑士':'the palace paladins','教主':'the High Priest','教徒':'the cultists','街市行人':'market pedestrians'}
plan['identity_inputs']={}
for name,v in cast['identities'].items():
    aid=ids.get(name,v.get('master_asset_id'))
    plan['identity_inputs'][name]={'name_en':names_en[name],'asset_id':aid,'kind':'four_view' if aid else ('missing' if name=='教主' else 'background')}
plan['identity_inputs']['教主']['gap']='教主目前只有立绘，缺少四视图；身份槽位待补，未以概念图代替。'
plan['model_contracts']={'seedance25':{'max_images':30},'minimax-h3':{'max_images':9,'max_chars':7000},'verified':'2026-10-25官方资料；实际执行入口仍需核实'}
plan['cast_overrides']={'CY003A':{'visible':['DeepSeek','Claude'],'offscreen':[],'reflection':[],'note':'只有小鱼的手与局部身体、Claude右缘裙装与橙发；Claude接碗手不入画。'}}
plan['shot_notes']['CY020B']='此分镜火把形制与前面交接火把的镜头有历史差异；须统一为同一短柄仪式火把，修正前不冻结输入。'
plan['shot_notes']['CY032A']='分镜图中Claude已经持勺；此图只能作交接后的构图参考，不能指定首帧，必须先演宝宝递柄、Claude握牢、宝宝松手。'
plan['shot_notes']['CY024A0']='分镜图手位与动态要求相反：必须千问左臂抱小鱼、右手持扇；不得用作强约束首帧，修正或替换后再冻结。'
plan['action_overrides']={'CY003A':'继承已经递出的饭碗，双手悬停，热气升起；右侧没有接碗手。'}
plan['character_continuity_zh']={'Claude':'Claude花饰固定自身左鬓；教堂受缚至离殿赤足，受火后的焦损持续到离殿；数日后街市恢复清洁服装。'}
plan['character_continuity_en']={'Claude':'Claude keeps her own left-temple flower and ivory veil. During the church sequence she is barefoot; fire damage persists until departure. Clean clothes return only in the later market scene.'}
plan['pilot_batch']='GB001'
plan['continuous_line_parts']={'CY024A9':'统御','CY024A10':'万千','CY024A11':'深流','CY024A12':'的','CY024A1':'水之灵啊，'}
plan['execution_notes']['CY027F1']='省略重复开锁操作，画内展示最后一只踝扣打开，结束两踝均开。'
plan['pilot_reference_order']=['CHAR-DEEPSEEK','CHAR-CLAUDE']
(out/'批次计划.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
first={'arc_zh':'捧饭前行→被队伍挡住→视线相接→一次递碗→等待回应。','arc_en':'A child stops before a procession, meets Claude\'s gaze, offers rice once, and waits.','entry_bridge_zh':'全片从阳光街市和捧饭脚步开始。','exit_bridge_zh':'饭碗悬停无人接住，下一批切进Claude向下的眼睛，饭碗与鲸帽成为眼底倒影。','shots':{}}
values=[
('CY001','眼高远景沿街侧向跟随；小鱼停步时随之减速，黑袍近景掠过形成视差。','Track laterally at child-eye level and ease to a stop with her.','直接从捧饭前行开始；停步抬眼后接她看见的人。','Open on her walk; her raised eyeline motivates the next cut.','DeepSeek walks with the bowl, stops before the crossing procession and looks up toward Claude.','Footsteps and market murmur, followed by continuing robe rustle.'),
('CY002','保持有意定镜；Claude转头，前景黑袍缓慢经过，眼神落定后留一拍。','Hold the camera still as foreground robes drift and Claude turns.','承接小鱼右侧视线，切Claude中近景；脚步与衣料跨切点不断。','Cut along the child\'s eyeline to Claude; ambience remains continuous.','Claude turns toward the stopped footsteps and looks down toward the child at screen left.','Market murmur recedes beneath close fabric movement.'),
('CY003','同轴过肩中景缓慢小幅前移，脸、碗和右缘Claude肩部同时保留。','Push in gently beside Claude\'s shoulder, keeping the child and bowl visible.','眼神落定后反打小鱼；举碗一次，句尾碗已经到达两人之间。','Reverse along the eyeline; one lift and offer reaches the space between them.','DeepSeek looks at Claude, then the rice, and raises and extends the bowl once.','Soft sleeves and a slight bowl-handling sound, below the invitation.'),
('CY003A','同碗沿高度与手位切近景；延续前移后柔和收停，两秒等待。','Match the rim and grip in close-up; ease the preceding push to a stop.','继承已经递出的饭碗，不从胸前重新举起；无人接碗。','Match the already offered bowl; do not repeat the lift.','The child holds the full bowl between them; steam rises and no receiving hand enters.','Distant market murmur and quiet breathing; no repeated line.')]
for sid,cz,ce,tz,te,ae,ee in values:first['shots'][sid]=dict(camera_zh=cz,camera_en=ce,transition_zh=tz,transition_en=te,action_en=ae,effects_en=ee)
(out/'动态审查-首批.json').write_text(json.dumps({'batches':{'GB001':first}},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Prepared v003 project plan and first-batch direction; remaining reviews are independently authored.')
