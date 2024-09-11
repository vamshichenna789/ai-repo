from google.cloud import aiplatform
from google.cloud.aiplatform import pipeline_jobs
from google.cloud.aiplatform import training_utils
import os
import kfp
from kfp import dsl
from kfp import components
from kfp import compiler
from kfp.dsl import component
from google.cloud.aiplatform import model_monitoring

# Initialize the AI Platform client
aiplatform.init(project='cdp-demo-395508', location='us-central1',staging_bucket="gs://cdp-demo-395508-ai-landingzone-logs/")
    # Define the custom training job
@component(packages_to_install = [
        "google-cloud-aiplatform==1.34.0","google-cloud-bigquery==3.13.0","google-cloud-storage==2.10.0",
         "kfp==2.3.0"],)

def iris_training_job():
    from google.cloud import aiplatform
    from google.cloud.aiplatform import model_monitoring
    aiplatform.init(project='cdp-demo-395508', location='us-central1',staging_bucket="gs://cdp-demo-395508-ai-landingzone-models")
    # Define the custom training job
    training_job = aiplatform.CustomContainerTrainingJob(
        display_name="iris-training-job",
        container_uri="us-central1-docker.pkg.dev/cdp-demo-395508/ml-repo/iris-train:latest",
        #command=["python", "train.py"],
        model_serving_container_image_uri="us-central1-docker.pkg.dev/cdp-demo-395508/ml-repo/iris-serve:latest",
        staging_bucket = "gs://cdp-demo-395508-ai-landingzone-models/model"
    )
    
    # Run the training job
    model = training_job.run(
        dataset=None,  # Not using a predefined dataset
        model_display_name="iris-model",
        replica_count=1,
        machine_type="n1-standard-4",
        base_output_dir="gs://cdp-demo-395508-ai-landingzone-models/",
        service_account="mlops-sa@cdp-demo-395508.iam.gserviceaccount.com",
        args=[],
    )
    
    # Deploy the model to an endpoint
    endpoint = model.deploy(
        machine_type="n1-standard-4",
        service_account = "mlops-sa@cdp-demo-395508.iam.gserviceaccount.com",
        min_replica_count=1,
        max_replica_count=1,
        sync=True
    )
    # Set the monitoring configurations
    PROJECT_ID = "cdp-demo-395508"
    LOCATION = "us-central1"
    USER_EMAIL = "krishna.chenna@fisclouds.com"
    BUCKET_URI = "gs://cdp-demo-395508-ai-landingzone-datasets"

    # Monitoring interval in hours
    MONITOR_INTERVAL = 1

    # Create schedule configuration
    schedule_config = model_monitoring.ScheduleConfig(monitor_interval=MONITOR_INTERVAL)

    # Create alerting configuration
    alerting_config = model_monitoring.EmailAlertConfig(
        user_emails=[USER_EMAIL],
        enable_logging=True
    )

    # Set drift detection thresholds
    DRIFT_THRESHOLD_VALUE = 0.05
    DRIFT_THRESHOLDS = {
        "sepal_length": DRIFT_THRESHOLD_VALUE,
        "sepal_width": DRIFT_THRESHOLD_VALUE,
        "petal_length": DRIFT_THRESHOLD_VALUE,
        "petal_width": DRIFT_THRESHOLD_VALUE,
    }

    # Configure drift detection
    drift_config = model_monitoring.DriftDetectionConfig(drift_thresholds=DRIFT_THRESHOLDS)

    # Configure skew detection
    DATASET_GCS_URI = "gs://cdp-demo-395508-ai-landingzone-datasets/iris.csv"

    SKEW_THRESHOLD_VALUE = 0.5
    SKEW_THRESHOLDS = {
        "sepal_length": SKEW_THRESHOLD_VALUE,
        "sepal_width": SKEW_THRESHOLD_VALUE,
        "petal_length": SKEW_THRESHOLD_VALUE,
        "petal_width": SKEW_THRESHOLD_VALUE,
    }

    skew_config = model_monitoring.SkewDetectionConfig(
        data_source=DATASET_GCS_URI,
        data_format='csv',
        skew_thresholds=SKEW_THRESHOLDS
    )

    # Create the objective configuration (for drift and skew detection)
    objective_config = model_monitoring.ObjectiveConfig(
        skew_detection_config=skew_config,
        drift_detection_config=drift_config,
        explanation_config=None
    )

    # Sampling rate
    SAMPLE_RATE = 0.5
    logging_sampling_strategy = model_monitoring.RandomSampleConfig(sample_rate=SAMPLE_RATE)

    # Create the model deployment monitoring job
    monitoring_job = aiplatform.ModelDeploymentMonitoringJob.create(
        display_name="iris-monitoring-job",
        project=PROJECT_ID,
        location=LOCATION,
        endpoint=endpoint,
        logging_sampling_strategy=logging_sampling_strategy,
        schedule_config=schedule_config,
        alert_config=alerting_config,
        objective_configs=objective_config,
        analysis_instance_schema_uri=f"{BUCKET_URI}/schema.yaml",  # Ensure the schema.yaml file exists
    )

    print("Model Monitoring job created:", monitoring_job.resource_name)
    
    print(f"Model deployed at endpoint: {endpoint.resource_name}")

if __name__ == "__main__":
    iris_training_job()
