
from google.cloud import aiplatform
SERVICE_ACCOUNT = "mlops-sa@cdp-demo-395508.iam.gserviceaccount.com"
BUCKET_URI = "gs://cdp-demo-395508-ai-landingzone-logs"
PIPELINE_ROOT = "{}/pipeline_root/".format(BUCKET_URI)
project = "cdp-demo-395508"
location = "us-central1"
aiplatform.init(project=project,location=location,staging_bucket="gs://cdp-demo-395508-ai-landingzone-logs/logs/staging")
    # Define the custom training job
job = aiplatform.PipelineJob(
    display_name='iris Pipeline',
    enable_caching=False,
    template_path="gs://cdp-demo-395508-ai-landingzone-models/pipelines/TrainingPipeline/irisTrainingPipeline.yaml",
    pipeline_root=PIPELINE_ROOT,
    location='us-central1',

)
job.run(service_account=SERVICE_ACCOUNT)