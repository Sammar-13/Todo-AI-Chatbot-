# ✅ Vercel Deployment Checklist

## Quick Reference: Deploy Frontend in 5 Steps

---

## ✅ Step 1: Create Vercel Account (2 min)

- [ ] Go to: https://vercel.com/signup
- [ ] Click "Continue with GitHub"
- [ ] Authorize Vercel to access your GitHub
- [ ] You're logged in!

**Result**: Vercel dashboard open

---

## ✅ Step 2: Import Project (1 min)

- [ ] Click "Add New" → "Project"
- [ ] Select "FULL-STACK-WEB-TODO-APP-" repository
- [ ] Click "Import"

**Result**: Configuration page appears

---

## ✅ Step 3: Configure Project (1 min)

### Project Settings
- [ ] Project Name: `hackathon-todo` (or your choice)
- [ ] Framework Preset: `Next.js` (auto-detected)
- [ ] **Root Directory: Select `frontend/`** (IMPORTANT!)

### Environment Variables
- [ ] Add `NEXT_PUBLIC_API_URL` = (empty for now)
- [ ] Add `NEXT_PUBLIC_APP_NAME` = `Hackathon Todo` (optional)

**Result**: Ready to deploy

---

## ✅ Step 4: Deploy! (2-5 min)

- [ ] Click big "Deploy" button
- [ ] Watch the build logs
- [ ] Wait for "Deployment Complete" ✅

**Result**: Live URL provided

---

## ✅ Step 5: Get Your URL

- [ ] Copy live URL from deployment page
- [ ] Format: `https://your-project-name.vercel.app`
- [ ] Save it for later use!

**Result**: Frontend is LIVE! 🎉

---

## 🚀 After Frontend Deployment

### Deploy Backend (Follow this after frontend)
1. Use `/docs/QUICK_DEPLOYMENT.md` Step 2-3
2. Deploy to Railway
3. Get backend URL

### Update Frontend API URL
1. Go back to Vercel dashboard
2. Click your project
3. Go to "Settings" → "Environment Variables"
4. Update `NEXT_PUBLIC_API_URL` to your backend URL
5. Click "Deployments" → Click latest → "Redeploy"

### Update Backend CORS
1. Go to Railway dashboard
2. Backend project → Variables
3. Update `CORS_ORIGINS` with your Vercel URL
4. Redeploy

### Test Everything
1. Open your Vercel URL
2. Sign up with test account
3. Create a task
4. Update a task
5. Delete a task
6. Everything works? ✅

---

## 📋 Troubleshooting

### "Build Failed"
- Check "Deployments" → Click failed deployment
- View build logs
- Common issues:
  - `frontend/` not selected as root
  - Node version mismatch
  - Missing environment variables

### "Cannot reach API"
- Check `NEXT_PUBLIC_API_URL` environment variable
- Should point to backend: `https://your-backend.railway.app`
- Redeploy after updating

### "CORS Error in Browser"
- Backend `CORS_ORIGINS` missing your Vercel URL
- Format: `https://your-project-name.vercel.app`
- Redeploy backend

### "Pages show 404"
- Check that `frontend/` was selected as root directory
- Redeploy to fix

---

## 🔗 Your Live URLs

After all deployments, you'll have:

### Frontend (Live App)
```
https://your-project-name.vercel.app
```

### Backend (API)
```
https://your-backend.railway.app
https://your-backend.railway.app/docs (API docs)
https://your-backend.railway.app/health (Health check)
```

### GitHub
```
https://github.com/Sammar-13/FULL-STACK-WEB-TODO-APP-
```

---

## 📊 Deployment Timeline

| Step | Time |
|------|------|
| Create account + import | 3 min |
| Configure | 1 min |
| Deploy | 2-5 min |
| Get URL | 1 min |
| **Total** | **7-10 min** |

---

## ✨ What's Next After Vercel Deployment

1. Deploy backend to Railway (15 min total including DB)
2. Update API URL in Vercel
3. Test full stack
4. Demo to judges!

---

## 💡 Pro Tips

1. **Auto-deploy**: Every git push = auto-deploy (no manual steps!)
2. **Rollback**: One click to go back to previous version
3. **Logs**: Check "Deployments" tab if something goes wrong
4. **Custom domain**: Add domain in "Settings" → "Domains"
5. **HTTPS**: Automatic ✅

---

## 🎯 Success Criteria

- [ ] Vercel account created
- [ ] Project imported
- [ ] `frontend/` selected as root
- [ ] Deployment succeeded
- [ ] Live URL works
- [ ] Can see homepage
- [ ] Button clicks work
- [ ] No console errors

---

Last Updated: 2026-01-04
