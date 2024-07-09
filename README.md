# Predicting BTC/USD Prices with ARIMA Model using MLOps

![Screenshot](https://github.com/Lylrg/btc-usd-prediction/blob/main/images/Captura%20de%20pantalla%202024-07-08%20a%20las%2018.45.07.png)

Welcome to our project on predicting BTC/USD prices using ARIMA (AutoRegressive Integrated Moving Average) model!📈 This project demonstrates how we leverage machine learning for time series forecasting and deploy models using MLflow and Amazon SageMaker.🚀


![Static Badge](https://img.shields.io/badge/MLflow-555555?logo=MLflow&logoColor=blue)
![Static Badge](https://img.shields.io/badge/Bitcoin-555555?logo=Bitcoin&logoColor=green)
![Static Badge](https://img.shields.io/badge/ARIMA-555555)
![Static Badge](https://img.shields.io/badge/AWS-555555?logo=Amazon%20Web%20Services&logoColor=yellow)
![Static Badge](https://img.shields.io/badge/S3-555555?logo=Amazon%20S3&logoColor=yellow)


## Project Overview

In this project, we aimed to predict the future price of Bitcoin (BTC/USD) using historical data and real-time updates from the CryptoCompare API. The ARIMA model was selected for its performance in training and testing phases.


## Setup AWS CLI configuration

We followed the setup instructions detailed in [this repository](https://github.com/vb100/deploy-ml-mlflow-aws/blob/main/README.md), which provided comprehensive guidance on configuring AWS CLI for seamless integration with MLflow and Amazon SageMaker.

### Step-by-Step Process

1. **Training the Model with MLflow**

   Run `train.py` to initiate training and track experiments with MLflow. This generates the `MLflow` folder containing experiment logs and artifacts, including the trained model.

2. **Building and Pushing Docker Image**

   Using the artifacts from MLflow, build a Docker image containing the trained model(go to the artifact directory):
   
   ```bash
   mlflow sagemaker build-and-push-container 

  After, check AWS ECR repos list to get the image URI.

3. **Deploy image to Sagemaker**
 Run `arimadeploy.py` to ddeploy image to Sagemaker

4. **Store fetched btc data to a s3 bucket**
 Run `fetch_bucket.py` store a csv file from btc fetched data into a s3 bucket

5. **Retrain the model if it's necesary**
 Run `test_model.py` to predict in base of the data stored in the s3 bucket. If the R2 score is less than 0.80 the model it's retrained and saved as a new version into s3.


## Team
This project was developed by:

[![LinkedIn](https://img.shields.io/badge/Alexandre-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/alex-conte/)
[![LinkedIn](https://img.shields.io/badge/Rodrigo-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rodrigo-pierini/)
[![LinkedIn](https://img.shields.io/badge/Lydia-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/lylrg/)

