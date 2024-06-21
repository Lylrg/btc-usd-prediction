import requests
import pandas as pd
import boto3
from io import StringIO

def fetch_historical_data(api_key, limit=2000):
    url = "https://min-api.cryptocompare.com/data/v2/histohour"
    params = {
        'fsym': 'BTC',
        'tsym': 'USD',
        'limit': limit,
        'api_key': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()['Data']['Data']
        df = pd.DataFrame(data)
        return df
    else:
        print(f"Error fetching data: {response.status_code}")
        return pd.DataFrame()

def save_data_to_s3(df, bucket_name, filename):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket_name, filename).put(Body=csv_buffer.getvalue())
    print(f"Data saved to {bucket_name}/{filename}")

def preprocess_data(df):
    df = df.drop(columns=['conversionType', 'conversionSymbol'])
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    # Additional preprocessing steps if necessary
    return df

if __name__ == '__main__':
    api_key = '17011d57142c4a08089d7a61548de4f7cd9bb98bb186872eea1889a03c47ca73'
    bucket_name = 'sagemakerbtcdata'
    
    # Step 1: Fetch data
    raw_df = fetch_historical_data(api_key)
    if not raw_df.empty:
        save_data_to_s3(raw_df, bucket_name, 'bitcoin_data.csv')
        
        # Step 2: Preprocess data
        preprocessed_df = preprocess_data(raw_df)
        save_data_to_s3(preprocessed_df, bucket_name, 'preprocessed_bitcoin_data.csv')
