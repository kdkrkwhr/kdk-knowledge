"""Copy the Graphify build into docs/graph/ so the wiki build can read it from git.

Run after `/graphify docs/wiki` (or `--update`). graphify-out/ is ignored by git;
docs/graph/graph.json is the committed input for scripts/build_wiki.py.
"""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "graphify-out"
CACHE = ROOT / "docs/wiki/graphify-out/cache/semantic"
TARGET = ROOT / "docs/graph"


def rationale_from_cache() -> dict[str, str]:
    """The graph build drops node attributes; the semantic cache still has `rationale`."""
    found = {}
    for path in CACHE.rglob("*.json") if CACHE.exists() else []:
        for node in json.loads(path.read_text(encoding="utf-8")).get("nodes", []):
            if node.get("rationale"):
                found[node["id"]] = node["rationale"]
    return found


def main() -> None:
    graph = json.loads((OUT / "graph.json").read_text(encoding="utf-8"))
    previous = TARGET / "graph.json"
    rationale = {}
    if previous.exists():
        rationale = {n["id"]: n["rationale"] for n in json.loads(previous.read_text(encoding="utf-8"))["nodes"]
                     if n.get("rationale")}
    rationale.update(rationale_from_cache())
    for node in graph["nodes"]:
        if node["id"] in rationale:
            node["rationale"] = rationale[node["id"]]
    labels = OUT / ".graphify_labels.json"
    if labels.exists():
        graph["community_labels"] = json.loads(labels.read_text(encoding="utf-8"))
    TARGET.mkdir(exist_ok=True)
    (TARGET / "graph.json").write_text(json.dumps(graph, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if (OUT / "GRAPH_REPORT.md").exists():
        shutil.copy(OUT / "GRAPH_REPORT.md", TARGET / "GRAPH_REPORT.md")
    kept = sum(1 for n in graph["nodes"] if n.get("rationale"))
    print(f"docs/graph/graph.json: {len(graph['nodes'])} nodes, {len(graph['links'])} links, rationale on {kept}")


if __name__ == "__main__":
    main()
