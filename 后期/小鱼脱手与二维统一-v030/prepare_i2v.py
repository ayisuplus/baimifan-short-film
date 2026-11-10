import json, copy, shutil
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
COMFY = Path('G:/comfyui/ComfyUI/ComfyUI')
STYLE = ('Animate this exact hand-drawn Japanese 2D anime frame. Keep clean dark ink contours, flat matte skin, hard-edged two-tone cel shadows, broad drawn hair locks and painted blue gothic cathedral scenery in EVERY frame. Preserve the exact character identities, clothing, scale, architecture, colors, camera angle and composition. No 3D rendering, glossy plastic, realistic skin, dimensional fur, cuts, camera orbit, extra limbs, text, subtitles or new characters. A restrained dramatic anime shot, not a looping illustration. ')
SHOTS = {
 '037': (68, 'The small blue-haired girl in the blue whale hood stands at the left facing the black-and-gold robed priest at the right. His hand begins on her near shoulder. He gives ONE brief firm push away from himself, then immediately withdraws his hand. The girl recoils toward the left, bends both knees, loses her footing and catches herself with her palms on the stone floor. Her knees settle down and her weight is supported by her hands and knees; then she raises her head toward the departing priest. Clear anticipation, weight shift, fall, soft impact and settle. The priest remains upright at the right; his arm returns to his own side. No flying, kicking, elastic bouncing, repeated shoves or instant teleportation. Her hood, skirt and hair follow the movement with a slight delay. End with the girl low on the floor, looking up to the right.'),
 '041a': (60, 'Floor-level close shot. The blue-haired girl lies low at the LEFT and her extended hand holds the black-and-gold robe hem at the RIGHT. She first curls her fingers tightly around the cloth fold, visibly bunching it into her grip. The priest then takes a decisive step away to screen RIGHT; the garment moves with his body and straightens into a taut diagonal between her hand and his leg. Her arm follows only a few centimeters and reaches full extension. The cloth is pulled out of her fingers; her fingers open reluctantly and lose contact completely. The released hem swings right and exits the frame. Her EMPTY hand falls down onto the stone floor and stays there. Her eyes follow the departing priest with helpless disbelief. One continuous causal action: grasp, tension, release, hand landing. Keep her torso supported on the floor, do not drag her body. The cloth must not pass through her hand, detach as a separate scarf, grow longer, or move left. No repeated grabbing after release, no new hand, no camera movement. End on the girl alone at the left with her empty hand on the floor and clear empty space at right.'),
 '041b': (78, 'Rear view of the same black-and-gold robed priest, walking AWAY from the camera UP the central altar steps. He takes three deliberate natural steps, placing a foot on each higher tread before raising his weight. His shoulders rise with each step; the heavy robe hem follows the ankles with a small delay and never floats through the stone. The torch stays in his right hand, its violet flame flickers gently. Preserve the altar destination, fixed stair axis, the blue windows and the symmetrical braziers. No backward steps, sliding, leg crossing, robe stretching or camera movement. End farther up the stairs, still facing away.'),
 '041c': (94, 'Close insert of the same hand holding a burning violet torch above a stationary pile of dry timber. The hand smoothly lowers the torch diagonally toward the wood. The flame tip TOUCHES one piece of timber first. Only AFTER contact, a small violet flame catches at that exact contact point, then spreads naturally along neighboring wood surfaces. The hand pauses briefly to ensure ignition, then lifts the same torch slightly away. Keep the hand, torch and wood solid and stable. No fire on uncontacted wood before the torch arrives, no exploding pile, instant full-screen blaze, morphing wood, detached hand or teleporting torch. Flat drawn violet flames with crisp contours; no photorealistic volumetric glow. One controlled ignition action.'),
 '041d': (66, 'The same young adult orange-haired woman Claude remains secured by her wrists to the same wooden cross, in her cream dress with orange embroidery, black collar ribbon, flower and veil. Preserve her original strained emotional acting: she draws a tense breath, briefly squeezes her eyes shut and makes ONE short involuntary forward shoulder strain and distressed cry, then settles slightly while still afraid. The wrists and chain attachment points stay fixed; the body does not straighten into a new pose. No repeated head throwing, looping screams or grin. Violet drawn flames flicker in the lower foreground, with a few embers drifting upward. The orange hair remains orange with limited violet rim light. Maintain readable face and clean hard-edged 2D shading, without 3D light effects. No injuries, gore or burning skin. Fixed close shot, no zoom.'),
}

def main():
    template=json.loads((ROOT/'后期/Claude二维画风去重-v029/035-r3.api.json').read_text(encoding='utf-8'))
    for i,(shot,(frames,action)) in enumerate(SHOTS.items()):
        key=COMFY/'output/Baimifan/v030'/f'{shot}-2d-key-r1_00001_.png'
        if not key.exists():
            print(f'{shot}: keyframe pending')
            continue
        dest=f'Baimifan_v030_{shot}_2d_key_r1.png'
        shutil.copy2(key,COMFY/'input'/dest)
        shutil.copy2(key,OUT/f'{shot}-二维定帧.png')
        w=copy.deepcopy(template)
        w['7']['inputs']['image']=dest
        w['8']['inputs'].update(prompt=STYLE+action,duration_sec=frames/24)
        w['12']['inputs'].update(global_prompt=STYLE+action,total_frames=frames,seed=202610300310+i)
        w['14']['inputs']['filename_prefix']=f'Baimifan/v030/{shot}-2d-i2v-r1-no-upscale'
        (OUT/f'{shot}-video-r1.api.json').write_text(json.dumps(w,ensure_ascii=False,indent=2),encoding='utf-8')
        print(f'{shot}: workflow ready, {frames} requested frames')

if __name__=='__main__': main()
