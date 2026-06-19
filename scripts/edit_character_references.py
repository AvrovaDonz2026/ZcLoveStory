#!/usr/bin/env python3
"""Edit green-screen character references with Qingyun /v1/images/edits."""

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


ROOT = Path(__file__).resolve().parents[1]
REF_DIR = ROOT / "site" / "game" / "reference" / "round1"
META_DIR = REF_DIR / "_meta"

COMMON = """Edit this existing green-screen VN character reference.

Preserve: pure #00FF00 chroma key background, clean cutout-ready silhouette, Japanese visual novel linework, grounded contemporary campus realism, low-saturation palette, restrained emotion, no logo, no readable text.

Goal: make the character visually distinct at a glance from the other male characters by changing clothing silhouette, color block, accessories, and carried object. Keep the character semi-anonymous and ordinary, not idol-like, not glamorous.
"""

EDITS = {
    "ref_mutou_neutral": {
        "input": "ref_mutou_neutral_v01.png",
        "output": "ref_mutou_neutral_v02.png",
        "prompt": """Character role: Mutou, the club president.

Distinct look: black short stand-collar jacket, medium gray button shirt, charcoal straight pants, white sneakers, gray evidence folder held at the side. No glasses, no crossbody bag, no cardigan, no table. Keep him calm, reserved, slightly guarded, competent but ordinary. Outfit should read as the darkest and sharpest silhouette among the boys.""",
    },
    "ref_mutou_tired": {
        "input": "ref_mutou_tired_v01.png",
        "output": "ref_mutou_tired_v02.png",
        "prompt": """Character role: Mutou, tired variant of the club president.

Distinct look: same identity and outfit family as Mutou neutral: black short stand-collar jacket, medium gray shirt, charcoal pants, gray evidence folder or folder edge. No glasses, no crossbody bag, no cardigan. Pose: head slightly lowered, one hand near sleeve cuff or folder, tired eyes. He must still be recognizable as Mutou and clearly separate from Recorder and Witness.""",
    },
    "ref_recorder_neutral": {
        "input": "ref_recorder_neutral_v01.png",
        "output": "ref_recorder_neutral_v02.png",
        "prompt": """Character role: the Recorder, player-view narrator.

Distinct look: light beige utility vest over a white rolled-sleeve shirt, dark olive or brown trousers, red-brown clipboard notebook, recorder pen clipped to the vest, small wristwatch. Hair can be tied back or neatly parted to avoid matching Mutou. No black jacket, no blue cardigan, no glasses, no crossbody bag. Remove the table if possible; keep one portable evidence notebook and recorder pen. Silhouette should be lighter and more documentarian than Mutou.""",
    },
    "ref_witness_neutral": {
        "input": "ref_witness_neutral_v01.png",
        "output": "ref_witness_neutral_v02.png",
        "prompt": """Character role: the Witness, semi-anonymous observer.

Distinct look: blue-gray long knit cardigan over an off-white turtleneck, round glasses, tan canvas crossbody bag, small spiral notepad and pen. Slightly softer hair shape and side-looking observant posture. No black jacket, no gray evidence folder, no beige utility vest. Silhouette should read as the softest and most observer-like among the boys.""",
    },
    "ref_mutou_soft": {
        "input": "ref_mutou_neutral_v02.png",
        "output": "ref_mutou_soft_v01.png",
        "prompt": """Character role: Mutou, softer reassurance variant of the club president.

Preserve Mutou's distinct identity exactly: black short stand-collar jacket, medium gray button shirt, charcoal straight pants, white sneakers, gray evidence folder. No glasses, no crossbody bag, no cardigan, no beige utility vest. Change only expression and gesture: shoulders less guarded, eyes slightly gentler, one hand open or lightly touching the folder as if answering carefully. He should feel warmer but still restrained and ordinary.""",
    },
    "ref_recorder_thinking": {
        "input": "ref_recorder_neutral_v02.png",
        "output": "ref_recorder_thinking_v01.png",
        "prompt": """Character role: the Recorder, thinking variant of the player-view narrator.

Preserve the Recorder's distinct identity exactly: light beige utility vest over a white rolled-sleeve shirt, dark olive or brown trousers, red-brown clipboard notebook, recorder pen clipped to the vest, small wristwatch. No black jacket, no blue cardigan, no glasses, no crossbody bag. Change only expression and gesture: thoughtful, pen near chin or notebook, slightly narrowed eyes, as if checking the order of evidence.""",
    },
    "ref_witness_concerned": {
        "input": "ref_witness_neutral_v02.png",
        "output": "ref_witness_concerned_v01.png",
        "prompt": """Character role: the Witness, concerned observer variant.

Preserve the Witness's distinct identity exactly: blue-gray long knit cardigan, off-white turtleneck, round glasses, tan canvas crossbody bag, small spiral notepad and pen. No black jacket, no gray evidence folder, no beige utility vest. Change only expression and gesture: worried but careful, one hand near the spiral notepad or lightly folded arms, side-looking posture, not dramatic.""",
    },
    "ref_classmate_a_question": {
        "input": "ref_classmate_a_neutral_v01.png",
        "output": "ref_classmate_a_question_v01.png",
        "prompt": """Character role: Classmate A, ordinary club member asking a question.

Distinct look: warm rust-brown hoodie or cardigan over an off-white shirt, simple dark trousers, loose blank paper in one hand. No black jacket, no gray evidence folder, no beige utility vest, no blue cardigan, no round glasses, no tan crossbody bag. Pose: upright half-body or knee-up, slightly nervous but sincere, one hand raised a little as if asking. Make the warm hoodie/cardigan color unmistakable so this character is readable at a glance.""",
    },
}


def multipart_body(fields: dict[str, str], files: dict[str, tuple[str, bytes, str]]) -> tuple[bytes, str]:
    boundary = "----shezhang-edits-boundary"
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
    raise ValueError("No image payload found in edits response")


def write_meta(name: str, cfg: dict[str, str], args: argparse.Namespace, response: dict) -> None:
    META_DIR.mkdir(parents=True, exist_ok=True)
    meta = {
        "asset_id": name,
        "input": str((REF_DIR / cfg["input"]).relative_to(ROOT)),
        "output": str((REF_DIR / cfg["output"]).relative_to(ROOT)),
        "model": args.model,
        "mode": "edits",
        "api_base": args.api_base,
        "size": args.size,
        "prompt": COMMON + "\n" + cfg["prompt"],
        "response": {
            "id": response.get("id"),
            "created": response.get("created"),
            "response_keys": sorted(response.keys()),
        },
    }
    (META_DIR / cfg["output"].replace(".png", ".json")).write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-base", default="https://api.qingyuntop.top")
    parser.add_argument("--api-key", default=os.environ.get("QINGYUN_API_KEY"))
    parser.add_argument("--model", default="gpt-image-2")
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--only", action="append", default=[])
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--timeout", type=int, default=360)
    parser.add_argument("--delay", type=float, default=2.0)
    parser.add_argument("--max-retries", type=int, default=1)
    args = parser.parse_args()
    if not args.api_key:
        print("QINGYUN_API_KEY is required", file=sys.stderr)
        return 2

    names = args.only or list(EDITS)
    for name in names:
        if name not in EDITS:
            print(f"Unknown edit id: {name}", file=sys.stderr)
            return 2
    for index, name in enumerate(names, 1):
        cfg = EDITS[name]
        source = REF_DIR / cfg["input"]
        target = REF_DIR / cfg["output"]
        if not source.exists():
            raise FileNotFoundError(source)
        if target.exists() and not args.force:
            print(f"[{index}/{len(names)}] skip existing {target}")
            continue
        prompt = COMMON + "\n" + cfg["prompt"]
        last_error: Exception | None = None
        for attempt in range(1, args.max_retries + 2):
            try:
                print(f"[{index}/{len(names)}] editing {name} attempt {attempt}")
                response = request_edit(args, source, prompt)
                target.write_bytes(extract_b64(response))
                write_meta(name, cfg, args, response)
                print(f"[{index}/{len(names)}] wrote {target}")
                last_error = None
                break
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as exc:
                last_error = exc
                print(f"[{index}/{len(names)}] error {name}: {exc}", file=sys.stderr)
                if attempt <= args.max_retries:
                    time.sleep(args.delay * attempt)
        if last_error is not None:
            raise last_error
        time.sleep(args.delay)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
