"""Normalize model references, prepare internal previews and crop samples. Requires Pillow."""

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


def read_image(path):
    with Image.open(path) as source:
        return ImageOps.exif_transpose(source).convert("RGBA")


def writable_targets(out, names):
    out.mkdir(parents=True, exist_ok=True)
    targets = [out / name for name in names]
    for target in targets:
        if target.exists():
            raise ValueError(f"Output exists; choose a new directory: {target}")
    return targets


def prepare_references(paths, out, extras=()):
    targets = writable_targets(out, ["manifest.json", *extras] + [f"reference-{i:02d}.png" for i in range(1, len(paths) + 1)])
    images, manifest = [], []
    for index, (path, target) in enumerate(zip(paths, targets[1 + len(extras):]), 1):
        original = read_image(path)
        width, height = original.size
        transparent = original.getchannel("A").getextrema()[0] < 255
        image = Image.new("RGBA", original.size, (255, 255, 255, 255))
        image.alpha_composite(original)
        image = image.convert("RGB")
        image.thumbnail((4096, 4096), Image.Resampling.LANCZOS)
        image.save(target)
        divisor = math.gcd(width, height)
        manifest.append({
            "id": index, "sourcePath": str(path.resolve()), "path": str(target.resolve()),
            "sourceWidth": width, "sourceHeight": height,
            "width": image.width, "height": image.height,
            "sourceRatio": f"{width // divisor}:{height // divisor}",
            "whiteBackgroundApplied": transparent, "resized": image.size != original.size,
        })
        images.append(image)
    targets[0].write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return images


def preprocess(args):
    prepare_references(args.images, args.out)
    print(json.dumps({"manifest": str((args.out / "manifest.json").resolve())}))


def sample_plan(count):
    if not 1 <= count <= 12:
        raise ValueError("Sample planning supports 1–12 images; initial task input requires 2–12.")
    sizes = [count] if count <= 6 else [count // 2, count - count // 2]
    groups, start = [], 1
    for group_id, size in enumerate(sizes, 1):
        columns = 1 if size == 1 else 2 if size <= 4 else 3
        groups.append({
            "groupId": group_id,
            "imageIds": list(range(start, start + size)),
            "suggestedGrid": {"columns": columns, "rows": math.ceil(size / columns)},
        })
        start += size
    return {"maxInFlight": 6, "groups": groups}


def prepare(args):
    plan = sample_plan(len(args.images))
    images = prepare_references(args.images, args.out, ("contact-sheet.png", "sample-plan.json"))
    sheet_path, manifest_path = args.out / "contact-sheet.png", args.out / "manifest.json"
    columns = min(3, len(images))
    sheet = Image.new("RGB", (columns * 360, math.ceil(len(images) / columns) * 304), "#e8e8e8")
    draw = ImageDraw.Draw(sheet)
    for index, image in enumerate(images, 1):
        width, height = image.size
        thumb = ImageOps.contain(image, (344, 264), Image.Resampling.LANCZOS)
        left = ((index - 1) % columns) * 360
        top = ((index - 1) // columns) * 304
        draw.text((left + 10, top + 8), f"{index}  |  {width} x {height}", fill="black")
        sheet.paste(thumb, (left + (360 - thumb.width) // 2, top + 32 + (264 - thumb.height) // 2))
    sheet.save(sheet_path)
    plan_path = args.out / "sample-plan.json"
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"sheet": str(sheet_path.resolve()), "manifest": str(manifest_path.resolve()), "samplePlan": str(plan_path.resolve())}, ensure_ascii=False))


def crop(args):
    image = read_image(args.image)
    entries = json.loads(args.boxes.read_text(encoding="utf-8-sig"))
    if not isinstance(entries, list) or not 1 <= len(entries) <= 6:
        raise ValueError("Boxes must be a list containing 1–6 regions.")
    ids = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Each region must contain id and box.")
        number, box = entry.get("id"), entry.get("box")
        if type(number) is not int or not 1 <= number <= 12 or number in ids:
            raise ValueError("Region IDs must be unique global image IDs from 1 to 12.")
        ids.add(number)
        if not isinstance(box, list) or len(box) != 4 or any(type(v) is not int for v in box):
            raise ValueError("Each box must contain four integer pixel coordinates.")
        left, top, right, bottom = box
        if not (0 <= left < right <= image.width and 0 <= top < bottom <= image.height):
            raise ValueError(f"Region {number} lies outside the image or has no area.")
    targets = writable_targets(args.out, [f"{entry['id']:02d}.png" for entry in entries])
    results = []
    for entry, target in zip(entries, targets):
        region = image.crop(entry["box"])
        region.save(target)
        results.append({"id": entry["id"], "path": str(target.resolve()), "size": list(region.size)})
    print(json.dumps(results, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    normalize = commands.add_parser("preprocess", help="White RGB references, max edge 4096; never upscale.")
    normalize.add_argument("--out", type=Path, required=True)
    normalize.add_argument("images", type=Path, nargs="+")
    normalize.set_defaults(run=preprocess)
    prep = commands.add_parser("prepare")
    prep.add_argument("--out", type=Path, required=True)
    prep.add_argument("images", type=Path, nargs="+")
    prep.set_defaults(run=prepare)
    cut = commands.add_parser("crop")
    cut.add_argument("--image", type=Path, required=True)
    cut.add_argument("--boxes", type=Path, required=True)
    cut.add_argument("--out", type=Path, required=True)
    cut.set_defaults(run=crop)
    args = parser.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
