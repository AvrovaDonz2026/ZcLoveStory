#!/usr/bin/env python3
"""Generate round-1 green-screen reference images with Qingyun-compatible APIs."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT_DOC = ROOT / "docs" / "reference_prompts_round1.md"
OUT_DIR = ROOT / "site" / "game" / "reference" / "round1"
META_DIR = OUT_DIR / "_meta"

STYLE_REFS = [
    Path("/home/donz/assets_generated/bg/01_s02.png"),
    Path("/home/donz/assets_generated/remaining_pro_chara/01_s01.png"),
    Path("/home/donz/assets_generated/style_anchor/cash_anchor.png"),
    Path("/home/donz/assets_generated/compat_ui_p0/p_s03.png"),
]

PRIORITY_16 = [
    "ref_mutou_neutral",
    "ref_mutou_tired",
    "ref_recorder_neutral",
    "ref_witness_neutral",
    "ref_folder_gray_open",
    "ref_tabs_four",
    "ref_evidence_six_cards",
    "ref_keyword_box_cards",
    "ref_evaluation_table_sheet",
    "ref_redacted_chat_bubbles",
    "ref_project_song_commission_cards",
    "ref_apr9_folded_date_page",
    "ref_apr19_timeline_strip",
    "ref_after_sticky_notes",
    "ref_title_table_arrangement",
    "ref_evidence_cabinet_module",
]

SIZES = {
    "ref_mutou_neutral": "1024x1536",
    "ref_mutou_tired": "1024x1536",
    "ref_mutou_soft": "1024x1536",
    "ref_recorder_neutral": "1024x1536",
    "ref_recorder_thinking": "1024x1536",
    "ref_witness_neutral": "1024x1536",
    "ref_witness_concerned": "1024x1536",
    "ref_classmate_a_neutral": "1024x1536",
    "ref_phone_chat_shell": "1080x1920",
    "ref_social_post_shell": "1080x1920",
    "ref_timeline_ui_shell": "1080x1920",
    "ref_evidence_card_ui_shell": "1080x1920",
}


def read_doc() -> str:
    return PROMPT_DOC.read_text(encoding="utf-8")


def block_after_heading(doc: str, heading: str) -> str:
    pattern = re.compile(
        rf"^## {re.escape(heading)}\n.*?```text\n(.*?)\n```",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(doc)
    if not match:
        raise ValueError(f"Could not find heading block: {heading}")
    return match.group(1).strip()


def parse_items(doc: str) -> dict[str, str]:
    pattern = re.compile(
        r"^### (ref_[a-z0-9_]+)\n\n```text\n(.*?)\n```",
        re.MULTILINE | re.DOTALL,
    )
    return {name: prompt.strip() for name, prompt in pattern.findall(doc)}


def data_url(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    raw = path.read_bytes()
    return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"


def request_json(url: str, payload: dict, key: str, timeout: int) -> dict:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def decode_data_url(value: str) -> tuple[bytes, str]:
    if value.startswith("data:"):
        head, encoded = value.split(",", 1)
        ext = ".png"
        if "jpeg" in head or "jpg" in head:
            ext = ".jpg"
        elif "webp" in head:
            ext = ".webp"
        return base64.b64decode(encoded), ext
    if re.fullmatch(r"[A-Za-z0-9+/=\s]+", value) and len(value) > 2000:
        return base64.b64decode(value), ".png"
    raise ValueError("Not an inline image")


def extract_image(response: dict) -> tuple[bytes, str, str]:
    data = response.get("data")
    if isinstance(data, list) and data:
        item = data[0]
        if isinstance(item, dict):
            if item.get("b64_json"):
                return base64.b64decode(item["b64_json"]), ".png", "data.b64_json"
            if item.get("url"):
                url = item["url"]
                if str(url).startswith("data:"):
                    raw, ext = decode_data_url(url)
                    return raw, ext, "data.url:data"
                with urllib.request.urlopen(url, timeout=180) as resp:
                    return resp.read(), Path(urllib.parse.urlparse(url).path).suffix or ".png", "data.url"

    choices = response.get("choices")
    if isinstance(choices, list):
        for choice in choices:
            message = choice.get("message", {}) if isinstance(choice, dict) else {}
            candidates = []
            content = message.get("content")
            if isinstance(content, str):
                candidates.append(content)
                candidates.extend(re.findall(r"!\[[^\]]*\]\((data:image/[^)]+)\)", content))
                candidates.extend(re.findall(r"(data:image/[A-Za-z0-9.+-]+;base64,[A-Za-z0-9+/=\s]+)", content))
            elif isinstance(content, list):
                for part in content:
                    if not isinstance(part, dict):
                        continue
                    candidates.extend(
                        str(v)
                        for k, v in part.items()
                        if k in {"image_url", "url", "b64_json", "data"} and isinstance(v, str)
                    )
                    image_url = part.get("image_url")
                    if isinstance(image_url, dict) and isinstance(image_url.get("url"), str):
                        candidates.append(image_url["url"])
            for key in ("images", "image_urls"):
                value = message.get(key)
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, str):
                            candidates.append(item)
                        elif isinstance(item, dict):
                            for nested_key in ("url", "b64_json", "data"):
                                if isinstance(item.get(nested_key), str):
                                    candidates.append(item[nested_key])
            for candidate in candidates:
                try:
                    raw, ext = decode_data_url(candidate)
                    return raw, ext, "choices.message"
                except Exception:
                    continue

    raise ValueError("Could not find an image in API response")


def make_prompt(common: str, item_prompt: str, negative: str) -> str:
    style_note = (
        "Text-described style anchor from /home/donz/assets_generated/: clean Japanese visual novel linework, "
        "grounded contemporary campus realism, tidy flat-to-soft shading, low-saturation gray / off-white / muted blue palette, "
        "restrained emotion, readable object-first composition, paper texture and slightly worn edges for evidence props, "
        "light gray fictional social UI shells with small red notification accents for interface assets. "
        "This prompt uses textual style description only; no local reference image is attached to the images endpoint."
    )
    return "\n\n".join([common, style_note, item_prompt, negative])


def payload_chat(model: str, prompt: str, size: str, include_refs: bool) -> dict:
    content = [{"type": "text", "text": prompt + f"\n\nTarget size/aspect: {size}."}]
    if include_refs:
        for ref in STYLE_REFS:
            if ref.exists():
                content.append({"type": "image_url", "image_url": {"url": data_url(ref)}})
    return {
        "model": model,
        "messages": [{"role": "user", "content": content}],
    }


def payload_images(model: str, prompt: str, size: str) -> dict:
    return {
        "model": model,
        "prompt": prompt,
        "size": size,
        "n": 1,
    }


def generate_one(args: argparse.Namespace, name: str, prompt: str) -> Path:
    size = args.size or SIZES.get(name, "1536x1536")
    url = args.api_base.rstrip("/")
    if args.mode == "chat":
        endpoint = url + "/v1/chat/completions"
        payload = payload_chat(args.model, prompt, size, args.with_style_refs)
    else:
        endpoint = url + "/v1/images/generations"
        payload = payload_images(args.model, prompt, size)

    response = request_json(endpoint, payload, args.api_key, args.timeout)
    raw, ext, source = extract_image(response)
    ext = ".png" if ext.lower() in {"", ".jpeg"} else ext
    out = OUT_DIR / f"{name}_v01{ext}"
    meta = META_DIR / f"{name}_v01.json"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    META_DIR.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    safe_response = {
        "id": response.get("id"),
        "model": response.get("model", args.model),
        "created": response.get("created"),
        "image_source": source,
        "response_keys": sorted(response.keys()),
    }
    meta.write_text(
        json.dumps(
            {
                "asset_id": name,
                "output": str(out.relative_to(ROOT)),
                "prompt": prompt,
                "model": args.model,
                "mode": args.mode,
                "api_base": args.api_base,
                "size": size,
                "style_refs": [str(p) for p in STYLE_REFS if p.exists()] if args.with_style_refs else [],
                "response": safe_response,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-base", default="https://api.qingyuntop.top")
    parser.add_argument("--api-key", default=os.environ.get("QINGYUN_API_KEY"))
    parser.add_argument("--mode", choices=["chat", "images"], default="images")
    parser.add_argument("--model", default="gpt-image-2")
    parser.add_argument("--only", action="append", default=[])
    parser.add_argument("--priority16", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--size")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--with-style-refs", action="store_true")
    args = parser.parse_args()
    if not args.api_key:
        print("QINGYUN_API_KEY is required", file=sys.stderr)
        return 2

    doc = read_doc()
    common = block_after_heading(doc, "通用前缀")
    negative = block_after_heading(doc, "通用负面约束")
    items = parse_items(doc)

    if args.all:
        names = list(items)
    elif args.priority16:
        names = PRIORITY_16
    elif args.only:
        names = args.only
    else:
        print("Use --only NAME, --priority16, or --all", file=sys.stderr)
        return 2

    missing = [name for name in names if name not in items]
    if missing:
        print(f"Unknown prompt ids: {', '.join(missing)}", file=sys.stderr)
        return 2

    for index, name in enumerate(names, 1):
        existing = sorted(OUT_DIR.glob(f"{name}_v01.*"))
        if existing and not args.force:
            print(f"[{index}/{len(names)}] skip existing {name}: {existing[0]}")
            continue
        prompt = make_prompt(common, items[name], negative)
        last_error: Exception | None = None
        for attempt in range(1, args.max_retries + 2):
            try:
                print(f"[{index}/{len(names)}] generating {name} attempt {attempt}")
                out = generate_one(args, name, prompt)
                print(f"[{index}/{len(names)}] wrote {out}")
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
