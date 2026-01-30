# Deploy to Google App Engine

## Quick Deployment Guide

### Prerequisites
1. **Google Cloud SDK**: https://cloud.google.com/sdk/docs/install
2. **Login**: `gcloud auth login`
3. **Set project**: `gcloud config set project YOUR_PROJECT_ID`

---

## Step 1: Create Cloud Storage Bucket (One-time)

```bash
# Create bucket for database storage
gsutil mb -l us-central1 gs://inventory-slawburger

# Verify bucket created
gsutil ls gs://inventory-slawburger/
```

---

## Step 2: Deploy to App Engine

```bash
cd C:\inv_slawV202

# Deploy (first time will ask to choose region - select us-central1)
gcloud app deploy

# When prompted:
# - Choose region: us-central1 (or same as duty tracker)
# - Confirm deployment: Y
```

**Deployment takes 3-5 minutes**

---

## Step 3: Get Your App URL

```bash
# Open app in browser
gcloud app browse

# Or get URL directly
gcloud app describe --format="value(defaultHostname)"
```

Your URL will be: `https://YOUR_PROJECT_ID.uc.r.appspot.com`

---

## Step 4: Update Duty Tracker Navigation

1. Open `C:\duty-tracker\frontend\src\lib\components\Navigation.svelte`
2. Find `http://localhost:5001`
3. Replace with your App Engine URL: `https://YOUR_PROJECT_ID.uc.r.appspot.com`
4. Deploy frontend:
   ```bash
   cd C:\duty-tracker\frontend
   npm run build
   firebase deploy --only hosting
   ```

---

## Verify Deployment

### Test Inventory App
```bash
# Get your URL
APP_URL=$(gcloud app describe --format="value(defaultHostname)")

# Test endpoints
curl https://$APP_URL/api/stock
curl https://$APP_URL/api/recipes
```

### Check Logs
```bash
gcloud app logs tail -s default
```

### View in Console
https://console.cloud.google.com/appengine

---

## Database Persistence

- **On Startup**: Downloads `inventory.db` from Cloud Storage
- **On Shutdown**: Uploads `inventory.db` to Cloud Storage
- **Backup**: `gsutil cp gs://inventory-slawburger/inventory.db ./backup.db`

---

## Troubleshooting

### Deployment Fails
```bash
# Check logs
gcloud app logs tail -s default

# Redeploy
gcloud app deploy --quiet
```

### Database Not Loading
```bash
# Check bucket
gsutil ls gs://inventory-slawburger/

# Check permissions
gcloud projects get-iam-policy YOUR_PROJECT_ID
```

### Update Code
```bash
# Just redeploy
gcloud app deploy
```

---

## Cost

- **App Engine**: $0-5/month (free tier covers most usage)
- **Cloud Storage**: ~$0.02/month
- **Total**: ~$0-5/month

---

## Useful Commands

```bash
# View versions
gcloud app versions list

# Stop a version (to save costs)
gcloud app versions stop VERSION_ID

# View services
gcloud app services list

# Delete app (if needed)
gcloud app services delete default
```

---

## Next Steps

1. ✅ Deploy: `gcloud app deploy`
2. ✅ Get URL: `gcloud app describe --format="value(defaultHostname)"`
3. ✅ Update duty tracker navigation
4. ✅ Test the integration!
