#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# Financial Help Hub - GitHub Push Script
# ═══════════════════════════════════════════════════════════════

echo "🚀 Pushing Financial Help Hub to GitHub..."
echo ""

# Step 1: Initialize git repository
echo "📁 Step 1: Initializing Git repository..."
git init

# Step 2: Add all files
echo "📦 Step 2: Adding files..."
git add .

# Step 3: Create initial commit
echo "💾 Step 3: Creating initial commit..."
git commit -m "Initial commit - Financial Help Hub

Features:
- Beautiful colorful UI with 6 gradient schemes
- Authentication system (login/signup)
- Donation flow with payment modals
- Supabase database integration
- 15 inspirational quotes
- Vercel-ready deployment
- Mobile responsive design"

# Step 4: Add remote (REPLACE WITH YOUR REPO URL)
echo "🔗 Step 4: Adding remote repository..."
echo ""
echo "⚠️  IMPORTANT: Replace <YOUR_USERNAME> and <YOUR_REPO> below!"
echo ""
read -p "Enter your GitHub username: " username
read -p "Enter your repository name: " reponame

git remote add origin https://github.com/$username/$reponame.git

# Step 5: Push to GitHub
echo "⬆️  Step 5: Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Done! Your code is now on GitHub!"
echo "🌐 Visit: https://github.com/$username/$reponame"
echo ""
echo "📌 Next steps:"
echo "  1. Go to vercel.com/new"
echo "  2. Import your GitHub repository"
echo "  3. Add environment variables (SUPABASE_URL, SUPABASE_KEY, SECRET_KEY)"
echo "  4. Deploy!"
