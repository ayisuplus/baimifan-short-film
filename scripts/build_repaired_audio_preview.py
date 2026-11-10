"""Render the adopted seven BGM sources and natural-rate Japanese voices.

No generation, download, looping, time stretching, or source-file mutation.
Requires numpy and ffmpeg. All absolute timings are derived/verified against
the supplied shot plan. Outputs are review candidates, not audition approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess

import numpy as np


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def check(condition, message):
    if not condition:
        raise ValueError(message)


def db_gain(db):
    return 10 ** (db / 20)


def decode(ffmpeg, path, sr):
    result = subprocess.run(
        [ffmpeg, "-v", "error", "-i", str(path), "-vn", "-ac", "2", "-ar", str(sr),
         "-f", "f32le", "pipe:1"], capture_output=True, check=True)
    return np.frombuffer(result.stdout, dtype="<f4").reshape(-1, 2).copy()


def encode(ffmpeg, samples, sr, path):
    codec = ["-c:a", "pcm_s24le"] if path.suffix == ".wav" else ["-c:a", "libmp3lame", "-b:a", "192k"]
    subprocess.run(
        [ffmpeg, "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", "pipe:0",
         *codec, str(path)], input=samples.astype("<f4", copy=False).tobytes(), check=True)


def coverage_check(cues, silences, total):
    spans = sorted([(x["timeline_start"], x["timeline_end"], x["id"])
                    for x in cues + silences])
    cursor = 0.0
    for start, end, ident in spans:
        check(abs(start - cursor) < 0.00001, f"Timeline gap/overlap before {ident}: {cursor} vs {start}")
        check(end > start, f"Nonpositive interval {ident}")
        cursor = end
    check(abs(cursor - total) < 0.00001, f"Coverage end {cursor} != film duration {total}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--source", default="镜头设计/shot-plan-v0.57.json")
    parser.add_argument("--bgm-plan", default="后期/收尾修复-v001/BGM剪辑方案.json")
    parser.add_argument("--voice-plan", default="后期/收尾修复-v001/配音对位方案.json")
    parser.add_argument("--out", default="后期/收尾修复-v001")
    parser.add_argument("--sample-rate", type=int, default=48000)
    parser.add_argument("--bgm-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Validate and write edit JSON without audio rendering")
    parser.add_argument("--refresh-manifest", action="store_true", help="Refresh source hash only when rendered audio inputs/timings are unchanged")
    args = parser.parse_args()
    root = args.root.resolve()
    sr = args.sample_rate
    check(sr in (24000, 44100, 48000), "Use a supported preview sample rate")
    ffmpeg = shutil.which("ffmpeg")
    check(ffmpeg, "ffmpeg must already be installed")
    source_path, bgm_path, voice_path = [root / x for x in (args.source, args.bgm_plan, args.voice_plan)]
    source, design, voice_plan = [read_json(p) for p in (source_path, bgm_path, voice_path)]
    out = root / args.out
    out.mkdir(parents=True, exist_ok=True)
    shots = {s["id"]: s for s in source["shots"]}
    total = float(source["total_seconds"])
    cursor = 0
    for shot in source["shots"]:
        check(abs(shot["start_second"] - cursor) < .00001, f"Noncontiguous shot {shot['id']}")
        check(abs(shot["end_second"] - shot["start_second"] - shot["seconds"]) < .00001,
              f"Shot duration inconsistent {shot['id']}")
        cursor = shot["end_second"]
    check(abs(cursor-total) < .00001, "Shot total mismatch")
    check(abs(total - voice_plan["new_duration"]) < .00001, "Voice plan and source film durations differ")
    check(set(shots) == {s["shot_id"] for s in voice_plan["shots"]}, "Voice/shot ID set mismatch")
    for s in voice_plan["shots"]:
        actual = shots[s["shot_id"]]
        check(abs(actual["start_second"]-s["new_start"]) < .00001 and
              abs(actual["end_second"]-s["new_end"]) < .00001,
              f"Voice/shot timing mismatch: {s['shot_id']}")
    check(sha256(root / voice_plan["source"]) == voice_plan["source_sha256"], "Voice baseline source hash changed")

    def resolve(anchor):
        shot = shots[anchor["shot_id"]]
        if anchor.get("edge") == "end":
            return float(shot["end_second"])
        offset = anchor["offset_seconds"]
        check(-.00001 <= offset <= shot["seconds"]+.00001, f"Anchor outside shot: {anchor}")
        return round(shot["start_second"] + offset, 5)

    events = voice_plan["mix_events"]
    event_map = {e["id"]: e for e in events}
    check(len(event_map) == len(events), "Duplicate voice events")
    # This speech pause moves with the natural-rate master, not old shot +5s.
    prayer_start = event_map["MASTER-GPT-2"]["timeline_end"]
    prayer_end = event_map["MASTER-GPT-3"]["timeline_start"]
    check(abs(prayer_end-prayer_start-.8) < .00001, "GPT prayer pause is not 0.8s")
    check(shots["CY024A5"]["start_second"] <= prayer_start < prayer_end <= shots["CY024A5"]["end_second"],
          "Prayer pause not inside CY024A5")
    source_meta = {s["id"]: s for s in design["sources"]}
    cues = []
    for proposed in design["cues"]:
        c = dict(proposed)
        start, end = resolve(c["start_anchor"]), resolve(c["end_anchor"])
        if c["id"] == "M09":
            end = prayer_start
        if c["id"] == "M10":
            start = prayer_end
        if c.get("source_alignment"):
            align = c["source_alignment"]
            action_time = resolve(align["action_anchor"])
            hit_time = align["evidence"]["source_seconds"]
            sin = hit_time - (action_time-start)
            c["aligned_action_timeline"] = action_time
            c["measured_source_transient"] = hit_time
        elif c.get("end_evidence"):
            sin = c["end_evidence"]["source_seconds"]-(end-start)
        else:
            sin = c["source_in"]
        sout = sin + end-start
        meta = source_meta[c["music_id"]]
        check(0 <= sin < sout <= meta["measured_duration"], f"Source range exceeded: {c['id']} {sin}..{sout}")
        check(c["playback_rate"] == 1.0 and c["overlap_seconds"] == 0, "Unsupported stretch/crossfade")
        check(c["fade_in_seconds"]+c["fade_out_seconds"] <= end-start, f"Fades overlap in {c['id']}")
        c.update(timeline_start=start, timeline_end=end, duration=round(end-start,5),
                 source_in=round(sin,5), source_out=round(sout,5), original_source_in=proposed["source_in"],
                 original_source_out=proposed["source_out"])
        cues.append(c)
    silences = []
    for proposed in design["silences"]:
        silence = dict(proposed)
        start, end = resolve(silence["start_anchor"]), resolve(silence["end_anchor"])
        if silence["id"] == "S04":
            start, end = prayer_start, prayer_end
        silence.update(timeline_start=start, timeline_end=end, duration=round(end-start,5))
        silences.append(silence)
    coverage_check(cues, silences, total)
    action_points = []
    for original in design["action_points"]:
        p = dict(original)
        t = resolve(p["anchor"])
        if p["film_time"] == 286:
            t = prayer_start
        c = next((x for x in cues if x["timeline_start"] <= t < x["timeline_end"]), None)
        p.update(timeline_time=t, source_seconds=round(c["source_in"]+t-c["timeline_start"],5) if c else None)
        action_points.append(p)
    assets = {}
    for path in sorted({c["path"] for c in cues} | {e["file"] for e in events}):
        absolute = root / path
        check(absolute.is_file(), f"Missing source: {path}")
        assets[path] = {"sha256": sha256(absolute), "bytes": absolute.stat().st_size}
    for master in voice_plan["masters"]:
        check(assets[master["path"]]["sha256"] == master["sha256"], f"Master hash changed: {master['id']}")
    for e in events:
        check(e["rate"] == 1, f"Non-natural voice rate: {e['id']}")
        check(0 <= e["timeline_start"] < e["timeline_end"] <= total, f"Voice outside film: {e['id']}")
        check(abs(e["timeline_end"]-e["timeline_start"]-(e["file_out"]-e["file_in"])) < .00001,
              f"Voice duration mismatch {e['id']}")
    report = {"schema":"bmr-audio-preview-edit/v1", "status":"validated_not_rendered", "source":args.source,
              "source_sha256":sha256(source_path), "bgm_plan_sha256":sha256(bgm_path),
              "voice_plan_sha256":sha256(voice_path), "film_seconds":total, "sample_rate":sr,
              "cues":cues, "silences":silences, "action_points":action_points, "voice_events":events,
              "input_assets":assets, "checks":{"source_ranges":True,"full_timeline_covered_once":True,
              "natural_rate_all_sources":True,"voice_timeline_matches_shots":True,"auditory_review":False},
              "mix":{"music_nominal_db":-17,"voice_db":0,"dialogue_music_duck_db":-7,
                     "duck_attack_seconds":.10,"duck_release_seconds":.45,"voice_fade_or_stretch":False,
                     "music_fades":"equal-power, within each cue; no overlapping tracks",
                     "sfx_ambience_rendered":False,"preview_not_final_mix":True},
              "note":"本预览只含现有音乐与日语配音，尚无拟音/环境声；停乐段因此可能只剩对白或数字静音。频谱瞬态不是已听审音乐重拍。"}
    report_path = out / "实际BGM剪辑.json"

    def save_report():
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

    if args.refresh_manifest:
        old = read_json(report_path)
        check(old["status"] == "rendered_candidate_not_audition_approved", "No rendered manifest to refresh")
        check(old["bgm_plan_sha256"] == report["bgm_plan_sha256"] and
              old["voice_plan_sha256"] == report["voice_plan_sha256"] and
              old["input_assets"] == assets and old["film_seconds"] == total and old["sample_rate"] == sr,
              "Audio inputs changed; rerender required")
        keys = ("id", "timeline_start", "timeline_end", "source_in", "source_out", "nominal_gain_db",
                "fade_in_seconds", "fade_out_seconds")
        check([[c[k] for k in keys] for c in old["cues"]] == [[c[k] for k in keys] for c in cues],
              "Music edit changed; rerender required")
        check(old["silences"] == silences, "Silence map changed; rerender required")
        check(all(sha256(out/name)==info["sha256"] for name,info in old["output_assets"].items()),
              "Rendered output changed")
        old.setdefault("source_hash_refreshes", []).append({"previous":old["source_sha256"],
                   "current":report["source_sha256"],"reason":"Shot text changed; audio inputs, edit timing and rendered outputs reverified unchanged"})
        old["source_sha256"] = report["source_sha256"]
        report = old
        save_report()
        print("Refreshed source hash; original render evidence and output hashes preserved")
        return
    save_report()
    if args.dry_run:
        print(json.dumps({"status":"validated", "seconds":total, "cues":len(cues), "voices":len(events)}, ensure_ascii=False))
        return
    n = round(total*sr)
    bgm = np.zeros((n,2), dtype=np.float32)
    for c in cues:
        samples = decode(ffmpeg, root/c["path"], sr)
        a, b = round(c["source_in"]*sr), round(c["source_out"]*sr)
        start, end = round(c["timeline_start"]*sr), round(c["timeline_end"]*sr)
        count = end-start
        check(a+count <= len(samples), f"Decoded source exhausted: {c['id']}")
        chunk = samples[a:a+count].copy()
        check(abs((b-a)-count) <= 1, f"Sample rounding drift {c['id']}")
        chunk *= db_gain(c["nominal_gain_db"])
        fi, fo = round(c["fade_in_seconds"]*sr), round(c["fade_out_seconds"]*sr)
        if fi:
            chunk[:fi] *= np.sin(np.linspace(0, math.pi/2, fi, dtype=np.float32))[:,None]
        if fo:
            chunk[-fo:] *= np.sin(np.linspace(math.pi/2, 0, fo, dtype=np.float32))[:,None]
        bgm[start:end] += chunk
        c["rendered_source_samples"] = [a,a+count]
        c["rendered_timeline_samples"] = [start,end]
        del samples, chunk
    encode(ffmpeg,bgm,sr,out/"BGM试听.wav")
    encode(ffmpeg,bgm,sr,out/"BGM试听.mp3")
    report["outputs"] = ["BGM试听.wav","BGM试听.mp3"]
    report["bgm_peak_dbfs"] = float(20*np.log10(max(float(np.abs(bgm).max()),1e-12)))
    if not args.bgm_only:
        voices = np.zeros_like(bgm)
        duck = np.ones(n,dtype=np.float32)
        gain = db_gain(-7)
        attack, release = round(.10*sr),round(.45*sr)
        report['mix']['scene_duck_regions'] = voice_plan.get('music_duck_regions', [])
        for region in voice_plan.get('music_duck_regions', []):
            check(0 <= region['start'] < region['end'] <= total, 'Scene duck outside timeline')
            check(-30 <= region['gain_db'] <= 0, 'Invalid scene duck gain')
            start, end = round(region['start']*sr), round(region['end']*sr)
            level = db_gain(region['gain_db'])
            a = max(0, start-round(region.get('attack_seconds', .1)*sr))
            b = min(n, end+round(region.get('release_seconds', .2)*sr))
            duck[a:start] = np.minimum(duck[a:start], np.linspace(1, level, start-a, dtype=np.float32))
            duck[start:end] = np.minimum(duck[start:end], level)
            duck[end:b] = np.minimum(duck[end:b], np.linspace(level, 1, b-end, dtype=np.float32))
        for e in events:
            samples = decode(ffmpeg,root/e["file"],sr)
            a,b = round(e["file_in"]*sr),round(e["file_out"]*sr)
            start,end = round(e["timeline_start"]*sr),round(e["timeline_end"]*sr)
            check(b <= len(samples) and b>a, f"Voice source range invalid {e['id']}")
            check(abs((b-a)-(end-start))<=1, f"Voice sample mismatch {e['id']}")
            count=b-a
            check(start+count<=n,f"Voice exceeds final sample {e['id']}")
            voices[start:start+count] += samples[a:b]
            env_start,env_end=max(0,start-attack),min(n,end+release)
            duck[env_start:start]=np.minimum(duck[env_start:start],np.linspace(1,gain,start-env_start,dtype=np.float32))
            duck[start:end]=np.minimum(duck[start:end],gain)
            duck[end:env_end]=np.minimum(duck[end:env_end],np.linspace(gain,1,env_end-end,dtype=np.float32))
            e["rendered_source_samples"]=[a,b]
            e["rendered_timeline_samples"]=[start,start+count]
            e["duck_window_seconds"]=[env_start/sr,env_end/sr]
            del samples
        report['mix']['scene_duck_checks'] = [dict(id=r['id'], max_gain_db=float(20*np.log10(float(duck[round(r['start']*sr):round(r['end']*sr)].max()))), target_db=r['gain_db']) for r in voice_plan.get('music_duck_regions', [])]
        check(all(x['max_gain_db'] <= x['target_db'] + .0001 for x in report['mix']['scene_duck_checks']), 'Scene duck released inside protected region')
        bgm *= duck[:,None]
        bgm += voices
        del voices,duck
        peak=float(np.abs(bgm).max())
        scale=min(1.0,db_gain(-1)/max(peak,1e-12))
        bgm *= scale
        report["mix"]["pre_attenuation_peak_dbfs"] = float(20*np.log10(max(peak,1e-12)))
        report["mix"]["global_peak_protection_gain_db"] = float(20*np.log10(scale))
        report["mix"]["post_attenuation_peak_dbfs"] = float(20*np.log10(max(float(np.abs(bgm).max()),1e-12)))
        report["mix"]["peak_protection"] = "constant global attenuation only when needed; no dynamics compression"
        encode(ffmpeg,bgm,sr,out/"全片声音预览.mp3")
        report["outputs"].append("全片声音预览.mp3")
    report["output_assets"]={name:{"sha256":sha256(out/name),"bytes":(out/name).stat().st_size} for name in report["outputs"]}
    report["render_decode_checks"] = {}
    for name in report["outputs"]:
        decoded = decode(ffmpeg, out/name, sr)
        check(len(decoded) == n, f"Output duration differs from timeline: {name}")
        check(bool(np.isfinite(decoded).all()), f"Nonfinite rendered sample: {name}")
        proof = {"decoded_samples":len(decoded),"decoded_seconds":len(decoded)/sr,
                 "peak_dbfs":float(20*np.log10(max(float(np.abs(decoded).max()),1e-12))),"all_finite":True}
        if name == "BGM试听.wav":
            proof["silence_max_abs"] = [float(np.abs(decoded[round(x["timeline_start"]*sr):round(x["timeline_end"]*sr)]).max())
                                         for x in silences]
            check(all(value == 0 for value in proof["silence_max_abs"]), "Music leaks into intentional silence")
        report["render_decode_checks"][name] = proof
        del decoded
    report["status"]="rendered_candidate_not_audition_approved"
    report["checks"]["input_sources_unchanged_after_render"] = all(sha256(root/path)==info["sha256"] for path,info in assets.items())
    check(report["checks"]["input_sources_unchanged_after_render"],"An input source changed during render")
    save_report()
    print(json.dumps({"status":report["status"],"seconds":total,"outputs":report["outputs"]},ensure_ascii=False))


if __name__ == "__main__":
    main()
