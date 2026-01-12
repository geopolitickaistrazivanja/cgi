// Mobile menu toggle
(function() {
    'use strict';
    
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const offcanvas = document.getElementById('offcanvas');
    const offcanvasClose = document.getElementById('offcanvasClose');
    const body = document.body;
    
    if (mobileMenuBtn && offcanvas) {
        mobileMenuBtn.addEventListener('click', function() {
            offcanvas.classList.add('open');
            body.classList.add('offcanvas-open');
        });
    }
    
    if (offcanvasClose) {
        offcanvasClose.addEventListener('click', function() {
            offcanvas.classList.remove('open');
            body.classList.remove('offcanvas-open');
        });
    }
})();

// Search overlay toggle
(function() {
    'use strict';
    
    const searchBtn = document.getElementById('searchBtn');
    const searchBtnMobile = document.getElementById('searchBtnMobile');
    const searchOverlay = document.getElementById('searchOverlay');
    const searchClose = document.getElementById('searchClose');
    const searchInput = document.getElementById('searchInput');
    const body = document.body;
    
    function openSearch() {
        if (searchOverlay) {
            searchOverlay.classList.add('active');
            body.classList.add('search-active');
            if (searchInput) {
                setTimeout(() => {
                    searchInput.focus();
                }, 100);
            }
        }
    }
    
    function closeSearch() {
        if (searchOverlay) {
            searchOverlay.classList.remove('active');
            body.classList.remove('search-active');
            if (searchInput) {
                searchInput.value = '';
            }
        }
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
    
    if (searchOverlay) {
        searchOverlay.addEventListener('click', function(e) {
            if (e.target === searchOverlay) {
                closeSearch();
            }
        });
    }
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && searchOverlay && searchOverlay.classList.contains('active')) {
            closeSearch();
        }
    });
})();

// Offcanvas menu navigation
(function() {
    'use strict';
    
    const offcanvasLinks = document.querySelectorAll('.offcanvas-item:not(.offcanvas-item-parent)');
    const offcanvas = document.getElementById('offcanvas');
    const body = document.body;
    
    offcanvasLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href && href !== '#' && !this.closest('.offcanvas-item-dropdown')) {
                e.preventDefault();
                offcanvas.classList.remove('open');
                body.classList.remove('offcanvas-open');
                setTimeout(function() {
                    window.location.href = href;
                }, 200);
            }
        });
    });
})();

// Offcanvas dropdown toggle
(function() {
    'use strict';
    
    const offcanvasDropdownToggles = document.querySelectorAll('.offcanvas-dropdown-toggle');
    
    offcanvasDropdownToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const dropdown = this.closest('.offcanvas-item-dropdown');
            if (dropdown) {
                dropdown.classList.toggle('open');
            }
        });
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.offcanvas-item-dropdown')) {
            offcanvasDropdownToggles.forEach(function(toggle) {
                const dropdown = toggle.closest('.offcanvas-item-dropdown');
                if (dropdown && dropdown.classList.contains('open')) {
                    dropdown.classList.remove('open');
                }
            });
        }
    });
})();

// Desktop dropdown scroll handling
(function() {
    'use strict';
    
    document.addEventListener('DOMContentLoaded', function() {
        const dropdownMenus = document.querySelectorAll('.dropdown-menu');
        
        dropdownMenus.forEach(function(dropdownMenu) {
            dropdownMenu.addEventListener('wheel', function(e) {
                const { scrollTop, scrollHeight, clientHeight } = dropdownMenu;
                const deltaY = e.deltaY;
                const scrollingDown = deltaY > 0;
                const scrollingUp = deltaY < 0;
                
                // Calculate maximum scroll position with small tolerance for rounding
                const maxScrollTop = Math.max(0, scrollHeight - clientHeight);
                const tolerance = 1; // 1px tolerance for floating point precision
                
                // Check current position relative to limits (with more aggressive tolerance)
                const isAtTop = scrollTop <= tolerance;
                const isAtBottom = scrollTop >= (maxScrollTop - tolerance);
                
                // If at top and trying to scroll up, allow page scroll immediately
                if (isAtTop && scrollingUp) {
                    // Don't prevent anything, let event bubble naturally to page
                    return;
                }
                
                // If at bottom and trying to scroll down, allow page scroll immediately
                if (isAtBottom && scrollingDown) {
                    // Don't prevent anything, let event bubble naturally to page
                    return;
                }
                
                // Also check if we're very close to the limits (within 5px) and scrolling toward them
                const nearTop = scrollTop <= 5 && scrollingUp;
                const nearBottom = scrollTop >= (maxScrollTop - 5) && scrollingDown;
                
                if (nearTop || nearBottom) {
                    // Allow page scroll when very close to limits
                    return;
                }
                
                // Check if scroll would exceed bounds (predictive check)
                const newScrollTop = scrollTop + deltaY;
                const wouldExceedTop = newScrollTop < -tolerance;
                const wouldExceedBottom = newScrollTop > (maxScrollTop + tolerance);
                
                // If scroll would exceed bounds, allow page scroll immediately
                if (wouldExceedTop || wouldExceedBottom) {
                    return; // Don't prevent, let page scroll
                }
                
                // Check if we can actually scroll in the requested direction
                const canScrollInDirection = scrollingDown ? scrollTop < maxScrollTop : scrollTop > 0;
                
                // If we can't scroll in the requested direction, allow page scroll
                if (!canScrollInDirection) {
                    return; // Don't prevent, let page scroll
                }
                
                // Otherwise, prevent page scroll and let dropdown scroll naturally
                e.stopPropagation();
            }, { passive: false });
        });
    });
})();