# Google Cloud SDK Installation for Windows (PowerShell)

## Quick Install via PowerShell

### Option 1: Download and Install (Recommended)

```powershell
# Download the installer
$url = "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe"
$output = "$env:TEMP\GoogleCloudSDKInstaller.exe"
Invoke-WebRequest -Uri $url -OutFile $output

# Run the installer
Start-Process -FilePath $output -Wait

# After installation, restart PowerShell and run:
gcloud init
```

### Option 2: Manual Download

1. Download: https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe
2. Run the installer
3. Follow the installation wizard
4. **Restart PowerShell**
5. Verify: `gcloud --version`

---

## After Installation

```powershell
# Login to Google Cloud
gcloud auth login

# Set your project (same as duty tracker)
gcloud config set project YOUR_PROJECT_ID

# List projects to find your project ID
gcloud projects list

# Create Cloud Storage bucket
gsutil mb -l us-central1 gs://inventory-slawburger

# Deploy to App Engine
cd C:\inv_slawV202
gcloud app deploy

# Get your app URL
gcloud app describe --format="value(defaultHostname)"
```

---

## Troubleshooting

### "gcloud is not recognized"

**Solution**: Restart PowerShell after installation

```powershell
# Close and reopen PowerShell, then verify:
gcloud --version
```

### Find Your Project ID

```powershell
# After gcloud is installed:
gcloud projects list

# Or check Firebase console:
# https://console.firebase.google.com/
```

---

## Alternative: Use Cloud Shell (No Installation)

If you don't want to install anything:

1. Go to: https://console.cloud.google.com
2. Click the Cloud Shell icon (top right, looks like `>_`)
3. Upload your files or clone from git
4. Run deployment commands in the browser

---

## Estimated Time

- **Download**: 2-3 minutes
- **Install**: 5-10 minutes
- **Configure**: 2-3 minutes
- **Deploy**: 3-5 minutes

**Total**: ~15-20 minutes

---

## Next Steps

1. Install Google Cloud SDK
2. Restart PowerShell
3. Run: `gcloud init`
4. Deploy: `gcloud app deploy`

Let me know when you've installed it and I'll help with the deployment!
