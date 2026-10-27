const search = document.querySelector('#wiki-search');
const results = document.querySelector('#search-results');
const status = document.querySelector('#search-status');
const root = document.body.dataset.searchRoot || '.';
let documents = [];

function showResults() {
  const query = search.value.trim().toLocaleLowerCase();
  results.replaceChildren();
  results.hidden = !query;
  if (!query) {
    status.textContent = '문서 본문에서 검색합니다. / 키로 검색창에 이동할 수 있어요.';
    return;
  }
  const found = documents.filter(item =>
    `${item.title} ${item.summary} ${item.body}`.toLocaleLowerCase().includes(query));
  for (const entry of found) {
    const item = document.createElement('li');
    const link = document.createElement('a');
    link.href = `${root}/${entry.url}`;
    link.textContent = entry.title;
    const summary = document.createElement('small');
    summary.textContent = entry.summary;
    item.append(link, summary);
    results.append(item);
  }
  status.textContent = found.length ? `${found.length}개 문서를 찾았습니다.` : '검색 결과가 없습니다. 다른 단어로 찾아보세요.';
}

fetch(`${root}/search-index.json`).then(response => {
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}).then(data => {
  documents = data;
  showResults();
}).catch(() => {
  status.textContent = '검색 자료를 불러오지 못했습니다. 문서 목록에서 직접 찾아보세요.';
});

search.addEventListener('input', showResults);
document.querySelector('#clear-search').addEventListener('click', () => {
  search.value = '';
  showResults();
  search.focus();
});
document.addEventListener('keydown', event => {
  if (event.key === '/' && !/^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName)) {
    event.preventDefault();
    search.focus();
  }
  if (event.key === 'Escape' && document.activeElement === search) {
    search.value = '';
    showResults();
  }
});
