import pandas as pd
import requests

# Function to fetch historical data
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

api_key = '17011d57142c4a08089d7a61548de4f7cd9bb98bb186872eea1889a03c47ca73'
df = fetch_historical_data(api_key)

# Drop unnecessary columns and prepare the data
df = df.drop(columns=['conversionType', 'conversionSymbol'])
df['time'] = pd.to_datetime(df['time'], unit='s')
df.set_index('time', inplace=True)