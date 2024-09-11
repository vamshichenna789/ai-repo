import kfp
from kfp import dsl
from kfp import components
from train_component import iris_training_component
from endpoint_component import iris_deployment_component

@dsl.pipeline(
    name="iris_pipeline",
    description='Pipeline to train and deploy the Iris model using AI Platform.'
)
def iris_pipeline(
    project: str = 'cdp-demo-395508',
    location: str = 'us-central1',
    container_uri: str = 'us-central1-docker.pkg.dev/cdp-demo-395508/ml-repo/iris-train:latest',
    model_serving_container_image_uri: str = 'us-central1-docker.pkg.dev/cdp-demo-395508/ml-repo/iris-serve:latest',
    staging_bucket: str = 'gs://cdp-demo-395508-ai-landingzone-models',
    model_display_name: str = 'iris-model',
    replica_count: int = 1,
    machine_type: str = 'n1-standard-4',
    base_output_dir: str = 'gs://cdp-demo-395508-ai-landingzone-models/',
    service_account: str = 'mlops-sa@cdp-demo-395508.iam.gserviceaccount.com',
    user_email: list(str) = ['krishna.chenna@fisclouds.com',],
    bucket_uri: str = 'gs://cdp-demo-395508-ai-landingzone-datasets',
    dataset_gcs_uri: str = 'gs://cdp-demo-395508-ai-landingzone-datasets/iris.csv',
    drift_threshold_value: float = 0.05,
    skew_threshold_value: float = 0.5,
    sample_rate: float = 0.5,
    monitor_interval: int = 1  # hours
):
 
    training_op = iris_training_component(
        project=project,
        location=location,
        container_uri=container_uri,
        model_serving_container_image_uri=model_serving_container_image_uri,
        staging_bucket=staging_bucket,
        model_display_name=model_display_name,
        replica_count=replica_count,
        machine_type=machine_type,
        base_output_dir=base_output_dir,
        service_account=service_account
    )

   
    deploy_op = iris_deployment_component(
        project=project,
        location=location,
        model_display_name=model_display_name,
        machine_type=machine_type,
        service_account=service_account,
        user_email=user_email,
        bucket_uri=bucket_uri,
        dataset_gcs_uri=dataset_gcs_uri,
        drift_threshold_value=drift_threshold_value,
        skew_threshold_value=skew_threshold_value,
        sample_rate=sample_rate,
        monitor_interval=monitor_interval
    )
    deploy_op.after(training_op)

