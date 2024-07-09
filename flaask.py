import pandas as pd
import json
import boto3
from flask import Flask, request, jsonify

app = Flask(__name__)

global app_name
global region
app_name = 'arima-model-btc'
region = 'eu-north-1'

def check_status(app_name):
    sage_client = boto3.client('sagemaker', region_name=region)
    endpoint_description = sage_client.describe_endpoint(EndpointName=app_name)
    endpoint_status = endpoint_description["EndpointStatus"]
    return endpoint_status

def query_endpoint(app_name, input_json):
    client = boto3.session.Session().client("sagemaker-runtime", region)

    response = client.invoke_endpoint(
        EndpointName=app_name,
        Body=input_json,
        ContentType='application/json',
    )
    preds = response['Body'].read().decode('utf-8')
    predictions = json.loads(preds)
    print("Received response: {}".format(predictions))
    return preds

@app.route('/')
def home():
    return "Welcome to the ARIMA Model Prediction API!"

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            input_data = request.json
            input_json = json.dumps(input_data)
            predictions2 = query_endpoint(app_name=app_name, input_json=input_json)
            return jsonify(predictions2)
        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        return jsonify({'error': 'Invalid HTTP method, only POST is allowed'})

if __name__ == '__main__':
    print("Application status is: {}".format(check_status(app_name)))
    app.run(host='0.0.0.0', port=8000)
