/**
 * Legal Disclaimer Modal
 * Shows on every page load for nasdaq.html and requires user acknowledgment
 * This appears BEFORE the onboarding modal
 */

function initDisclaimerModal() {
    // Wait for translations to be loaded
    if (typeof setLanguage === 'undefined' || typeof translations === 'undefined') {
        // If translations not loaded yet, wait a bit
        setTimeout(initDisclaimerModal, 100);
        return;
    }

    const overlay = document.getElementById('disclaimer-modal-overlay');
    const checkbox = document.getElementById('disclaimer-modal-checkbox');
    const continueBtn = document.getElementById('disclaimer-modal-continue-btn');
    const body = document.body;

    if (!overlay || !checkbox || !continueBtn) {
        // Disclaimer modal not found on this page, exit silently
        return;
    }

    // Check if user came from another page on the same site
    const referrer = document.referrer;
    const currentOrigin = window.location.origin;
    const referrerUrl = referrer ? new URL(referrer) : null;
    
    // Don't show modal if coming from same origin (internal navigation)
    const isInternalNavigation = referrerUrl && referrerUrl.origin === currentOrigin;
    
    if (isInternalNavigation) {
        // User came from another page on the same site, skip the modal
        return;
    }

    // Show modal for direct loads, bookmarks, external links, or page refreshes
    overlay.classList.add('show');
    body.style.overflow = 'hidden'; // Prevent scrolling

    // Update translations
    if (typeof updateTranslations === 'function') {
        updateTranslations();
    }

    // Handle checkbox change
    checkbox.addEventListener('change', () => {
        continueBtn.disabled = !checkbox.checked;
    });

    // Handle continue button
    continueBtn.addEventListener('click', () => {
        if (checkbox.checked) {
            overlay.classList.remove('show');
            body.style.overflow = ''; // Restore scrolling
            
            // After disclaimer is acknowledged, trigger onboarding check if it exists
            // This allows the onboarding flow to proceed if needed
            if (typeof checkAndShowOnboarding === 'function') {
                // Small delay to ensure smooth transition
                setTimeout(() => {
                    checkAndShowOnboarding();
                }, 300);
            }
        }
    });

    // Prevent closing by clicking outside (user must acknowledge)
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            // Prevent closing by clicking outside - user must check the box and click continue
            e.stopPropagation();
        }
    });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDisclaimerModal);
} else {
    initDisclaimerModal();
}

