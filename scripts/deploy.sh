#!/bin/bash

set -e

# Variables
PROJECT_ID="cdp-demo-395508"
REGION="us-central1"

# Build and push the Docker image
cd docker
./build_push.sh
cd ..

# Upload the dataset to GCS
gsutil cp src/data/iris_data.csv gs://${PROJECT_ID}-ai-landingzone-datasets/iris_data.csv

# Deploy the Vertex AI pipeline
python3 src/pipelines/iris_pipeline.py

echo "Deployment completed successfully."
