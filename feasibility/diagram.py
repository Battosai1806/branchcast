"""Convert a diagram image into editable shape data using the OpenAI Responses API."""
import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

SHAPE = {"type": "object", "properties": {"type": {"type": "string", "enum": ["rectangle", "ellipse", "diamond", "arrow"]}, "label": {"type": "string"}, "x": {"type": "number"}, "y": {"type": "number"}, "width": {"type": "number"}, "height": {"type": "number"}}, "required": ["type", "label", "x", "y", "width", "height"], "additionalProperties": False}
SCHEMA = {"type": "object", "properties": {"shapes": {"type": "array", "items": SHAPE}}, "required": ["shapes"], "additionalProperties": False}

def convert(path, api_key, model="gpt-4o-mini"):
    mime = mimetypes.guess_type(str(path))[0]
    if mime not in {"image/png", "image/jpeg", "image/webp", "image/gif"}:
        raise ValueError("Use a PNG, JPEG, WebP, or GIF image.")
    data = Path(path).read_bytes()
    if len(data) > 10 * 1024 * 1024:
        raise ValueError("Image must be 10 MB or smaller.")
    image = base64.b64encode(data).decode("ascii")
    body = {"model": model, "store": False, "input": [{"role": "user", "content": [{"type": "input_text", "text": "Convert this rough diagram into editable shapes. Preserve labels and approximate layout. Coordinates and sizes are percentages of the image from 0 to 100. Use rectangle, ellipse, diamond, or arrow. Return an empty array if there is no diagram."}, {"type": "input_image", "image_url": f"data:{mime};base64,{image}"}]}], "text": {"format": {"type": "json_schema", "name": "diagram", "strict": True, "schema": SCHEMA}}}
    request = urllib.request.Request("https://api.openai.com/v1/responses", data=json.dumps(body).encode(), headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=90) as response:
        result = json.load(response)
    for item in result.get("output", []):
        for part in item.get("content", []):
            if part.get("type") == "refusal":
                raise ValueError("The model declined this image.")
            if part.get("type") == "output_text":
                diagram = json.loads(part["text"])
                validate(diagram)
                return diagram
    raise ValueError("The model returned no diagram output; check for an incomplete response.")

def validate(diagram):
    if not isinstance(diagram, dict) or set(diagram) != {"shapes"} or not isinstance(diagram["shapes"], list):
        raise ValueError("Invalid diagram response.")
    for shape in diagram["shapes"]:
        if not isinstance(shape, dict) or set(shape) != {"type", "label", "x", "y", "width", "height"} or shape["type"] not in {"rectangle", "ellipse", "diamond", "arrow"} or not isinstance(shape["label"], str):
            raise ValueError("Invalid shape response.")
        for key in ("x", "y", "width", "height"):
            if isinstance(shape[key], bool) or not isinstance(shape[key], (int, float)) or not 0 <= shape[key] <= 100:
                raise ValueError(f"Invalid shape {key}; expected a percentage from 0 to 100.")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--output", type=Path, default=Path("diagram.json"))
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    args = parser.parse_args()
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        parser.error("Set OPENAI_API_KEY in your environment; do not commit it.")
    try:
        result = convert(args.image, key, args.model)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"Saved {len(result['shapes'])} editable shapes to {args.output}.")
    except (OSError, ValueError, urllib.error.URLError) as exc:
        print(f"Diagram conversion failed: {exc}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
