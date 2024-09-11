# AI Landing Zone on Google Cloud

This repository contains the source code for a quick start AI project on Google Cloud Platform (GCP), including a machine learning model, Vertex AI pipeline, Docker configuration, CI/CD setup, and deployment scripts.

## Repository Structure

- `src/`: Source code for models, pipelines, and data.
  - `models/`: Machine learning model code and dependencies.
  - `pipelines/`: Vertex AI pipeline definitions.
  - `data/`: Sample datasets.
- `docker/`: Docker-related files for containerizing the training job.
- `scripts/`: Deployment and management scripts.
- `.github/workflows/`: GitHub Actions workflows for CI/CD.

## Setup Instructions

1. **Prerequisites**

   Ensure that the required GCP resources (buckets, Vertex AI Workbench, Artifact Registry) have been created using Terraform or other means.

2. **Clone the Repository**

   ```bash
   git clone https://github.com/your-org/ai-landingzone.git
   cd ai-landingzone
