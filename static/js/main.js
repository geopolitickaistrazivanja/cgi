// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const offcanvas = document.getElementById('offcanvas');
const offcanvasClose = document.getElementById('offcanvasClose');
const offcanvasOverlay = document.getElementById('offcanvasOverlay');

function openOffcanvas() {
    if (offcanvas && window.innerWidth <= 767) {
        offcanvas.classList.add('open');
        if (offcanvasOverlay) {
            offcanvasOverlay.classList.add('active');
        }
        document.body.style.overflow = 'hidden';
    }
}

function closeOffcanvas() {
    if (offcanvas) {
        offcanvas.classList.remove('open');
        if (offcanvasOverlay) {
            offcanvasOverlay.classList.remove('active');
        }
        document.body.style.overflow = '';
    }
}

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', openOffcanvas);
}

if (offcanvasClose) {
    offcanvasClose.addEventListener('click', closeOffcanvas);
}

// Close offcanvas when clicking on overlay
if (offcanvasOverlay) {
    offcanvasOverlay.addEventListener('click', closeOffcanvas);
}

// Close offcanvas when clicking outside (on the offcanvas itself, not the content)
if (offcanvas) {
    offcanvas.addEventListener('click', (e) => {
        if (e.target === offcanvas) {
            closeOffcanvas();
        }
    });
}

// Search Functionality
const searchBtn = document.getElementById('searchBtn');
const searchBtnMobile = document.getElementById('searchBtnMobile');
const searchOverlay = document.getElementById('searchOverlay');
const searchClose = document.getElementById('searchClose');
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');

function openSearch() {
    searchOverlay.classList.add('active');
    searchInput.focus();
    document.body.style.overflow = 'hidden';
}

function closeSearch() {
    searchOverlay.classList.remove('active');
    searchInput.value = '';
    searchResults.innerHTML = '';
    document.body.style.overflow = '';
}

if (searchBtn) {
    searchBtn.addEventListener('click', openSearch);
}
if (searchBtnMobile) {
    searchBtnMobile.addEventListener('click', openSearch);
}
if (searchClose) {
    searchClose.addEventListener('click', closeSearch);
}

// Close search on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && searchOverlay.classList.contains('active')) {
        closeSearch();
    }
});

// Search with debounce
let searchTimeout;
searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    const query = e.target.value.trim();
    
    if (query.length < 2) {
        searchResults.innerHTML = '';
        return;
    }
    
    searchTimeout = setTimeout(() => {
        fetch(`/prodavnica/pretraga/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                displaySearchResults(data.products);
            })
            .catch(error => {
                console.error('Search error:', error);
            });
    }, 300);
});

function displaySearchResults(products) {
    if (products.length === 0) {
        searchResults.innerHTML = '<div class="search-result-item">Nema rezultata</div>';
        return;
    }
    
    searchResults.innerHTML = products.map(product => `
        <div class="search-result-item" onclick="window.location.href='/prodavnica/proizvod/${product.slug}/'">
            ${product.image ? `<img src="${product.image}" alt="${product.title}">` : ''}
            <div>
                <h4>${product.title}</h4>
                <p>${product.price} RSD</p>
            </div>
        </div>
    `).join('');
}

// Add to Cart
document.querySelectorAll('.add-to-cart-form').forEach(form => {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const productId = form.dataset.productId;
        const quantity = form.querySelector('#quantity').value;
        const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
        
        try {
            const response = await fetch(`/prodavnica/dodaj-u-korpu/${productId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `quantity=${quantity}`
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Update cart count
                const cartCount = document.querySelector('.cart-count');
                if (cartCount) {
                    cartCount.textContent = data.cart_count;
                    if (data.cart_count > 0) {
                        cartCount.style.display = 'flex';
                    }
                } else {
                    // Create cart count if it doesn't exist
                    const cartIcon = document.querySelector('.cart-icon');
                    if (cartIcon && data.cart_count > 0) {
                        let countEl = cartIcon.querySelector('.cart-count');
                        if (!countEl) {
                            countEl = document.createElement('span');
                            countEl.className = 'cart-count';
                            cartIcon.appendChild(countEl);
                        }
                        countEl.textContent = data.cart_count;
                    }
                }
                
                // Show success message
                alert(data.message);
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Add to cart error:', error);
            alert('Došlo je do greške. Molimo pokušajte ponovo.');
        }
    });
});

// Back to Top Button
const backToTop = document.getElementById('backToTop');

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        backToTop.classList.add('visible');
    } else {
        backToTop.classList.remove('visible');
    }
});

backToTop.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Disable hover effects on touch devices
if ('ontouchstart' in window || navigator.maxTouchPoints > 0) {
    document.body.classList.add('touch-device');
}

// Auto-hide messages
setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.style.transition = 'opacity 0.5s ease';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 500);
    });
}, 5000);

