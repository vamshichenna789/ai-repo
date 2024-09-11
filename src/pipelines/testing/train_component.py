from kfp.dsl import component
@component(packages_to_install=[
    "google-cloud-aiplatform==1.34.0",
    "google-cloud-storage==2.10.0",
    "kfp==2.3.0"
])
def iris_training_component(
    project: str,
    location: str,
    container_uri: str,
    model_serving_container_image_uri: str,
    staging_bucket: str,
    model_display_name: str,
    replica_count: int,
    machine_type: str,
    base_output_dir: str,
    service_account: str
):
    from google.cloud import aiplatform
    aiplatform.init(project=project, location=location, staging_bucket=staging_bucket)

    # Define the custom training job
    training_job = aiplatform.CustomContainerTrainingJob(
        display_name=model_display_name,
        container_uri=container_uri,
        model_serving_container_image_uri=model_serving_container_image_uri,
        staging_bucket=staging_bucket
    )

    # Run the training job
    model = training_job.run(
        dataset=None,
        model_display_name=model_display_name,
        replica_count=replica_count,
        machine_type=machine_type,
        base_output_dir=base_output_dir,
        service_account=service_account,
        args=[],
    )


