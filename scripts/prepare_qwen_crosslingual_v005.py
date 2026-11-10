from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'声音/千问跨语言试音-v005'
OUT.mkdir(exist_ok=True)
workflow=json.loads(Path('G:/comfyui/ComfyUI/workflow/BreezeTTS2-deploy/voice-design-api.json').read_text(encoding='utf8'))
workflow['2']['inputs'].update(text='走吧。别怕，抱紧我。夜风虽凉，有我在，你不必独自面对。等这一切平息，我会带你平安回去。',instruction='一位古风美人的声音，端雅、从容，温柔中有笃定的保护感。用自然清晰的普通话说话，像近距离安抚身边的人，不要播音腔或吟诗腔。',seed=20261029,max_new_tokens=256)
workflow['3']['inputs']['filename_prefix']='audio/BreezeTTS2/WhiteRice-Qwen-v005/Chinese-Design'
target=OUT/'Breeze-中文声线.api.json'
if not target.exists():target.write_text(json.dumps(workflow,ensure_ascii=False,indent=2),encoding='utf8')
print(target)
