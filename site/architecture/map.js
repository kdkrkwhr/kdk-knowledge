const $ = selector => document.querySelector(selector);
let knowledge;
let selected = null;
const positions = {hub: 'node-hub', notebuddy: 'node-left', standards: 'node-right'};
const typeNames = {hub: '허브', project: '프로젝트', criteria: '개발 기준', career: '경력', technology: '기술'};

function sourceLinks(ids) {
  const list = document.createElement('ul');
  for (const id of ids) {
    const source = knowledge.sources.find(item => item.id === id);
    if (!source) continue;
    const item = document.createElement('li');
    const link = document.createElement('a');
    link.href = source.url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.textContent = `${source.title} · ${source.revision.slice(0, 7)}`;
    item.append(link);
    list.append(item);
  }
  return list;
}

function showDetail(id) {
  selected = id;
  const entity = knowledge.entities.find(item => item.id === id);
  const panel = $('#map-detail');
  panel.replaceChildren();
  const kind = document.createElement('p');
  kind.className = 'eyebrow';
  kind.textContent = typeNames[entity.type] || entity.type;
  const title = document.createElement('h3');
  title.textContent = entity.title;
  const summary = document.createElement('p');
  summary.textContent = entity.summary;
  panel.append(kind, title, summary);
  const related = knowledge.relations.filter(relation => relation.from === id || relation.to === id);
  for (const relation of related) {
    const other = knowledge.entities.find(item => item.id === (relation.from === id ? relation.to : relation.from));
    const label = document.createElement('p');
    label.className = 'relation-label';
    label.textContent = `${relation.label} · ${other.title} (편집 관계)`;
    panel.append(label, sourceLinks(relation.evidence));
  }
  if (!related.length && entity.evidence.length) panel.append(sourceLinks(entity.evidence));
  if (!related.length && !entity.evidence.length) {
    const note = document.createElement('p');
    note.textContent = '아직 연결된 공개 근거가 없습니다.';
    panel.append(note);
  }
  document.querySelectorAll('.graph-node').forEach(node => node.setAttribute('aria-pressed', String(node.dataset.id === id)));
}

function render() {
  const query = $('#map-search').value.trim().toLocaleLowerCase();
  const type = $('#type-filter').value;
  const visible = knowledge.entities.filter(item =>
    (type === 'all' || item.type === type) &&
    `${item.title} ${item.summary}`.toLocaleLowerCase().includes(query));
  const nodes = $('#graph-nodes');
  nodes.replaceChildren();
  for (const entity of visible) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = `graph-node ${positions[entity.id] || ''}`;
    button.dataset.id = entity.id;
    button.setAttribute('aria-pressed', String(selected === entity.id));
    const kind = document.createElement('small');
    kind.textContent = typeNames[entity.type] || entity.type;
    const title = document.createElement('strong');
    title.textContent = entity.title;
    button.append(kind, title);
    button.addEventListener('click', () => showDetail(entity.id));
    nodes.append(button);
  }
  $('#map-empty').hidden = visible.length > 0;
  $('#map-status').textContent = visible.length ? `${visible.length} / ${knowledge.entities.length}개 항목` : '검색 결과가 없습니다. 검색어나 필터를 바꿔 보세요.';
  $('#graph').classList.toggle('filtered', Boolean(query) || type !== 'all');
  // shortcut: larger collections use a readable node grid; add computed edge layout when the corpus grows.
  $('#graph').classList.toggle('many', visible.length > 3);
  if (selected && !visible.some(item => item.id === selected)) {
    selected = null;
    $('#map-detail').replaceChildren();
    const title = document.createElement('h3');
    title.textContent = '항목을 선택해 주세요';
    $('#map-detail').append(title);
  }
}

async function start() {
  try {
    const response = await fetch('../knowledge.json');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    knowledge = await response.json();
    $('#map-search').addEventListener('input', render);
    $('#type-filter').addEventListener('change', render);
    $('#map-reset').addEventListener('click', () => {
      $('#map-search').value = '';
      $('#type-filter').value = 'all';
      render();
      $('#map-search').focus();
    });
    render();
  } catch {
    $('#map-status').textContent = '관계 자료를 불러오지 못했습니다. 관계 JSON을 직접 확인해 주세요.';
  }
}
start();
