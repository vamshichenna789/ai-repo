#!/bin/bash

# Variables
PROJECT_ID="YOUR_GCP_PROJECT_ID"
REGION="us-central1"
REPO="ml-repo"
IMAGE_NAME="iris-train"
TAG="latest"

# Authenticate with Google Cloud
gcloud auth configure-docker us-central1-docker.pkg.dev

# Build the Docker image
docker build -t us-central1-docker.pkg.dev/${PROJECT_ID}/${REPO}/${IMAGE_NAME}:${TAG} -f Dockerfile ../

# Push the Docker image to Artifact Registry
docker push us-central1-docker.pkg.dev/${PROJECT_ID}/${REPO}/${IMAGE_NAME}:${TAG}
