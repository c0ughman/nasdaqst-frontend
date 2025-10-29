# Nasdaq Sentiment Tracker - Authentication Setup Guide

This guide will help you set up Clerk authentication for your Nasdaq Sentiment Tracker application.

## Overview

The authentication system uses [Clerk](https://clerk.com) to protect access to the main dashboard (`nasdaq.html`). The flow is:

1. **Landing Page** (`index.html`) - Publicly accessible
2. **Sign Up** (`signup.html`) - Create a new account
3. **Login** (`login.html`) - Sign in to existing account
4. **Dashboard** (`nasdaq.html`) - Protected, requires authentication

## Setup Instructions

### Step 1: Create a Clerk Account

1. Go to [clerk.com](https://clerk.com) and sign up for a free account
2. Create a new application in the Clerk dashboard
3. Choose "Email & Password" as your authentication method (you can add more later)

### Step 2: Get Your Publishable Key

1. In the Clerk dashboard, go to **API Keys**
2. Copy your **Publishable Key** (starts with `pk_test_` or `pk_live_`)
3. **Important**: Keep your Secret Key private - never use it in frontend code!

### Step 3: Update Your Files

You need to replace `YOUR_CLERK_PUBLISHABLE_KEY` in the following files:

#### 1. `login.html` (Line 171)
```html
<script
    async
    crossorigin="anonymous"
    data-clerk-publishable-key="YOUR_CLERK_PUBLISHABLE_KEY"
    src="https://clerk.com/clerk.browser.js"
    type="text/javascript"
></script>
```

#### 2. `signup.html` (Line 171)
```html
<script
    async
    crossorigin="anonymous"
    data-clerk-publishable-key="YOUR_CLERK_PUBLISHABLE_KEY"
    src="https://clerk.com/clerk.browser.js"
    type="text/javascript"
></script>
```

#### 3. `nasdaq.html` (Line 12)
```html
<script
    async
    crossorigin="anonymous"
    data-clerk-publishable-key="YOUR_CLERK_PUBLISHABLE_KEY"
    src="https://clerk.com/clerk.browser.js"
    type="text/javascript"
></script>
```

### Step 4: Configure Clerk Dashboard

1. In your Clerk dashboard, go to **Paths**
2. Set the following URLs:
   - **Sign-in URL**: `/login.html`
   - **Sign-up URL**: `/signup.html`
   - **After sign-in URL**: `/nasdaq.html`
   - **After sign-up URL**: `/nasdaq.html`

3. Go to **Domains** and add your Netlify domain:
   - For development: `localhost` and `127.0.0.1`
   - For production: Your Netlify URL (e.g., `your-app.netlify.app`)

### Step 5: Deploy to Netlify

1. Make sure all your files are in the `frontend/` folder
2. In Netlify, set your **Publish directory** to `frontend`
3. Deploy your site
4. Update Clerk dashboard with your Netlify URL

## File Structure

```
frontend/
├── index.html          # Landing page (public)
├── login.html          # Login page
├── signup.html         # Sign up page
├── nasdaq.html         # Dashboard (protected)
├── js/
│   └── auth.js         # Authentication utilities (optional helper)
├── _redirects          # Netlify routing config
└── AUTHENTICATION_SETUP.md  # This file
```

## How It Works

### Authentication Flow

1. **User visits the site**
   - Landing page (`index.html`) is publicly accessible
   - Shows "Get Started" button → redirects to signup
   - Shows "Login" button → redirects to login

2. **User signs up/logs in**
   - Clerk handles authentication securely
   - After successful auth, redirects to `nasdaq.html`

3. **Protected Dashboard**
   - `nasdaq.html` checks for active Clerk session on load
   - If not authenticated → redirects to landing page
   - If authenticated → shows dashboard

### Security Features

- **Session-based authentication**: Clerk manages secure sessions
- **Automatic redirects**: Unauthenticated users can't access dashboard
- **Client-side protection**: Authentication check runs before page loads
- **Secure logout**: Properly clears session and redirects

## Testing Locally

To test locally, you'll need to run a local server (Clerk requires localhost or HTTPS):

### Option 1: Python
```bash
cd frontend
python3 -m http.server 8000
```
Then visit: `http://localhost:8000`

### Option 2: Node.js (http-server)
```bash
cd frontend
npx http-server -p 8000
```
Then visit: `http://localhost:8000`

### Option 3: VS Code Live Server
1. Install "Live Server" extension
2. Right-click `index.html` → "Open with Live Server"

## Testing the Authentication Flow

1. **Test Unauthenticated Access**:
   - Visit `http://localhost:8000/nasdaq.html` directly
   - Should redirect to `index.html`

2. **Test Sign Up**:
   - Click "Let's Get Started" on landing page
   - Fill out sign-up form
   - Should redirect to `nasdaq.html` after signup

3. **Test Login**:
   - Click "Login" on landing page
   - Enter credentials
   - Should redirect to `nasdaq.html`

4. **Test Session Persistence**:
   - After logging in, refresh the page
   - Should remain logged in (stay on `nasdaq.html`)

5. **Test Logout** (when implemented):
   - Click logout button
   - Should redirect to landing page
   - Accessing `nasdaq.html` should redirect back to landing

## Customization

### Styling Clerk Components

The login and signup pages already include custom styling for Clerk components to match your dark theme. The styling is defined in the `appearance` object:

```javascript
appearance: {
    elements: {
        formButtonPrimary: "bg-gradient-to-r from-green-400 to-cyan-400 hover:from-green-500 hover:to-cyan-500 text-black font-semibold",
        formFieldInput: "bg-black bg-opacity-30 border border-gray-700 text-white focus:border-green-400",
        // ... more customization
    }
}
```

### Adding Social Login

To add Google, GitHub, etc.:
1. Go to Clerk dashboard → **User & Authentication** → **Social Connections**
2. Enable the providers you want
3. Clerk will automatically show them in login/signup forms

## Troubleshooting

### "Clerk is not defined" Error
- Make sure the Clerk script tag is in the `<head>` section
- Wait for `window.Clerk.load()` to complete before checking auth

### Redirect Loop
- Check that your Clerk dashboard URLs match your actual file names
- Make sure you're using the correct publishable key

### Session Not Persisting
- Check browser console for errors
- Ensure cookies are enabled
- Verify domain is correctly configured in Clerk dashboard

### CORS Errors
- Make sure you're using `localhost` or HTTPS (not `file://`)
- Add your domain to Clerk dashboard under **Domains**

## Production Checklist

Before going to production:

- [ ] Replace `YOUR_CLERK_PUBLISHABLE_KEY` in all files
- [ ] Add production domain to Clerk dashboard
- [ ] Test all authentication flows
- [ ] Enable production mode in Clerk (upgrade from test keys)
- [ ] Set up proper error handling
- [ ] Configure session timeout settings in Clerk
- [ ] Review Clerk security settings

## Additional Resources

- [Clerk Documentation](https://clerk.com/docs)
- [Clerk JavaScript SDK](https://clerk.com/docs/references/javascript/overview)
- [Netlify Deployment Guide](https://docs.netlify.com/)

## Support

If you run into issues:
1. Check the browser console for error messages
2. Review Clerk dashboard logs
3. Consult [Clerk's documentation](https://clerk.com/docs)
4. Check Netlify deploy logs

---

**Note**: This setup uses Clerk's embedded components (Option B from our plan) for maximum customization and brand consistency.
