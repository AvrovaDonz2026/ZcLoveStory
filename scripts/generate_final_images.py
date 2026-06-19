#!/usr/bin/env python3
"""Generate final WebGAL background/CG assets from round-1 references."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
REF_DIR = ROOT / "site" / "game" / "reference" / "round1"
SOURCE_DIR = ROOT / "site" / "game" / "reference" / "final_sources"
META_DIR = SOURCE_DIR / "_meta"

COMMON = """Create a final WebGAL visual novel image for "Shezhang Love Story".

Style: Japanese visual novel background/CG illustration, grounded contemporary campus realism, clean readable linework, tidy flat-to-soft shading, low-saturation gray/off-white/muted blue palette with occasional warm desk-lamp light, restrained mood, documentary evidence-room feeling.

Privacy and text rules: no real school logo, no brand, no readable private messages, no account IDs, no QR codes, no real names, no readable Chinese text. Use blank title bands, pseudo-text, blurred bars, or empty cards where text would be.

Composition rules: wide 16:9 WebGAL image, leave the lower 25% visually calm because the game engine will overlay its own dialogue box later, keep the main subject inside the central 60% so center-cropping remains safe, no watermark, no border, no green screen in the final output.

Strictly forbidden: do not draw any game UI, dialogue box, text box, choice menu, title overlay, button, arrow indicator, subtitle panel, lower-third panel, screen frame, or translucent rounded rectangle. The output must be a clean background/CG image only.
"""

UI_COMMON = """Create a WebGAL visual novel UI bitmap asset for "Shezhang Love Story".

Style: Japanese visual novel interface ornament, grounded contemporary campus realism, archive-folder evidence motif, clean readable shape language, low-saturation gray/off-white/muted blue palette with tiny warm paper accents, restrained and polished.

Privacy and text rules: no real school logo, no brand, no readable private messages, no account IDs, no QR codes, no real names, no readable Chinese text. Leave all labels blank; real text will be rendered by CSS/WebGAL.

Composition rules: isolated UI component on a clean neutral or lightly textured paper surface, no green screen, no watermark, no border around the whole image. Make the component useful as a reusable web UI asset.
"""

ASSETS = {
    "bg_title_folder_table": {
        "input": "ref_title_table_arrangement_v01.png",
        "output": "site/game/background/title/bg_title_folder_table_v01.webp",
        "prompt": """Use the input image only as a reference for the gray folder, tabs, lamp, recorder pen, and evidence-table arrangement.

Final image: a rainy-night campus clubroom table, viewed from a slightly high angle. A gray folder sits at the center under a warm desk lamp, with four blank tabs and six chapter tabs partially visible, a recorder pen nearby, and a few anonymous paper edges. The room beyond the table is softly out of focus: window with rain streaks, empty chairs, quiet after-hours atmosphere. Mood: the first screen of a restrained evidence-themed VN, not a crime thriller poster.""",
    },
    "bg_clubroom_night": {
        "input": "ref_title_table_arrangement_v01.png",
        "output": "site/game/background/clubroom/bg_clubroom_night_v01.webp",
        "prompt": """Use the input image as reference for the folder/table prop language, but expand it into a complete room.

Final image: nighttime campus clubroom interior after rain, warm desk lamp on a long table, gray folder and anonymous papers near the center, two or three simple chairs, rainy window reflections, blank noticeboard, no school mark. The composition should support dialogue scenes with character sprites in front. Calm, tense, quiet, ordinary.""",
    },
    "bg_archive_table": {
        "input": "ref_keyword_box_cards_v01.png",
        "output": "site/game/background/evidence/bg_archive_table_v01.webp",
        "prompt": """Use the input image as reference for tactile evidence props: archival card box, black index cards, pale comparison cards, paper texture, tabs, and warm lamp mood.

Final image: archive sorting table in a small campus room. A gray archival card box, blank index cards, transparent sleeves, clipped pages, paper tabs, and sticky notes are arranged carefully under warm desk-lamp light. Everything is anonymous and reorganized; no readable text. It should feel like a careful record room, not police evidence.""",
    },
    "bg_evidence_cabinet": {
        "input": "ref_evidence_cabinet_module_v01.png",
        "output": "site/game/background/evidence/bg_evidence_cabinet_v01.webp",
        "prompt": """Use the input image as reference for the six-compartment evidence cabinet module.

Final image: full 16:9 evidence display room background. A low glass cabinet with six empty/blank evidence compartments sits under soft practical light. Each compartment contains anonymous cards or paper objects with no readable text. Add faint reflections and dark surrounding shelves, but keep the image clean enough for VN dialogue scenes. Quiet, archival, not horror.""",
    },
    "bg_corridor_rain": {
        "output": "site/game/background/campus/bg_corridor_rain_v01.webp",
        "prompt": """Final image: rainy campus corridor in the evening, empty and anonymous. Long hallway with windows on one side, rain streaks and soft reflections on the floor, blank noticeboard, lockers or clubroom doors without logos, no people, no readable posters, no school crest. The mood should support an observer-view scene: quiet, uncertain, ordinary, not horror. Leave the lower 25% visually calm for the WebGAL dialogue box and keep the vanishing point slightly above center.""",
    },
    "cg_hub_tabs": {
        "input": "ref_folder_gray_open_v01.png",
        "output": "site/game/background/cg/cg_hub_tabs_v01.webp",
        "prompt": """Use the input image as reference for the open gray folder, tabs, clipped blank sheets, and recorder pen.

Final image: a CG-style top-down open folder hub. Four main blank tabs represent main route, cast, timeline, and evidence room without readable labels. Six smaller chapter tabs peek from the side. The folder rests on a quiet table with warm lamp falloff and clean paper textures. It should function as the hub menu visual for a WebGAL VN.""",
    },
    "ev_evidence_six_cards": {
        "input": "ref_evidence_six_cards_v01.png",
        "output": "site/game/background/evidence/ev_evidence_six_cards_v01.webp",
        "prompt": """Use the input image as reference for the six evidence cards, but remove any decorative character silhouettes or bouquet-like elements if present.

Final image: a 16:9 evidence-room display of six anonymous chapter cards. Each card has a blank title bar, pseudo-text rows, small icons or tags, and tactile paper edges. The categories are visually distinct but contain no readable final text. Clean, organized, and suitable as a full-screen evidence page.""",
    },
    "cg_ch01_keyword_box": {
        "input": "ref_keyword_box_cards_v01.png",
        "output": "site/game/background/cg/cg_ch01_keyword_box_v01.webp",
        "prompt": """Use the input image as reference for the gray archival card box, black index cards, pale comparison cards, folded gray strip, and tactile paper/card texture.

Final image: chapter CG for "Chapter 1: Keywords". A gray archival card box sits on an evidence table under warm lamp light. One side contains heavier black keyword index cards, the other side contains softer pale comparison cards. Include blank label bars, pseudo-text lines, subtle red annotation marks, and one folded gray paper strip. No readable words, no real screenshots. Mood: careful indexing, not judgment.""",
    },
    "ev_ch01_keyword_cards": {
        "input": "ref_keyword_box_cards_v01.png",
        "output": "site/game/background/evidence/ev_ch01_keyword_cards_v01.webp",
        "prompt": """Use the input image as reference for the keyword index card system.

Final image: full-screen evidence page for Chapter 1. Arrange black keyword cards and pale comparison cards side by side on a desk. Make the two groups visually balanced and easy to compare. Leave blank title strips and pseudo-text rows for later overlay. Add small tabs and paperclips; keep all text unreadable. Documentary, organized, low-saturation.""",
    },
    "cg_cast_blank_cards": {
        "input": "ref_tabs_four_v01.png",
        "output": "site/game/background/cg/cg_cast_blank_cards_v01.webp",
        "prompt": """Use the input image as reference for tactile paper tabs and blank dossier surfaces.

Final image: character relationship CG. Four anonymous dossier cards lie on an archive table under warm desk-lamp light. Each card has a blank name strip, a blank role strip, a few pseudo-text note rows, and no portrait photo. Use four distinct but muted tab colors to imply Recorder, Mutou, Witness, and Classmate A without showing faces or real identifiers. No readable text, no logos, no real school marks.""",
    },
    "ev_timeline_index": {
        "input": "ref_apr19_timeline_strip_v01.png",
        "output": "site/game/background/evidence/ev_timeline_index_v01.webp",
        "prompt": """Use the input image as reference for an evidence timeline strip, time segments, muted cards, and blue bookmark accents.

Final image: full-screen timeline index page. Six anonymous chapter cards or date slots run across a desk in a readable sequence. Each card has a blank title bar, pseudo-text rows, small status dots, and a muted color tab. Include a thin route line connecting the cards, but no readable dates or messages. It should feel like a private archive timeline, not a menu UI.""",
    },
    "cg_ch02_evaluation_table": {
        "input": "ref_evaluation_table_sheet_v01.png",
        "output": "site/game/background/cg/cg_ch02_evaluation_table_v01.webp",
        "prompt": """Use the input image as reference for the two-column evaluation table, sticky notes, gray-white chat bubbles, red line marks, and anonymous evidence-paper texture.

Final image: chapter CG for "Chapter 2: Concrete Evaluation". A large two-column paper sheet lies on a desk, visually dividing "event/action" on the left from "person/identity" on the right without readable text. Several red arrows or thin red lines show how an evaluation moves from one column to the other. Include anonymous gray chat bubble printouts and blank sticky notes. No real chat UI, no readable labels.""",
    },
    "ev_ch02_chat_bubbles": {
        "input": "ref_redacted_chat_bubbles_v01.png",
        "output": "site/game/background/evidence/ev_ch02_chat_bubbles_v01.webp",
        "prompt": """Use the input image as reference for anonymous redacted chat bubble cutouts.

Final image: full-screen evidence page of gray and white chat bubble printouts spread across a desk. Bubbles have blank bands or redaction strips, no avatars, no names, no timestamps, no platform branding. Add a few red lines and neutral sticky notes indicating evaluation movement. Clean and readable as a VN evidence background.""",
    },
    "cg_ch03_shared_story_cards": {
        "input": "ref_project_song_commission_cards_v01.png",
        "output": "site/game/background/cg/cg_ch03_shared_story_cards_v01.webp",
        "prompt": """Use the input image as reference for project checklist, song/lyrics note, commission/order-style record, call review note, and step-back/compromise label.

Final image: chapter CG for "Chapter 3: Shared Narrative". Several anonymous cards are arranged in a vertical or diagonal chain on an archive table: project checklist, music/lyrics note, commission record, call review note, and compromise/step-back tag. Use blank boxes and pseudo-text only. The visual should communicate that conflict and collaboration coexist in one shared story.""",
    },
    "ev_ch03_project_song_commission": {
        "input": "ref_project_song_commission_cards_v01.png",
        "output": "site/game/background/evidence/ev_ch03_project_song_commission_v01.webp",
        "prompt": """Use the input image as reference for shared-narrative paper cards.

Final image: full-screen evidence page with three clear sections: project, song/creative note, and commission/order-style record. All money amounts, account details, names, and platform marks are removed. Use blank header strips, pseudo-text, paperclips, and muted color tags. Low-saturation documentary VN style.""",
    },
    "cg_ch04_apr9_fold": {
        "input": "ref_apr9_folded_date_page_v01.png",
        "output": "site/game/background/cg/cg_ch04_apr9_fold_v01.webp",
        "prompt": """Use the input image as reference for the folded April 9 date page, horizontal fold, blank date area, subheading blocks, and arrow-shaped footer note.

Final image: chapter CG for "Chapter 4: April 9". A thin folded date page lies under a desk lamp. Four blank subheading blocks imply separation/review, observer angle, same-day interaction, and later note, but no readable text. The fold line should visually suggest contradiction and careful re-reading. Keep the page central with calm lower area for VN dialogue.""",
    },
    "cg_ch05_night_to_day": {
        "input": "ref_apr19_timeline_strip_v01.png",
        "output": "site/game/background/cg/cg_ch05_night_to_day_v01.webp",
        "prompt": """Use the input image as reference for the April 19 horizontal timeline strip, four time segments, gray chat bubble clusters, and blue bookmark.

Final image: chapter CG for "Chapter 5: April 19". A long horizontal evidence timeline runs from deep night to afternoon across a desk. Use four blank time blocks, dense gray chat bubble clusters near the night segment, calmer notes near the afternoon segment, and a modest blue bookmark as the daily-life object. No readable timestamps or messages.""",
    },
    "ev_ch05_gift_bookmark": {
        "input": "ref_apr19_timeline_strip_v01.png",
        "output": "site/game/background/evidence/ev_ch05_gift_bookmark_v01.webp",
        "prompt": """Use the input image as reference for the April 19 timeline and blue bookmark motif.

Final image: evidence page focusing on the emotional shift from high-pressure conversation to daily-life arrangement. Place a small blue bookmark, a modest blank gift note, and a short strip of anonymous gray chat bubbles on a quiet desk. No luxury object, no real place, no readable text. Gentle, ordinary, restrained.""",
    },
    "cg_ch06_after_sticky_notes": {
        "input": "ref_after_sticky_notes_v01.png",
        "output": "site/game/background/cg/cg_ch06_after_sticky_notes_v01.webp",
        "prompt": """Use the input image as reference for five sticky notes with muted colors, paper curl, and category-like blank title areas.

Final image: chapter CG for "Chapter 6: After Separation". Five sticky notes are arranged across an archive desk, each representing one aftermath category: strong emotion, offline activity, organization task, item/consumption, and follow-up. Do not render readable labels. Add faint route-line fragments and clipped blank notes around them. Mood: aftermath that has not naturally stopped.""",
    },
    "ev_ch06_route_and_items": {
        "input": "ref_after_sticky_notes_v01.png",
        "output": "site/game/background/evidence/ev_ch06_route_and_items_v01.webp",
        "prompt": """Use the input image as reference for aftermath sticky notes.

Final image: full-screen evidence page for after-separation materials. Include five sticky notes, a faint erased route line on paper, a cropped meeting-note corner, a small anonymous merchandise-like object with no logo, and stacked blank notes. No real locations, no tickets, no IDs, no readable text. Practical aftermath, not adventure planning.""",
    },
    "cg_final_closed_folder": {
        "input": "ref_title_table_arrangement_v01.png",
        "output": "site/game/background/cg/cg_final_closed_folder_v01.webp",
        "prompt": """Use the input image as reference for the gray folder, chapter tabs, lamp, and quiet table arrangement.

Final image: closing CG. A closed gray folder lies on the table under a warm desk lamp, with six flattened chapter tabs visible but blank. The recorder pen rests nearby. The mood is quiet completion, not victory or judgment. No readable cover text, no UI, no character silhouettes.""",
    },
    "ui_title_logo": {
        "common": UI_COMMON,
        "size": "1536x512",
        "width": 960,
        "height": 320,
        "output": "site/game/template/assets/ui_title_logo_v01.webp",
        "prompt": """Asset: blank title plaque for the title screen, not the full screen.

Create a horizontal gray paper-folder label plate with layered paper tabs and a subtle warm desk-lamp edge light. It should have an empty central title area where real CSS text can sit later. No readable letters, no pseudo-Chinese strokes, no icons that imply a real school or brand. Shape should be compact and stable, suitable for placement in the upper-left title area.""",
    },
    "ui_choice_tabs": {
        "common": UI_COMMON,
        "size": "1536x512",
        "width": 1280,
        "height": 360,
        "output": "site/game/template/assets/ui_choice_tabs_v01.webp",
        "prompt": """Asset: reusable choice-button background for a visual novel choice menu.

Create one long horizontal paper file-tab button base with layered archive-paper texture, very subtle muted blue and pale yellow tab edges, a thin graphite outline, and a blank center for real text. No readable letters, no numbers, no arrows, no checkmarks, no icons, no drop shadow baked too strongly. It should remain legible behind dark red or charcoal menu text.""",
    },
}


def multipart_body(fields: dict[str, str], files: dict[str, tuple[str, bytes, str]]) -> tuple[bytes, str]:
    boundary = "----shezhang-final-assets-boundary"
    parts: list[bytes] = []
    for name, value in fields.items():
        parts.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode(
                "utf-8"
            )
        )
    for name, (filename, data, content_type) in files.items():
        parts.append(
            (
                f"--{boundary}\r\n"
                f"Content-Disposition: form-data; name=\"{name}\"; filename=\"{filename}\"\r\n"
                f"Content-Type: {content_type}\r\n\r\n"
            ).encode("utf-8")
            + data
            + b"\r\n"
        )
    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(parts), boundary


def request_edit(args: argparse.Namespace, image_path: Path, prompt: str) -> dict:
    body, boundary = multipart_body(
        {
            "model": args.model,
            "prompt": prompt,
            "size": args.size,
        },
        {
            "image": (image_path.name, image_path.read_bytes(), "image/png"),
        },
    )
    req = urllib.request.Request(
        args.api_base.rstrip("/") + "/v1/images/edits",
        data=body,
        headers={
            "Authorization": f"Bearer {args.api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=args.timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def request_generation(args: argparse.Namespace, prompt: str, size: str) -> dict:
    payload = {
        "model": args.model,
        "prompt": prompt,
        "size": size,
        "n": 1,
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        args.api_base.rstrip("/") + "/v1/images/generations",
        data=body,
        headers={
            "Authorization": f"Bearer {args.api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=args.timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def extract_b64(response: dict) -> bytes:
    data = response.get("data")
    if isinstance(data, list) and data:
        item = data[0]
        if isinstance(item, dict) and isinstance(item.get("b64_json"), str):
            return base64.b64decode(item["b64_json"])
        if isinstance(item, dict) and isinstance(item.get("url"), str):
            url = item["url"]
            if url.startswith("data:"):
                return base64.b64decode(url.split(",", 1)[1])
            with urllib.request.urlopen(url, timeout=180) as resp:
                return resp.read()
    text = json.dumps(response)
    match = re.search(r"data:image/[^;]+;base64,([A-Za-z0-9+/=\s]+)", text)
    if match:
        return base64.b64decode(match.group(1))
    raise ValueError("No image payload found in image response")


def make_prompt(cfg: dict[str, str]) -> str:
    return cfg.get("common", COMMON) + "\n" + cfg["prompt"]


def write_cover_webp(source: Path, target: Path, width: int, height: int, quality: int) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as raw:
        image = raw.convert("RGB")
        scale = max(width / image.width, height / image.height)
        resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
        left = max(0, (resized.width - width) // 2)
        top = max(0, (resized.height - height) // 2)
        cropped = resized.crop((left, top, left + width, top + height))
        cropped.save(target, "WEBP", quality=quality, method=6)


def write_meta(
    name: str,
    cfg: dict[str, str],
    args: argparse.Namespace,
    source: Path,
    response: dict,
    mode: str,
    request_size: str,
    final_width: int,
    final_height: int,
) -> None:
    META_DIR.mkdir(parents=True, exist_ok=True)
    output = ROOT / cfg["output"]
    meta = {
        "asset_id": name,
        "source_output": str(source.relative_to(ROOT)),
        "final_output": str(output.relative_to(ROOT)),
        "model": args.model,
        "mode": mode,
        "api_base": args.api_base,
        "size": request_size,
        "final_size": [final_width, final_height],
        "prompt": make_prompt(cfg),
        "response": {
            "id": response.get("id"),
            "created": response.get("created"),
            "response_keys": sorted(response.keys()),
        },
    }
    if cfg.get("input"):
        meta["input"] = str((REF_DIR / cfg["input"]).relative_to(ROOT))
    (META_DIR / f"{name}_v01.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-base", default="https://api.qingyuntop.top")
    parser.add_argument("--api-key", default=os.environ.get("QINGYUN_API_KEY"))
    parser.add_argument("--model", default="gpt-image-2")
    parser.add_argument("--size", default="1536x864")
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--quality", type=int, default=90)
    parser.add_argument("--only", action="append", default=[])
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--delay", type=float, default=3.0)
    parser.add_argument("--max-retries", type=int, default=0)
    args = parser.parse_args()
    if not args.api_key:
        print("QINGYUN_API_KEY is required", file=sys.stderr)
        return 2

    names = args.only or list(ASSETS)
    for name in names:
        if name not in ASSETS:
            print(f"Unknown asset id: {name}", file=sys.stderr)
            return 2

    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    for index, name in enumerate(names, 1):
        cfg = ASSETS[name]
        source_ref = REF_DIR / cfg["input"] if cfg.get("input") else None
        final_out = ROOT / cfg["output"]
        source_out = SOURCE_DIR / f"{name}_source_v01.png"
        request_size = cfg.get("size", args.size)
        final_width = int(cfg.get("width", args.width))
        final_height = int(cfg.get("height", args.height))
        if source_ref is not None and not source_ref.exists():
            raise FileNotFoundError(source_ref)
        if final_out.exists() and source_out.exists() and not args.force:
            print(f"[{index}/{len(names)}] skip existing {name}", flush=True)
            continue
        prompt = make_prompt(cfg)
        last_error: Exception | None = None
        for attempt in range(1, args.max_retries + 2):
            try:
                print(f"[{index}/{len(names)}] generating {name} attempt {attempt}", flush=True)
                if source_ref is None:
                    response = request_generation(args, prompt, request_size)
                    mode = "generations"
                else:
                    response = request_edit(args, source_ref, prompt)
                    mode = "edits"
                source_out.write_bytes(extract_b64(response))
                write_cover_webp(source_out, final_out, final_width, final_height, args.quality)
                write_meta(name, cfg, args, source_out, response, mode, request_size, final_width, final_height)
                print(f"[{index}/{len(names)}] wrote {final_out}", flush=True)
                last_error = None
                break
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as exc:
                last_error = exc
                print(f"[{index}/{len(names)}] error {name}: {exc}", file=sys.stderr, flush=True)
                if attempt <= args.max_retries:
                    time.sleep(args.delay * attempt)
        if last_error is not None:
            raise last_error
        time.sleep(args.delay)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
