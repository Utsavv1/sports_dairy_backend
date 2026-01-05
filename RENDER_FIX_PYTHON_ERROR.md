# Fix: Render Python 3.13 Rust Compilation Error

## 🔴 Problem
Render is using Python 3.13 which doesn't have pre-built wheels for `cryptography` and `bcrypt`, causing Rust compilation errors on read-only filesystem.

## ✅ Solution Applied

We've replaced problematic packages:
- ❌ `python-jose[cryptography]` → ✅ `pyjwt` + `cryptography` (with pre-built wheels)
- ❌ `passlib[bcrypt]` → ✅ `passlib` + `bcrypt` (specific version with wheels)

## 🚀 Deploy Steps on Render

### Method 1: Force Python 3.11 in Render Dashboard (RECOMMENDED)

1. **Go to your Render service** → Settings
2. **Scroll to "Python Version"**
3. **Select "3.11" from dropdown**
4. **Save Changes**
5. **Go to "Manual Deploy"** → "Clear build cache & deploy"

### Method 2: Set Environment Variable

1. **Go to your Render service** → Environment
2. **Add Environment Variable:**
   ```
   Key: PYTHON_VERSION
   Value: 3.11.9
   ```
3. **Save Changes**
4. **Manual Deploy** → "Clear build cache & deploy"

### Method 3: Configure in Dashboard Settings

1. **Root Directory:** `backend`
2. **Build Command:**
   ```bash
   bash render-build.sh
   ```
   
   OR if that doesn't work:
   ```bash
   pip install --upgrade pip && pip install --no-cache-dir --prefer-binary -r requirements.txt
   ```

3. **Start Command:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

### Method 4: Use render.yaml Blueprint

1. **In Render Dashboard:** New → Blueprint
2. **Connect your GitHub repository**
3. **Render will automatically detect and use `render.yaml`**

## 🔍 Verify Python Version

After deployment, check logs for:
```
Python version: 3.11.9
```

If you still see `python3.13`, do this:

1. **In Render Dashboard:**
   - Settings → Delete "PYTHON_VERSION" if it exists
   - Add it again: `PYTHON_VERSION=3.11.9`
   - Clear build cache
   - Redeploy

2. **Check Build Logs** for:
   ```
   Using Python version 3.11.9
   ```

## 📦 What Changed in Code

### requirements.txt
```diff
- python-jose[cryptography]==3.3.0
- passlib[bcrypt]==1.7.4
+ pyjwt==2.8.0
+ cryptography==41.0.7
+ passlib==1.7.4
+ bcrypt==4.1.2
```

### security.py
```diff
- from jose import JWTError, jwt
+ import jwt
+ from jwt.exceptions import InvalidTokenError
```

```diff
- except JWTError:
+ except InvalidTokenError:
```

## 🆘 If Still Not Working

### Option 1: Check Render Settings
```bash
# In Render Shell (after deployment fails)
python --version  # Should show 3.11.x
```

### Option 2: Contact Render Support
- Open a ticket with Render
- Mention: "Need Python 3.11, but getting 3.13"
- Reference: `runtime.txt` not being respected

### Option 3: Use Docker Deployment
If Python version keeps reverting to 3.13:
1. Use Render's Docker deployment instead
2. We already have `Dockerfile` ready
3. In Render: New → Web Service → Docker

## 📝 Checklist

- [ ] Updated `requirements.txt` (removed python-jose, passlib[bcrypt])
- [ ] Updated `security.py` (using pyjwt instead of jose)
- [ ] Created `runtime.txt` with Python 3.11.9
- [ ] Set PYTHON_VERSION in Render environment
- [ ] Cleared build cache in Render
- [ ] Verified Python 3.11 in build logs
- [ ] Successfully deployed without Rust errors

## 🎯 Expected Build Log (Success)

```
==> Building...
==> Using Python version 3.11.9 specified in runtime.txt
==> Installing dependencies from requirements.txt
Collecting fastapi==0.109.0
  Using cached fastapi-0.109.0-py3-none-any.whl
Collecting pyjwt==2.8.0
  Using cached PyJWT-2.8.0-py3-none-any.whl
Collecting cryptography==41.0.7
  Using cached cryptography-41.0.7-cp311-cp311-manylinux_2_28_x86_64.whl
...
Successfully installed ...
==> Build successful!
```

## ❌ Failed Build Log (Problem)

```
==> Building...
==> Using Python version 3.13.x  ⚠️ WRONG VERSION
...
Preparing metadata (pyproject.toml): finished with status 'error'
error: failed to create directory `/usr/local/cargo/...`
Caused by: Read-only file system (os error 30)
💥 maturin failed
==> Build failed
```

## 💡 Quick Fix Command

If Render keeps using Python 3.13:

**In Render Dashboard → Shell (after deployment):**
```bash
# Check Python version
python --version

# If it shows 3.13, force reinstall with Python 3.11
python3.11 -m pip install --upgrade pip
python3.11 -m pip install -r requirements.txt
```

Then in Settings, change Start Command to:
```bash
python3.11 -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## 🎉 Success Indicators

✅ Build logs show Python 3.11.9
✅ No Rust compilation errors
✅ All dependencies installed successfully
✅ Service starts without errors
✅ API endpoint `/health` returns 200 OK

## 📞 Support

If none of these work:
1. **Check Render Status:** https://status.render.com/
2. **Render Community:** https://community.render.com/
3. **Open Support Ticket:** dashboard.render.com → Help

