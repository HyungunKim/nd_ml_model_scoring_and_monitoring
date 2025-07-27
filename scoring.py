from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json



#################Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path']) 
model_path = os.path.join(config['output_model_path'])


#################Function for model scoring
def score_model(model_path=model_path):
    # Check if model directory exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model directory not found: {model_path}")

    # Load the trained model
    model_file = os.path.join(model_path, 'trainedmodel.pkl')
    with open(model_file, 'rb') as f:
        model = pickle.load(f)

    # Load test data
    test_data_file = os.path.join(test_data_path, 'testdata.csv')
    test_data = pd.read_csv(test_data_file)

    # Split features and target
    X_test = test_data.drop(['corporation', 'exited'], axis=1)
    y_test = test_data['exited']

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate F1 score
    f1 = metrics.f1_score(y_test, y_pred)

    # Write the result to latestscore.txt
    score_file = os.path.join(model_path, 'latestscore.txt')
    with open(score_file, 'w') as f:
        f.write(str(f1))

    return f1

if __name__ == '__main__':
    score_model()
