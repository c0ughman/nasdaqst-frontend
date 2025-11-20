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
    
    // Function to start audio playback
    function startAudio() {
        if (audioStarted) return;
        audioStarted = true;
        console.log('Starting audio playback');
        
        audio.play().catch(error => {
            console.error('Error playing audio:', error);
            // If audio fails to play, enable controls anyway
            enableControls();
        });
    }
    
    // Try to play audio immediately when loaded (will likely be blocked by browser)
    audio.addEventListener('canplaythrough', () => {
        if (!audioStarted) {
            console.log('Audio ready, attempting to play');
            audio.play().then(() => {
                audioStarted = true;
                console.log('Audio started playing automatically');
            }).catch(() => {
                console.log('Audio autoplay blocked - will play on first user interaction');
            });
        }
    });
    
    // Also try when loadeddata fires
    audio.addEventListener('loadeddata', () => {
        if (!audioStarted) {
            audio.play().then(() => {
                audioStarted = true;
                console.log('Audio started on loadeddata');
            }).catch(() => {
                // Will play on interaction
            });
        }
    });
    
    // Start audio on ANY user interaction anywhere on the page
    // This must happen BEFORE the checkbox can be clicked
    const startAudioOnAnyInteraction = (e) => {
        if (!audioStarted && overlay.classList.contains('show')) {
            console.log('User interaction detected, starting audio immediately');
            startAudio();
            // Remove listeners after audio starts
            document.removeEventListener('click', startAudioOnAnyInteraction, true);
            document.removeEventListener('touchstart', startAudioOnAnyInteraction, true);
            document.removeEventListener('mousedown', startAudioOnAnyInteraction, true);
        }
    };
    
    // Use capture phase on document to catch ALL clicks before they reach any element
    document.addEventListener('click', startAudioOnAnyInteraction, { capture: true, once: false });
    document.addEventListener('touchstart', startAudioOnAnyInteraction, { capture: true, once: false });
    document.addEventListener('mousedown', startAudioOnAnyInteraction, { capture: true, once: false });

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

