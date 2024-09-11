import kfp
from kfp import dsl
from iris_pipeline import iris_training_job
@dsl.pipeline(
    name='Iris Training and Deployment Pipeline',
    description='Pipeline to train and deploy the Iris model using AI Platform.'
)
def iris_pipeline():
    # Define the component
    train_and_deploy_op = iris_training_job()