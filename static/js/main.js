// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const offcanvas = document.getElementById('offcanvas');
const offcanvasClose = document.getElementById('offcanvasClose');
const offcanvasOverlay = document.getElementById('offcanvasOverlay');

function openOffcanvas() {
    if (offcanvas && window.innerWidth <= 767) {
        document.body.classList.add('offcanvas-open');
        offcanvas.classList.add('open');
        // No overlay needed since offcanvas covers full screen
    }
}

function closeOffcanvas() {
    if (offcanvas) {
        offcanvas.classList.remove('open');
        document.body.classList.remove('offcanvas-open');
    }
}

// Wait for DOM to be ready before attaching event listeners
document.addEventListener('DOMContentLoaded', function() {
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', openOffcanvas);
    }
    
    // Make menu label clickable
    const mobileMenuLabel = document.getElementById('mobileMenuLabel');
    if (mobileMenuLabel) {
        mobileMenuLabel.addEventListener('click', openOffcanvas);
    }
    
    // Offcanvas dropdown toggle - arrow button toggles dropdown, text link navigates
    const dropdownToggles = document.querySelectorAll('.offcanvas-dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const dropdown = this.closest('.offcanvas-item-dropdown');
            if (dropdown) {
                dropdown.classList.toggle('open');
            }
        });
    });
    
    // Close offcanvas when clicking on navigation links (regular links and dropdown items)
    const offcanvasLinks = document.querySelectorAll('.offcanvas-menu-list .offcanvas-item, .offcanvas-dropdown-item');
    offcanvasLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 767) {
                // No closeOffcanvas() call - instant navigation without animation
                // Navigation happens naturally without preventDefault
            }
        });
    });
});

if (offcanvasClose) {
    offcanvasClose.addEventListener('click', closeOffcanvas);
}

// Overlay not needed since offcanvas covers full screen

// Close offcanvas when clicking outside (on the offcanvas itself, not the content)
if (offcanvas) {
    offcanvas.addEventListener('click', (e) => {
        if (e.target === offcanvas) {
            closeOffcanvas();
        }
    });
}

// Search Functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchBtn = document.getElementById('searchBtn');
    const searchBtnMobile = document.getElementById('searchBtnMobile');
    const searchOverlay = document.getElementById('searchOverlay');
    const searchClose = document.getElementById('searchClose');
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    
    if (!searchOverlay || !searchInput || !searchResults) {
        console.log('Search elements not found, skipping search initialization');
        return;
    }
    
    function openSearch() {
        if (searchOverlay) {
            searchOverlay.classList.add('active');
            document.body.classList.add('search-open');
            if (searchInput) {
                searchInput.focus();
            }
            document.body.style.overflow = 'hidden';
        }
    }
    
    function closeSearch() {
        if (searchOverlay) {
            searchOverlay.classList.remove('active');
            document.body.classList.remove('search-open');
            if (searchInput) {
                searchInput.value = '';
            }
            if (searchResults) {
                searchResults.innerHTML = '';
            }
            document.body.style.overflow = '';
        }
    }
    
    if (searchBtn) {
        searchBtn.addEventListener('click', openSearch);
    }
    if (searchBtnMobile) {
        searchBtnMobile.addEventListener('click', openSearch);
    }
    
    // Make search label clickable
    const mobileSearchLabel = document.getElementById('mobileSearchLabel');
    if (mobileSearchLabel) {
        mobileSearchLabel.addEventListener('click', openSearch);
    }
    if (searchClose) {
        searchClose.addEventListener('click', closeSearch);
    }
    
    // Close search on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && searchOverlay && searchOverlay.classList.contains('active')) {
            closeSearch();
        }
    });
    
    // Search functionality can be added here for topics if needed
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

// Position dropdown menu dynamically using fixed positioning
(function() {
    function initDropdowns() {
        if (window.innerWidth <= 767) return; // Only on desktop
        
        const navItemDropdowns = document.querySelectorAll('.nav-item-dropdown');
        
        navItemDropdowns.forEach(dropdown => {
            const navItemLink = dropdown.querySelector('.nav-item-link');
            const dropdownMenu = dropdown.querySelector('.dropdown-menu');
            
            if (!navItemLink || !dropdownMenu) return;
            
            function positionDropdown() {
                const rect = navItemLink.getBoundingClientRect();
                
                // Position dropdown below the nav item, centered (getBoundingClientRect gives viewport coordinates)
                // Bridge element handles the gap
                dropdownMenu.style.position = 'fixed';
                dropdownMenu.style.top = rect.bottom + 'px';
                dropdownMenu.style.left = (rect.left + rect.width / 2) + 'px';
                dropdownMenu.style.transform = 'translateX(-50%)';
                dropdownMenu.style.zIndex = '10000';
            }
            
            // Position on hover
            dropdown.addEventListener('mouseenter', positionDropdown);
            navItemLink.addEventListener('mouseenter', positionDropdown);
            
            // Prevent page scroll when scrolling inside dropdown
            dropdownMenu.addEventListener('wheel', function(e) {
                const dropdownMenu = this;
                const canScrollUp = dropdownMenu.scrollTop > 0;
                const canScrollDown = dropdownMenu.scrollTop < (dropdownMenu.scrollHeight - dropdownMenu.clientHeight);
                
                if ((e.deltaY < 0 && canScrollUp) || (e.deltaY > 0 && canScrollDown)) {
                    e.stopPropagation();
                }
            }, { passive: false });
            
            // Update position when scrolling or resizing
            function updatePosition() {
                if (dropdown.classList.contains('dropdown-open')) {
                    positionDropdown();
                }
            }
            
            window.addEventListener('scroll', updatePosition, true);
            window.addEventListener('resize', updatePosition);
        });
    }
    
    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initDropdowns);
    } else {
        initDropdowns();
    }
    
    // Re-init on resize to handle desktop/mobile switching
    window.addEventListener('resize', function() {
        if (window.innerWidth > 767) {
            initDropdowns();
        }
    });
})();

// Auto-hide messages
setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.style.transition = 'opacity 0.5s ease';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 500);
    });
}, 5000);

