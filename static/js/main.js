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

// Language Switcher Click Toggle (Desktop and Mobile)
(function() {
    'use strict';
    
    document.addEventListener('DOMContentLoaded', function() {
        // Desktop language switcher
        const desktopLangBtn = document.getElementById('languageSwitcherBtn');
        const desktopLangSwitcher = desktopLangBtn ? desktopLangBtn.closest('.language-switcher-desktop') : null;
        const desktopLangMenu = document.getElementById('languageDropdownMenu');
        
        // Mobile language switcher
        const mobileLangBtn = document.getElementById('languageSwitcherMobileBtn');
        const mobileLangSwitcher = mobileLangBtn ? mobileLangBtn.closest('.language-switcher-mobile') : null;
        const mobileLangMenu = document.getElementById('languageDropdownMenuMobile');
        
        // Toggle desktop dropdown
        if (desktopLangBtn && desktopLangSwitcher) {
            desktopLangBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                const isOpen = desktopLangSwitcher.classList.contains('open');
                
                if (isOpen) {
                    desktopLangSwitcher.classList.remove('open');
                    desktopLangBtn.setAttribute('aria-expanded', 'false');
                } else {
                    // Close any other open language switchers
                    if (mobileLangSwitcher) {
                        mobileLangSwitcher.classList.remove('open');
                        mobileLangBtn.setAttribute('aria-expanded', 'false');
                    }
                    desktopLangSwitcher.classList.add('open');
                    desktopLangBtn.setAttribute('aria-expanded', 'true');
                }
            });
        }
        
        // Toggle mobile dropdown
        if (mobileLangBtn && mobileLangSwitcher) {
            mobileLangBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                const isOpen = mobileLangSwitcher.classList.contains('open');
                
                if (isOpen) {
                    mobileLangSwitcher.classList.remove('open');
                    mobileLangBtn.setAttribute('aria-expanded', 'false');
                } else {
                    // Close any other open language switchers
                    if (desktopLangSwitcher) {
                        desktopLangSwitcher.classList.remove('open');
                        desktopLangBtn.setAttribute('aria-expanded', 'false');
                    }
                    mobileLangSwitcher.classList.add('open');
                    mobileLangBtn.setAttribute('aria-expanded', 'true');
                }
            });
        }
        
        // Handle language switching - convert URL paths correctly
        function convertPathForLanguage(path, targetLang) {
            let converted = path;
            
            // First, remove the language prefix (Django will add it back, but we need correct structure)
            // Remove current language prefixes to get base path - handle with or without leading slash
            converted = converted.replace(/^\/(en|sr-latn|sr-cyrl)\//, '/');
            // Also handle if path starts directly with language code (shouldn't happen but safety)
            if (converted.match(/^\/?(en|sr-latn|sr-cyrl)\//)) {
                converted = converted.replace(/^\/(en|sr-latn|sr-cyrl)\//, '/');
            }
            
            // Handle accounts URLs
            if (converted.includes('/korisnici/') || converted.includes('/users/')) {
                if (targetLang === 'en') {
                    // Convert to English structure
                    converted = converted.replace(/\/korisnici\//g, '/users/');
                    converted = converted.replace(/\/registracija\//g, '/register/');
                    converted = converted.replace(/\/prijava\//g, '/login/');
                    converted = converted.replace(/\/odjava\//g, '/logout/');
                    converted = converted.replace(/\/nalog\//g, '/account/');
                } else {
                    // Convert to Serbian structure
                    converted = converted.replace(/\/users\//g, '/korisnici/');
                    converted = converted.replace(/\/register\//g, '/registracija/');
                    converted = converted.replace(/\/login\//g, '/prijava/');
                    converted = converted.replace(/\/logout\//g, '/odjava/');
                    converted = converted.replace(/\/account\//g, '/nalog/');
                }
            }
            
            // Handle topics URLs
            if (converted.includes('/teme/') || converted.includes('/topics/')) {
                if (targetLang === 'en') {
                    converted = converted.replace(/\/teme\//g, '/topics/');
                } else {
                    converted = converted.replace(/\/topics\//g, '/teme/');
                }
            }
            
            // Handle core URLs (about, contact)
            if (converted.includes('/o-nama/') || converted.includes('/about/')) {
                if (targetLang === 'en') {
                    converted = converted.replace(/\/o-nama\//g, '/about/');
                } else {
                    converted = converted.replace(/\/about\//g, '/o-nama/');
                }
            }
            
            if (converted.includes('/kontakt/') || converted.includes('/contact/')) {
                if (targetLang === 'en') {
                    converted = converted.replace(/\/kontakt\//g, '/contact/');
                } else {
                    converted = converted.replace(/\/contact\//g, '/kontakt/');
                }
            }
            
            return converted;
        }
        
        // Set up language switcher buttons to update next URL
        const languageNextDesktop = document.getElementById('languageNextDesktop');
        const languageNextMobile = document.getElementById('languageNextMobile');
        
        // Update language switcher forms to convert paths before submit
        // Use mousedown to ensure we capture the language code before form submits
        if (desktopLangMenu) {
            const desktopButtons = desktopLangMenu.querySelectorAll('button[type="submit"][data-lang-code]');
            desktopButtons.forEach(function(button) {
                button.addEventListener('mousedown', function(e) {
                    const targetLang = this.getAttribute('data-lang-code');
                    if (targetLang && languageNextDesktop) {
                        const currentPath = languageNextDesktop.value || window.location.pathname;
                        languageNextDesktop.value = convertPathForLanguage(currentPath, targetLang);
                    }
                });
            });
            // Also handle submit event as fallback
            desktopLangMenu.addEventListener('submit', function(e) {
                if (e.submitter) {
                    const targetLang = e.submitter.getAttribute('data-lang-code');
                    if (targetLang && languageNextDesktop) {
                        const currentPath = languageNextDesktop.value || window.location.pathname;
                        languageNextDesktop.value = convertPathForLanguage(currentPath, targetLang);
                    }
                }
            });
        }
        
        if (mobileLangMenu) {
            const mobileButtons = mobileLangMenu.querySelectorAll('button[type="submit"][data-lang-code]');
            mobileButtons.forEach(function(button) {
                button.addEventListener('mousedown', function(e) {
                    const targetLang = this.getAttribute('data-lang-code');
                    if (targetLang && languageNextMobile) {
                        const currentPath = languageNextMobile.value || window.location.pathname;
                        languageNextMobile.value = convertPathForLanguage(currentPath, targetLang);
                    }
                });
            });
            // Also handle submit event as fallback
            mobileLangMenu.addEventListener('submit', function(e) {
                if (e.submitter) {
                    const targetLang = e.submitter.getAttribute('data-lang-code');
                    if (targetLang && languageNextMobile) {
                        const currentPath = languageNextMobile.value || window.location.pathname;
                        languageNextMobile.value = convertPathForLanguage(currentPath, targetLang);
                    }
                }
            });
        }
        
        // Close language dropdowns when clicking outside
        document.addEventListener('click', function(e) {
            if (desktopLangSwitcher && !desktopLangSwitcher.contains(e.target)) {
                desktopLangSwitcher.classList.remove('open');
                if (desktopLangBtn) {
                    desktopLangBtn.setAttribute('aria-expanded', 'false');
                }
            }
            if (mobileLangSwitcher && !mobileLangSwitcher.contains(e.target)) {
                mobileLangSwitcher.classList.remove('open');
                if (mobileLangBtn) {
                    mobileLangBtn.setAttribute('aria-expanded', 'false');
                }
            }
        });
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
                
                // Calculate maximum scroll position
                const maxScrollTop = Math.max(0, scrollHeight - clientHeight);
                
                // Check if we can scroll in the requested direction
                const canScrollDown = scrollTop < maxScrollTop;
                const canScrollUp = scrollTop > 0;
                
                // If we can't scroll in the requested direction, allow page scroll immediately
                if ((scrollingDown && !canScrollDown) || (scrollingUp && !canScrollUp)) {
                    // Don't prevent anything - let the event bubble to the page
                    return;
                }
                
                // Check if the scroll would exceed bounds (predictive check)
                const newScrollTop = scrollTop + deltaY;
                const wouldExceedTop = newScrollTop < 0;
                const wouldExceedBottom = newScrollTop > maxScrollTop;
                
                // If scroll would exceed bounds, allow page scroll immediately
                if (wouldExceedTop || wouldExceedBottom) {
                    // Don't prevent anything - let the event bubble to the page
                    return;
                }
                
                // Otherwise, we can scroll the dropdown, so prevent page scroll
                e.stopPropagation();
            }, { passive: false });
        });
    });
})();