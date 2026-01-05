# Render Deployment Guide for Sports Diary Backend

## 🚀 Quick Deploy

### Prerequisites
- MongoDB Atlas account (or external MongoDB instance)
- Render account

## Step-by-Step Deployment

### 1. Prepare MongoDB

**Option A: MongoDB Atlas (Recommended)**
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Go to Database Access → Add New Database User
4. Go to Network Access → Add IP Address → Allow Access from Anywhere (0.0.0.0/0)
5. Get your connection string:
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string (e.g., `mongodb+srv://username:password@cluster.mongodb.net/sportsdiary?retryWrites=true&w=majority`)

### 2. Deploy to Render

#### Method 1: Using Render Dashboard (Easiest)

1. **Create New Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   ```
   Name: sportsdiary-backend
   Region: Choose closest to your users
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install --upgrade pip && pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Set Environment Variables**
   Click "Advanced" → "Add Environment Variable":
   
   ```bash
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/sportsdiary?retryWrites=true&w=majority
   SECRET_KEY=your-super-secret-key-min-32-characters-long
   ALGORITHM=HS256
   PYTHON_VERSION=3.11.9
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)

#### Method 2: Using render.yaml

1. Push the `render.yaml` file to your repository
2. In Render Dashboard, select "Blueprint"
3. Connect your repository
4. Render will automatically detect and use `render.yaml`

### 3. Seed Database (Optional)

After deployment, you can seed your database:

1. Go to Render Dashboard → Your Service → Shell
2. Run:
   ```bash
   cd /opt/render/project/src/backend
   python seed_mongodb.py
   ```

Or seed from your local machine:
```bash
# Update MONGODB_URL in .env to your Render MongoDB URL
python seed_mongodb.py
```

### 4. Verify Deployment

Test your API:
```bash
# Replace with your actual Render URL
curl https://your-app.onrender.com/health
curl https://your-app.onrender.com/api/auth/health
```

## 🔧 Troubleshooting

### Error: "Read-only file system" or Rust compilation issues

**Fix 1: Ensure Python 3.11 is specified**
- Create `runtime.txt` with content: `python-3.11.9`
- Or set in Render dashboard: Environment Variables → `PYTHON_VERSION=3.11.9`

**Fix 2: Update requirements.txt**
Make sure you're using compatible versions:
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pydantic==2.5.3
pydantic-settings==2.1.0
motor==3.3.2
pymongo==4.6.1
python-dotenv==1.0.0
python-multipart==0.0.6
```

**Fix 3: Use Render's Python 3.11 runtime**
In Render Dashboard:
- Settings → Runtime → Select "Python 3.11"

### Error: "ModuleNotFoundError"

**Fix:** Check your build command includes all dependencies:
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

### Error: "Connection refused" or MongoDB connection issues

**Fix:** Verify MongoDB connection string:
1. Check `MONGODB_URL` environment variable is set correctly
2. Ensure MongoDB Atlas allows connections from all IPs (0.0.0.0/0)
3. Test connection locally first:
   ```bash
   python test_mongodb_connection.py
   ```

### Error: "Application failed to start"

**Fix:** Check logs in Render Dashboard:
1. Go to your service → Logs
2. Look for error messages
3. Common issues:
   - Missing environment variables
   - Incorrect start command
   - MongoDB connection failure

### Build takes too long or times out

**Fix:** Optimize build:
1. Use `.dockerignore` to exclude unnecessary files
2. Consider using Docker deployment instead
3. Upgrade to Render paid plan for faster builds

## 🔒 Security Best Practices

1. **Never commit sensitive data**
   - Add `.env` to `.gitignore`
   - Use Render's environment variables

2. **Use strong SECRET_KEY**
   ```bash
   # Generate a secure key
   openssl rand -hex 32
   ```

3. **Restrict MongoDB access**
   - In production, use specific IP whitelist
   - Enable MongoDB authentication
   - Use strong passwords

4. **Enable HTTPS**
   - Render provides SSL by default
   - Update frontend to use `https://` for API calls

## 📊 Monitoring

1. **Health Check**
   - Endpoint: `/health`
   - Render automatically monitors this

2. **View Logs**
   - Render Dashboard → Your Service → Logs
   - Enable log persistence for debugging

3. **Performance Metrics**
   - Render Dashboard → Your Service → Metrics
   - Monitor CPU, Memory, Response Time

## 💰 Cost Optimization

1. **Free Tier Limits**
   - 750 hours/month
   - Auto-sleep after 15 minutes of inactivity
   - Wakes up on first request (cold start ~30s)

2. **Keep Service Awake**
   - Upgrade to paid plan ($7/month)
   - Or use external monitoring (UptimeRobot, Better Uptime)

3. **Database Costs**
   - MongoDB Atlas: Free tier (512MB)
   - Consider upgrading if you need more storage

## 🔄 CI/CD

Render automatically redeploys when you push to your branch:

```bash
# Make changes
git add .
git commit -m "Update backend"
git push origin main

# Render will automatically deploy
```

To disable auto-deploy:
- Render Dashboard → Settings → Auto-Deploy → Disable

## 📱 Connect Frontend

Update your frontend environment variables:

```bash
# .env or .env.production
VITE_API_URL=https://your-backend.onrender.com
```

Or in your frontend code:
```javascript
// frontend/src/services/api.js
const API_URL = import.meta.env.VITE_API_URL || 'https://your-backend.onrender.com';
```

## 🆘 Need Help?

1. **Render Documentation**: https://render.com/docs
2. **Render Community**: https://community.render.com/
3. **MongoDB Atlas Support**: https://www.mongodb.com/docs/atlas/

## 📝 Checklist

- [ ] MongoDB Atlas cluster created
- [ ] MongoDB connection string obtained
- [ ] `runtime.txt` added with Python 3.11.9
- [ ] Render web service created
- [ ] Environment variables configured
- [ ] Build and start commands set
- [ ] Deployment successful
- [ ] Health endpoint responding
- [ ] Database seeded (if needed)
- [ ] Frontend connected to backend
- [ ] CORS configured for frontend domain
- [ ] SSL/HTTPS working

## 🎉 Success!

Your backend should now be live at: `https://your-app-name.onrender.com`

Test it:
```bash
curl https://your-app-name.onrender.com/health
```

Expected response:
```json
{"status": "healthy", "message": "Sports Diary API is running"}
```

