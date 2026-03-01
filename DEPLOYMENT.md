# Render Deployment Guide

## 📋 Prerequisites

1. **GitHub Account**: Your code is already on GitHub at `https://github.com/pao0318/operate-backend.git`
2. **Render Account**: Sign up at [render.com](https://render.com) (free tier available)

## 🚀 Deployment Steps

### Step 1: Connect GitHub to Render

1. Go to [render.com](https://render.com) and sign in
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub account if not already connected
4. Select the repository: `pao0318/operate-backend`

### Step 2: Deploy Using Blueprint

Render will automatically detect the `render.yaml` file and set up:

- **PostgreSQL Database** (`operate-db`)
  - Free tier
  - Database name: `operate_db`
  - User: `operate_user`
  - Region: Oregon

- **Web Service** (`operate-backend`)
  - Python runtime
  - Free tier
  - Region: Oregon
  - Auto-deploy on push to main branch

### Step 3: Review Configuration

The `render.yaml` file includes:

**Build Command:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
alembic upgrade head
# Seed scripts run automatically
python seed_cases.py
python seed_available_services.py
python seed_extracted_key_metrics_individual.py
python seed_covenant_status_data.py
python seed_quarterly_dscr.py
python seed_quarter_financial_drivers.py
python seed_q3_highlights.py
python seed_fry14_schedule_template.py
python seed_detailed_findings_y14.py
python seed_shipment_details.py
python seed_detailed_findings_operational.py
python seed_datasimulator_benefits.py
```

**Start Command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Environment Variables:**
- `APP_ENV=production`
- `APP_DEBUG=false`
- `CORS_ORIGINS=*` (update with your frontend URL)
- `DATABASE_URL` (auto-configured from database)

### Step 4: Update CORS Origins (Important!)

After deployment, update the CORS origins in Render dashboard:

1. Go to your web service → **Environment**
2. Update `CORS_ORIGINS` with your frontend URL:
   ```
   https://your-frontend-domain.com,http://localhost:3000
   ```

### Step 5: Monitor Deployment

1. Click **"Apply"** to start deployment
2. Monitor the build logs in Render dashboard
3. Wait for deployment to complete (usually 5-10 minutes)

### Step 6: Access Your API

Once deployed, your API will be available at:
```
https://operate-backend.onrender.com
```

**API Documentation:**
- Swagger UI: `https://operate-backend.onrender.com/docs`
- ReDoc: `https://operate-backend.onrender.com/redoc`
- Health Check: `https://operate-backend.onrender.com/api/health`

## 🔄 Continuous Deployment

Render will automatically redeploy when you push to the `main` branch:

```bash
git add .
git commit -m "Your commit message"
git push origin main
```

## 🗄️ Database Management

### Access Database

1. Go to Render Dashboard → Your Database
2. Click **"Connect"** to get connection details
3. Use the **External Database URL** to connect via psql or GUI tools

### Run Migrations Manually (if needed)

```bash
# SSH into your Render service (if needed)
alembic upgrade head
```

### Re-run Seed Scripts (if needed)

If you need to re-seed data:
1. Go to Render Dashboard → Your Web Service
2. Click **"Manual Deploy"** → **"Clear build cache & deploy"**

Or connect to the database and run seed scripts manually.

## 📊 Monitoring

### Health Check

Render automatically monitors: `https://operate-backend.onrender.com/api/health`

### Logs

View logs in Render Dashboard → Your Service → **Logs**

## ⚙️ Environment Variables Reference

| Variable | Value | Description |
|----------|-------|-------------|
| `APP_ENV` | `production` | Application environment |
| `APP_DEBUG` | `false` | Debug mode (disable in production) |
| `CORS_ORIGINS` | Your frontend URLs | Comma-separated allowed origins |
| `DATABASE_URL` | Auto-configured | PostgreSQL connection string |
| `PYTHON_VERSION` | `3.11.0` | Python runtime version |

## 🆓 Free Tier Limitations

- **Database**: 1 GB storage, expires after 90 days
- **Web Service**: 750 hours/month, spins down after 15 min of inactivity
- **Cold starts**: ~30 seconds when service spins up

## 🔧 Troubleshooting

### Build Fails

1. Check build logs in Render dashboard
2. Verify `requirements.txt` has all dependencies
3. Ensure Python version matches (3.11.0)

### Database Connection Issues

1. Verify `DATABASE_URL` is set correctly
2. Check database is running in Render dashboard
3. Review connection string format

### Seed Scripts Fail

1. Check if tables exist (Alembic migrations ran)
2. Verify seed scripts don't have duplicate data issues
3. Review logs for specific error messages

### CORS Errors

Update `CORS_ORIGINS` environment variable with your frontend URL

## 📝 Additional Configuration

### Custom Domain

1. Go to your web service → **Settings**
2. Add custom domain under **Custom Domains**
3. Update DNS records as instructed

### Scale Up

Upgrade from free tier in Render dashboard for:
- No cold starts
- More resources
- Persistent database

## 🔐 Security Recommendations

1. **Update CORS**: Replace `*` with specific frontend URLs
2. **Environment Variables**: Add any API keys via Render dashboard (not in code)
3. **Database Backups**: Enable on paid plans
4. **HTTPS**: Automatically enabled by Render

## 📚 Resources

- [Render Documentation](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Render Python Guide](https://render.com/docs/deploy-fastapi)

## ✅ Post-Deployment Checklist

- [ ] Deployment successful
- [ ] Health check endpoint responding
- [ ] Database connected and seeded
- [ ] API documentation accessible at `/docs`
- [ ] CORS configured for frontend
- [ ] All endpoints tested
- [ ] Frontend connected to production API
- [ ] Monitoring set up
