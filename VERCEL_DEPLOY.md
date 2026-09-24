# Financial Help Hub - Vercel Deployment

## Files Created:
✅ vercel.json - Vercel configuration
✅ .vercelignore - Files to ignore during deploy
✅ app.py - Updated for Vercel (removed dev server code)

## Deploy to Vercel:

### Option 1: Vercel CLI (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd /path/to/financial-help-hub
vercel
```

### Option 2: GitHub + Vercel Dashboard
1. Push code to GitHub
2. Go to https://vercel.com/new
3. Import the repository
4. Add environment variables:
   - SUPABASE_URL: https://tzrcjamabhduxezmeyze.supabase.co
   - SUPABASE_KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   - SECRET_KEY: financial-help-hub-vercel-secret-2024
5. Deploy!

## Environment Variables (set in Vercel Dashboard):
- SUPABASE_URL
- SUPABASE_KEY  
- SECRET_KEY

## Files in this directory:
