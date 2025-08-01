from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json

###################Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
model_path = os.path.join(config['output_model_path']) 


#################Function for training the model
def train_model():
    # Check if model directory exists, if not create it
    if not os.path.exists(model_path):
        os.makedirs(model_path)

    # Read data directly from the output folder
    data_file = os.path.join(dataset_csv_path, 'finaldata.csv')

    # Check if the file exists
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file not found: {data_file}")

    # Read data
    data = pd.read_csv(data_file)

    # Split features and target
    X = data.drop(['corporation', 'exited'], axis=1)
    y = data['exited']

    # Create and train model
    model = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                    intercept_scaling=1, l1_ratio=None, max_iter=100,
                    multi_class='auto', n_jobs=None, penalty='l2',
                    random_state=0, solver='liblinear', tol=0.0001, verbose=0,
                    warm_start=False)

    # Fit the logistic regression to your data
    model.fit(X, y)

    # Write the trained model to your workspace in a file called trainedmodel.pkl
    model_file = os.path.join(model_path, 'trainedmodel.pkl')
    with open(model_file, 'wb') as f:
        pickle.dump(model, f)

    return model

if __name__ == '__main__':
    train_model()
