from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
import shutil
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json



##################Load config.json and correct path variable
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
model_path = os.path.join(config['output_model_path'])
prod_deployment_path = os.path.join(config['prod_deployment_path']) 


####################function for deployment
def store_model_into_pickle():
    # Create deployment directory if it doesn't exist
    if not os.path.exists(prod_deployment_path):
        os.makedirs(prod_deployment_path)

    # Copy the trained model
    model_file = os.path.join(model_path, 'trainedmodel.pkl')
    if os.path.exists(model_file):
        shutil.copy2(model_file, os.path.join(prod_deployment_path, 'trainedmodel.pkl'))
    else:
        raise FileNotFoundError(f"Model file not found: {model_file}")

    # Copy the latest score
    score_file = os.path.join(model_path, 'latestscore.txt')
    if os.path.exists(score_file):
        shutil.copy2(score_file, os.path.join(prod_deployment_path, 'latestscore.txt'))
    else:
        raise FileNotFoundError(f"Score file not found: {score_file}")

    # Copy the ingested files record directly from the output folder
    ingested_files_path = os.path.join(dataset_csv_path, 'ingestedfiles.txt')
    if os.path.exists(ingested_files_path):
        shutil.copy2(ingested_files_path, os.path.join(prod_deployment_path, 'ingestedfiles.txt'))
    else:
        raise FileNotFoundError(f"Ingested files record not found: {ingested_files_path}")

    print(f"Model deployed to: {prod_deployment_path}")

if __name__ == '__main__':
    store_model_into_pickle()
