#!/bin/bash
# Ensure logs directory exists
mkdir -p logs

# If credentials file doesn't exist but environment variables are set, create it
if [ ! -f logs/toast_credentials.txt ]; then
    if [ ! -z "$CLIENT_ID" ] && [ ! -z "$RESTAURANT_GUID" ]; then
        echo "Creating credentials file from environment variables..."
        cat > logs/toast_credentials.txt << EOF
CLIENT_ID=$CLIENT_ID
CLIENT_SECRET=$CLIENT_SECRET
RESTAURANT_GUID=$RESTAURANT_GUID
ACCESS_TOKEN=$ACCESS_TOKEN
MANAGEMENT_GROUP_GUID=$MANAGEMENT_GROUP_GUID
EOF
        chmod 600 logs/toast_credentials.txt
        echo "Credentials file created successfully"
    fi
fi

# Run the Flask app
exec gunicorn -b :$PORT --timeout 300 --workers 1 app:app
