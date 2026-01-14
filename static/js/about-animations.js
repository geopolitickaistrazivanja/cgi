// Modern scroll animations for About page - List items with staggered animation
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
        
        // Create Intersection Observer for list container
        const listObserverOptions = {
            root: null,
            rootMargin: '0px 0px -10% 0px',
            threshold: 0.1
        };
        
        const listObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const listContainer = entry.target;
                    const listItems = listContainer.querySelectorAll('.scroll-list-item');
                    
                    // Animate each list item with stagger effect
                    listItems.forEach((item, index) => {
                        setTimeout(() => {
                            item.classList.add('is-visible');
                        }, index * 80); // 80ms delay between each item
                    });
                    
                    listObserver.unobserve(listContainer);
                }
            });
        }, listObserverOptions);
        
        // Observe the monographs list container
        const monographsList = document.querySelector('.monographs-list');
        if (monographsList) {
            listObserver.observe(monographsList);
        }
    }
    
    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAboutAnimations);
    } else {
        initAboutAnimations();
    }
})();