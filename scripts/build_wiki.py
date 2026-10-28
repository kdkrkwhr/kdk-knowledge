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


def related_html(layer, doc_id):
    rows = []
    for entity in layer["entities"]:
        docs = layer["mentions"][entity["id"]]
        if doc_id in docs:
            rows.append((entity, sorted(doc for doc in docs if doc != doc_id)))
    if not rows:
        return ""
    rows.sort(key=lambda row: (-len(row[1]), row[0]["title"]))
    items = []
    for entity, others in rows[:12]:
        links = " · ".join(f'<a href="{html.escape(doc, quote=True)}.html">{html.escape(layer["titles"][doc])}</a>'
                           for doc in others[:4])
        items.append(f'<li><a href="../architecture/?node={html.escape(entity["id"], quote=True)}">'
                     f'{html.escape(entity["title"])}</a>{" — 같은 개념: " + links if links else ""}</li>')
    community = layer["doc_community"].get(doc_id)
    topic = (f'<p>주제 묶음: <a href="topics.html#topic-{community}">{html.escape(layer["labels"].get(community, ""))}</a></p>'
             if community is not None else "")
    return ('<section class="wiki-related"><h2>관련 개념</h2><p class="muted">Graphify가 이 문서에서 추출한 개념과, '
            '같은 개념이 나오는 다른 문서입니다. 자동 추출 결과이며 위 본문처럼 사람이 대조한 문장은 아닙니다.</p>'
            f'<ul>{"".join(items)}</ul>{topic}</section>')


def topics_page(template, layer, documents):
    """One page: a section per Graphify community with its documents and concepts."""
    by_community = {}
    for doc, community in layer["doc_community"].items():
        by_community.setdefault(community, {"docs": [], "concepts": []})["docs"].append(doc)
    for entity in layer["entities"]:
        for community, label in layer["labels"].items():
            if entity["community"] == label:
                by_community.setdefault(community, {"docs": [], "concepts": []})["concepts"].append(entity)
    body = ['<h1>주제 지도</h1><p>Graphify가 위키 문서에서 추출한 개념을 연결 구조로 묶은 주제입니다. '
            '묶음 이름은 사람이 붙였고, 각 항목의 설명은 추출된 요약이라 사람이 대조한 본문과 구분해 읽습니다. '
            f'기준 커밋 <code>{html.escape((layer["revision"] or "")[:7])}</code>.</p>']
    toc = []
    for community, group in sorted(by_community.items(), key=lambda item: -len(item[1]["docs"]) - len(item[1]["concepts"])):
        label = layer["labels"].get(community, f"주제 {community}")
        toc.append(f'<a href="#topic-{community}">{html.escape(label)}</a>')
        body.append(f'<h2 id="topic-{community}">{html.escape(label)}</h2>')
        if group["docs"]:
            body.append("<p>문서: " + " · ".join(
                f'<a href="{html.escape(doc, quote=True)}.html">{html.escape(layer["titles"][doc])}</a>'
                for doc in sorted(group["docs"])) + "</p>")
        if group["concepts"]:
            body.append("<ul>" + "".join(
                f'<li><strong>{html.escape(entity["title"])}</strong>'
                f'{" — " + html.escape(entity["summary"]) if entity["summary"] else ""}</li>'
                for entity in sorted(group["concepts"], key=lambda item: item["title"])) + "</ul>")
    navigation = "\n".join('<a href="{}.html">{}</a>'.format(html.escape(meta["id"], quote=True),
                                                           html.escape(doc_body.splitlines()[0].removeprefix("# ")))
                           for meta, doc_body, _ in documents)
    page = template.replace("{{TITLE}}", "주제 지도").replace("{{NAV}}", navigation)
    page = page.replace("{{NAV_COUNT}}", str(len(documents))).replace("{{TOC}}", "\n".join(toc))
    page = page.replace("{{BODY}}", "\n".join(body)).replace("{{RELATED}}", "")
    page = page.replace('<a href="{{SOURCE_MD}}">Markdown 원문 보기</a> · 문장과 원본 파일을 사람이 대조했습니다.',
                        '<a href="../knowledge.json">관계 JSON 보기</a> · 자동 추출 결과이며 사람이 대조한 문장은 아닙니다.')
    return page.replace("{{EVIDENCE}}", '<li>docs/graph/graph.json · Graphify 추출 · '
                        f'{html.escape((layer["revision"] or "")[:7])}</li>')


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
    outputs = {}
    search = []
    entities, relations = [], []
    ids = {meta["id"] for meta, _, _ in documents}
    graph = load_graph(root)
    layer = graph_layer(graph, documents) if graph else None
    for meta, body, raw in documents:
        navigation = "\n".join(
            '<a href="{}.html"{}>{}</a>'.format(
                html.escape(item_meta["id"], quote=True),
                ' aria-current="page"' if item_meta["id"] == meta["id"] else '',
                html.escape(item_body.splitlines()[0].removeprefix("# ")),
            ) for item_meta, item_body, _ in documents
        )
        for sid in meta["sources"]:
            if sid not in source_by_id:
                raise ValueError(f"missing source: {sid}")
        rendered, toc, plain = render_markdown(body, names, source_urls)
        for link in PUBLIC_BLOB.findall(body):
            if link not in source_urls:
                raise ValueError(f"unregistered source: {link}")
        title = body.splitlines()[0].removeprefix("# ")
        if not body.startswith("# "):
            raise ValueError(f"missing title: {meta['id']}")
        toc_html = "\n".join(f'<a href="#{anchor}">{html.escape(text)}</a>' for anchor, text in toc)
        evidence_html = "\n".join(
            f'<li><a href="{html.escape(source_by_id[sid]["url"], quote=True)}">'
            f'{html.escape(source_by_id[sid]["title"])} · {source_by_id[sid]["revision"][:7]}</a></li>'
            for sid in meta["sources"]
        ) or "<li>이 안내 문서에는 별도 원본 코드 근거가 없습니다.</li>"
        page = template.replace("{{TITLE}}", html.escape(title)).replace("{{NAV}}", navigation)
        page = page.replace("{{NAV_COUNT}}", str(len(documents)))
        page = page.replace("{{TOC}}", toc_html).replace("{{BODY}}", rendered)
        page = page.replace("{{EVIDENCE}}", evidence_html).replace("{{SOURCE_MD}}", f'markdown/{meta["id"]}.md')
        page = page.replace("{{RELATED}}", related_html(layer, meta["id"]) if layer else "")
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
        outputs["wiki/topics.html"] = topics_page(template, layer, documents)
        analysis = {"tool": "Graphify", "status": "run", "revision": layer["revision"],
                    "scope": f"docs/wiki Markdown {len(documents)}개를 입력으로 추출. 노드 {len(graph['nodes'])}, "
                             f"관계 {len(graph['links'])}, 주제 {len(layer['labels'])}. 코드 노드는 문서로 접었고 "
                             "개념·설계 노드만 항목으로 실었다."}
    outputs["search-index.json"] = json.dumps(search, ensure_ascii=False, indent=2) + "\n"
    knowledge = {"schemaVersion": 1, "updatedAt": "2026-10-28", "analysis": analysis,
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
        raise SystemExit("Stale generated wiki files: " + ", ".join(stale))
    print(f"{'Checked' if args.check else 'Built'} {len(generated)} wiki outputs")
