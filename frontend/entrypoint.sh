#!/bin/bash

# Default to PROD=False if not explicitly set
PROD=${PROD:-True}

echo "PROD is set to $PROD"

if [ $PROD == True ]; then
    echo "Running Vite in production mode..."
    npm run build
    npm install -g serve
    serve -s dist
else
    echo "Running Vite in development mode..."
    npm run dev
fi
