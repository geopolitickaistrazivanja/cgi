// Modern scroll animations using Intersection Observer API
(function() {
    'use strict';
    
    // Initialize animations when DOM is ready
    function initScrollAnimations() {
        // Check if Intersection Observer is supported
        if (!('IntersectionObserver' in window)) {
            // Fallback: show all elements immediately
            document.querySelectorAll('.scroll-fade-in, .scroll-slide-left, .scroll-slide-right, .scroll-scale, .content-image, .content-images-grid').forEach(el => {
                el.classList.add('is-visible');
            });
            return;
        }
        
        // Create Intersection Observer with modern options
        const observerOptions = {
            root: null, // Use viewport as root
            rootMargin: '0px 0px -15% 0px', // Trigger when element is 15% from bottom of viewport
            threshold: [0, 0.1, 0.2] // Multiple thresholds for smoother triggering
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    // Unobserve after animation completes to improve performance
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);
        
        // Observe all elements with scroll animation classes
        const animatedElements = document.querySelectorAll(
            '.scroll-fade-in, .scroll-slide-left, .scroll-slide-right, .scroll-scale, .content-image, .content-images-grid, .content-section-image-layout, .author-images-grid'
        );
        
        animatedElements.forEach(element => {
            observer.observe(element);
        });
    }
    
    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initScrollAnimations);
    } else {
        initScrollAnimations();
    }
})();
