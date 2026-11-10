"""Freeze the three missing continuity drawings before image generation."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
target = ROOT / "镜头设计/生成记录/连续性衔接-请求-v011.json"
if target.exists():
    raise SystemExit("Frozen request already exists; preserve it.")
refs = [
    "镜头设计/图像/S04-粗分镜-v002.png",
    "镜头设计/图像/S05B-粗分镜-v005.png",
    "镜头设计/图像/S06-粗分镜-v002.png",
    "概念参考/01-Claude-母版概念参考.webp",
    "概念参考/02-DeepSeek-母版概念参考.webp",
]
prompt = """Create ONE finished gothic fantasy anime storyboard sheet containing EXACTLY THREE cinematic widescreen panels stacked vertically, ONE COLUMN, THREE ROWS. Each individual panel must be 16:9, so the entire sheet has a tall 16:27 shape. Two thin, straight pure white horizontal gutters separate the three equal panels. No text, letters, captions, numbers, labels, prompt panels, UI or watermark. Fully painted detailed film stills, delicate anime faces, expressive acting, warm candle light against cold blue stained glass; match the supplied existing storyboard's rendering and architecture, not a sketch and not a character sheet.

References in order: (1) existing church crisis panels, for priest, costume, altar, baby's condition, and the stone water basin on the right of the altar. (2) existing rescue panels, for ChatGPT the white dragon woman, Claude, the burnt altar, and support gestures. (3) existing sunny ending, for exact wooden bench, market, recovered baby, gown and spatial relation. (4) Claude's original identity master: adult young woman, long orange hair, dim amber eyes, orange flower on HER LEFT temple, veil, ivory dress with orange-gold botanical embroidery. (5) DeepSeek's original identity master: a VERY SMALL chibi whale baby, round face, huge blue whale hat, fluffy navy-blue winter outfit, blue hair, never a teenager. Preserve the character identities, clothes and their original colors. All three scenes belong to the same film, but are different moments; do not blend their lighting or actions.

TOP PANEL — CY021A, a replacement torch is visibly handed to the priest, BEFORE the fire is lit. Interior night. Medium shot with clear handoff, priest in black-and-gold ornate robes on screen-left, an ordinary hooded cultist at screen-right placing the shaft of a SECOND LIT TORCH into the priest's open receiving hand; both hands anatomically distinct on the wooden shaft, flame above and clear of fingers. Only ONE lit torch in this panel. In the lower right/background, the stone water basin visibly contains the FIRST extinguished torch with a black wet head and faint steam. They are TWO distinct objects. Far behind, orange-haired Claude is still restrained to the same low wooden cross on the raised altar, dress and piled dry wood completely UNLIT. At the very bottom-left, only a small portion of the exhausted baby's blue whale hat/blue sleeve may be visible beside the priest's hem to establish reach; the child is lying down, no gore, no new violence. Preserve the same gothic church. This is a causal handoff, not a battle pose; no priest torch duplication, no fire on the altar yet.

MIDDLE PANEL — CY028A, AFTER the battle and after rescue, Claude has just been gently lowered from GPT's arms and is supported on her own feet. A calm full-body two-person master shot from head to floor, re-establishing the new position: Claude screen-left, ChatGPT screen-right. Claude looks tired, knees slightly soft, both slippers/feet touch the stone floor clearly under the dress hem; no floating, no chains attached to her, no hand-holding yet. GPT is an adult white dragon woman with long white-lavender hair, lilac eyes, two white horns, pointed ears, folded white wings, ONE white scaled tail, and the same white dress and silver knot ornaments as reference 2. GPT's LEFT hand lightly steadies Claude's near upper arm at screen center, while GPT's RIGHT hand is extended in front of them, palm up and empty, waiting for a voluntary response. Claude has not grasped that offered palm; her own hands rest near her chest/waist. Both have two arms, no intertwined duplicate hands. The open palm and the fact that Claude can stand must be legible in the same frame. Their eyes are gentle and tired rather than triumphantly smiling. Background is the same altar after rescue: empty wooden cross, released cuffs and loose chains still attached to the wood, blackened fuel, NO fire, small drifting dust, dim candles, cold blue stained glass. Any far background black-robed figures lie motionless on the floor; no standing enemies. Do not insert extra allies into this intimate transition.

BOTTOM PANEL — CY031A, several days later in the sunny market. Medium-wide relationship shot showing the bench and both characters. DeepSeek the tiny whale baby sits at screen-left with a steaming metal rice bowl supported securely on her lap/left forearm. She scoots left to make space, turns right with a small welcoming smile, her right hand holds a spoon by the handle still near the bowl. Claude enters from SCREEN-RIGHT and is just lowering herself onto the newly offered right-hand bench seat, knees bent and one open hand braced gently against the bench; she looks at the baby, softly surprised and relieved. Show the arrival/settling gesture, NOT a static already eating pose. Claude has NOT accepted the spoon and does NOT hold any utensil yet. Both adult feet near the ground and the baby's short dangling legs are visible. Warm late afternoon light, blue market awnings, flowers and cobbles exactly like reference 3. Gown and whale outfit are clean again after the time skip; don't invent bandages or accessories. Only these two foreground people. No second bowl, no feeding, no already raised spoon near Claude's mouth.

The three panels must be visually clean and fully separated with pure white gutters, all different clear narrative states. Keep top and middle dark and candlelit, bottom warm and sunny. No explanatory text anywhere."""
request = {
    "prompt": prompt,
    "referenced_image_paths": [str((ROOT / p).resolve()) for p in refs],
    "transparent_background": False,
}
record = {
    "version": "v011",
    "purpose": "Fill causal handoff, assisted standing and bench arrival after full continuity review.",
    "shot_ids": ["CY021A", "CY028A", "CY031A"],
    "expected_sheet": {"cols": 1, "rows": 3},
    "request": request,
    "pre_submit_inputs": [
        {
            "path": p,
            "sha256": hashlib.sha256((ROOT / p).read_bytes()).hexdigest(),
        }
        for p in refs
    ],
    "target": "镜头设计/图像/连续性-动作衔接-v001.png",
}
target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(str(target))
