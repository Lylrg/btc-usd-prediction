import boto3
import pandas as pd
from io import StringIO
import tarfile
import os
import statsmodels.api as sm
from sklearn.metrics import r2_score
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import mlflow
import os
import numpy as np
import joblib

def download_data_from_s3(bucket_name, filename):
    s3_resource = boto3.resource('s3')
    try:
        obj = s3_resource.Object(bucket_name, filename)
        data = obj.get()['Body'].read().decode('utf-8')
        return pd.read_csv(StringIO(data))
    except s3_resource.meta.client.exceptions.NoSuchKey:
        print(f"Error: The specified key '{filename}' does not exist in bucket '{bucket_name}'.")
        return None

def download_and_extract_model(bucket_name, model_path, extract_to='/tmp'):
    s3_resource = boto3.resource('s3')
    try:
        obj = s3_resource.Object(bucket_name, model_path)
        with open(f'{extract_to}/model.tar.gz', 'wb') as f:
            f.write(obj.get()['Body'].read())
    except s3_resource.meta.client.exceptions.NoSuchKey:
        print(f"Error: The specified key '{model_path}' does not exist in bucket '{bucket_name}'.")
        return None

    # Extract the tar.gz file
    with tarfile.open(f'{extract_to}/model.tar.gz', 'r:gz') as tar:
        tar.extractall(path=extract_to)

    # Load the ARIMA model from the extracted .pkl file
    model_file = None
    for root, dirs, files in os.walk(extract_to):
        for file in files:
            if file.endswith('.pkl'):
                model_file = os.path.join(root, file)
                break
    if model_file is None:
        raise FileNotFoundError("Model file (.pkl) not found in the extracted tar.gz")

    # Load the ARIMA model
    model = sm.load(model_file)
    
    return model



def upload_model_to_s3(model, bucket_name, key):
    s3_client = boto3.client('s3')
    # Save the model to a temporary file
    model_path = '/tmp/trained_arima_model.pkl'
    joblib.dump(model, model_path)
    # Upload the model to S3
    s3_client.upload_file(model_path, bucket_name, key)
    print(f"Model successfully uploaded to s3://{bucket_name}/{key}")

if __name__ == '__main__':
    # Replace with your actual bucket names and paths
    model_bucket = 'mlflow-sagemaker-eu-north-1-339712788522'
    model_path = 'arima-model-btc-model-alxsclsbrn6ez2alhog1/model.tar.gz'
    data_bucket = 'sagemakerbtcdata'
    data_filename = 'preprocessed_bitcoin_data.csv'

    # Step 1: Download new data
    new_data_df = download_data_from_s3(data_bucket, data_filename)
    if new_data_df is None:
        print("Data download failed. Exiting script.")
        exit(1)

    # Step 2: Download and extract the trained model
    model = download_and_extract_model(model_bucket, model_path)
    if model is None:
        print("Model download failed. Exiting script.")
        exit(1)

    # Step 3: Predict using the ARIMA model
    start_index = new_data_df.index[0]
    end_index = new_data_df.index[-1]
    model_fit = model.fit()
    predictions = model_fit.predict(start=start_index, end=end_index, typ='levels')

# Step 4: Evaluate predictions
    y_true = new_data_df['close']  
    r2 = r2_score(y_true, predictions)

    # Print or use the R2 score as needed
    print(f"R^2 Score: {r2}")


    if r2 < 0.80:
        # Define the split ratio
        train_size = int(len(new_data_df) * 0.8)
        train, test = new_data_df[:train_size], new_data_df[train_size:]
        result = adfuller(new_data_df['close'])
        if result[1] > 0.05:
            new_data_df['close_diff'] = new_data_df['close'].diff().dropna()
            result_diff = adfuller(new_data_df['close_diff'].dropna())
            if result_diff[1] < 0.05:
                d = 1
            else:
                d = 2  # Adjust as needed based on further differencing checks
        else:
            d = 0
    series_to_use = new_data_df['close_diff'].dropna() if d > 0 else new_data_df['close']

# Set ARIMA order parameters
    p = 1
    q = 1

    # Fit the ARIMA model
    model = ARIMA(new_data_df['close'], order=(p, d, q))
    model_fit = model.fit()
 

    # Predict the test set
    start_index = test.index[0]
    end_index = test.index[-1]
    predictions = model_fit.predict(start=start_index, end=end_index, typ='levels')


    # Calculate metrics

    R2 = r2_score(test['close'], predictions)

    print(f" R2: {R2}")


    # Save the new trained model with versioning in the filename
    new_model_key = 'arima-model-btc-model-alxsclsbrn6ez2alhog1/version2_trained_arima_model.pkl'
    upload_model_to_s3(model_fit, model_bucket, new_model_key)
    
