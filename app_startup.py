"""
Startup script for App Engine with Cloud Storage persistence.
Downloads SQLite database from Cloud Storage on startup.
Falls back to local database if Cloud Storage is unavailable.
"""
import os
from google.cloud import storage

BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME', 'inventory-slawburger')
DB_FILE = 'data/inventory.db'
GCS_DB_PATH = 'inventory.db'
CLOUD_ENABLED = False  # Will be set to True if credentials are found

def check_cloud_credentials():
    """Check if Google Cloud credentials are available"""
    global CLOUD_ENABLED
    
    # Check for Application Default Credentials
    if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        CLOUD_ENABLED = True
        return True
    
    try:
        # Try to create a client to test credentials
        client = storage.Client()
        CLOUD_ENABLED = True
        return True
    except Exception as e:
        print(f"⚠️  Google Cloud credentials not found: {str(e)[:100]}")
        print(f"ℹ️  Will use local database only (changes won't sync to cloud)")
        CLOUD_ENABLED = False
        return False

def sync_database_from_storage():
    """Download database from Cloud Storage on startup"""
    if not check_cloud_credentials():
        print(f"ℹ️  Initializing local database...")
        os.makedirs('data', exist_ok=True)
        from src.database import init_db
        init_db()
        return
    
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(GCS_DB_PATH)
        
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        if blob.exists():
            print(f"📥 Downloading database from gs://{BUCKET_NAME}/{GCS_DB_PATH}")
            blob.download_to_filename(DB_FILE)
            print(f"✅ Database loaded successfully from Cloud Storage")
        else:
            print(f"ℹ️  No existing database found in Cloud Storage")
            print(f"ℹ️  Initializing new database...")
            from src.database import init_db
            init_db()
            # Upload the new database
            try:
                blob.upload_from_filename(DB_FILE)
                print(f"✅ New database created and uploaded to Cloud Storage")
            except Exception as e:
                print(f"⚠️  Could not upload database: {e}")
    except Exception as e:
        print(f"⚠️  Error with Cloud Storage: {e}")
        print(f"ℹ️  Using local database...")
        os.makedirs('data', exist_ok=True)
        from src.database import init_db
        init_db()

def sync_database_to_storage():
    """Upload database to Cloud Storage (if credentials available)"""
    if not CLOUD_ENABLED:
        return  # Skip if cloud is not enabled
    
    try:
        if os.path.exists(DB_FILE):
            client = storage.Client()
            bucket = client.bucket(BUCKET_NAME)
            blob = bucket.blob(GCS_DB_PATH)
            blob.upload_from_filename(DB_FILE)
            print(f"✅ Database synced to Cloud Storage")
        else:
            print(f"⚠️  Database file not found: {DB_FILE}")
    except Exception as e:
        print(f"⚠️  Error syncing to Cloud Storage: {e}")
    except Exception as e:
        print(f"⚠️  Error uploading database: {e}")

# Download database when module is imported (on app startup)
print("🚀 Starting App Engine instance...")
sync_database_from_storage()
