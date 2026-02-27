let allNews = [];

async function loadNews() {
    const container = document.getElementById('news-container');
    try {
        const response = await fetch('data.json');
        allNews = await response.json();

        allNews.sort((a, b) => new Date(b.date) - new Date(a.date));

        renderNews(allNews);
    } catch (e) {
        container.innerHTML = '<p style="grid-column: 1/-1; text-align: center;">No se pudieron cargar las noticias. El script está recolectando datos...</p>';
    }
}

function renderNews(newsArray) {
    const container = document.getElementById('news-container');
    if (newsArray.length === 0) {
        container.innerHTML = '<p style="grid-column: 1/-1; text-align: center;">No se han encontrado noticias.</p>';
        return;
    }

    container.innerHTML = newsArray.map(item => `
        <article class="card ${item.is_important ? 'vip-card' : ''}">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                <div style="display:flex; gap:8px; align-items:center;">
                    <span>${item.source}</span>
                    ${item.is_important ? '<span class="vip-badge">🔥 DESTACADO</span>' : ''}
                </div>
                <small style="color: var(--dim); font-size: 0.75rem;">${new Date(item.date).toLocaleDateString()}</small>
            </div>
            
            ${item.tags && item.tags.length > 0 ?
            `<div style="display:flex; gap:6px; flex-wrap:wrap; margin-bottom:0.5rem;">
                    ${item.tags.map(tag => `<span class="cat-tag">${tag}</span>`).join('')}
                </div>` : ''}
                
            <h3>${item.title}</h3>
            ${item.description ? '<p class="desc">' + item.description + '</p>' : ''}
            <a href="${item.link}" target="_blank" class="read-btn">Leer más →</a>
        </article>
    `).join('');
}

document.getElementById('searchInput').addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const filteredNews = allNews.filter(item =>
        item.title.toLowerCase().includes(searchTerm) ||
        (item.description && item.description.toLowerCase().includes(searchTerm)) ||
        item.source.toLowerCase().includes(searchTerm) ||
        (item.tags && item.tags.some(t => t.toLowerCase().includes(searchTerm)))
    );
    renderNews(filteredNews);
});

loadNews();
