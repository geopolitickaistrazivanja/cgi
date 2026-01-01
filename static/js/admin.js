// Django Admin Customizations
document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    // Force light theme - remove any dark theme attributes
    if (document.documentElement.hasAttribute('data-theme')) {
        document.documentElement.removeAttribute('data-theme');
    }
    if (document.documentElement.classList.contains('dark')) {
        document.documentElement.classList.remove('dark');
    }
    // Ensure light theme is set
    document.documentElement.setAttribute('data-theme', 'light');
    
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
    
    // Translate breadcrumbs
    const breadcrumbs = document.querySelector('.breadcrumbs');
    if (breadcrumbs) {
        const breadcrumbLinks = breadcrumbs.querySelectorAll('a');
        breadcrumbLinks.forEach(function(link) {
            const text = link.textContent.trim();
            // Translate "Home"
            if (text === 'Home') {
                link.textContent = 'Početna';
            }
            // Translate app names
            else if (text === 'Blog') {
                link.textContent = 'Blog';
            }
            else if (text === 'Accounts') {
                link.textContent = 'Nalozi';
            }
            else if (text === 'Core') {
                link.textContent = 'Osnovno';
            }
            else if (text === 'Shop') {
                link.textContent = 'Prodavnica';
            }
            else if (text === 'Authentication and Authorization' || text === 'Authentication & Authorization') {
                link.textContent = 'Autentifikacija i autorizacija';
            }
        });
        
        // Also translate any text nodes in breadcrumbs (non-link text)
        const breadcrumbText = breadcrumbs.textContent;
        if (breadcrumbText.includes('Home')) {
            // Replace "Home" in the entire breadcrumb text
            breadcrumbs.innerHTML = breadcrumbs.innerHTML.replace(/Home/g, 'Početna');
        }
    }
    
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
        } else if (text === 'Users') {
            caption.textContent = 'Korisnici';
        }
    });
    
    // Translate "Users" in module links
    const moduleLinks = document.querySelectorAll('.module a');
    moduleLinks.forEach(function(link) {
        const text = link.textContent.trim();
        if (text === 'Users') {
            link.textContent = 'Korisnici';
        }
    });
    
    // Translate table headers
    const tableHeaders = document.querySelectorAll('thead th, .results th');
    tableHeaders.forEach(function(th) {
        const link = th.querySelector('a');
        if (link) {
            const text = link.textContent.trim();
            if (text === 'Username') {
                link.textContent = 'Korisničko ime';
            } else if (text === 'Email address') {
                link.textContent = 'Email adresa';
            } else if (text === 'First name') {
                link.textContent = 'Ime';
            } else if (text === 'Last name') {
                link.textContent = 'Prezime';
            } else if (text === 'Staff status') {
                link.textContent = 'Status osoblja';
            } else if (text === 'Superuser status') {
                link.textContent = 'Status superkorisnika';
            } else if (text === 'Active') {
                link.textContent = 'Aktivan';
            } else if (text === 'Date joined') {
                link.textContent = 'Datum registracije';
            } else if (text === 'Last login') {
                link.textContent = 'Poslednja prijava';
            }
        }
        // Also check text content directly (for non-link headers)
        const text = th.textContent.trim();
        if (text.includes('Username') && !text.includes('Korisničko ime')) {
            th.innerHTML = th.innerHTML.replace(/Username/g, 'Korisničko ime');
        }
        if (text.includes('Email address') && !text.includes('Email adresa')) {
            th.innerHTML = th.innerHTML.replace(/Email address/g, 'Email adresa');
        }
        if (text.includes('First name') && !text.includes('Ime')) {
            th.innerHTML = th.innerHTML.replace(/First name/g, 'Ime');
        }
        if (text.includes('Last name') && !text.includes('Prezime')) {
            th.innerHTML = th.innerHTML.replace(/Last name/g, 'Prezime');
        }
        if (text.includes('Staff status') && !text.includes('Status osoblja')) {
            th.innerHTML = th.innerHTML.replace(/Staff status/g, 'Status osoblja');
        }
    });
    
    // Translate common buttons
    const saveButton = document.querySelector('input[name="_save"]');
    if (saveButton && saveButton.value === 'Save') {
        saveButton.value = 'Sačuvaj';
    }
    
    const saveAddAnotherButton = document.querySelector('input[name="_addanother"]');
    if (saveAddAnotherButton && saveAddAnotherButton.value === 'Save and add another') {
        saveAddAnotherButton.value = 'Sačuvaj i dodaj novi';
    }
    
    const saveContinueButton = document.querySelector('input[name="_continue"]');
    if (saveContinueButton && saveContinueButton.value === 'Save and continue editing') {
        saveContinueButton.value = 'Sačuvaj i nastavi sa izmenama';
    }
    
    const deleteButton = document.querySelector('a.deletelink, .deletelink-button');
    if (deleteButton && deleteButton.textContent.trim() === 'Delete') {
        deleteButton.textContent = 'Obriši';
    }
    
    // Translate "Change" links
    const changeLinks = document.querySelectorAll('a[href*="/change/"]');
    changeLinks.forEach(function(link) {
        if (link.textContent.trim() === 'Change') {
            link.textContent = 'Izmeni';
        }
    });
    
    // Translate "View on site" links
    const viewOnSiteLinks = document.querySelectorAll('.viewsitelink');
    viewOnSiteLinks.forEach(function(link) {
        if (link.textContent.trim() === 'View on site') {
            link.textContent = 'Pogledaj na sajtu';
        }
    });
    
    // Translate "History" links
    const historyLinks = document.querySelectorAll('a[href*="/history/"]');
    historyLinks.forEach(function(link) {
        if (link.textContent.trim() === 'History') {
            link.textContent = 'Istorija';
        }
    });
    
    // Translate pagination text
    const pagination = document.querySelector('.paginator');
    if (pagination) {
        let paginationText = pagination.textContent;
        paginationText = paginationText.replace(/Showing (\d+) to (\d+) of (\d+) results?/g, 'Prikazano $1 do $2 od $3 rezultata');
        paginationText = paginationText.replace(/Show all/g, 'Prikaži sve');
        paginationText = paginationText.replace(/Previous/g, 'Prethodno');
        paginationText = paginationText.replace(/Next/g, 'Sledeće');
        if (pagination.textContent !== paginationText) {
            pagination.textContent = paginationText;
        }
    }
    
    // Translate "No results found" or similar messages
    const noResults = document.querySelector('.no-results, .empty-form');
    if (noResults) {
        let noResultsText = noResults.textContent;
        if (noResultsText.includes('No results found') || noResultsText.includes('No')) {
            noResultsText = noResultsText.replace(/No results found/g, 'Nema rezultata');
            noResultsText = noResultsText.replace(/^No$/g, 'Ne');
            if (noResults.textContent !== noResultsText) {
                noResults.textContent = noResultsText;
            }
        }
    }
    
    // Translate delete confirmation text
    const deleteConfirm = document.querySelector('.delete-confirmation, .deletelink-confirmation');
    if (deleteConfirm) {
        let confirmText = deleteConfirm.textContent;
        confirmText = confirmText.replace(/Yes, I'm sure/g, 'Da, siguran sam');
        confirmText = confirmText.replace(/The following objects will be deleted:/g, 'Sledeći objekti će biti obrisani:');
        confirmText = confirmText.replace(/Are you sure you want to delete/g, 'Da li ste sigurni da želite da obrišete');
        if (deleteConfirm.textContent !== confirmText) {
            deleteConfirm.textContent = confirmText;
        }
    }
    
    // Translate "Select all" text
    const selectAllLinks = document.querySelectorAll('.selector-chosen a, .selector-available a');
    selectAllLinks.forEach(function(link) {
        if (link.textContent.trim() === 'Choose all') {
            link.textContent = 'Izaberi sve';
        } else if (link.textContent.trim() === 'Remove all') {
            link.textContent = 'Ukloni sve';
        }
    });
    
    // Translate filter labels
    const filterLabels = document.querySelectorAll('#changelist-filter h3, .filter-list h3');
    filterLabels.forEach(function(label) {
        const text = label.textContent.trim();
        if (text === 'By date') {
            label.textContent = 'Po datumu';
        } else if (text === 'By status') {
            label.textContent = 'Po statusu';
        } else if (text === 'By type') {
            label.textContent = 'Po tipu';
        }
    });
});

