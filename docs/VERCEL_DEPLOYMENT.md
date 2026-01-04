# 🚀 Deploy Frontend to Vercel

## Quick Vercel Deployment Guide (5 Minutes)

This guide will help you deploy your Next.js frontend to Vercel in 5 minutes.

---

## Prerequisites

- GitHub account (already have it ✅)
- Your code pushed to GitHub (already done ✅)
- Vercel account (free - create it now)

---

## Step 1: Create Vercel Account (2 minutes)

### 1.1 Go to Vercel
Open: https://vercel.com/signup

### 1.2 Sign Up Options
- **Recommended**: Click "Continue with GitHub"
- This auto-connects your GitHub account
- Easier deployment!

### 1.3 Authorize GitHub
- Click "Authorize Vercel"
- Grant access to your repositories
- Done!

---

## Step 2: Import Your Project (1 minute)

### 2.1 Go to Dashboard
After signup, you'll be on Vercel dashboard

### 2.2 Create New Project
- Click "Add New" → "Project"
- Or click "Import Project"

### 2.3 Import from GitHub
- Look for: "FULL-STACK-WEB-TODO-APP-"
- Click "Import"
- (If you don't see it, click "Adjust GitHub App Permissions" and grant access)

---

## Step 3: Configure Project (1 minute)

### 3.1 Project Settings
After importing, you'll see configuration page:

**Project Name**: `hackathon-todo` (or your preferred name)

**Framework Preset**: Select "Next.js" (should auto-detect)

**Root Directory**: Select `frontend/` from dropdown

---

## Step 4: Set Environment Variables (1 minute)

### 4.1 Add Environment Variables
Under "Environment Variables" section, add:

```
Name: NEXT_PUBLIC_API_URL
Value: (leave empty for now, update later)
```

**Why this variable?**
- Frontend needs to know where the backend API is
- Will update this after deploying backend

### 4.2 Other Variables (Optional for now)
```
NEXT_PUBLIC_APP_NAME = Hackathon Todo
```

### 4.3 Skip Production Variables
- You can add more later
- Just click "Deploy" for now

---

## Step 5: Deploy! (Click and Wait)

### 5.1 Click Deploy Button
- Large "Deploy" button at bottom
- Click it!

### 5.2 Wait for Deployment
- Vercel will:
  1. Clone your repository
  2. Install dependencies (`npm install`)
  3. Build the project (`npm run build`)
  4. Deploy to CDN

**Estimated time**: 2-5 minutes

### 5.3 Watch the Build Log
- You'll see real-time build progress
- Green checkmarks = success
- Red X = error (check logs)

---

## Step 6: Get Your Live URL (Immediate)

### 6.1 Deployment Complete
After build succeeds, you'll see:

```
✅ Deployment Complete
🎉 Congratulations! Your site is live!

https://your-project-name.vercel.app
```

### 6.2 Copy Your URL
This is your live frontend URL!

**Example**: `https://hackathon-todo-sammar.vercel.app`

---

## Step 7: Update Frontend API URL (1 minute)

### 7.1 Backend Deployment First
Before this step, you need to:
1. Deploy backend to Railway
2. Get your backend URL: `https://your-backend.railway.app`

### 7.2 Update NEXT_PUBLIC_API_URL
If you already have backend URL:

**In Vercel Dashboard:**
1. Go to your project
2. Click "Settings" tab
3. Go to "Environment Variables"
4. Find `NEXT_PUBLIC_API_URL`
5. Change value to: `https://your-backend-url`
6. Click "Save"

### 7.3 Redeploy
1. Go to "Deployments" tab
2. Click the three dots on latest deployment
3. Click "Redeploy"
4. Wait 1-2 minutes

---

## Step 8: Test Your Live App

### 8.1 Open Your URL
Open in browser: `https://your-project-name.vercel.app`

### 8.2 Test Features
- Sign up with a test account
- Create a task
- Update a task
- Delete a task
- All should work!

### 8.3 If Something Breaks
Check:
1. **NEXT_PUBLIC_API_URL correct?**
   - Should point to your backend
   - Should start with `https://`

2. **Backend running?**
   - Visit `https://your-backend/health`
   - Should return `{"status": "healthy"}`

3. **CORS configured?**
   - Backend must have your Vercel URL in `CORS_ORIGINS`
   - Format: `https://your-project.vercel.app`

---

## Common Issues & Fixes

### Issue: "Cannot GET /docs"
**Cause**: You're visiting `/docs` on frontend (that's backend!)
**Fix**: Visit `https://your-backend-url/docs` instead

### Issue: "API is unreachable"
**Cause**: NEXT_PUBLIC_API_URL not set or wrong
**Fix**:
1. Go to Vercel project settings
2. Update environment variable
3. Redeploy

### Issue: "Deployment failed"
**Check**:
1. View build logs (Vercel shows error)
2. Is `frontend/` the root directory?
3. Are all dependencies installed?
4. Run `npm install` locally and test build

### Issue: "CORS error in browser"
**Cause**: Backend doesn't allow your Vercel domain
**Fix**:
1. Backend needs `CORS_ORIGINS` updated
2. Add your Vercel URL: `https://your-project.vercel.app`
3. Redeploy backend

---

## Production Settings (Important!)

After first deployment, update these settings:

### 1. Enable Automatic Deployments
**Already enabled by default** ✅
- Every git push → auto-deploys
- No manual steps needed!

### 2. Add Custom Domain (Optional)
1. Go to project "Settings"
2. Click "Domains"
3. Add your domain
4. Follow DNS instructions

### 3. Enable Automatic HTTPS
**Already enabled by default** ✅
- All traffic is HTTPS
- No setup needed!

### 4. Configure Caching
Already configured in your code! ✅
- Static assets: 7 days
- Health checks: 5 minutes
- API responses: No cache (authenticated)

---

## Advanced: Environment Variables by Environment

You can set different variables for different deployments:

```
Production (main branch):
NEXT_PUBLIC_API_URL = https://api.yourdomain.com

Preview (pull requests):
NEXT_PUBLIC_API_URL = https://staging-api.railway.app

Development (local):
NEXT_PUBLIC_API_URL = http://localhost:8000
```

**How to set:**
1. Go to Settings → Environment Variables
2. Add variable
3. Select which deployments it applies to

---

## Monitoring Your Deployment

### View Logs
1. Go to "Deployments" tab
2. Click on a deployment
3. See full build and runtime logs

### View Analytics
1. Click "Analytics" tab
2. See:
   - Page views
   - Response times
   - Cache hit rate
   - Error rates

### Set Up Alerts
1. Go to "Settings" → "Alerts"
2. Get notified when:
   - Deployment fails
   - Performance issues
   - Error spikes

---

## Update Your App (After Deployment)

### To Make Changes:
```bash
1. Make code changes locally
2. Commit: git commit -m "message"
3. Push: git push origin main
4. Vercel auto-deploys (no manual steps!)
5. Check: https://your-project.vercel.app (live!)
```

**That's it!** No need to rebuild or redeploy manually!

---

## Rollback Previous Deployment

If something breaks:

1. Go to "Deployments" tab
2. Find previous good deployment
3. Click three dots
4. Click "Promote to Production"
5. Done! (1 click to rollback)

---

## Performance Monitoring

Your app already has optimizations:
- ✅ GZIP compression (automatic)
- ✅ Image optimization (automatic)
- ✅ Code splitting (automatic)
- ✅ Caching headers (configured)

**Check performance:**
1. Go to project → "Analytics"
2. See response times and cache hit rates
3. Use Lighthouse: https://pagespeed.web.dev

---

## Success Checklist

- [ ] Created Vercel account
- [ ] Imported GitHub project
- [ ] Selected `frontend/` as root
- [ ] Set NEXT_PUBLIC_API_URL (can be empty initially)
- [ ] Clicked Deploy
- [ ] Waited for build to complete
- [ ] Got live URL
- [ ] Tested signup/login
- [ ] Tested create/update/delete tasks
- [ ] Verified API connection works

---

## Final URLs

After deployment, you'll have:

```
Frontend (Live App):
https://your-project-name.vercel.app

Backend API (add after Railway deployment):
https://your-backend.railway.app
https://your-backend.railway.app/docs (API docs)
https://your-backend.railway.app/health (Health check)
```

---

## Next Steps

1. **Deploy Backend**: Follow `/docs/QUICK_DEPLOYMENT.md` Step 2-3
2. **Update API URL**: Come back here after backend is live
3. **Update CORS**: Tell backend about your Vercel URL
4. **Test Everything**: Sign up, create tasks, verify it works
5. **Demo to Judges**: Show them your live app!

---

## Support

### If Deployment Fails
1. Check build logs in Vercel dashboard
2. Read `/docs/DEPLOYMENT_GUIDE.md` troubleshooting section
3. Verify git push was successful
4. Verify `frontend/` is the root directory

### If App Doesn't Work After Deployment
1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Check Network tab for failed requests
4. Verify `NEXT_PUBLIC_API_URL` is set correctly
5. Verify backend is running and responds to requests

### Resources
- Vercel Docs: https://vercel.com/docs
- Next.js Docs: https://nextjs.org/docs
- GitHub Status: https://www.githubstatus.com

---

## Estimated Timeline

| Step | Time |
|------|------|
| Create account | 2 min |
| Import project | 1 min |
| Configure | 1 min |
| Deploy | 2-5 min |
| Test | 2 min |
| **Total** | **8-12 min** |

---

**You're ready to deploy! Start now and you'll be live in 10 minutes!** 🚀

---

Last Updated: 2026-01-04
Version: 1.0.0
