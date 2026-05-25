'use strict';

const BASE = window.__base || '/web';

let searchTimer = null;
const $q = document.getElementById('q');
const $results = document.getElementById('search-results');
const $tree = document.getElementById('tree-nav');

function doSearch() {
  const q = ($q.value || '').trim();
  if (!q) {
    $results.classList.add('hidden');
    $results.innerHTML = '';
    $tree.style.display = '';
    return;
  }
  fetch(`${BASE}/api/search?q=${encodeURIComponent(q)}&top_k=20`)
    .then(r => r.json())
    .then(data => {
      const items = (data.matches || []);
      if (!items.length) {
        $results.innerHTML = '<div class="sr-title">无结果</div>';
      } else {
        $results.innerHTML =
          `<div class="sr-title">${items.length} matches</div>` +
          items.map(m =>
            `<a class="sr-item" href="${BASE}/skill/${m.path.replace(/\.md$/, '')}">
              <div><span class="name">${escapeHtml(m.name)}</span><span class="dim">${m.dimension || ''} · ${m.score}</span></div>
              <div class="desc">${escapeHtml(m.description || '')}</div>
            </a>`
          ).join('');
      }
      $results.classList.remove('hidden');
      $tree.style.display = 'none';
    })
    .catch(err => {
      $results.innerHTML = `<div class="sr-title">error: ${err}</div>`;
      $results.classList.remove('hidden');
    });
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

$q.addEventListener('input', () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(doSearch, 180);
});

document.addEventListener('keydown', e => {
  if (e.key === '/' && document.activeElement !== $q) {
    e.preventDefault();
    $q.focus();
  } else if (e.key === 'Escape' && document.activeElement === $q) {
    $q.value = '';
    doSearch();
  }
});
