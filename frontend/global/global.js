// global.js
function confirmDelete() {
    return window.confirm("Are you sure you want to delete this record? This action cannot be undone.");
}

// Auto-dismiss flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const flashes = document.querySelectorAll('.flash');
        flashes.forEach(f => {
            f.style.transition = "opacity 0.4s ease";
            f.style.opacity = "0";
            setTimeout(() => f.remove(), 400);
        });
    }, 5000);
    
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        // Check if the current route starts with the link's href...
        // ...but only if the link isn't just '/' (dashboard/index).
        if (linkPath === currentPath || (linkPath !== '/' && currentPath.startsWith(linkPath))) {
            link.classList.add('active');
        }
    });
});

// Custom Select Component Logic
function initCustomSelects() {
    const selects = document.querySelectorAll('select:not(.custom-select-initialized)');
    
    selects.forEach(select => {
        select.classList.add('custom-select-initialized');
        
        // Hide native select visually but keep it focusable and validatable
        select.style.opacity = '0';
        select.style.position = 'absolute';
        select.style.pointerEvents = 'none';
        
        const wrapper = document.createElement('div');
        wrapper.className = 'custom-select-wrapper';
        
        const trigger = document.createElement('div');
        trigger.className = 'custom-select-trigger';
        if (select.disabled || select.hasAttribute('disabled')) {
            trigger.classList.add('disabled');
        }
        
        // Initial selected text
        let selectedOption = select.options[select.selectedIndex];
        let placeholder = select.getAttribute('placeholder') || 'Select...';
        let initialText = selectedOption ? selectedOption.text : placeholder;
        
        trigger.innerHTML = `<span>${initialText}</span><svg opacity="0.5" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transition: transform 0.2s;"><polyline points="6 9 12 15 18 9"></polyline></svg>`;
        
        const optionsList = document.createElement('div');
        optionsList.className = 'custom-options';

        const optionsContainer = document.createElement('div');
        optionsContainer.className = 'custom-options-list';

        const enableSearch = select.hasAttribute('data-searchable');
        let searchInput = null;
        let emptyState = null;

        if (enableSearch) {
            const searchWrap = document.createElement('div');
            searchWrap.className = 'custom-search-wrap';

            searchInput = document.createElement('input');
            searchInput.type = 'text';
            searchInput.className = 'custom-select-search';
            searchInput.placeholder = select.getAttribute('data-search-placeholder') || 'Search...';

            searchInput.addEventListener('click', (e) => e.stopPropagation());
            searchInput.addEventListener('keydown', (e) => e.stopPropagation());

            searchWrap.appendChild(searchInput);
            optionsList.appendChild(searchWrap);
        }
        
        Array.from(select.options).forEach(option => {
            const opt = document.createElement('div');
            opt.className = 'custom-option';
            if (option.selected) opt.classList.add('selected');
            if (!option.value) opt.classList.add('placeholder-option'); 
            
            opt.textContent = option.text;
            opt.dataset.value = option.value;
            
            opt.addEventListener('click', (e) => {
                e.stopPropagation();
                
                // Update native select
                select.value = opt.dataset.value;
                select.dispatchEvent(new Event('change'));
                
                // Update Visual Trigger
                trigger.querySelector('span').textContent = opt.textContent;
                
                // Update selected classes 
                optionsList.querySelectorAll('.custom-option').forEach(o => o.classList.remove('selected'));
                opt.classList.add('selected');

                if (searchInput) {
                    searchInput.value = '';
                    optionsContainer.querySelectorAll('.custom-option').forEach(o => {
                        o.style.display = '';
                    });
                    if (emptyState) {
                        emptyState.style.display = 'none';
                    }
                }
                
                // Close Menu
                wrapper.classList.remove('open');
            });
            optionsContainer.appendChild(opt);
        });

        if (enableSearch) {
            emptyState = document.createElement('div');
            emptyState.className = 'custom-option-empty';
            emptyState.textContent = 'No matches found.';
            emptyState.style.display = 'none';
            optionsList.appendChild(emptyState);

            searchInput.addEventListener('input', () => {
                const term = searchInput.value.trim().toLowerCase();
                let visibleCount = 0;

                optionsContainer.querySelectorAll('.custom-option').forEach(opt => {
                    if (opt.classList.contains('placeholder-option')) {
                        opt.style.display = term ? 'none' : '';
                        return;
                    }

                    const isMatch = opt.textContent.toLowerCase().includes(term);
                    opt.style.display = isMatch ? '' : 'none';
                    if (isMatch) visibleCount++;
                });

                emptyState.style.display = visibleCount === 0 ? 'block' : 'none';
            });
        }

        optionsList.appendChild(optionsContainer);
        
        wrapper.appendChild(trigger);
        wrapper.appendChild(optionsList);
        
        select.parentNode.insertBefore(wrapper, select.nextSibling);

        // Open/Close toggle
        trigger.addEventListener('click', (e) => {
            if (trigger.classList.contains('disabled')) return;
            e.preventDefault();
            e.stopPropagation();
            
            // Close all other open selects
            document.querySelectorAll('.custom-select-wrapper.open').forEach(w => {
                if (w !== wrapper) w.classList.remove('open');
            });
            
            wrapper.classList.toggle('open');

            if (wrapper.classList.contains('open') && searchInput) {
                searchInput.focus();
            }
        });
    });
    
    // Clicking outside closes the dropdown
    document.addEventListener('click', () => {
        document.querySelectorAll('.custom-select-wrapper.open').forEach(w => w.classList.remove('open'));
    });
}

document.addEventListener('DOMContentLoaded', initCustomSelects);

function initPageTransitions() {
    const mainContent = document.querySelector('.main-content');
    if (!mainContent) return;

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!reduceMotion) {
        mainContent.classList.add('page-enter');
        requestAnimationFrame(() => {
            mainContent.classList.remove('page-enter');
        });
    }

    document.addEventListener('click', (event) => {
        const link = event.target.closest('a[href]');
        if (!link) return;

        if (link.target === '_blank' || link.hasAttribute('download')) return;

        const href = link.getAttribute('href');
        if (!href) return;
        if (href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:') || href.startsWith('javascript:')) return;

        if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;

        const nextUrl = new URL(link.href, window.location.href);
        if (nextUrl.origin !== window.location.origin) return;

        const isSamePageAnchor =
            nextUrl.pathname === window.location.pathname &&
            nextUrl.search === window.location.search &&
            nextUrl.hash;
        if (isSamePageAnchor) return;

        event.preventDefault();

        if (reduceMotion) {
            window.location.assign(nextUrl.href);
            return;
        }

        mainContent.classList.add('page-leave');
        window.setTimeout(() => {
            window.location.assign(nextUrl.href);
        }, 170);
    }, true);
}

document.addEventListener('DOMContentLoaded', initPageTransitions);
