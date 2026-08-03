import argparse
import json
import re
from pathlib import Path


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".heic", ".webp", ".gif", ".tif", ".tiff"}


def story_documents(root: Path):
    for path in root.rglob("*.docx"):
        lowered = path.name.lower()
        if "__macosx" in {part.lower() for part in path.parts} or path.name.startswith("~$"):
            continue
        if re.search(r"complete[ _-]*story|project[ _-]*complete", lowered):
            yield path.resolve()


def normalized_key(path: Path):
    return path.name.lower()


def main():
    parser = argparse.ArgumentParser(description="Refresh a lightweight project routing catalog.")
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--catalog", type=Path, default=Path(".agents/resume-tailor-project-catalog.json"))
    args = parser.parse_args()
    root = args.workspace.resolve()
    catalog_path = args.catalog if args.catalog.is_absolute() else root / args.catalog

    existing = {"version": 1, "projects": []}
    if catalog_path.exists():
        existing = json.loads(catalog_path.read_text(encoding="utf-8"))
    by_name = {
        normalized_key(Path(item["source_document_path"])): item
        for item in existing.get("projects", [])
    }

    refreshed = []
    for source in sorted(story_documents(root)):
        key = normalized_key(source)
        item = dict(by_name.get(key, {}))
        item.setdefault("project_name", re.sub(r"(?i)[ _-]*(project[ _-]*)?complete[ _-]*story", "", source.stem).strip(" _-"))
        item.setdefault("employer_or_experience", "")
        item["source_document_path"] = source.relative_to(root).as_posix()
        item.setdefault("broad_project_themes", [])
        item.setdefault("relevant_role_families", [])
        images = []
        image_dir = source.parent / "images"
        if image_dir.exists():
            images = sorted({p.suffix.lower().lstrip(".") for p in image_dir.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS})
        item.setdefault("supporting_image_types", images)
        refreshed.append(item)

    output = {"version": 1, "projects": refreshed}
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    catalog_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Catalog refreshed: {len(refreshed)} projects")


if __name__ == "__main__":
    main()
