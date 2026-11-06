#!/usr/bin/env python3
"""Generate a PNG with OpenAI Image 2.6; Python standard library only."""
import argparse
import base64
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--prompt")
    source.add_argument("--prompt-file", type=Path)
    parser.add_argument("--model", choices=["gpt-image-2.6-sunburst", "gpt-image-2.6-flare"],
                        default="gpt-image-2.6-sunburst")
    parser.add_argument("--quality", choices=["auto", "low", "medium", "high"], default="auto")
    parser.add_argument("--output", type=Path, default=Path("outputs/image.png"))
    parser.add_argument("--dry-run", action="store_true", help="Print request without API call or key")
    args = parser.parse_args()
    try:
        prompt = args.prompt if args.prompt is not None else args.prompt_file.read_text(encoding="utf-8")
        if not prompt.strip():
            parser.error("Prompt must not be empty.")
        payload = dict(model=args.model, prompt=prompt, quality=args.quality,
                       n=1, output_format="png")
        if args.dry_run:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0
        if args.output.exists():
            parser.error("Output already exists. Choose a different --output path.")
        key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not key:
            parser.error("Set OPENAI_API_KEY in the execution environment. Do not commit the key.")
        request = urllib.request.Request(
            "https://api.openai.com/v1/images/generations",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
            method="POST")
        with urllib.request.urlopen(request, timeout=300) as response:
            result = json.load(response)
        encoded = result["data"][0]["b64_json"]
        image = base64.b64decode(encoded, validate=True)
        if not image.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("API response is not a PNG image.")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("xb") as output:
            output.write(image)
        print("Saved: " + str(args.output))
        return 0
    except urllib.error.HTTPError as error:
        print(f"API request failed (HTTP {error.code}). Check model access, billing and rate limits.", file=sys.stderr)
    except urllib.error.URLError:
        print("Could not reach api.openai.com. Check Cloud network access.", file=sys.stderr)
    except (OSError, ValueError, KeyError, IndexError, TypeError):
        print("Could not read the prompt, decode the API result, or save the image.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
