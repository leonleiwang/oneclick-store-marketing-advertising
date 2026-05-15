#!/usr/bin/env python3
"""Generate or save image prompts through an OpenAI-compatible Images API."""

from __future__ import annotations

import argparse
import base64
import binascii
import http.client
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ENV_BASE_URL = "IMG_BASE_URL"
ENV_MODEL = "IMG_MODEL"
ENV_API_KEY = "IMG_API_KEY"
ENV_ALIASES = {
    ENV_BASE_URL: ("OPENAI_BASE_URL", "OPENAI_API_BASE", "BASE_URL"),
    ENV_MODEL: ("OPENAI_IMAGE_MODEL", "IMAGE_MODEL", "OPENAI_MODEL"),
    ENV_API_KEY: ("OPENAI_API_KEY", "API_KEY"),
}
REQUIRED_CONFIGS = (ENV_BASE_URL, ENV_MODEL, ENV_API_KEY)
ASSET_TYPE_DIRS = {
    "poster": "poster",
    "rollup": "rollup",
    "banner": "rollup",
    "window": "window",
    "price-tag": "price-tag",
    "shelf-talker": "price-tag",
    "event-page": "event-page",
    "flyer": "event-page",
    "social": "social",
    "product": "product",
    "lifestyle": "product",
    "extra": "extras",
    "extras": "extras",
    "custom": "custom",
}
REFERENCE_IMAGE_MIME_TYPES = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "webp": "image/webp",
}
DEFAULT_TIMEOUT_SECONDS = 180
DEFAULT_RETRIES = 2


def fail(message: str, exit_code: int = 1) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(exit_code)


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt:
        prompt = args.prompt.strip()
    else:
        try:
            prompt = Path(args.prompt_file).read_text(encoding="utf-8").strip()
        except OSError as exc:
            fail(f"Cannot read prompt file: {exc}")
    if not prompt:
        fail("Prompt cannot be empty.")
    return prompt


def strip_env_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def find_default_env_file() -> Path | None:
    for directory in (Path.cwd(), *Path.cwd().parents):
        env_file = directory / ".env"
        if env_file.is_file():
            return env_file
    return None


def load_env_file(env_file: Path | None) -> None:
    if env_file is None:
        return
    try:
        lines = env_file.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        fail(f"Cannot read env file: {exc}")

    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            fail(f"Invalid .env line {line_number}; expected KEY=value.")
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            fail(f"Missing variable name on .env line {line_number}.")
        if key not in os.environ:
            os.environ[key] = strip_env_value(value)


def config_candidates(name: str) -> tuple[str, ...]:
    return (name, *ENV_ALIASES.get(name, ()))


def get_config(name: str) -> str | None:
    for candidate in config_candidates(name):
        value = os.environ.get(candidate, "").strip()
        if value:
            return value
    return None


def collect_config() -> tuple[dict[str, str], list[str]]:
    config: dict[str, str] = {}
    missing: list[str] = []
    for name in REQUIRED_CONFIGS:
        value = get_config(name)
        if value:
            config[name] = value
        else:
            missing.append(name)
    return config, missing


def is_pollinations_dev_url(base_url: str | None) -> bool:
    if not base_url:
        return False
    host = urllib.parse.urlparse(base_url).netloc.lower()
    return host in {"image.pollinations.ai", "gen.pollinations.ai"}


def missing_required_config(config: dict[str, str], missing: list[str]) -> list[str]:
    if is_pollinations_dev_url(config.get(ENV_BASE_URL)):
        return [name for name in missing if name != ENV_API_KEY]
    return missing


def format_missing_config(missing: list[str]) -> str:
    return ", ".join(" / ".join(config_candidates(name)) for name in missing)


def build_payload(args: argparse.Namespace, prompt: str, model: str) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "n": args.n,
        "size": args.size,
    }
    if args.quality:
        payload["quality"] = args.quality
    if args.format:
        payload["output_format"] = args.format
    return payload


def multipart_boundary() -> str:
    return f"----codex-image-boundary-{int(time.time() * 1000)}"


def multipart_field(name: str, value: str, boundary: str) -> bytes:
    return (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
        f"{value}\r\n"
    ).encode("utf-8")


def multipart_file_field(name: str, path: Path, boundary: str) -> bytes:
    try:
        image_bytes = path.read_bytes()
    except OSError as exc:
        fail(f"Cannot read reference image: {exc}")

    mime_type = REFERENCE_IMAGE_MIME_TYPES[path.suffix.lower().lstrip(".")]
    header = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{name}"; filename="{path.name}"\r\n'
        f"Content-Type: {mime_type}\r\n\r\n"
    ).encode("utf-8")
    return header + image_bytes + b"\r\n"


def build_multipart_body(args: argparse.Namespace, prompt: str, model: str) -> tuple[bytes, str]:
    if not args.image:
        fail("Multipart requests require --image.")

    image_path = Path(args.image)
    if not image_path.is_file():
        fail(f"Reference image does not exist: {args.image}")

    suffix = image_path.suffix.lower().lstrip(".")
    if suffix not in REFERENCE_IMAGE_MIME_TYPES:
        supported = ", ".join(REFERENCE_IMAGE_MIME_TYPES)
        fail(f"Unsupported reference image format .{suffix}; supported: {supported}.")

    boundary = multipart_boundary()
    parts = [
        multipart_field("model", model, boundary),
        multipart_field("prompt", prompt, boundary),
        multipart_field("n", str(args.n), boundary),
        multipart_field("size", args.size, boundary),
    ]
    if args.quality:
        parts.append(multipart_field("quality", args.quality, boundary))
    if args.format:
        parts.append(multipart_field("output_format", args.format, boundary))
    parts.append(multipart_file_field("image", image_path, boundary))
    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(parts), boundary


def safe_filename_stem(value: str) -> str:
    chars: list[str] = []
    for char in value.lower():
        if char.isascii() and (char.isalnum() or char in {"-", "_"}):
            chars.append(char)
        elif char in {" ", ".", "/", "\\"}:
            chars.append("-")
    stem = "".join(chars).strip("-_")
    return stem or "prompt"


def prompt_filename(args: argparse.Namespace) -> str:
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    if args.prompt_file:
        source_stem = safe_filename_stem(Path(args.prompt_file).stem)
    else:
        source_stem = "prompt"
    asset_dir = ASSET_TYPE_DIRS[args.asset_type]
    return f"{asset_dir}-{source_stem}-{timestamp}.txt"


def save_prompt(prompt: str, args: argparse.Namespace) -> Path | None:
    if not args.job_dir:
        return None
    prompt_dir = Path(args.job_dir) / "prompts"
    prompt_dir.mkdir(parents=True, exist_ok=True)
    output_path = prompt_dir / prompt_filename(args)
    try:
        output_path.write_text(f"{prompt}\n", encoding="utf-8")
    except OSError as exc:
        fail(f"Cannot write prompt file: {exc}")
    return output_path


def resolve_output_dir(args: argparse.Namespace) -> Path:
    if args.job_dir:
        return Path(args.job_dir) / ASSET_TYPE_DIRS[args.asset_type]
    return Path(args.output_dir)


def print_prompt_only(prompt: str, prompt_path: Path | None, missing: list[str]) -> None:
    if missing:
        print("Image API config is incomplete; auto mode saved and printed the prompt only.")
        print(f"Missing config: {format_missing_config(missing)}")
        print("Set IMG_BASE_URL, IMG_MODEL, and IMG_API_KEY to generate images with the same command.")
    else:
        print("Prompt mode: saved and printed the prompt only.")
    if prompt_path:
        print(f"Prompt saved: {prompt_path}")
    print("\nPrompt:\n")
    print(prompt)


def image_endpoint(base_url: str, args: argparse.Namespace) -> str:
    if args.image:
        return f"{base_url}/images/edits"
    return f"{base_url}/images/generations"


def parse_size(size: str) -> tuple[int, int]:
    parts = size.lower().split("x", 1)
    if len(parts) != 2:
        fail(f"Invalid size '{size}'. Expected WIDTHxHEIGHT, such as 1024x1536.")
    try:
        width = int(parts[0])
        height = int(parts[1])
    except ValueError:
        fail(f"Invalid size '{size}'. Width and height must be integers.")
    if width < 1 or height < 1:
        fail("Image width and height must be positive.")
    return width, height


def pollinations_image_url(base_url: str, args: argparse.Namespace, prompt: str, model: str) -> str:
    if args.image:
        fail("Pollinations dev mode in this script supports text-to-image only; remove --image.")
    width, height = parse_size(args.size)
    encoded_prompt = urllib.parse.quote(prompt)

    if "gen.pollinations.ai" in urllib.parse.urlparse(base_url).netloc.lower():
        url = f"{base_url.rstrip('/')}/image/{encoded_prompt}"
    else:
        url = f"{base_url.rstrip('/')}/prompt/{encoded_prompt}"

    params = {
        "width": str(width),
        "height": str(height),
        "nologo": "true",
        "referrer": "oneclick-store-marketing",
    }
    if model and model.lower() != "mock":
        params["model"] = model
    return f"{url}?{urllib.parse.urlencode(params)}"


def post_json(url: str, api_key: str, payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    last_error = ""
    for attempt in range(DEFAULT_RETRIES + 1):
        try:
            with urllib.request.urlopen(request, timeout=DEFAULT_TIMEOUT_SECONDS) as response:
                raw = response.read().decode("utf-8")
                return parse_api_result(raw)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            fail(f"Image API returned HTTP {exc.code}: {detail}")
        except urllib.error.URLError as exc:
            last_error = f"Cannot connect to image API: {exc.reason}"
        except http.client.RemoteDisconnected:
            last_error = "Image API closed the connection."
        except TimeoutError:
            last_error = "Image API request timed out."
        if attempt < DEFAULT_RETRIES:
            time.sleep(retry_delay(attempt))
    fail(f"{last_error} Retried {DEFAULT_RETRIES} times.")


def post_multipart(url: str, api_key: str, body: bytes, boundary: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    last_error = ""
    for attempt in range(DEFAULT_RETRIES + 1):
        try:
            with urllib.request.urlopen(request, timeout=DEFAULT_TIMEOUT_SECONDS) as response:
                raw = response.read().decode("utf-8")
                return parse_api_result(raw)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            fail(f"Image API returned HTTP {exc.code}: {detail}")
        except urllib.error.URLError as exc:
            last_error = f"Cannot connect to image API: {exc.reason}"
        except http.client.RemoteDisconnected:
            last_error = "Image API closed the connection."
        except TimeoutError:
            last_error = "Image API request timed out."
        if attempt < DEFAULT_RETRIES:
            time.sleep(retry_delay(attempt))
    fail(f"{last_error} Retried {DEFAULT_RETRIES} times.")


def parse_api_result(raw: str) -> dict[str, Any]:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        fail(f"Image API did not return valid JSON: {raw[:500]}")
    if not isinstance(parsed, dict):
        fail("Image API response is invalid: top-level result is not an object.")
    return parsed


def retry_delay(attempt: int) -> float:
    return 1.5 * (attempt + 1)


def filename_for(index: int, suffix: str) -> str:
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    return f"image-{timestamp}-{index + 1:02d}.{suffix.lstrip('.')}"


def suffix_from_url(url: str, fallback: str) -> str:
    path = urllib.parse.urlparse(url).path
    suffix = Path(path).suffix.lower().lstrip(".")
    if suffix in {"png", "jpg", "jpeg", "webp"}:
        return "jpg" if suffix == "jpeg" else suffix
    return fallback


def save_b64_image(item: dict[str, Any], output_dir: Path, index: int, fmt: str) -> Path:
    encoded = item.get("b64_json")
    if not isinstance(encoded, str) or not encoded:
        fail("Image result is missing b64_json.")
    try:
        image_bytes = base64.b64decode(encoded)
    except (binascii.Error, ValueError) as exc:
        fail(f"Cannot decode b64 image: {exc}")
    output_path = output_dir / filename_for(index, fmt)
    try:
        output_path.write_bytes(image_bytes)
    except OSError as exc:
        fail(f"Cannot write image file: {exc}")
    return output_path


def save_url_image(item: dict[str, Any], output_dir: Path, index: int, fmt: str) -> Path:
    image_url = item.get("url")
    if not isinstance(image_url, str) or not image_url:
        fail("Image result is missing url.")
    suffix = suffix_from_url(image_url, fmt)
    output_path = output_dir / filename_for(index, suffix)
    request = urllib.request.Request(
        image_url,
        headers={
            "User-Agent": "oneclick-store-marketing/1.0",
            "Accept": "image/png,image/jpeg,image/webp,*/*",
        },
        method="GET",
    )
    last_error = ""
    for attempt in range(DEFAULT_RETRIES + 1):
        try:
            with urllib.request.urlopen(request, timeout=DEFAULT_TIMEOUT_SECONDS) as response:
                image_bytes = response.read()
                break
        except urllib.error.HTTPError as exc:
            fail(f"Image URL returned HTTP {exc.code}: {exc.reason}")
        except urllib.error.URLError as exc:
            last_error = f"Cannot download image URL: {exc.reason}"
        except http.client.RemoteDisconnected:
            last_error = "Image download connection closed."
        except TimeoutError:
            last_error = "Image download timed out."
        if attempt < DEFAULT_RETRIES:
            time.sleep(retry_delay(attempt))
    else:
        fail(f"{last_error} Retried {DEFAULT_RETRIES} times.")
    try:
        output_path.write_bytes(image_bytes)
    except OSError as exc:
        fail(f"Cannot write image file: {exc}")
    return output_path


def save_images(result: dict[str, Any], output_dir: Path, fmt: str) -> list[Path]:
    data = result.get("data")
    if not isinstance(data, list) or not data:
        fail("Image API response does not contain a non-empty data array.")
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            fail("Image API data item is not an object.")
        if item.get("b64_json"):
            paths.append(save_b64_image(item, output_dir, index, fmt))
        elif item.get("url"):
            paths.append(save_url_image(item, output_dir, index, fmt))
        else:
            fail("Image result has neither b64_json nor url.")
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate local-store marketing visuals or save executable prompts."
    )
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt", help="Prompt text to send or save.")
    prompt_group.add_argument("--prompt-file", help="UTF-8 text file containing the prompt.")
    parser.add_argument(
        "--mode",
        choices=("auto", "prompt", "image"),
        default="auto",
        help="auto generates images when config exists; otherwise saves prompts. prompt never calls the API. image requires config.",
    )
    parser.add_argument(
        "--job-dir",
        help="Campaign output root, for example generated-campaigns/guzi-launch-20260515-180000.",
    )
    parser.add_argument(
        "--asset-type",
        choices=tuple(ASSET_TYPE_DIRS),
        default="custom",
        help="Asset folder/type for the generated prompt or image.",
    )
    parser.add_argument(
        "--output-dir",
        default="generated-campaigns",
        help="Fallback output directory when --job-dir is not provided.",
    )
    parser.add_argument("--env-file", help="Optional .env file. Defaults to searching upward from cwd.")
    parser.add_argument("--size", default="1024x1024", help="Image size, default 1024x1024.")
    parser.add_argument("--quality", help="Optional image quality parameter, such as low, medium, or high.")
    parser.add_argument(
        "--format",
        choices=("png", "jpeg", "webp"),
        default="png",
        help="Desired output image format, default png.",
    )
    parser.add_argument("--n", type=int, default=1, help="Number of images to generate, default 1.")
    parser.add_argument("--image", help="Optional reference image path; uses /images/edits when provided.")
    args = parser.parse_args()
    if args.n < 1:
        fail("--n must be at least 1.")
    return args


def main() -> None:
    args = parse_args()
    env_file = Path(args.env_file) if args.env_file else find_default_env_file()
    load_env_file(env_file)
    prompt = read_prompt(args)
    config, missing = collect_config()
    effective_missing = missing_required_config(config, missing)
    if effective_missing and args.mode == "image":
        fail(f"image mode requires complete config. Missing: {format_missing_config(effective_missing)}")

    prompt_path = save_prompt(prompt, args)
    if args.mode == "prompt" or effective_missing:
        print_prompt_only(prompt, prompt_path, effective_missing if args.mode == "auto" else [])
        return

    base_url = config[ENV_BASE_URL].rstrip("/")
    model = config[ENV_MODEL]
    api_key = config.get(ENV_API_KEY, "")
    endpoint = image_endpoint(base_url, args)

    if is_pollinations_dev_url(base_url):
        image_url = pollinations_image_url(base_url, args, prompt, model)
        result = {"data": [{"url": image_url}]}
    elif args.image:
        body, boundary = build_multipart_body(args, prompt, model)
        result = post_multipart(endpoint, api_key, body, boundary)
    else:
        result = post_json(endpoint, api_key, build_payload(args, prompt, model))

    paths = save_images(result, resolve_output_dir(args), args.format)
    print("Image generation complete.")
    if prompt_path:
        print(f"Prompt saved: {prompt_path}")
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
