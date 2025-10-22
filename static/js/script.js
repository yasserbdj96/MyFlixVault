// Tab switching functionality
document.querySelectorAll('.tab-button').forEach(button => {
  button.addEventListener('click', function() {
    const tab = this.dataset.tab;
    const currentQuery = new URLSearchParams(window.location.search).get('q') || '';
    const sortBy = new URLSearchParams(window.location.search).get('sort') || 'name';
    window.location.href = `/?tab=${tab}&q=${encodeURIComponent(currentQuery)}&sort=${sortBy}`;
  });
});

// Condition filtering for series
document.querySelectorAll('.condition-button').forEach(button => {
  button.addEventListener('click', function() {
    const condition = this.dataset.condition;
    
    // Update active state
    document.querySelectorAll('.condition-button').forEach(btn => {
      btn.classList.remove('active');
    });
    this.classList.add('active');
    
    // Filter cards
    filterCards();
  });
});

// Enhanced search functionality with client-side filtering
let searchTimeout;
const searchInput = document.getElementById('search-input');

if (searchInput) {
  searchInput.addEventListener('input', function() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      filterCards();
      updateURL(this.value);
    }, 300);
  });

  // Also trigger on Enter key for accessibility
  searchInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      clearTimeout(searchTimeout);
      filterCards();
      updateURL(this.value);
    }
  });
}

// Client-side filtering function
function filterCards() {
  const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
  const activeTab = document.querySelector('.tab-button.active').dataset.tab;
  const activeCondition = document.querySelector('.condition-button.active')?.dataset.condition || 'all';
  
  const container = document.getElementById(`${activeTab}-container`);
  if (!container) return;
  
  const cards = container.querySelectorAll('.card');
  let visibleCount = 0;
  
  cards.forEach(card => {
    const name = card.dataset.name.toLowerCase();
    const type = card.dataset.type;
    const country = card.dataset.country || '';
    const condition = card.dataset.condition || '';
    
    // Apply search filter
    const matchesSearch = !query || 
      name.includes(query) || 
      country.includes(query) ||
      (card.querySelector('h3')?.textContent.toLowerCase().includes(query));
    
    // Apply condition filter (only for series)
    const matchesCondition = activeTab !== 'series' || 
      activeCondition === 'all' || 
      condition === activeCondition;
    
    const shouldShow = matchesSearch && matchesCondition;
    card.style.display = shouldShow ? '' : 'none';
    
    if (shouldShow) visibleCount++;
  });
  
  // Show/hide empty state
  const emptyState = container.querySelector('.empty-state');
  if (emptyState) {
    emptyState.style.display = visibleCount === 0 ? 'block' : 'none';
  }
}

// Update URL without refreshing page
function updateURL(query) {
  const activeTab = document.querySelector('.tab-button.active').dataset.tab;
  const sortBy = document.getElementById('sort-select').value;
  const newURL = `/?tab=${activeTab}&q=${encodeURIComponent(query)}&sort=${sortBy}`;
  
  // Update URL without page refresh
  window.history.replaceState({}, '', newURL);
}

// Initialize filtering on page load
document.addEventListener('DOMContentLoaded', function() {
  filterCards();
});

// Lazy loading for images
if ('IntersectionObserver' in window) {
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        if (img.dataset.src) {
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
        }
        observer.unobserve(img);
      }
    });
  });

  document.querySelectorAll('img[data-src]').forEach(img => {
    imageObserver.observe(img);
  });
}

// Card animations on scroll
const observeCards = () => {
  const cards = document.querySelectorAll('.card');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }, index * 50);
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1
  });

  cards.forEach(card => {
    card.style.opacity = '1';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(card);
  });
};

// Run on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', observeCards);
} else {
  observeCards();
}

// Keyboard shortcuts for navigation
document.addEventListener('keydown', (e) => {
  // Ctrl/Cmd + K for search focus
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    searchInput?.focus();
    searchInput?.select();
  }
  
  // Escape to clear search
  if (e.key === 'Escape' && searchInput === document.activeElement) {
    searchInput.value = '';
    filterCards();
    updateURL('');
    searchInput.blur();
  }
  
  // Tab switching with 1/2 keys
  if (e.key === '1' && searchInput !== document.activeElement) {
    document.querySelector('[data-tab="series"]')?.click();
  }
  if (e.key === '2' && searchInput !== document.activeElement) {
    document.querySelector('[data-tab="movies"]')?.click();
  }
});

// Toast notification system
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
    <span>${message}</span>
  `;
  
  Object.assign(toast.style, {
    position: 'fixed',
    bottom: '20px',
    right: '20px',
    background: type === 'success' ? '#46d369' : type === 'error' ? '#f44336' : '#2196f3',
    color: 'white',
    padding: '1rem 1.5rem',
    borderRadius: '8px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
    zIndex: '10000',
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    animation: 'slideInUp 0.3s ease',
    fontSize: '0.95rem',
    fontWeight: '500'
  });
  
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = 'slideOutDown 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// Add animation keyframes
const style = document.createElement('style');
style.textContent = `
  @keyframes slideInUp {
    from {
      transform: translateY(100px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
  
  @keyframes slideOutDown {
    from {
      transform: translateY(0);
      opacity: 1;
    }
    to {
      transform: translateY(100px);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);

// Export notification on successful actions
const urlParams = new URLSearchParams(window.location.search);
if (urlParams.get('action') === 'added') {
  showToast('Entry added successfully!', 'success');
} else if (urlParams.get('action') === 'edited') {
  showToast('Entry updated successfully!', 'success');
} else if (urlParams.get('action') === 'deleted') {
  showToast('Entry deleted successfully!', 'success');
}

// Context menu for cards (right-click options)
document.querySelectorAll('.card').forEach(card => {
  card.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    showCardContextMenu(e, card);
  });
});

function showCardContextMenu(event, card) {
  // Remove any existing context menus
  document.querySelectorAll('.context-menu').forEach(menu => menu.remove());
  
  const menu = document.createElement('div');
  menu.className = 'context-menu';
  menu.style.cssText = `
    position: fixed;
    top: ${event.clientY}px;
    left: ${event.clientX}px;
    background: var(--card-bg);
    border: 2px solid var(--border-color);
    border-radius: 8px;
    padding: 0.5rem 0;
    z-index: 10000;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    min-width: 180px;
  `;
  
  const name = card.dataset.name;
  const type = card.dataset.type;
  
  const menuItems = [
    { icon: 'play', text: 'Play', action: () => card.click() },
    { icon: 'edit', text: 'Edit', action: () => card.querySelector('.edit-btn')?.click() },
    { icon: 'copy', text: 'Copy Name', action: () => copyToClipboard(name) },
    { icon: 'share', text: 'Share', action: () => shareMedia(name, type) },
    { icon: 'trash', text: 'Delete', action: () => card.querySelector('.delete-btn')?.click(), danger: true }
  ];
  
  menuItems.forEach(item => {
    const menuItem = document.createElement('div');
    menuItem.style.cssText = `
      padding: 0.7rem 1rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.7rem;
      color: ${item.danger ? 'var(--danger-color)' : 'var(--text-color)'};
      transition: background 0.2s ease;
    `;
    menuItem.innerHTML = `<i class="fas fa-${item.icon}"></i> ${item.text}`;
    menuItem.addEventListener('mouseenter', () => {
      menuItem.style.background = item.danger ? 'rgba(244, 67, 54, 0.1)' : 'var(--secondary-color)';
    });
    menuItem.addEventListener('mouseleave', () => {
      menuItem.style.background = 'transparent';
    });
    menuItem.addEventListener('click', () => {
      item.action();
      menu.remove();
    });
    menu.appendChild(menuItem);
  });
  
  document.body.appendChild(menu);
  
  // Close menu on click outside
  setTimeout(() => {
    document.addEventListener('click', () => menu.remove(), { once: true });
  }, 0);
  
  // Adjust position if menu goes off-screen
  const rect = menu.getBoundingClientRect();
  if (rect.right > window.innerWidth) {
    menu.style.left = (event.clientX - rect.width) + 'px';
  }
  if (rect.bottom > window.innerHeight) {
    menu.style.top = (event.clientY - rect.height) + 'px';
  }
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    showToast('Copied to clipboard!', 'success');
  }).catch(() => {
    showToast('Failed to copy', 'error');
  });
}

function shareMedia(name, type) {
  if (navigator.share) {
    navigator.share({
      title: name,
      text: `Check out this ${type}: ${name}`
    }).catch(() => {});
  } else {
    copyToClipboard(name);
  }
}

// Smooth scroll to top button
const scrollToTopBtn = document.createElement('button');
scrollToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
scrollToTopBtn.style.cssText = `
  position: fixed;
  bottom: 80px;
  right: 20px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: var(--primary-color);
  color: white;
  border: none;
  cursor: pointer;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease, transform 0.3s ease;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  font-size: 1.2rem;
`;

document.body.appendChild(scrollToTopBtn);

window.addEventListener('scroll', () => {
  if (window.scrollY > 300) {
    scrollToTopBtn.style.opacity = '1';
    scrollToTopBtn.style.pointerEvents = 'all';
  } else {
    scrollToTopBtn.style.opacity = '0';
    scrollToTopBtn.style.pointerEvents = 'none';
  }
});

scrollToTopBtn.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

scrollToTopBtn.addEventListener('mouseenter', () => {
  scrollToTopBtn.style.transform = 'translateY(-5px)';
});

scrollToTopBtn.addEventListener('mouseleave', () => {
  scrollToTopBtn.style.transform = 'translateY(0)';
});

// Offline detection
window.addEventListener('offline', () => {
  showToast('You are offline. Some features may not work.', 'error');
});

window.addEventListener('online', () => {
  showToast('You are back online!', 'success');
});

// Performance optimization: Throttle scroll events
function throttle(func, delay) {
  let lastCall = 0;
  return function(...args) {
    const now = new Date().getTime();
    if (now - lastCall < delay) return;
    lastCall = now;
    return func(...args);
  };
}

// Apply filter persistence
const activeCondition = sessionStorage.getItem('activeCondition');
if (activeCondition) {
  const conditionBtn = document.querySelector(`[data-condition="${activeCondition}"]`);
  if (conditionBtn) {
    conditionBtn.click();
  }
}

document.querySelectorAll('.condition-button').forEach(btn => {
  btn.addEventListener('click', function() {
    sessionStorage.setItem('activeCondition', this.dataset.condition);
    filterCards();
  });
});

// Log user interactions for analytics (optional)
function logInteraction(action, details) {
  console.log(`[MyFlixVault] ${action}:`, details);
  // Here you could send to an analytics service
}

// Track card clicks
document.querySelectorAll('.card').forEach(card => {
  card.addEventListener('click', () => {
    logInteraction('card_click', {
      name: card.dataset.name,
      type: card.dataset.type
    });
  });
});

console.log('%cMyFlixVault Enhanced 🎬', 'color: #e50914; font-size: 24px; font-weight: bold;');
console.log('%cKeyboard Shortcuts:', 'color: #46d369; font-size: 14px; font-weight: bold;');
console.log('Ctrl/Cmd + K: Focus search');
console.log('Escape: Clear search');
console.log('1: Switch to Series tab');
console.log('2: Switch to Movies tab');