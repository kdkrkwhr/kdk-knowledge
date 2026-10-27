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
    navigation = "\n".join(
        f'<a href="{html.escape(meta["id"])}.html">{html.escape(body.splitlines()[0].removeprefix("# "))}</a>'
        for meta, body, _ in documents
    )
    outputs = {}
    search = []
    entities, relations = [], []
    ids = {meta["id"] for meta, _, _ in documents}
    for meta, body, raw in documents:
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
        page = page.replace("{{TOC}}", toc_html).replace("{{BODY}}", rendered)
        page = page.replace("{{EVIDENCE}}", evidence_html).replace("{{SOURCE_MD}}", f'markdown/{meta["id"]}.md')
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
    outputs["search-index.json"] = json.dumps(search, ensure_ascii=False, indent=2) + "\n"
    knowledge = {"schemaVersion": 1, "updatedAt": "2026-10-27",
                 "analysis": {"tool": "Graphify", "status": "not-run", "revision": None,
                              "scope": "No extraction has been run for this repository."},
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
