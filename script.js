async function loadNews() {
    const container = document.getElementById('news-container');
    try {
        const response = await fetch('data.json');
        const data = await response.json();

        container.innerHTML = data.map(item => `
            <article class="card">
                <span>${item.source}</span>
                <h3>${item.title}</h3>
                <p><a href="${item.link}" target="_blank">Leer más →</a></p>
                <small style="color: #666">${new Date(item.date).toLocaleDateString()}</small>
            </article>
        `).join('');
    } catch (e) {
        container.innerHTML = '<p>No se pudieron cargar las noticias. El script está recolectando datos...</p>';
    }
}

loadNews();
