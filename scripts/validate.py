"""Validate the public snapshot before upload to GitHub Pages."""

import json
import re
import sys
from pathlib import Path


ALLOWED_SITE_FILES = {
    "index.html", "style.css", "wiki.js", "knowledge.json",
    "architecture/index.html", "architecture/map.js",
}
SHA = re.compile(r"^[0-9a-f]{40}$")
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
LOCAL_PATH = re.compile(r"/Users/|/home/|[A-Z]:\\\\Users\\", re.I)


def validate(root: Path) -> list:
    site = root / "site"
    errors = []
    actual = {str(path.relative_to(site)) for path in site.rglob("*") if path.is_file()}
    for name in sorted(actual - ALLOWED_SITE_FILES):
        errors.append(f"Unexpected public file: {name}")
    for name in sorted(ALLOWED_SITE_FILES - actual):
        errors.append(f"Missing public file: {name}")
    for path in site.rglob("*"):
        if path.is_symlink():
            errors.append(f"Public symlink: {path.relative_to(site)}")
        elif path.is_file() and path.suffix in {".html", ".css", ".js", ".json"}:
            content = path.read_text(encoding="utf-8")
            if EMAIL.search(content):
                errors.append(f"Public email address in {path.relative_to(site)}")
            if LOCAL_PATH.search(content):
                errors.append(f"Public local path in {path.relative_to(site)}")
    try:
        data = json.loads((site / "knowledge.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return errors + [f"Invalid knowledge.json: {error}"]
    if data.get("analysis", {}).get("status") != "not-run":
        errors.append("Analysis status must remain not-run until verified extraction is added")
    if data.get("analysis", {}).get("revision") is not None:
        errors.append("No Graphify revision can be claimed before extraction")
    sources = {}
    for source in data.get("sources", []):
        sid = source.get("id")
        if not sid or sid in sources:
            errors.append(f"Duplicate or missing source id: {sid}")
        sources[sid] = source
        revision = source.get("revision", "")
        if not SHA.fullmatch(revision):
            errors.append(f"Source {sid} needs a full revision SHA")
        if source.get("visibility") != "public":
            errors.append(f"Source {sid} must be public")
        if source.get("kind") not in {"readme", "code", "criteria"}:
            errors.append(f"Source {sid} needs a supported kind")
        expected = "https://github.com/{}/blob/{}/{}".format(
            source.get("repository"), revision, source.get("path"))
        if source.get("url") != expected:
            errors.append(f"Source {sid} URL must pin repository/path/revision")
    page = (site / "index.html").read_text(encoding="utf-8")
    registered_urls = {source.get("url") for source in sources.values()}
    for url in re.findall(r'href="([^"]+)"', page):
        if url.startswith("https://github.com/kdkrkwhr/") and "/blob/" in url and url not in registered_urls:
            errors.append(f"Unregistered source link: {url}")
    entities = {}
    for entity in data.get("entities", []):
        eid = entity.get("id")
        if not eid or eid in entities:
            errors.append(f"Duplicate or missing entity id: {eid}")
        entities[eid] = entity
        for sid in entity.get("evidence", []):
            if sid not in sources:
                errors.append(f"Entity {eid} has missing evidence {sid}")
    relations = set()
    for relation in data.get("relations", []):
        rid = relation.get("id")
        if not rid or rid in relations:
            errors.append(f"Duplicate or missing relation id: {rid}")
        relations.add(rid)
        if relation.get("origin") != "curated":
            errors.append(f"Relation {rid} must be marked curated")
        for endpoint in ("from", "to"):
            if relation.get(endpoint) not in entities:
                errors.append(f"Relation {rid} has missing {endpoint} entity")
        if not relation.get("evidence"):
            errors.append(f"Relation {rid} needs evidence")
        for sid in relation.get("evidence", []):
            if sid not in sources:
                errors.append(f"Relation {rid} has missing evidence {sid}")
    return errors


if __name__ == "__main__":
    failures = validate(Path(__file__).resolve().parents[1])
    if failures:
        print("\n".join(failures), file=sys.stderr)
        raise SystemExit(1)
    print("Public snapshot validation passed")
