#!/bin/bash

set -e

# Validate GCS buckets
gsutil ls gs://ai-landingzone-datasets/
gsutil ls gs://ai-landingzone-models/

# Validate deployed model endpoints
gcloud ai endpoints list | grep "iris-model"

echo "All resources are validated and exist."
