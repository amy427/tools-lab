import argparse
from pathlib import Path

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Batch Renamer: rename files in a folder by rule.")
    p.add_argument("folder", help="Target folder path")
    p.add_argument("--prefix", default="img_", help="New filename prefix")
    p.add_argument("--start", type=int, default=1, help="Start index")
    p.add_argument("--only-images", action="store_true", help="Rename only images")
    p.add_argument("--dry-run", action="store_true", help="Preview without renaming")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    folder = Path(args.folder).expanduser()

    if not folder.exists() or not folder.is_dir():
        raise SystemExit(f"[ERROR] Folder not found or not a directory: {folder}")

    files = sorted([p for p in folder.iterdir() if p.is_file()])

    idx = args.start
    planned = []

    for p in files:
        ext = p.suffix.lower()
        if args.only_images and ext not in IMAGE_EXTS:
            continue

        new_name = f"{args.prefix}{idx}{ext}"
        new_path = p.with_name(new_name)

        if new_path.exists():
            raise SystemExit(f"[ERROR] Target exists, stop to avoid overwrite: {new_path}")

        planned.append((p, new_path))
        idx += 1

    if not planned:
        print("[INFO] No files matched. Nothing to do.")
        return

    for old, new in planned:
        print(f"{old.name}  ->  {new.name}")

    if args.dry_run:
        print("[INFO] Dry-run mode. No files renamed.")
        return

    for old, new in planned:
        old.rename(new)

    print(f"[OK] Renamed {len(planned)} file(s).")


if __name__ == "__main__":
    main()
