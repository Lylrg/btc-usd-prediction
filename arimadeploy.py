import mlflow.sagemaker

# Define variables
experiment_id = '790719470095171806'
run_id = 'cadaf377c7ca46599d393560a36669b8'
region = 'eu-north-1'
aws_id = '339712788522'
arn = 'arn:aws:iam::339712788522:role/arn'
app_name = 'arima-model-btc'
model_uri = f'mlruns/{experiment_id}/{run_id}/artifacts/arima-model'
tag_id = '2.14.1'  # Image tag from Amazon Container Services

image_url = f'{aws_id}.dkr.ecr.{region}.amazonaws.com/mlflow-pyfunc:{tag_id}'

# Create a SageMakerDeploymentClient
#client = mlflow.sagemaker.SageMakerDeploymentClient(
    #region_name=region,
    #assumed_role_arn=arn,
#)


# Define target URI for AWS SageMaker
target_uri = f'sagemaker:/{region}'

# Create a SageMakerDeploymentClient
client = mlflow.sagemaker.SageMakerDeploymentClient(target_uri)

# Deploy the model to SageMaker
client.create_deployment(
    name=app_name,
    model_uri=model_uri,
    config={
        "image_url": image_url,
        "execution_role_arn": arn,
        "instance_type": "ml.m5.xlarge"
    }
)
