#!/bin/bash


##########################BACKEND##########################
echo "Building backend"
ENV_NAME=$(grep -m1 '^name:' environment.yml | cut -d ' ' -f2)

if conda info --envs | grep -q "^$ENV_NAME"; then
    echo "✅ Environment '$ENV_NAME' already exists. Updating..."
    conda env update -n "$ENV_NAME" -f environment.yml
else
    echo "🆕 Environment '$ENV_NAME' does not exist. Creating..."
    conda env create -f environment.yml
fi

echo "Backend ✅"
conda activate $ENV_NAME
##########################FRONTEND##########################
echo "Building frontend"

cd frontend/

npm install
echo "Frontend ✅"
