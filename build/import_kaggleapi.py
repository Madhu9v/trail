import os
from kaggle.api.kaggle_api_extended import KaggleApi

# Set Kaggle config directory to where kaggle.json is located
os.environ['KAGGLE_CONFIG_DIR'] = r'C:\Users\CHARAN\Downloads'

# Authenticate and initialize the API
api = KaggleApi()
api.authenticate()

# Download the dataset and unzip
api.dataset_download_files('tonygordonjr/spotify-dataset-2023', path='.', unzip=True)

print("Download complete.")



