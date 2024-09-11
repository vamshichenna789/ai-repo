from kfp.dsl import component
@component(packages_to_install=[
    "google-cloud-aiplatform==1.34.0",
    "google-cloud-storage==2.10.0",
    "kfp==2.3.0"
])
def iris_deployment_component(
    project: str,
    location: str,
    model_display_name: str,
    machine_type: str,
    service_account: str,
    user_email: list[str],
    bucket_uri: str,
    dataset_gcs_uri: str,
    drift_threshold_value: float,
    skew_threshold_value: float,
    sample_rate: float,
    monitor_interval: int
):
    from google.cloud import aiplatform
    from google.cloud.aiplatform import model_monitoring

    aiplatform.init(project=project, location=location)

    model_uid = aiplatform.Model.list(
                filter=f'display_name={model_display_name}',      
                order_by="update_time",
                location=location)[-1]
    model = model_uid.resource_name
    

    # Deploy the model to an endpoint
    endpoint = model.deploy(
        machine_type=machine_type,
        service_account=service_account,
        min_replica_count=1,
        max_replica_count=1,
        sync=True
    )

    # Monitoring setup
    schedule_config = model_monitoring.ScheduleConfig(monitor_interval=monitor_interval)

    alerting_config = model_monitoring.EmailAlertConfig(
        user_emails=user_email,
        enable_logging=True
    )

    drift_config = model_monitoring.DriftDetectionConfig(
        drift_thresholds={
            "sepal_length": drift_threshold_value,
            "sepal_width": drift_threshold_value,
            "petal_length": drift_threshold_value,
            "petal_width": drift_threshold_value,
        }
    )

    skew_config = model_monitoring.SkewDetectionConfig(
        data_source=dataset_gcs_uri,
        data_format="csv",
        skew_thresholds={
            "sepal_length": skew_threshold_value,
            "sepal_width": skew_threshold_value,
            "petal_length": skew_threshold_value,
            "petal_width": skew_threshold_value,
        }
    )

    objective_config = model_monitoring.ObjectiveConfig(
        skew_detection_config=skew_config,
        drift_detection_config=drift_config
    )

    logging_sampling_strategy = model_monitoring.RandomSampleConfig(sample_rate=sample_rate)

    # Create model monitoring job
    monitoring_job = aiplatform.ModelDeploymentMonitoringJob.create(
        display_name="iris-monitoring-job",
        project=project,
        location=location,
        endpoint=endpoint,
        logging_sampling_strategy=logging_sampling_strategy,
        schedule_config=schedule_config,
        alert_config=alerting_config,
        objective_configs=objective_config,
        analysis_instance_schema_uri=f"{bucket_uri}/schema.yaml",
    )

    print("Model deployed at endpoint:", endpoint.resource_name)
    print("Model monitoring job created:", monitoring_job.resource_name)
