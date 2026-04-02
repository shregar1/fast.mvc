/**
 * FastX Theme Sync
 * Synchronizes dark/light mode across Launch Page, Swagger UI, and Docs
 */

(function() {
    'use strict';

    const STORAGE_KEY = 'theme';
    const THEME_DARK = 'dark';
    const THEME_LIGHT = 'light';

    /**
     * Get the current theme from localStorage or default to dark
     */
    function getStoredTheme() {
        try {
            return localStorage.getItem(STORAGE_KEY) || THEME_DARK;
        } catch (e) {
            return THEME_DARK;
        }
    }

    /**
     * Save theme to localStorage
     */
    function setStoredTheme(theme) {
        try {
            localStorage.setItem(STORAGE_KEY, theme);
        } catch (e) {
            // Ignore storage errors
        }
    }

    /**
     * Apply theme to MkDocs Material
     */
    function applyMkDocsTheme(theme) {
        const body = document.body;

        if (theme === THEME_LIGHT) {
            body.setAttribute('data-md-color-scheme', 'default');
            body.setAttribute('data-md-color-primary', 'cyan');
        } else {
            body.setAttribute('data-md-color-scheme', 'slate');
            body.setAttribute('data-md-color-primary', 'cyan');
        }
    }

    /**
     * Sync theme from localStorage on page load
     */
    function syncTheme() {
        const storedTheme = getStoredTheme();

        // Check if there's a mismatch between stored theme and current theme
        const currentScheme = document.body.getAttribute('data-md-color-scheme');
        const expectedScheme = storedTheme === THEME_LIGHT ? 'default' : 'slate';

        if (currentScheme !== expectedScheme) {
            applyMkDocsTheme(storedTheme);
        }
    }

    /**
     * Listen for theme toggle clicks and sync to localStorage
     */
    function setupThemeListener() {
        // Watch for changes to data-md-color-scheme attribute
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'attributes' && mutation.attributeName === 'data-md-color-scheme') {
                    const scheme = document.body.getAttribute('data-md-color-scheme');
                    const theme = scheme === 'default' ? THEME_LIGHT : THEME_DARK;
                    setStoredTheme(theme);
                }
            });
        });

        observer.observe(document.body, {
            attributes: true,
            attributeFilter: ['data-md-color-scheme']
        });
    }

    /**
     * Initialize theme sync
     */
    function init() {
        // Apply stored theme on load
        syncTheme();

        // Set up listener for theme changes
        setupThemeListener();

        // Listen for storage events from other pages
        window.addEventListener('storage', function(e) {
            if (e.key === STORAGE_KEY) {
                const newTheme = e.newValue || THEME_DARK;
                applyMkDocsTheme(newTheme);
            }
        });
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
