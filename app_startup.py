"""
Startup script for App Engine with Cloud Storage persistence.
Downloads SQLite database from Cloud Storage on startup.
"""
import os
from google.cloud import storage

BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME', 'inventory-slawburger')
DB_FILE = 'data/inventory.db'
GCS_DB_PATH = 'inventory.db'

def sync_database_from_storage():
    """Download database from Cloud Storage on startup"""
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(GCS_DB_PATH)
        
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        if blob.exists():
            print(f"📥 Downloading database from gs://{BUCKET_NAME}/{GCS_DB_PATH}")
            blob.download_to_filename(DB_FILE)
            print(f"✅ Database loaded successfully")
        else:
            print(f"ℹ️  No existing database found in Cloud Storage")
            print(f"ℹ️  Initializing new database...")
            from src.database import init_db
            init_db()
            # Upload the new database
            blob.upload_from_filename(DB_FILE)
            print(f"✅ New database created and uploaded to Cloud Storage")
    except Exception as e:
        print(f"⚠️  Error downloading database: {e}")
        print(f"ℹ️  Initializing new database locally...")
        from src.database import init_db
        init_db()

def sync_database_to_storage():
    """Upload database to Cloud Storage"""
    try:
        if os.path.exists(DB_FILE):
            client = storage.Client()
            bucket = client.bucket(BUCKET_NAME)
            blob = bucket.blob(GCS_DB_PATH)
            blob.upload_from_filename(DB_FILE)
            print(f"✅ Database synced to gs://{BUCKET_NAME}/{GCS_DB_PATH}")
        else:
            print(f"⚠️  Database file not found: {DB_FILE}")
    except Exception as e:
        print(f"⚠️  Error uploading database: {e}")

# Download database when module is imported (on app startup)
print("🚀 Starting App Engine instance...")
sync_database_from_storage()
