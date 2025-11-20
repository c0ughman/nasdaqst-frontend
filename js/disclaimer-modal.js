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
    const body = document.body;

    if (!overlay || !checkbox) {
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
    
    console.log('Disclaimer modal check:', {
        referrer: referrer,
        currentPath: window.location.pathname,
        referrerPath: referrerUrl?.pathname,
        isInternalNavigation: isInternalNavigation,
        overlayFound: !!overlay
    });
    
    if (isInternalNavigation) {
        // User came from another page on the same site (different path), skip the modal
        console.log('Skipping disclaimer - internal navigation from another page');
        return;
    }
    
    // Show modal for: direct loads, bookmarks, external links, or page refreshes (same path)
    console.log('Showing disclaimer modal');
    overlay.classList.add('show');
    body.style.overflow = 'hidden'; // Prevent scrolling

    // Update translations
    if (typeof updateTranslations === 'function') {
        updateTranslations();
    }

    // Disable checkbox initially (until audio finishes)
    checkbox.disabled = true;
    checkbox.checked = false;

    // Create and play audio (path relative to HTML file location)
    // Use document base URL or construct from current location
    const baseUrl = document.querySelector('base')?.href || window.location.origin;
    const currentPath = window.location.pathname;
    
    // Get directory path
    let dirPath = '';
    if (currentPath.includes('/')) {
        const lastSlash = currentPath.lastIndexOf('/');
        if (lastSlash >= 0) {
            dirPath = currentPath.substring(0, lastSlash + 1);
        }
    }
    
    // Try constructing the full URL
    const audioPath = baseUrl + dirPath + 'disclaimer.mp3';
    
    console.log('Loading audio from:', audioPath);
    console.log('Base URL:', baseUrl, 'Directory:', dirPath, 'Pathname:', currentPath);
    const audio = new Audio(audioPath);
    audio.playbackRate = 1.0; // Play at normal speed
    
    let audioStarted = false;
    
    // Function to start audio playback (requires user interaction)
    function startAudio() {
        if (audioStarted) return;
        audioStarted = true;
        
        audio.play().catch(error => {
            console.error('Error playing audio:', error);
            // If audio fails to play, enable controls anyway
            enableControls();
        });
    }
    
    // Try to play audio immediately when modal shows
    // Also try to play when audio is loaded
    audio.addEventListener('loadeddata', () => {
        if (!audioStarted) {
            // Try to play immediately
            audio.play().then(() => {
                audioStarted = true;
                console.log('Audio started playing');
            }).catch(() => {
                // Audio blocked - will play on user interaction
                console.log('Audio autoplay blocked - waiting for user interaction');
            });
        }
    });
    
    // Try to play on ANY user interaction with the modal
    // Use capture phase to catch events before they reach child elements
    const startAudioOnInteraction = (e) => {
        if (!audioStarted) {
            console.log('User interaction detected on modal, starting audio');
            startAudio();
        }
    };
    
    // Listen for interactions on the entire modal overlay using capture phase
    // This catches clicks anywhere on the modal, including checkbox, before they bubble
    overlay.addEventListener('click', startAudioOnInteraction, { once: true, capture: true });
    overlay.addEventListener('touchstart', startAudioOnInteraction, { once: true, capture: true });
    overlay.addEventListener('mousedown', startAudioOnInteraction, { once: true, capture: true });
    
    // Also listen on the document level as a fallback
    const documentClickHandler = (e) => {
        // Only trigger if modal is visible and audio hasn't started
        if (overlay.classList.contains('show') && !audioStarted) {
            console.log('Document click detected while modal visible, starting audio');
            startAudio();
            document.removeEventListener('click', documentClickHandler);
        }
    };
    document.addEventListener('click', documentClickHandler, { once: true });

    audio.addEventListener('ended', () => {
        // Audio finished playing, enable controls
        enableControls();
    });

    audio.addEventListener('error', (e) => {
        console.error('Audio error:', e);
        // If audio fails to load, enable controls anyway
        enableControls();
    });
    
    // Track if audio has started playing
    audio.addEventListener('play', () => {
        audioStarted = true;
    });

    // Function to enable checkbox
    function enableControls() {
        checkbox.disabled = false;
    }

    // Handle checkbox change - automatically proceed when checked (after audio finishes)
    checkbox.addEventListener('change', () => {
        if (!checkbox.disabled && checkbox.checked) {
            // User checked the box - close modal and proceed
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

