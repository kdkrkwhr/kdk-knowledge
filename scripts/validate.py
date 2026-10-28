"""Validate the public snapshot before upload to GitHub Pages."""

import json
import re
import sys
from pathlib import Path


STATIC_SITE_FILES = {
    "index.html", "style.css", "wiki.js", "knowledge.json", "search-index.json",
    "architecture/index.html", "architecture/map.js", "wiki/topics.html",
}
SHA = re.compile(r"^[0-9a-f]{40}$")
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
LOCAL_PATH = re.compile(r"/Users/|/home/|[A-Z]:\\\\Users\\", re.I)


def validate(root: Path) -> list:
    site = root / "site"
    errors = []
    names = {path.stem for path in (site / "wiki/markdown").glob("*.md")}
    allowed = STATIC_SITE_FILES | {f"wiki/{name}.html" for name in names} | {
        f"wiki/markdown/{name}.md" for name in names}
    actual = {path.relative_to(site).as_posix() for path in site.rglob("*") if path.is_file()}
    for name in sorted(actual - allowed):
        errors.append(f"Unexpected public file: {name}")
    for name in sorted(allowed - actual):
        errors.append(f"Missing public file: {name}")
    if not names:
        errors.append("Missing wiki Markdown documents")
    for path in site.rglob("*"):
        if path.is_symlink():
            errors.append(f"Public symlink: {path.relative_to(site)}")
        elif path.is_file() and path.suffix in {".html", ".css", ".js", ".json", ".md"}:
            content = path.read_text(encoding="utf-8")
            if EMAIL.search(content):
                errors.append(f"Public email address in {path.relative_to(site)}")
            if LOCAL_PATH.search(content):
                errors.append(f"Public local path in {path.relative_to(site)}")
    try:
        data = json.loads((site / "knowledge.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return errors + [f"Invalid knowledge.json: {error}"]
    analysis = data.get("analysis", {})
    if analysis.get("status") not in {"not-run", "run"}:
        errors.append("Analysis status must be not-run or run")
    if analysis.get("status") == "run" and not SHA.fullmatch(analysis.get("revision") or ""):
        errors.append("A Graphify run must name the full commit it was built at")
    if analysis.get("status") == "not-run" and analysis.get("revision") is not None:
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
    for path in [site / "index.html", *(site / "wiki").glob("*.html")]:
        for url in re.findall(r'href="([^"]+)"', path.read_text(encoding="utf-8")):
            if url.startswith("https://github.com/kdkrkwhr/") and "/blob/" in url and url not in registered_urls:
                errors.append(f"Unregistered source link: {url}")
    entities = {}
    for entity in data.get("entities", []):
        eid = entity.get("id")
        if not eid or eid in entities:
            errors.append(f"Duplicate or missing entity id: {eid}")
        entities[eid] = entity
        if entity.get("document") and entity["document"] not in actual:
            errors.append(f"Entity {eid} has missing wiki document")
        for sid in entity.get("evidence", []):
            if sid not in sources:
                errors.append(f"Entity {eid} has missing evidence {sid}")
    relations = set()
    for relation in data.get("relations", []):
        rid = relation.get("id")
        if not rid or rid in relations:
            errors.append(f"Duplicate or missing relation id: {rid}")
        relations.add(rid)
        if relation.get("origin") not in {"curated", "extracted"}:
            errors.append(f"Relation {rid} must be marked curated or extracted")
        if relation.get("origin") == "extracted" and (
                relation.get("confidence") not in {"EXTRACTED", "INFERRED", "AMBIGUOUS"}
                or not isinstance(relation.get("score"), (int, float))):
            errors.append(f"Extracted relation {rid} needs a confidence label and score")
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
