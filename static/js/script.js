// Tabs
document.querySelectorAll('.tab-button').forEach(button => {
  button.addEventListener('click', () => {
    const tab = button.dataset.tab;
    const url = new URL(window.location);
    url.searchParams.set('tab', tab);
    window.location.href = url.toString();
  });
});

// Search and Condition Filtering
const searchInput = document.getElementById('search-input');

function filterCards() {
  const query = searchInput.value.trim().toLowerCase();
  const activeTab = document.querySelector('.tab-button.active').dataset.tab;
  const condition = document.querySelector('.condition-button.active')?.dataset.condition || 'all';
  const container = document.getElementById(`${activeTab}-container`);
  const cards = container.querySelectorAll('.card');

  cards.forEach(card => {
    const name = (card.getAttribute('data-name') || '').toLowerCase();
    const type = (card.getAttribute('data-type') || '').toLowerCase();
    const ribbon = (card.querySelector('.ribbon')?.textContent || '').toLowerCase();

    const matchesQuery =
      name.includes(query) ||
      query.split(/\s+/).every(word => name.includes(word)) ||
      type.includes(query);

    const matchesCondition = (condition === 'all') || (ribbon === condition);

    card.style.display = (matchesQuery && matchesCondition) ? '' : 'none';
  });
}

searchInput.addEventListener('input', filterCards);

document.addEventListener('DOMContentLoaded', () => {
  const preQuery = searchInput?.value?.trim();
  if (preQuery) filterCards();
});

// Condition Buttons
document.querySelectorAll('.condition-button').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.condition-button').forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');
    filterCards();
  });
});

// Trailer Click
document.querySelectorAll('.card').forEach(card => {
  card.addEventListener('click', async () => {
    const h3 = card.querySelector('h3');
    const fullText = h3.textContent.trim();
    const yearMatch = fullText.match(/\((\d{4})\)$/);
    const year = yearMatch ? yearMatch[1] : '';
    const name = fullText.replace(/\(\d{4}\)$/, '').trim();
    let type = card.getAttribute('data-type');
    if (type === "series") {
      type = "tv";
    }
    const country = card.getAttribute('data-country') || '';

    // Build query parameters
    const params = new URLSearchParams();
    params.append('name', name);
    params.append('type', type);
    if (year) params.append('year', year);
    if (country) params.append('country', country);

    const res = await fetch(`/trailer?${params.toString()}`);
    const data = await res.json();

    if (data.trailer_url) {
      document.getElementById('trailer-frame').src = data.trailer_url;
      document.getElementById('trailer-modal').style.display = 'flex';
    } else {
      alert("Trailer not found!");
    }
  });
});


// Trailer Modal Close
function closeTrailer() {
  document.getElementById('local-media-modal').style.display = 'none';
  document.getElementById('trailer-frame').src = '';
}
