// Django Admin Customizations
document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    // Translate actions dropdown
    const actionSelect = document.querySelector('.actions select[name="action"]');
    if (actionSelect) {
        const options = actionSelect.querySelectorAll('option');
        options.forEach(function(option) {
            if (option.value === '') {
                option.textContent = '---------';
            } else if (option.textContent.includes('Delete selected')) {
                // Extract model name and translate
                const modelMatch = option.textContent.match(/Delete selected (.+)/);
                if (modelMatch) {
                    option.textContent = 'Obriši izabrane ' + modelMatch[1];
                } else {
                    option.textContent = 'Obriši izabrane';
                }
            }
        });
        
        // Translate label
        const label = actionSelect.closest('.actions')?.querySelector('label');
        if (label && label.textContent.includes('Action:')) {
            label.innerHTML = label.innerHTML.replace('Action:', 'Akcija:');
        }
    }
    
    // Translate action counter
    const actionCounter = document.querySelector('.action-counter');
    if (actionCounter) {
        const text = actionCounter.textContent;
        // Replace "X of Y selected" with Serbian
        const match = text.match(/(\d+)\s+of\s+(\d+)\s+selected/);
        if (match) {
            actionCounter.textContent = match[1] + ' od ' + match[2] + ' izabrano';
        }
    }
    
    // Translate "Go" button
    const goButton = document.querySelector('.actions button[type="submit"][name="index"]');
    if (goButton && (goButton.textContent.trim() === 'Go' || goButton.textContent.trim() === 'Izvrši')) {
        goButton.textContent = 'Izvrši';
    }
    
    // Translate search form
    const searchLabel = document.querySelector('#changelist-search label');
    if (searchLabel && searchLabel.textContent.includes('Search')) {
        // Label is usually just an image, so we check the placeholder
    }
    const searchInput = document.querySelector('#changelist-search input[type="text"]');
    if (searchInput && !searchInput.placeholder) {
        searchInput.placeholder = 'Pretraga';
    }
    const searchSubmit = document.querySelector('#changelist-search input[type="submit"]');
    if (searchSubmit && searchSubmit.value === 'Search') {
        searchSubmit.value = 'Pretraži';
    }
    
    // Translate "Add" links
    const addLinks = document.querySelectorAll('.object-tools .addlink');
    addLinks.forEach(function(link) {
        const text = link.textContent.trim();
        if (text.startsWith('Add ')) {
            const modelName = text.replace('Add ', '');
            link.textContent = 'Dodaj ' + modelName;
        }
    });
    
    // Translate app labels to Serbian
    const headings = document.querySelectorAll('h2, .module h2, .module caption');
    headings.forEach(function(heading) {
        const text = heading.textContent.trim();
        
        // Translate "Authentication and Authorization"
        if (text === 'Authentication and Authorization' || text === 'Authentication & Authorization') {
            heading.textContent = 'Autentifikacija i autorizacija';
        }
        // Translate "Accounts"
        else if (text === 'Accounts') {
            heading.textContent = 'Nalozi';
        }
        // Translate "Core"
        else if (text === 'Core') {
            heading.textContent = 'Osnovno';
        }
        // Translate "Shop"
        else if (text === 'Shop') {
            heading.textContent = 'Prodavnica';
        }
    });
    
    // Also check in module captions
    const captions = document.querySelectorAll('.module caption, .module h2');
    captions.forEach(function(caption) {
        const text = caption.textContent.trim();
        
        if (text === 'Authentication and Authorization' || text === 'Authentication & Authorization') {
            caption.textContent = 'Autentifikacija i autorizacija';
        } else if (text === 'Accounts') {
            caption.textContent = 'Nalozi';
        } else if (text === 'Core') {
            caption.textContent = 'Osnovno';
        } else if (text === 'Shop') {
            caption.textContent = 'Prodavnica';
        }
    });
});

