
#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status
set -o pipefail  # Catch errors in pipelines

########################## BACKEND ##########################
echo "🔧 Building backend"

ENV_FILE="backend/environment.yml"
ENV_NAME=$(grep -m1 '^name:' "$ENV_FILE" | cut -d ' ' -f2)

if conda info --envs | grep -q "^$ENV_NAME"; then
    echo "✅ Environment '$ENV_NAME' already exists. Updating..."
    conda env update -n "$ENV_NAME" -f "$ENV_FILE"
else
    echo "🆕 Environment '$ENV_NAME' does not exist. Creating..."
    conda env create -f "$ENV_FILE"
fi

echo "✅ Backend setup complete"
source "$(conda info --base)/etc/profile.d/conda.sh"  # Ensure conda command works in script
conda activate "$ENV_NAME"

########################## FRONTEND ##########################
echo "🌐 Building frontend"

cd frontend/
npm install

echo "✅ Frontend setup complete"