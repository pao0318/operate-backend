# Deploying to Render.com

This guide explains how to deploy the Operate Backend FastAPI application to Render.com.

## Prerequisites

- A [Render.com](https://render.com) account
- Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)

## Deployment Steps

### Step 1: Create a PostgreSQL Database

1. Log in to your Render dashboard
2. Click **New +** → **PostgreSQL**
3. Configure the database:
   - **Name**: `operate-db` (or your preferred name)
   - **Database**: `operate_db`
   - **User**: Leave default or customize
   - **Region**: Choose closest to your users
   - **Plan**: Free tier for testing, or paid for production
4. Click **Create Database**
5. Wait for the database to be created
6. Copy the **Internal Database URL** (you'll need this later)

### Step 2: Create the Web Service

1. Click **New +** → **Web Service**
2. Connect your Git repository
3. Configure the service:

   | Setting | Value |
   |---------|-------|
   | **Name** | `operate-backend` |
   | **Region** | Same as your database |
   | **Branch** | `main` (or your default branch) |
   | **Root Directory** | `operate-backend` (if in a monorepo) |
   | **Runtime** | Python 3 |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
   | **Plan** | Free tier or paid |

### Step 3: Configure Environment Variables

In the web service settings, add these environment variables:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Your PostgreSQL Internal URL (change `postgres://` to `postgresql+asyncpg://`) |
| `APP_ENV` | `production` |
| `APP_DEBUG` | `false` |
| `CORS_ORIGINS` | Your frontend URLs (comma-separated) |
| `PYTHON_VERSION` | `3.11.0` |

**Important**: Render provides the database URL as `postgres://...`. You need to change it to `postgresql+asyncpg://...` for async SQLAlchemy.

Example transformation:
```
# Render provides:
postgres://user:password@host:5432/database

# Change to:
postgresql+asyncpg://user:password@host:5432/database
```

### Step 4: Deploy

1. Click **Create Web Service**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Start your application

### Step 5: Run Database Migrations

After the first deployment, you need to run migrations. You have two options:

#### Option A: Using Render Shell (Recommended)

1. Go to your web service dashboard
2. Click **Shell** tab
3. Run:
   ```bash
   alembic upgrade head
   ```

#### Option B: Add Migration to Build Command

Update your build command to:
```bash
pip install -r requirements.txt && alembic upgrade head
```

**Note**: This runs migrations on every deploy, which is usually fine but may slow down deployments.

## render.yaml (Blueprint Spec)

For automated deployments, create a `render.yaml` file in your repository root:

```yaml
databases:
  - name: operate-db
    databaseName: operate_db
    user: operate_user
    plan: free
    region: oregon

services:
  - type: web
    name: operate-backend
    runtime: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt && alembic upgrade head
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: operate-db
          property: connectionString
      - key: APP_ENV
        value: production
      - key: APP_DEBUG
        value: false
      - key: CORS_ORIGINS
        value: "*"
      - key: PYTHON_VERSION
        value: 3.11.0
    healthCheckPath: /api/health
```

**Note**: When using the blueprint, you'll still need to manually update the `DATABASE_URL` to use `postgresql+asyncpg://` instead of `postgres://`.

## Post-Deployment

### Verify Deployment

1. Visit your service URL (e.g., `https://operate-backend.onrender.com`)
2. Check the health endpoint: `https://operate-backend.onrender.com/api/health`
3. Access API docs: `https://operate-backend.onrender.com/docs`

### Monitor Your Service

- **Logs**: View real-time logs in the Render dashboard
- **Metrics**: Monitor CPU, memory, and request metrics
- **Alerts**: Set up alerts for downtime or errors

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Ensure `DATABASE_URL` uses `postgresql+asyncpg://`
   - Check if the database is in the same region as the web service
   - Verify the database is running

2. **Import Errors**
   - Ensure all dependencies are in `requirements.txt`
   - Check Python version compatibility

3. **Migration Failures**
   - Run migrations manually via Shell
   - Check migration files for errors

4. **SSE Connection Issues**
   - Render supports long-running connections
   - Ensure your frontend handles reconnection

### Logs

View logs in the Render dashboard:
1. Go to your web service
2. Click **Logs** tab
3. Filter by time or search for specific errors

## Scaling

### Horizontal Scaling (Paid Plans)

1. Go to your web service settings
2. Increase the number of instances
3. Render automatically load balances

### Vertical Scaling

1. Upgrade your plan for more CPU/RAM
2. Restart the service to apply changes

## Cost Optimization

- **Free Tier**: Good for development/testing
  - Services spin down after 15 minutes of inactivity
  - Cold starts may take 30+ seconds
  
- **Paid Plans**: For production
  - Always-on services
  - Better performance
  - Custom domains with SSL

## Custom Domain

1. Go to your web service settings
2. Click **Custom Domains**
3. Add your domain
4. Configure DNS as instructed
5. SSL is automatically provisioned

## Continuous Deployment

Render automatically deploys when you push to your connected branch. To disable:

1. Go to service settings
2. Under **Build & Deploy**, toggle off auto-deploy
3. Use manual deploys or deploy hooks instead
