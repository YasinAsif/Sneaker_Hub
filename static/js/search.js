/**
 * SneakerHub — Live Search
 */
document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('input-search');
    const dropdown = document.getElementById('search-results-dropdown');
    if (!input || !dropdown) return;

    let debounceTimer;
    input.addEventListener('input', function () {
        clearTimeout(debounceTimer);
        const q = this.value.trim();
        if (q.length < 2) { dropdown.classList.remove('show'); dropdown.innerHTML = ''; return; }
        debounceTimer = setTimeout(() => {
            fetch(`/api/search?q=${encodeURIComponent(q)}`)
                .then(r => r.json())
                .then(results => {
                    if (!results.length) { dropdown.innerHTML = '<div class="p-3 text-muted text-center">No results found</div>'; dropdown.classList.add('show'); return; }
                    dropdown.innerHTML = results.map(p => `
                        <a href="${p.url}" class="search-result-item text-decoration-none">
                            <div class="placeholder-img" style="width:40px;height:40px;font-size:1rem;"><i class="bi bi-shoe"></i></div>
                            <div>
                                <div class="fw-bold text-light" style="font-size:.85rem">${p.brand} ${p.model}</div>
                                <div class="text-accent fw-bold" style="font-size:.8rem">$${p.price.toFixed(2)}</div>
                            </div>
                        </a>`).join('');
                    dropdown.classList.add('show');
                }).catch(() => dropdown.classList.remove('show'));
        }, 300);
    });

    document.addEventListener('click', function (e) {
        if (!e.target.closest('.search-form')) dropdown.classList.remove('show');
    });
});
