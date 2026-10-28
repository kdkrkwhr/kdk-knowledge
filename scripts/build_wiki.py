"""Build the public wiki from reviewed Markdown, using only Python's standard library."""

import argparse
import html
import json
import re
from pathlib import Path


INLINE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)|`([^`]+)`|\*\*([^*]+)\*\*")
HEADING = re.compile(r"^(#{1,3}) (.+)$")
LIST = re.compile(r"^(\d+\. |[-*] )(.+)$")
PUBLIC_BLOB = re.compile(r"https://github\.com/kdkrkwhr/[^\s)]+/blob/[^\s)]+")


def read_document(path):
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---\n"):
        raise ValueError(f"missing wiki metadata: {path.name}")
    try:
        metadata, body = raw[4:].split("\n---\n", 1)
        meta = json.loads(metadata)
    except (ValueError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid wiki metadata: {path.name}") from error
    return meta, body.strip() + "\n", raw


def render_inline(value, doc_names, source_urls):
    result = []
    start = 0
    for match in INLINE.finditer(value):
        result.append(html.escape(value[start:match.start()]))
        label, target, code, bold = match.groups()
        if target is not None:
            if target.startswith("https://github.com/kdkrkwhr/") and "/blob/" in target:
                if target not in source_urls:
                    raise ValueError(f"unregistered source: {target}")
            elif target.endswith(".md"):
                if target not in doc_names:
                    raise ValueError(f"broken wiki link: {target}")
                target = target[:-3] + ".html"
            elif not target.startswith("https://") and not target.startswith("#"):
                raise ValueError(f"unsupported wiki link: {target}")
            result.append(f'<a href="{html.escape(target, quote=True)}">{html.escape(label)}</a>')
        elif code is not None:
            result.append(f"<code>{html.escape(code)}</code>")
        else:
            result.append(f"<strong>{html.escape(bold)}</strong>")
        start = match.end()
    result.append(html.escape(value[start:]))
    return "".join(result)


def render_markdown(body, doc_names, source_urls):
    lines = body.splitlines()
    output, toc, plain = [], [], []
    paragraph = []
    list_kind = None
    code_lines = None
    heading_count = 0

    def flush_paragraph():
        if paragraph:
            output.append("<p>" + render_inline(" ".join(paragraph), doc_names, source_urls) + "</p>")
            paragraph.clear()

    def close_list():
        nonlocal list_kind
        if list_kind:
            output.append(f"</{list_kind}>")
            list_kind = None

    for line in lines + [""]:
        plain.append(line)
        if code_lines is not None:
            if line.startswith("```"):
                output.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines = None
            else:
                code_lines.append(line)
            continue
        if line.startswith("```"):
            flush_paragraph()
            close_list()
            code_lines = []
            continue
        heading = HEADING.match(line)
        if heading:
            flush_paragraph()
            close_list()
            level, title = len(heading[1]), heading[2]
            heading_count += 1
            anchor = f"section-{heading_count}"
            output.append(f'<h{level} id="{anchor}">{render_inline(title, doc_names, source_urls)}</h{level}>')
            if level > 1:
                toc.append((anchor, title))
            continue
        listing = LIST.match(line)
        if listing:
            flush_paragraph()
            kind = "ol" if listing[1][0].isdigit() else "ul"
            if list_kind != kind:
                close_list()
                output.append(f"<{kind}>")
                list_kind = kind
            output.append("<li>" + render_inline(listing[2], doc_names, source_urls) + "</li>")
            continue
        if not line.strip():
            flush_paragraph()
            close_list()
        else:
            if line.lstrip().startswith("<"):
                raise ValueError("raw HTML is not supported in wiki Markdown")
            close_list()
            paragraph.append(line.strip())
    if code_lines is not None:
        raise ValueError("unclosed code block")
    return "\n".join(output), toc, "\n".join(plain)


RELATION_LABELS = {"references": "참조", "implements": "구현", "cites": "인용", "calls": "호출",
                   "conceptually_related_to": "개념 연관", "shares_data_with": "데이터 공유",
                   "semantically_similar_to": "유사 구조", "rationale_for": "설계 근거"}
ENTITY_TYPES = {"concept": "concept", "rationale": "design"}
KIND_NAMES = {"project": "프로젝트", "resource": "공개 자료", "reference": "Fork / 참조", "criteria": "참고 기준",
              "technology": "기술", "implementation": "구현", "guide": "안내"}
GUIDE_GROUP = "안내·기준"
UPDATED = "2026-10-28"


def load_graph(root: Path):
    path = root / "docs/graph/graph.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def graph_layer(graph, documents):
    """Fold Graphify nodes onto wiki documents: concept/rationale nodes become entities,
    document/code nodes collapse into the document they came from."""
    doc_meta = {f"{meta['id']}.md": meta for meta, _, _ in documents}
    titles = {meta["id"]: body.splitlines()[0].removeprefix("# ") for meta, body, _ in documents}
    sources = {meta["id"]: meta["sources"] for meta, _, _ in documents}
    nodes = {node["id"]: node for node in graph["nodes"]}

    def owner(node):
        return doc_meta.get(node["source_file"], {}).get("id")

    def fold(node_id):
        node = nodes[node_id]
        return node_id if node["file_type"] in ENTITY_TYPES else owner(node)

    mentions = {node["id"]: set() for node in graph["nodes"] if node["file_type"] in ENTITY_TYPES}
    for node in graph["nodes"]:
        if node["id"] in mentions and owner(node):
            mentions[node["id"]].add(owner(node))
    relations = {}
    for edge in graph["links"]:
        a, b = fold(edge["source"]), fold(edge["target"])
        if not a or not b or a == b:
            continue
        for x, y in ((a, b), (b, a)):
            if x in mentions and y in sources:
                mentions[x].add(y)
        key = (a, b, edge["relation"])
        if key in relations:
            continue
        doc = doc_meta.get(edge["source_file"], {}).get("id")
        relations[key] = {"id": f"x-{len(relations) + 1}", "from": a, "to": b,
                          "label": RELATION_LABELS.get(edge["relation"], edge["relation"]),
                          "origin": "extracted", "confidence": edge["confidence"],
                          "score": edge["confidence_score"], "evidence": sources.get(doc, []),
                          "document": f"wiki/{doc}.html" if doc else None}
    entities = []
    for node in graph["nodes"]:
        if node["file_type"] not in ENTITY_TYPES:
            continue
        docs = sorted(mentions[node["id"]])
        entities.append({"id": node["id"], "type": ENTITY_TYPES[node["file_type"]], "title": node["label"],
                         "summary": node.get("rationale", ""), "origin": "extracted",
                         "community": node.get("community_name", ""),
                         "evidence": sorted({sid for doc in docs for sid in sources[doc]}),
                         "documents": [f"wiki/{doc}.html" for doc in docs]})
    doc_community = {}
    for node in graph["nodes"]:
        doc = owner(node)
        if node["file_type"] == "document" and doc and node["id"].startswith(re.sub(r"[^a-z0-9]", "_", doc.lower())):
            doc_community[doc] = node.get("community", 0)
    labels = {int(k): v for k, v in graph.get("community_labels", {}).items()}
    return {"entities": entities, "relations": list(relations.values()), "mentions": mentions,
            "titles": titles, "doc_community": doc_community, "labels": labels,
            "revision": graph.get("built_at_commit")}


def doc_concepts(layer, doc_id):
    """[(entity, other_docs)] for the concepts Graphify tied to this document, most shared first."""
    rows = []
    for entity in (layer["entities"] if layer else []):
        docs = layer["mentions"][entity["id"]]
        if doc_id in docs:
            rows.append((entity, sorted(doc for doc in docs if doc != doc_id)))
    rows.sort(key=lambda row: (-len(row[1]), row[0]["title"]))
    return rows


def related_docs(layer, doc_id, limit=6):
    """Other documents sharing the most extracted concepts with this one."""
    shared = {}
    for _, others in doc_concepts(layer, doc_id):
        for other in others:
            shared[other] = shared.get(other, 0) + 1
    return sorted(shared, key=lambda doc: (-shared[doc], doc))[:limit]


def related_html(layer, doc_id):
    rows = doc_concepts(layer, doc_id)
    if not rows:
        return ""
    chips = "".join(
        f'<a class="chip" href="../graph/?node={html.escape(entity["id"], quote=True)}" title="{html.escape(entity["summary"])}">'
        f'{html.escape(entity["title"])}{f"<small>{len(others)}</small>" if others else ""}</a>'
        for entity, others in rows[:16])
    return ('<section class="wiki-related" id="related"><h2>관련 개념</h2><p class="note" style="margin-top:0">Graphify가 이 문서에서 '
            '자동 추출한 개념입니다. 숫자는 같은 개념이 나오는 다른 문서 수이고, 누르면 그래프에서 그 개념을 엽니다. '
            f'위 본문처럼 사람이 대조한 문장은 아닙니다.</p><div class="chips">{chips}</div></section>')


def group_of(layer, meta):
    if layer and meta["id"] in layer["doc_community"]:
        return layer["labels"].get(layer["doc_community"][meta["id"]], GUIDE_GROUP)
    return GUIDE_GROUP


def nav_html(groups, titles, layer, prefix=""):
    """Sidebar/index grouping: one <details> per Graphify topic, documents inside."""
    parts = []
    for group, docs in groups:
        links = "".join(
            '<a href="{}{}.html" data-q="{}">{}</a>'.format(
                prefix, html.escape(doc, quote=True),
                html.escape(" ".join([titles[doc]] + [e["title"] for e, _ in doc_concepts(layer, doc)[:8]]), quote=True),
                html.escape(titles[doc]))
            for doc in docs)
        parts.append(f'<details><summary>{html.escape(group)}</summary>{links}</details>')
    return "\n".join(parts)


def index_grid(groups, documents, titles, layer):
    meta_by_id = {meta["id"]: meta for meta, _, _ in documents}
    cards = []
    for group, docs in groups:
        entries = []
        for doc in docs:
            concepts = [e["title"] for e, _ in doc_concepts(layer, doc)[:5]]
            summary = meta_by_id[doc]["summary"]
            entries.append(
                '<a class="entry" href="wiki/{}.html" data-q="{}"><span class="cnt">근거 {}</span><b>{}</b><small>{}</small></a>'.format(
                    html.escape(doc, quote=True), html.escape(" ".join([titles[doc], summary] + concepts), quote=True),
                    len(meta_by_id[doc]["sources"]), html.escape(titles[doc]),
                    html.escape(" · ".join(concepts) if concepts else summary)))
        cards.append(f'<div class="group"><h2>{html.escape(group)}<span>{len(docs)}개</span></h2>{"".join(entries)}</div>')
    return "\n".join(cards)


def info_card(meta, group, layer, titles, evidence_count):
    concepts = doc_concepts(layer, meta["id"])
    related = related_docs(layer, meta["id"])
    chips = "".join(f'<a class="chip" href="{html.escape(doc, quote=True)}.html">{html.escape(titles[doc])}</a>' for doc in related)
    card = (f'<div class="card"><div class="k">주제</div><div class="v">{html.escape(group)}</div>'
            f'<div class="k">근거 파일</div><div class="big">{evidence_count}<span> 건</span></div>'
            f'<div class="k">관련 개념</div><div class="big">{len(concepts)}<span> 개</span></div>'
            f'<div class="k">작성</div><div class="v">LLM 초안 · 사람 대조 · {UPDATED}</div></div>')
    if chips:
        card += f'<div class="card"><div class="k">같은 개념을 다루는 문서</div><div class="chips">{chips}</div></div>'
    return card


def build(root: Path) -> dict[str, str]:
    docs = root / "docs/wiki"
    sources = json.loads((docs / "sources.json").read_text(encoding="utf-8"))
    source_by_id = {source["id"]: source for source in sources}
    if len(source_by_id) != len(sources):
        raise ValueError("duplicate source id")
    source_urls = {source["url"] for source in sources}
    documents = [read_document(path) for path in sorted(docs.glob("*.md"))]
    names = {f"{meta['id']}.md" for meta, _, _ in documents}
    if len(names) != len(documents) or {path.name for path in docs.glob("*.md")} != names:
        raise ValueError("document filename/id mismatch")
    documents.sort(key=lambda item: (item[0]["order"], item[0]["id"]))
    template = (root / "templates/wiki-page.html").read_text(encoding="utf-8")
    index_template = (root / "templates/wiki-index.html").read_text(encoding="utf-8")
    outputs = {}
    search = []
    entities, relations = [], []
    ids = {meta["id"] for meta, _, _ in documents}
    graph = load_graph(root)
    layer = graph_layer(graph, documents) if graph else None
    titles = {meta["id"]: body.splitlines()[0].removeprefix("# ") for meta, body, _ in documents}
    grouped = {}
    for meta, _, _ in documents:
        grouped.setdefault(group_of(layer, meta), []).append(meta["id"])
    groups = sorted(grouped.items(), key=lambda item: (item[0] == GUIDE_GROUP, -len(item[1]), item[0]))
    navigation = nav_html(groups, titles, layer)
    for meta, body, raw in documents:
        for sid in meta["sources"]:
            if sid not in source_by_id:
                raise ValueError(f"missing source: {sid}")
        rendered, toc, plain = render_markdown(body, names, source_urls)
        for link in PUBLIC_BLOB.findall(body):
            if link not in source_urls:
                raise ValueError(f"unregistered source: {link}")
        title = titles[meta["id"]]
        if not body.startswith("# "):
            raise ValueError(f"missing title: {meta['id']}")
        group = group_of(layer, meta)
        lead = f'<div class="lead"><p>{html.escape(meta["summary"])}</p></div>'
        toc_html = '<div class="toc">' + "".join(f'<a href="#{anchor}">{html.escape(text)}</a>' for anchor, text in toc) + \
                   ('<a href="#related">관련 개념</a>' if layer and doc_concepts(layer, meta["id"]) else "") + \
                   '<a href="#sources">근거 문서</a></div>'
        rendered = rendered.replace("</h1>", "</h1>" + lead + toc_html, 1)
        evidence_html = "\n".join(
            f'<li id="s{n}"><span class="n">{n}</span><span><a href="{html.escape(source_by_id[sid]["url"], quote=True)}" target="_blank" rel="noopener">'
            f'{html.escape(source_by_id[sid]["title"])}</a><span class="p">{html.escape(source_by_id[sid]["repository"])} · '
            f'{html.escape(source_by_id[sid]["path"])}</span></span><span class="pill ok">커밋 {source_by_id[sid]["revision"][:7]}</span></li>'
            for n, sid in enumerate(meta["sources"], 1)
        ) or '<li><span class="n">-</span><span>이 안내 문서에는 별도 원본 코드 근거가 없습니다.</span><span></span></li>'
        page = template.replace("{{TITLE}}", html.escape(title)).replace("{{NAV}}", navigation)
        page = page.replace("{{GROUP}}", html.escape(group)).replace("{{KIND}}", KIND_NAMES.get(meta["type"], meta["type"]))
        page = page.replace("{{BODY}}", rendered).replace("{{RELATED}}", related_html(layer, meta["id"]) if layer else "")
        page = page.replace("{{EVIDENCE}}", evidence_html).replace("{{SOURCE_MD}}", f'markdown/{meta["id"]}.md')
        page = page.replace("{{CARD}}", info_card(meta, group, layer, titles, len(meta["sources"])))
        outputs[f'wiki/{meta["id"]}.html'] = page
        outputs[f'wiki/markdown/{meta["id"]}.md'] = raw
        search.append({"title": title, "summary": meta["summary"], "body": plain,
                       "url": f'wiki/{meta["id"]}.html', "type": meta["type"]})
        if meta["type"] not in {"guide"}:
            entities.append({"id": meta["id"], "type": meta["type"], "title": meta.get("mapTitle", title),
                             "summary": meta["summary"], "evidence": meta["sources"],
                             "document": f'wiki/{meta["id"]}.html'})
        for relation in meta["relations"]:
            if relation["to"] not in ids or relation["to"] == meta["id"]:
                raise ValueError(f"missing relation target: {relation['to']}")
            if not relation["evidence"] or not set(relation["evidence"]).issubset(meta["sources"]):
                raise ValueError(f"invalid relation evidence: {meta['id']}")
            relations.append({"id": f'r-{meta["id"]}-{relation["to"]}', "from": meta["id"],
                              "to": relation["to"], "label": relation["label"],
                              "origin": "curated", "evidence": relation["evidence"]})
    analysis = {"tool": "Graphify", "status": "not-run", "revision": None,
                "scope": "No extraction has been run for this repository."}
    if layer:
        entity_ids = {entity["id"] for entity in entities} | {entity["id"] for entity in layer["entities"]}
        entities.extend(layer["entities"])
        relations.extend(relation for relation in layer["relations"]
                         if relation["from"] in entity_ids and relation["to"] in entity_ids and relation["evidence"])
        analysis = {"tool": "Graphify", "status": "run", "revision": layer["revision"],
                    "scope": f"docs/wiki Markdown {len(documents)}개를 입력으로 추출. 노드 {len(graph['nodes'])}, "
                             f"관계 {len(graph['links'])}, 주제 {len(layer['labels'])}. 코드 노드는 문서로 접었고 "
                             "개념·설계 노드만 항목으로 실었다."}
    index = index_template.replace("{{GRID}}", index_grid(groups, documents, titles, layer))
    index = index.replace("{{DOC_COUNT}}", str(len(documents))).replace("{{TOPIC_COUNT}}", str(len(groups)))
    index = index.replace("{{CONCEPT_COUNT}}", str(len(layer["entities"]) if layer else 0))
    index = index.replace("{{SOURCE_COUNT}}", str(len(sources))).replace("{{UPDATED}}", UPDATED)
    outputs["index.html"] = index
    outputs["search-index.json"] = json.dumps(search, ensure_ascii=False, indent=2) + "\n"
    knowledge = {"schemaVersion": 1, "updatedAt": UPDATED, "analysis": analysis,
                 "sources": sources, "entities": entities, "relations": relations}
    outputs["knowledge.json"] = json.dumps(knowledge, ensure_ascii=False, indent=2) + "\n"
    return outputs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when committed generated files are stale")
    args = parser.parse_args()
    base = Path(__file__).resolve().parents[1]
    generated = build(base)
    stale = []
    generated_directory = base / "site/wiki"
    old_files = {path.relative_to(base / "site").as_posix()
                 for path in generated_directory.rglob("*") if path.is_file()}
    extras = old_files - generated.keys()
    if args.check:
        stale.extend(sorted(extras))
    else:
        for name in extras:
            (base / "site" / name).unlink()
    for name, content in generated.items():
        target = base / "site" / name
        if args.check:
            if not target.exists() or target.read_text(encoding="utf-8") != content:
                stale.append(name)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("stale generated files: " + ", ".join(stale))
    print(f"{'Checked' if args.check else 'Built'} {len(generated)} wiki outputs")
