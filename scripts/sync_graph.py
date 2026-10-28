"""Copy the Graphify build into docs/graph/ and publish the viewer at site/graph/.

Run after `/graphify docs/wiki` (or `--update`) and `graphify export html`. graphify-out/ is
ignored by git; docs/graph/graph.json is the committed input for scripts/build_wiki.py and
site/graph/index.html is the committed viewer (graphify's graph.html plus the MPX-style panel:
extracted summary, source document, open/preview, Korean relation tags, ?node= deep link).
"""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "graphify-out"
CACHE = ROOT / "docs/wiki/graphify-out/cache/semantic"
TARGET = ROOT / "docs/graph"

PANEL_JS = r"""
const KG_EXTRA = __EXTRA__;
const KG_REL = {references:'참조', implements:'구현', calls:'호출', cites:'인용', conceptually_related_to:'개념 연관',
  shares_data_with:'데이터 공유', semantically_similar_to:'유사 구조', rationale_for:'설계 근거'};
const KG_CONF = {EXTRACTED:'원문', INFERRED:'추론', AMBIGUOUS:'불확실'};
const KG_TYPE = {document:'문서', concept:'개념', rationale:'설계 개념', code:'코드 구성요소'};
function kgPreview(url) {
  document.getElementById('kg-frame').src = url;
  document.getElementById('kg-open').href = url;
  document.getElementById('kg-modal').style.display = 'flex';
}
function kgClose() { document.getElementById('kg-modal').style.display = 'none'; document.getElementById('kg-frame').src = 'about:blank'; }
function showInfo(nodeId) {
  const n = nodesDS.get(nodeId);
  if (!n) return;
  const x = KG_EXTRA[nodeId] || {};
  let h = `<div class="field"><b style="font-size:14px">${esc(n.label)}</b></div>`;
  h += `<div class="field">${esc(KG_TYPE[n.file_type] || n.file_type || '')} · ${esc(n.community_name || '')}</div>`;
  if (x.r) h += `<div class="field" style="margin-top:6px;padding:8px;border-left:3px solid #4E9F8F;background:rgba(78,159,143,.12);border-radius:4px"><div style="font-size:11px;opacity:.75">추출 요약 (자동)</div>${esc(x.r)}</div>`;
  if (x.h) {
    h += `<div class="field" style="margin-top:6px">${nodeId.startsWith('concept_') ? '처음 언급' : '출처'}: ${esc(x.t || '')}</div>`;
    h += `<div class="field" style="display:flex;gap:6px;margin-top:4px">`
       + `<a href="${esc(x.h)}" style="padding:4px 10px;border-radius:6px;background:#4E9F8F;color:#fff;text-decoration:none;font-size:12px">위키 열기</a>`
       + `<button data-preview="${esc(x.h)}" style="padding:4px 10px;border-radius:6px;border:1px solid #4E9F8F;background:transparent;color:inherit;font-size:12px;cursor:pointer">미리보기</button></div>`;
  }
  const edgeIds = network.getConnectedEdges(nodeId);
  const items = edgeIds.map(eid => {
    const e = edgesDS.get(eid); const other = e.from === nodeId ? e.to : e.from; const nb = nodesDS.get(other);
    const m = /^(\S+)\s*\[(\w+)\]/.exec(e.title || '') || [];
    const tag = `${KG_REL[m[1]] || m[1] || ''}${m[2] ? ' · ' + (KG_CONF[m[2]] || m[2]) : ''}`;
    const color = nb ? nb.color.background : '#555';
    return `<span class="neighbor-link" style="border-left-color:${esc(color)}" data-nid="${esc(other)}">${esc(nb ? nb.label : other)} <small style="opacity:.6">${esc(tag)}</small></span>`;
  }).join('');
  if (items) h += `<div class="field" style="margin-top:8px;color:var(--text-2);font-size:11px">연결 (${edgeIds.length})</div><div id="neighbors-list">${items}</div>`;
  document.getElementById('info-content').innerHTML = h;
}
document.addEventListener('click', ev => { const b = ev.target.closest('[data-preview]'); if (b) kgPreview(b.getAttribute('data-preview')); });
(function () {
  const wanted = new URLSearchParams(location.search).get('node');
  if (wanted && nodesDS.get(wanted)) network.once('stabilizationIterationsDone', () => setTimeout(() => focusNode(wanted), 50));
})();
"""
MODAL = """<div id="kg-modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:9999;align-items:center;justify-content:center" onclick="if(event.target===this)kgClose()">
<div style="width:min(1200px,92vw);height:88vh;background:#fff;border-radius:10px;display:flex;flex-direction:column;overflow:hidden">
<div style="display:flex;justify-content:flex-end;gap:8px;padding:6px 10px;background:#1E2A30"><a id="kg-open" target="_blank" style="color:#fff;font-size:13px">새 탭으로 열기</a><button onclick="kgClose()" style="font-size:13px">닫기 ✕</button></div>
<iframe id="kg-frame" style="flex:1;border:0;width:100%"></iframe></div></div>
"""
TOPBAR = ('<div style="padding:10px 12px;border-bottom:1px solid var(--border);font-size:13px">'
          '<a href="../" style="color:#4E9F8F;text-decoration:none;font-weight:600;white-space:nowrap">← 위키 목차</a>'
          '<div style="color:var(--muted);font-size:11px;margin-top:3px">노드를 누르면 추출 요약·출처·연결이 보입니다</div></div>')


def rationale_from_cache() -> dict[str, str]:
    """The graph build drops node attributes; the semantic cache still has `rationale`."""
    found = {}
    for path in CACHE.rglob("*.json") if CACHE.exists() else []:
        for node in json.loads(path.read_text(encoding="utf-8")).get("nodes", []):
            if node.get("rationale"):
                found[node["id"]] = node["rationale"]
    return found


def patch_viewer(graph) -> None:
    viewer = OUT / "graph.html"  # from `graphify export html`
    if not viewer.exists():
        return
    extra = {}
    for node in graph["nodes"]:
        source = node.get("source_file") or ""
        stem = source[:-3] if source.endswith(".md") else source
        item = {key: value for key, value in (("r", node.get("rationale")), ("h", f"../wiki/{stem}.html" if stem else None),
                                              ("t", stem)) if value}
        if item:
            extra[node["id"]] = item
    page = viewer.read_text(encoding="utf-8").replace('<html lang="en">', '<html lang="ko">', 1)
    page = page.replace("<title>graphify - graphify-out/graph.html</title>", "<title>지식 그래프 · kdk knowledge</title>", 1)
    page = page.replace('placeholder="Search nodes..."', 'placeholder="노드 검색 (문서·개념·설계)"', 1)
    page = page.replace("<h3>Node Info</h3>", "<h3>노드 정보</h3>", 1).replace("<h3>Communities</h3>", "<h3>주제 (커뮤니티)</h3>", 1)
    page = page.replace('<span class="empty">Click a node to inspect it</span>', '<span class="empty">노드를 누르면 여기에 나옵니다</span>')
    a = page.index("function showInfo(nodeId)")
    b = page.index("function focusNode", a)
    page = page[:a] + PANEL_JS.replace("__EXTRA__", json.dumps(extra, ensure_ascii=False).replace("</", "<\\/")) + "\n" + page[b:]
    page = page.replace('<div id="sidebar">', '<div id="sidebar">' + TOPBAR, 1)
    i = page.rindex("</body>")
    page = page[:i] + MODAL + page[i:]
    (ROOT / "site/graph").mkdir(exist_ok=True)
    (ROOT / "site/graph/index.html").write_text(page, encoding="utf-8")


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
    patch_viewer(graph)
    kept = sum(1 for n in graph["nodes"] if n.get("rationale"))
    print(f"docs/graph/graph.json: {len(graph['nodes'])} nodes, {len(graph['links'])} links, rationale on {kept}")


if __name__ == "__main__":
    main()
