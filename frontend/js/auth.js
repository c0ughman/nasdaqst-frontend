/**
 * Authentication utilities for Nasdaq Sentiment Tracker
 * Handles Clerk session management and route protection
 */

class AuthManager {
    constructor() {
        this.clerkLoaded = false;
        this.initPromise = null;
    }

    /**
     * Initialize Clerk and wait for it to load
     */
    async init() {
        if (this.initPromise) {
            return this.initPromise;
        }

        this.initPromise = new Promise(async (resolve, reject) => {
            try {
                // Wait for Clerk to be available
                if (!window.Clerk) {
                    await this.waitForClerk();
                }

                // Load Clerk
                await window.Clerk.load();
                this.clerkLoaded = true;
                resolve(true);
            } catch (error) {
                console.error('Failed to initialize Clerk:', error);
                reject(error);
            }
        });

        return this.initPromise;
    }

    /**
     * Wait for Clerk SDK to be available
     */
    async waitForClerk(timeout = 10000) {
        const startTime = Date.now();

        while (!window.Clerk) {
            if (Date.now() - startTime > timeout) {
                throw new Error('Clerk SDK failed to load');
            }
            await new Promise(resolve => setTimeout(resolve, 100));
        }
    }

    /**
     * Check if user is authenticated
     */
    async isAuthenticated() {
        if (!this.clerkLoaded) {
            await this.init();
        }
        return !!window.Clerk.user;
    }

    /**
     * Get current user
     */
    async getCurrentUser() {
        if (!this.clerkLoaded) {
            await this.init();
        }
        return window.Clerk.user;
    }

    /**
     * Protect a route - redirect to login if not authenticated
     */
    async protectRoute() {
        try {
            const isAuth = await this.isAuthenticated();

            if (!isAuth) {
                // Not authenticated, redirect to landing page
                window.location.href = '/index.html';
                return false;
            }

            return true;
        } catch (error) {
            console.error('Error protecting route:', error);
            window.location.href = '/index.html';
            return false;
        }
    }

    /**
     * Redirect authenticated users from public pages
     */
    async redirectIfAuthenticated(redirectTo = '/nasdaq.html') {
        try {
            const isAuth = await this.isAuthenticated();

            if (isAuth) {
                window.location.href = redirectTo;
                return true;
            }

            return false;
        } catch (error) {
            console.error('Error checking authentication:', error);
            return false;
        }
    }

    /**
     * Sign out user
     */
    async signOut() {
        try {
            if (!this.clerkLoaded) {
                await this.init();
            }

            await window.Clerk.signOut();
            window.location.href = '/index.html';
        } catch (error) {
            console.error('Error signing out:', error);
        }
    }

    /**
     * Get user session
     */
    async getSession() {
        if (!this.clerkLoaded) {
            await this.init();
        }
        return window.Clerk.session;
    }

    /**
     * Get session token (useful for API calls)
     */
    async getToken() {
        try {
            if (!this.clerkLoaded) {
                await this.init();
            }

            const session = await this.getSession();
            if (!session) return null;

            return await session.getToken();
        } catch (error) {
            console.error('Error getting token:', error);
            return null;
        }
    }

    /**
     * Listen for authentication state changes
     */
    onAuthStateChange(callback) {
        if (!window.Clerk) {
            console.error('Clerk not loaded yet');
            return;
        }

        window.Clerk.addListener((session) => {
            callback({
                isAuthenticated: !!session,
                user: window.Clerk.user,
                session: session
            });
        });
    }
}

// Create singleton instance
const authManager = new AuthManager();

// Export for use in other scripts
window.AuthManager = authManager;
