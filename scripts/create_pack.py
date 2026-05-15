#!/usr/bin/env python3
"""Create a OneClick Store Marketing delivery folder skeleton."""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path


ASSET_DIRS = (
    "prompts",
    "poster",
    "rollup",
    "window",
    "price-tag",
    "event-page",
    "social",
    "product",
    "extras",
)
MARKDOWN_FILES = {
    "campaign-brief.md": "# Campaign Brief\n\n",
    "copy-bank.md": "# Copy Bank\n\n",
    "print-assets.md": "# Print Assets\n\n",
    "social-pack.md": "# Social Pack\n\n",
    "event-playbook.md": "# Event Playbook\n\n",
    "image-prompts.md": "# Image Prompts\n\n",
}


def safe_slug(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff_-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-_")
    return value or "store-campaign"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold a local-store marketing delivery pack.")
    parser.add_argument("--slug", required=True, help="Campaign slug, such as guzi-launch.")
    parser.add_argument("--store-type", required=True, help="Store type, such as anime merch store.")
    parser.add_argument("--audience", required=True, help="Target audience, such as college students.")
    parser.add_argument("--campaign-goal", required=True, help="Campaign goal, such as new product launch.")
    parser.add_argument("--store-name", default="", help="Optional store name.")
    parser.add_argument("--product", default="", help="Optional product or service.")
    parser.add_argument("--offer", default="", help="Optional offer or event mechanic.")
    parser.add_argument("--output-root", default="generated-campaigns", help="Output root directory.")
    parser.add_argument("--timestamp", default="", help="Optional fixed timestamp yyyymmdd-hhmmss.")
    return parser.parse_args()


def brief_markdown(args: argparse.Namespace, job_dir: Path) -> str:
    lines = [
        "# Campaign Brief",
        "",
        "```text",
        "STORE_MARKETING_BRIEF {",
        f"  store_type: {args.store_type}",
        f"  store_name: {args.store_name or '[not provided]'}",
        f"  product_or_service: {args.product or '[not provided]'}",
        f"  audience: {args.audience}",
        f"  campaign_goal: {args.campaign_goal}",
        f"  offer: {args.offer or '[not provided]'}",
        f"  delivery_folder: {job_dir}",
        "}",
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    timestamp = args.timestamp or time.strftime("%Y%m%d-%H%M%S")
    job_dir = Path(args.output_root) / f"{safe_slug(args.slug)}-{timestamp}"
    job_dir.mkdir(parents=True, exist_ok=True)

    for dirname in ASSET_DIRS:
        (job_dir / dirname).mkdir(exist_ok=True)

    for filename, content in MARKDOWN_FILES.items():
        path = job_dir / filename
        if not path.exists():
            path.write_text(content, encoding="utf-8")

    (job_dir / "campaign-brief.md").write_text(brief_markdown(args, job_dir), encoding="utf-8")

    manifest = {
        "store_type": args.store_type,
        "store_name": args.store_name,
        "product_or_service": args.product,
        "audience": args.audience,
        "campaign_goal": args.campaign_goal,
        "offer": args.offer,
        "created_at": timestamp,
        "job_dir": str(job_dir),
        "asset_dirs": list(ASSET_DIRS),
    }
    (job_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(job_dir)


if __name__ == "__main__":
    main()
