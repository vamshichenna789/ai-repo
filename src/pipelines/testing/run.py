from google.cloud import aiplatform

# Set up project, location, and pipeline root
project = 'cdp-demo-395508'
location = 'us-central1'
pipeline_root = 'gs://cdp-demo-395508/pipeline-root'
template_path = 'irisTrainingPipeline.yaml'
service_account = 'mlops-sa@{project}.iam.gserviceaccount.com'

# Initialize the AI Platform client
aiplatform.init(project=project, location=location)

# Define parameter values
parameter_values = {
    'project': project,
    'location': location,
    'container_uri': 'us-central1-docker.pkg.dev/{project}/ml-repo/iris-train:latest',
    'model_serving_container_image_uri': 'us-central1-docker.pkg.dev/{project}/ml-repo/iris-serve:latest',
    'staging_bucket': 'gs://{project}-ai-landingzone-models',
    'model_display_name': 'iris-model',
    'replica_count': 1,
    'machine_type': 'n1-standard-4',
    'base_output_dir': 'gs://{project}-ai-landingzone-models/',
    'service_account': service_account,
    'user_email': ['krishna.chenna@fisclouds.com',],
    'bucket_uri': 'gs://{project}-ai-landingzone-datasets',
    'dataset_gcs_uri': 'gs://{project}-ai-landingzone-datasets/iris.csv',
    'drift_threshold_value': 0.05,
    'skew_threshold_value': 0.5,
    'sample_rate': 0.5,
    'monitor_interval': 1
}

job = aiplatform.PipelineJob(
    display_name='iris-training-pipeline',
    enable_caching=False,
    template_path=template_path,
    pipeline_root=pipeline_root,
    location=location,
    parameter_values=parameter_values
)


job.run(service_account=service_account)
