// Modern scroll animations for About page - List items with individual reveal animation
(function() {
    'use strict';
    
    // Initialize animations when DOM is ready
    function initAboutAnimations() {
        // Check if Intersection Observer is supported
        if (!('IntersectionObserver' in window)) {
            // Fallback: show all elements immediately
            document.querySelectorAll('.scroll-list-item').forEach(el => {
                el.classList.add('is-visible');
            });
            return;
        }
        
        // Create Intersection Observer for individual list items
        const itemObserverOptions = {
            root: null,
            rootMargin: '0px 0px -10% 0px',
            threshold: 0.1
        };
        
        const itemObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    itemObserver.unobserve(entry.target);
                }
            });
        }, itemObserverOptions);
        
        // Observe each list item individually
        const listItems = document.querySelectorAll('.scroll-list-item');
        listItems.forEach(item => {
            itemObserver.observe(item);
        });
    }
    
    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAboutAnimations);
    } else {
        initAboutAnimations();
    }
})();