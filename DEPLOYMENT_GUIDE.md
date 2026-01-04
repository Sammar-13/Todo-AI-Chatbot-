# Production Deployment Guide

## Overview
This guide covers deploying the Hackathon Todo application to production using modern cloud platforms.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Client Browser                       │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS
                     ▼
┌─────────────────────────────────────────────────────────┐
│              CDN (Vercel/Cloudflare)                    │
│         (Static assets, global distribution)            │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
   ┌─────────────┐         ┌──────────────┐
   │   Frontend  │         │   Backend    │
   │  (Vercel)   │         │  (Railway)   │
   │ Next.js App │         │  FastAPI     │
   └─────────────┘         └──────┬───────┘
                                  │
                                  ▼
                          ┌─────────────────┐
                          │   PostgreSQL    │
                          │    (Neon.tech)  │
                          └─────────────────┘
```

---

## Deployment Options

### Option 1: Vercel + Railway (Recommended for Hackathon) ✅
- **Frontend**: Vercel (free tier includes 100GB bandwidth)
- **Backend**: Railway (pay-as-you-go, ~$5-10/month)
- **Database**: Neon (PostgreSQL, free tier includes 3 projects)
- **Cost**: ~$10-15/month or less
- **Setup Time**: 20-30 minutes

### Option 2: AWS (Production Grade)
- **Frontend**: CloudFront + S3
- **Backend**: ECS/Lambda
- **Database**: RDS PostgreSQL
- **Cost**: $50-200+/month
- **Setup Time**: 1-2 hours

### Option 3: DigitalOcean App Platform
- **Frontend + Backend**: Single platform
- **Database**: Managed PostgreSQL
- **Cost**: $25-50/month
- **Setup Time**: 30-45 minutes

---

# Option 1: Vercel + Railway + Neon (Recommended)

## Prerequisites
- GitHub account (fork or push repo)
- Vercel account (free)
- Railway account (free)
- Neon account (free)

---

## Step 1: Set Up PostgreSQL Database (Neon)

### 1.1 Create Neon Account
1. Go to https://neon.tech
2. Sign up with GitHub
3. Create new project: "hackathon-todo-prod"
4. Select region closest to you
5. Tier: Free ($0/month)

### 1.2 Get Database Connection String
```
In Neon Dashboard:
1. Go to "Connection string" tab
2. Copy the connection string
3. Format: postgresql://user:password@host/dbname
4. Save this for later
```

### 1.3 Initialize Database Schema
```bash
# From your local machine
export DATABASE_URL="postgresql://user:password@host/dbname"

# Run migrations
cd backend
python -m alembic upgrade head

# Or manually create indexes
psql $DATABASE_URL < src/app/migrations/001_add_task_indexes.py
```

---

## Step 2: Deploy Backend to Railway

### 2.1 Prepare Backend for Deployment

#### Update requirements.txt
```bash
cd backend
pip freeze > requirements.txt

# Add production dependencies if missing
echo "gunicorn==21.2.0" >> requirements.txt
echo "python-dotenv==1.0.0" >> requirements.txt
```

#### Create Procfile
```bash
# Create backend/Procfile
echo "web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.app.main:app --bind 0.0.0.0:\$PORT" > Procfile
```

#### Create runtime.txt (Python version)
```bash
echo "python-3.11.7" > runtime.txt
```

#### Create .env.production
```bash
# backend/.env.production
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
DATABASE_URL=postgresql://user:password@host/dbname
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
JWT_SECRET=your-secret-key-min-32-chars-long
REFRESH_SECRET=your-refresh-secret-min-32-chars
```

### 2.2 Deploy to Railway

#### Via Web UI (Easiest)
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "Create New Project"
4. Select "Deploy from GitHub repo"
5. Authorize GitHub
6. Select your hackathon-todo repository
7. Select `backend` folder as root directory
8. Configure environment variables:
   - `DATABASE_URL` = Neon connection string
   - `CORS_ORIGINS` = your frontend domain
   - `JWT_SECRET` = generate random 32+ char string
   - `REFRESH_SECRET` = generate random 32+ char string
   - `ENVIRONMENT` = production
   - `DEBUG` = false

#### Via Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create new project
railway init

# Link to GitHub repo
# Follow prompts to connect GitHub

# Add PostgreSQL service
railway add

# Deploy
railway up

# View logs
railway logs
```

### 2.3 Get Backend URL
After deployment:
1. Go to Railway dashboard
2. Click on your project
3. Click the "Deployments" tab
4. Find the domain (e.g., `https://yourproject-prod.railway.app`)
5. Note this for frontend configuration

---

## Step 3: Deploy Frontend to Vercel

### 3.1 Update Frontend Configuration

#### Update environment variables (frontend/.env.production)
```bash
NEXT_PUBLIC_API_URL=https://your-backend-domain.railway.app
NEXT_PUBLIC_APP_NAME=Hackathon Todo
```

#### Update next.config.js
```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    formats: ['image/avif', 'image/webp'],
  },
  redirects: async () => [
    {
      source: '/dashboard',
      destination: '/dashboard/todos',
      permanent: false,
    },
  ],
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
```

### 3.2 Deploy to Vercel

#### Via Web UI (Easiest)
1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "Add New" → "Project"
4. Import your GitHub repository
5. Select `frontend` folder as root directory
6. Add environment variables:
   - `NEXT_PUBLIC_API_URL` = your Railway backend URL
7. Click "Deploy"

#### Via Vercel CLI
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel --prod

# Set environment variables
vercel env add NEXT_PUBLIC_API_URL
# Enter: https://your-backend-domain.railway.app
```

### 3.3 Get Frontend URL
After deployment:
1. Check email for Vercel confirmation
2. Go to https://vercel.com/dashboard
3. Find your project
4. Copy the domain (e.g., `https://yourdomain.vercel.app`)

---

## Step 4: Update Backend CORS

Now that you have the frontend domain:

1. Go to Railway dashboard
2. Select your backend project
3. Go to "Variables" tab
4. Update `CORS_ORIGINS` to include Vercel domain:
   ```
   https://yourdomain.vercel.app,https://yourdomain.vercel.app
   ```
5. Redeploy (Railway auto-redeploys on env change)

---

## Step 5: Custom Domain (Optional but Recommended)

### 5.1 Buy a Domain
- Namecheap, GoDaddy, Google Domains, etc.
- Cost: $10-15/year

### 5.2 Set Up Frontend Domain (Vercel)
1. Go to Vercel dashboard → Project settings
2. Click "Domains"
3. Add custom domain
4. Follow DNS setup instructions
5. Add CNAME record: `yourdomain.com` → `cname.vercel.com`

### 5.3 Set Up Backend Domain (Railway)
1. Go to Railway dashboard → Project settings
2. Click "Custom Domain"
3. Enter `api.yourdomain.com` or `backend.yourdomain.com`
4. Add CNAME record in DNS
5. Update CORS_ORIGINS in Railway variables

### 5.4 Update Frontend Environment
1. Update `NEXT_PUBLIC_API_URL` in Vercel:
   ```
   https://api.yourdomain.com
   ```
2. Redeploy frontend

---

# Option 2: AWS Deployment

## Prerequisites
- AWS account with billing enabled
- AWS CLI configured locally
- Docker (for containerization)

## Architecture
```
Route53 (DNS) → CloudFront (CDN) →
                ├── S3 + CloudFront (Frontend)
                └── API Gateway → ECS Fargate (Backend) → RDS (Database)
```

### 2.1 Create RDS PostgreSQL Database
```bash
# Via AWS Console
1. Go to RDS → Databases → Create database
2. Select PostgreSQL 15
3. Instance type: db.t3.micro (free tier eligible)
4. Storage: 20GB (free tier)
5. Enable automated backups (7 days)
6. Create security group allowing port 5432
7. Save master username and password
8. Note the endpoint URL
```

### 2.2 Build Docker Image for Backend
```bash
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2.3 Push to ECR (Elastic Container Registry)
```bash
# Create ECR repository
aws ecr create-repository --repository-name hackathon-todo-backend

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build and push
cd backend
docker build -t hackathon-todo-backend .
docker tag hackathon-todo-backend:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/hackathon-todo-backend:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/hackathon-todo-backend:latest
```

### 2.4 Create ECS Cluster and Service
```bash
# Via AWS Console or AWS CLI
aws ecs create-cluster --cluster-name hackathon-todo-prod

# Create task definition
# Use Fargate launch type
# Image: ECR image URL
# Port: 8000
# Memory: 512 MB
# CPU: 256
```

### 2.5 Deploy Frontend to S3 + CloudFront
```bash
# Build frontend
cd frontend
npm run build

# Create S3 bucket
aws s3 mb s3://hackathon-todo-prod

# Upload build files
aws s3 sync .next/static s3://hackathon-todo-prod/_next/static --cache-control max-age=31536000
aws s3 sync out s3://hackathon-todo-prod --cache-control max-age=86400

# Create CloudFront distribution
# Origin: S3 bucket
# Default root: index.html
# Compress: enabled
# HTTPS: required
```

---

# Option 3: DigitalOcean App Platform

## 3.1 Prepare Repository
```bash
# Ensure github repo has proper structure
hackathon-todo/
├── backend/
│   ├── src/
│   ├── requirements.txt
│   ├── Procfile
│   └── runtime.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── next.config.js
│   └── .env.production
└── README.md
```

## 3.2 Deploy to DigitalOcean
1. Go to https://cloud.digitalocean.com
2. Click "Apps" → "Create App"
3. Select your GitHub repository
4. Configure:
   - **Frontend service**: `frontend` folder, Node.js runtime, `npm run build` & `npm start`
   - **Backend service**: `backend` folder, Python runtime, `pip install -r requirements.txt` & `gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.app.main:app`
   - **Database**: Add PostgreSQL managed database
5. Set environment variables for both services
6. Deploy

---

# Post-Deployment Checklist

## Security
- [ ] Enable HTTPS (automatic on Vercel/Railway)
- [ ] Configure CORS properly (backend)
- [ ] Set secure JWT secrets (32+ random characters)
- [ ] Enable database SSL connection
- [ ] Configure firewall rules (allow only necessary ports)
- [ ] Set up database backups (automatic on managed services)
- [ ] Review security headers in response
- [ ] Enable rate limiting (already implemented)

## Monitoring
- [ ] Set up error tracking (Sentry, LogRocket)
- [ ] Monitor API response times
- [ ] Set up alerts for high error rates
- [ ] Monitor database performance
- [ ] Check application logs regularly

## Testing
- [ ] Test user registration and login
- [ ] Test create/read/update/delete tasks
- [ ] Test API rate limiting (101st request)
- [ ] Test GZIP compression (`curl -H "Accept-Encoding: gzip"`)
- [ ] Test CORS from different domains
- [ ] Test authentication token refresh
- [ ] Test logout functionality
- [ ] Load test with multiple concurrent users

## Optimization
- [ ] Monitor database query performance
- [ ] Check CPU/memory usage
- [ ] Analyze frontend bundle size
- [ ] Test page load speed (Lighthouse)
- [ ] Verify CDN is serving static assets
- [ ] Check database connection pool health

---

# Continuous Deployment (CI/CD)

## GitHub Actions Workflow

### Create .github/workflows/deploy.yml
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install backend dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Run backend tests
        run: |
          cd backend
          pytest tests/ -v

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install frontend dependencies
        run: |
          cd frontend
          npm ci

      - name: Build frontend
        run: |
          cd frontend
          npm run build

      - name: Run frontend tests
        run: |
          cd frontend
          npm run test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Vercel
        uses: vercel/action@master
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: frontend

      - name: Deploy to Railway
        run: |
          npm install -g @railway/cli
          cd backend
          railway deploy
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

---

# Troubleshooting

## Backend Won't Start
```bash
# Check logs
railway logs
# or
vercel logs <project-name>

# Common issues:
# - Missing DATABASE_URL env variable
# - Database not running or incorrect connection string
# - Python version mismatch
# - Missing requirements installed
```

## Frontend Can't Connect to Backend
```bash
# Check CORS configuration
curl -H "Origin: https://yourdomain.com" \
     -H "Access-Control-Request-Method: GET" \
     https://api.yourdomain.com/api/health -v

# Check backend is running
curl https://api.yourdomain.com/api/health

# Check NEXT_PUBLIC_API_URL is correct
# In browser console: console.log(process.env.NEXT_PUBLIC_API_URL)
```

## Database Connection Issues
```bash
# Test connection locally
psql postgresql://user:password@host/dbname

# Check connection string format
postgresql://username:password@hostname:5432/database_name

# Verify database is running and accessible
# Check firewall rules allow your backend service
```

## Rate Limiting Blocks Legitimate Traffic
```python
# Adjust in backend/src/app/middleware/rate_limit.py
rate_limiter = RateLimiter(requests_per_minute=200)  # Increase from 100

# Redeploy backend
```

---

# Rollback Instructions

## Rollback Frontend (Vercel)
1. Go to Vercel dashboard
2. Click on your project
3. Go to "Deployments" tab
4. Find previous working deployment
5. Click "Promote to Production"

## Rollback Backend (Railway)
1. Go to Railway dashboard
2. Click on your project
3. Go to "Deployments" tab
4. Find previous working deployment
5. Click the three dots menu
6. Select "Rollback"

## Rollback Database
```bash
# PostgreSQL automatic backups are available
# Contact Neon support to restore from backup
# Or restore from manual backup if created
```

---

# Production Best Practices

1. **Environment Separation**
   - Never use production secrets in development
   - Use separate databases for dev/staging/prod

2. **Database Backups**
   - Enable automatic daily backups (usually automatic)
   - Test backup restoration monthly
   - Keep 30 days of backups

3. **Monitoring**
   - Set up alerts for errors and slow queries
   - Monitor disk space and memory usage
   - Track API response times

4. **Updates**
   - Keep dependencies updated monthly
   - Test updates in staging before production
   - Monitor security advisories

5. **Logging**
   - Log all authentication events
   - Log failed API requests
   - Keep logs for 30-90 days

6. **Testing**
   - Write automated tests for critical paths
   - Run tests on every commit (CI/CD)
   - Perform manual testing in staging

---

# Cost Estimation

## Monthly Cost (Recommended Setup: Vercel + Railway + Neon)
| Service | Cost | Notes |
|---------|------|-------|
| Vercel Frontend | $0 | Free tier (up to 100GB bandwidth) |
| Railway Backend | $5-15 | Pay-as-you-go, ~500GB RAM |
| Neon Database | $0 | Free tier (3 projects) |
| Domain | ~$1 | Prorated from annual (~$12/year) |
| **Total** | **~$6-16/month** | Very affordable for hackathon |

## Scaling Costs
- If backend exceeds free tier: +$5 per month per additional resource
- If database exceeds free tier: +$0.16 per GB per month
- Still very affordable for small to medium traffic

---

# Success Checklist

- [ ] Database created and initialized
- [ ] Backend deployed and running
- [ ] Frontend deployed and running
- [ ] Custom domain configured (optional)
- [ ] SSL/HTTPS working
- [ ] Authentication working
- [ ] Tasks CRUD operations working
- [ ] Rate limiting active
- [ ] GZIP compression active
- [ ] Logs being collected
- [ ] Backups enabled
- [ ] Monitoring set up
- [ ] Team has access to dashboards
- [ ] Documentation updated with live URLs
- [ ] Ready to demo to judges!

---

Last Updated: 2026-01-04
Version: 1.0.0
