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

    // Get the Enter button and modal levels
    const enterButton = document.getElementById('disclaimer-enter-button');
    const level1 = document.getElementById('disclaimer-level-1');
    const level2 = document.getElementById('disclaimer-level-2');

    // Disable checkbox initially (until audio finishes)
    checkbox.disabled = true;
    checkbox.checked = false;

    // Enable Enter button immediately on level 1 (no need to wait for audio)
    if (enterButton) {
        enterButton.disabled = false;
    }

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
    
    // Create audio element
    const audio = new Audio(audioPath);
    audio.preload = 'auto';
    audio.autoplay = true; // Try setting autoplay attribute
    audio.volume = 1.0; // Set to maximum volume (0.0 to 1.0)
    audio.style.display = 'none';
    document.body.appendChild(audio);
    
    // Note: Volume can also be affected by:
    // - Browser tab volume (some browsers allow per-tab volume control)
    // - System volume settings
    // - Audio file encoding level (the MP3 file itself might be quiet)
    // - Browser autoplay policies (some browsers reduce volume for autoplay)
    
    let audioStarted = false;
    let isAttemptingPlay = false;
    
    // Function to start audio playback
    function startAudio() {
        if (audioStarted || isAttemptingPlay) return;
        
        isAttemptingPlay = true;
        // Create a play promise
        const playPromise = audio.play();
        
        if (playPromise !== undefined) {
            playPromise.then(() => {
                audioStarted = true;
                isAttemptingPlay = false;
                console.log('Audio started playing');
                console.log('Audio volume level:', audio.volume, '(1.0 = maximum)');
                
                // Enable Enter button when audio starts
                if (enterButton) {
                    enterButton.disabled = false;
                }
            }).catch(error => {
                isAttemptingPlay = false;
                // Only log real errors, not autoplay blocks (to reduce noise)
                if (error.name !== 'NotAllowedError') {
                    console.error('Audio playback failed:', error);
                    // If it's a real error (not block), we might want to enable controls
                    enableControls();
                } else {
                    // Autoplay blocked - button is already enabled
                    console.log('Autoplay blocked, user can still continue');
                }
            });
        } else {
            isAttemptingPlay = false;
        }
    }
    
    // Add event listener to Enter button to transition to level 2 and play audio
    if (enterButton) {
        enterButton.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent bubble to overlay

            // Hide level 1 and show level 2
            if (level1) level1.style.display = 'none';
            if (level2) level2.style.display = 'block';

            // Start audio when entering level 2
            startAudio();
        });
    }

    // Don't attempt to play audio immediately - wait for Enter button click
    // Audio will start when user clicks the Enter button to go to level 2

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

    // Function to enable checkbox and Enter button
    function enableControls() {
        checkbox.disabled = false;
        if (enterButton) {
            enterButton.disabled = false;
        }
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

