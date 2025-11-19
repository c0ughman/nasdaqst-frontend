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

    // Check if user came from another page on the same site (but not a refresh)
    const referrer = document.referrer;
    const currentUrl = window.location.href;
    const currentOrigin = window.location.origin;
    const referrerUrl = referrer ? new URL(referrer) : null;
    
    // Don't show modal if coming from a different page on the same site (internal navigation)
    // But DO show if it's a page refresh (same URL) or no referrer (direct load)
    const isInternalNavigation = referrerUrl && 
                                 referrerUrl.origin === currentOrigin && 
                                 referrerUrl.pathname !== window.location.pathname;
    
    if (isInternalNavigation) {
        // User came from another page on the same site (different path), skip the modal
        return;
    }
    
    // Show modal for: direct loads, bookmarks, external links, or page refreshes (same path)

    // Show modal for direct loads, bookmarks, external links, or page refreshes
    overlay.classList.add('show');
    body.style.overflow = 'hidden'; // Prevent scrolling

    // Update translations
    if (typeof updateTranslations === 'function') {
        updateTranslations();
    }

    // Disable checkbox and button initially (until audio finishes)
    checkbox.disabled = true;
    continueBtn.disabled = true;
    checkbox.checked = false;

    // Create and play audio
    const audio = new Audio('disclaimer.mp3');
    
    // Handle audio playback
    audio.addEventListener('loadeddata', () => {
        // Audio is loaded, start playing
        audio.play().catch(error => {
            console.error('Error playing audio:', error);
            // If audio fails to play, enable controls anyway
            enableControls();
        });
    });

    audio.addEventListener('ended', () => {
        // Audio finished playing, enable controls
        enableControls();
    });

    audio.addEventListener('error', (e) => {
        console.error('Audio error:', e);
        // If audio fails to load, enable controls anyway
        enableControls();
    });

    // Function to enable checkbox and button
    function enableControls() {
        checkbox.disabled = false;
        // Button stays disabled until checkbox is checked
        continueBtn.disabled = true;
    }

    // Handle checkbox change (only works after audio finishes)
    checkbox.addEventListener('change', () => {
        if (!checkbox.disabled) {
            continueBtn.disabled = !checkbox.checked;
        }
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

