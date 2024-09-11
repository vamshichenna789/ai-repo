import kfp
from kfp import dsl
from kfp import components
from kfp import compiler
from kfp.dsl import component
from google.cloud import aiplatform
from pipeline import iris_pipeline

compiler.Compiler().compile(
    pipeline_func=iris_pipeline, package_path="irisTrainingPipeline.yaml"
)
def UploadToGCS():
    from google.cloud import storage

    bucket_name = 'cdp-demo-395508-ai-landingzone-models'
    file_to_upload='irisTrainingPipeline.yaml'

    project_id = 'globe-amp-interestai-prod'
    file_to_upload =  file_to_upload # Replace with the path of the file you want to upload
    destination_blob_name = 'pipelines/TrainingPipeline/{}'.format(file_to_upload) # Replace with the desired destination in the bucket
    print(destination_blob_name)
    # Initialize a client
    client = storage.Client(project=project_id)

    # Get the bucket
    bucket = client.get_bucket(bucket_name)

    # Create a blob (file) in the bucket
    blob = bucket.blob(destination_blob_name)

    # Upload a file to the created blob
    blob.upload_from_filename(file_to_upload)

    print(f"File {file_to_upload} uploaded to {bucket_name} as {destination_blob_name}")



UploadToGCS()