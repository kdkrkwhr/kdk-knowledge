const search = document.querySelector('#wiki-search');
const results = document.querySelector('#search-results');
const status = document.querySelector('#search-status');
const entries = [...document.querySelectorAll('.entry')];

function showResults() {
  const query = search.value.trim().toLocaleLowerCase();
  results.replaceChildren();
  results.hidden = !query;
  if (!query) {
    status.textContent = '제목과 본문에서 찾습니다. / 키로 검색창에 이동할 수 있어요.';
    return;
  }
  const found = entries.filter(entry => entry.textContent.toLocaleLowerCase().includes(query));
  for (const entry of found) {
    const link = document.createElement('a');
    link.href = `#${entry.id}`;
    link.textContent = entry.querySelector('h1,h2').textContent;
    const item = document.createElement('li');
    item.append(link);
    results.append(item);
  }
  status.textContent = found.length ? `${found.length}개 문서를 찾았습니다.` : '검색 결과가 없습니다. 다른 단어로 찾아보세요.';
}

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
