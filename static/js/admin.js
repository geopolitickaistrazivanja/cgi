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
    
    // Translate form field labels and help text
    const fieldLabels = document.querySelectorAll('label, .field-label, .form-row label');
    fieldLabels.forEach(function(label) {
        const text = label.textContent.trim();
        // Common field labels
        if (text === 'Username') {
            label.textContent = 'Korisničko ime';
        } else if (text === 'Email address') {
            label.textContent = 'Email adresa';
        } else if (text === 'First name') {
            label.textContent = 'Ime';
        } else if (text === 'Last name') {
            label.textContent = 'Prezime';
        } else if (text === 'Password') {
            label.textContent = 'Lozinka';
        } else if (text === 'Password confirmation') {
            label.textContent = 'Potvrda lozinke';
        } else if (text === 'Is active') {
            label.textContent = 'Je aktivan';
        } else if (text === 'Is staff') {
            label.textContent = 'Je osoblje';
        } else if (text === 'Is superuser') {
            label.textContent = 'Je superkorisnik';
        } else if (text === 'Date joined') {
            label.textContent = 'Datum registracije';
        } else if (text === 'Last login') {
            label.textContent = 'Poslednja prijava';
        } else if (text === 'Groups') {
            label.textContent = 'Grupe';
        } else if (text === 'User permissions') {
            label.textContent = 'Korisnička dozvola';
        } else if (text === 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.') {
            label.textContent = 'Obavezno. Maksimalno 150 karaktera. Samo slova, cifre i @/./+/-/_.';
        }
    });
    
    // Translate help text
    const helpTexts = document.querySelectorAll('.help, .help-block, .field-help');
    helpTexts.forEach(function(help) {
        let text = help.textContent.trim();
        if (text.includes('Required. 150 characters or fewer')) {
            text = text.replace(/Required\. 150 characters or fewer\. Letters, digits and @\/\.\/\+\/-\/_ only\./g, 'Obavezno. Maksimalno 150 karaktera. Samo slova, cifre i @/./+/-/_.');
            help.textContent = text;
        }
        if (text.includes('Enter the same password as before')) {
            text = text.replace(/Enter the same password as before/g, 'Unesite istu lozinku kao pre');
            help.textContent = text;
        }
    });
    
    // Translate inline form labels
    const inlineLabels = document.querySelectorAll('.inline-group h2, .inline-related h3');
    inlineLabels.forEach(function(label) {
        const text = label.textContent.trim();
        if (text.includes('Add another')) {
            label.textContent = text.replace(/Add another/g, 'Dodaj novi');
        } else if (text.includes('Delete')) {
            label.textContent = text.replace(/Delete/g, 'Obriši');
        }
    });
    
    // Translate "Add" button in inline forms
    const addInlineButtons = document.querySelectorAll('.add-row a, .add-row button');
    addInlineButtons.forEach(function(button) {
        if (button.textContent.trim() === 'Add another') {
            button.textContent = 'Dodaj novi';
        }
    });
    
    // Translate "Remove" in inline forms
    const removeInlineLinks = document.querySelectorAll('.delete a, .inline-deletelink');
    removeInlineLinks.forEach(function(link) {
        if (link.textContent.trim() === 'Delete') {
            link.textContent = 'Obriši';
        }
    });
    
    // Translate "Today" and date picker text
    const todayLinks = document.querySelectorAll('a[href*="today"]');
    todayLinks.forEach(function(link) {
        if (link.textContent.trim() === 'Today') {
            link.textContent = 'Danas';
        }
    });
    
    // Translate form errors
    const errorLists = document.querySelectorAll('.errorlist li');
    errorLists.forEach(function(error) {
        let text = error.textContent.trim();
        if (text.includes('This field is required')) {
            text = text.replace(/This field is required/g, 'Ovo polje je obavezno');
            error.textContent = text;
        } else if (text.includes('Enter a valid email address')) {
            text = text.replace(/Enter a valid email address/g, 'Unesite validnu email adresu');
            error.textContent = text;
        } else if (text.includes('This value may contain only letters, numbers and @/./+/-/_ characters')) {
            text = text.replace(/This value may contain only letters, numbers and @\/\.\/\+\/-\/_ characters/g, 'Ova vrednost može sadržati samo slova, cifre i @/./+/-/_ karaktere');
            error.textContent = text;
        }
    });
    
    // Translate success messages
    const successMessages = document.querySelectorAll('.success, .messagelist .success');
    successMessages.forEach(function(msg) {
        let text = msg.textContent.trim();
        if (text.includes('was added successfully')) {
            text = text.replace(/was added successfully/g, 'je uspešno dodat');
            msg.textContent = text;
        } else if (text.includes('was changed successfully')) {
            text = text.replace(/was changed successfully/g, 'je uspešno izmenjen');
            msg.textContent = text;
        } else if (text.includes('was deleted successfully')) {
            text = text.replace(/was deleted successfully/g, 'je uspešno obrisan');
            msg.textContent = text;
        }
    });
    
    // Translate "Select" in select boxes
    const selectOptions = document.querySelectorAll('select option');
    selectOptions.forEach(function(option) {
        if (option.textContent.trim() === '---------') {
            // Already translated
        } else if (option.textContent.trim() === 'Yes') {
            option.textContent = 'Da';
        } else if (option.textContent.trim() === 'No') {
            option.textContent = 'Ne';
        }
    });
    
    // Translate "Actions" in changelist
    const actionsHeaders = document.querySelectorAll('.actions h3, .actions label');
    actionsHeaders.forEach(function(header) {
        if (header.textContent.includes('Actions')) {
            header.textContent = header.textContent.replace(/Actions/g, 'Akcije');
        }
    });
    
    // Translate "Filter" if it appears anywhere
    const filterHeaders = document.querySelectorAll('h2:contains("Filter"), h3:contains("Filter")');
    filterHeaders.forEach(function(header) {
        if (header.textContent.includes('Filter')) {
            header.textContent = header.textContent.replace(/Filter/g, 'Filter');
        }
    });
    
    // Use MutationObserver to catch dynamically added content
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1) { // Element node
                    // Re-run translations on new content
                    const newHeadings = node.querySelectorAll ? node.querySelectorAll('h2, .module h2, .module caption') : [];
                    newHeadings.forEach(function(heading) {
                        const text = heading.textContent.trim();
                        if (text === 'Users') {
                            heading.textContent = 'Korisnici';
                        } else if (text === 'Authentication and Authorization' || text === 'Authentication & Authorization') {
                            heading.textContent = 'Autentifikacija i autorizacija';
                        } else if (text === 'Accounts') {
                            heading.textContent = 'Nalozi';
                        } else if (text === 'Core') {
                            heading.textContent = 'Osnovno';
                        } else if (text === 'Shop') {
                            heading.textContent = 'Prodavnica';
                        }
                    });
                }
            });
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});

