# Personal knowledge hub design

This public repository is a personal map of projects, roles, outcomes, technology choices, lessons, and resulting development criteria. It begins with only two verified public references. Empty categories stay visibly empty until the owner provides publishable evidence.

## Approaches

- Static HTML, CSS, JavaScript, and JSON: chosen for GitHub Pages, keyboard access, no runtime API, and a small reviewable public artifact.
- A generated documentation framework: deferred because it adds installation and build dependencies before the corpus exists.
- Live Graphify and LLM calls: deferred because execution and data transmission have not been authorized.

## Boundaries

- `site/` contains only public HTML, CSS, JavaScript, and a source pinned relationship dataset. The wiki is written by an LLM against public source and labeled as reviewed commentary; it is not Graphify output.
- The architecture page visualizes the dataset's curated relations and explicitly states that Graphify has not run. It links to the existing notebook-pets Graphify page as a separate reference.
- Every relation names evidence IDs; each evidence URL pins a full commit. The validator rejects missing citations, non-public visibility, malformed revisions, and unsafe public files.
- `templates/` provides minimal project, career, technology, decision, and learning prompts. A person reviews both factual support and permission to publish before adding entries.
- GitHub Actions checks the repository, then uploads only `site/` to Pages. Pages activation is an external repository setting and must be verified separately.

## Experience

Use the notebook-pets wiki's thin bar, left navigation, central reading/search, and right article outline. Use the architecture page's separate search, type filters, selected item details, evidence links, and analysis revision. Keep Korean body text comfortably readable, support narrow screens and keyboard/touch navigation, and show honest empty results.
