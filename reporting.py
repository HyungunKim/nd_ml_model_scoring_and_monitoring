import pickle
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from diagnostics import model_predictions



###############Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path'])
model_path = os.path.join(config['output_model_path'])



##############Function for reporting
def score_model():
    # Load test data
    test_data_file = os.path.join(test_data_path, 'testdata.csv')
    test_data = pd.read_csv(test_data_file)

    # Get actual values
    y_true = test_data['exited']

    # Get predictions using the diagnostics module
    y_pred = model_predictions(test_data)

    # Create confusion matrix
    cm = metrics.confusion_matrix(y_true, y_pred)

    # Create a figure
    plt.figure(figsize=(10, 8))

    # Plot confusion matrix using seaborn
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Not Exited', 'Exited'],
                yticklabels=['Not Exited', 'Exited'])

    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')

    # Create model directory if it doesn't exist
    if not os.path.exists(model_path):
        os.makedirs(model_path)

    # Save the confusion matrix plot
    plt.savefig(os.path.join(model_path, 'confusionmatrix.png'))
    plt.close()

    print(f"Confusion matrix saved to {os.path.join(model_path, 'confusionmatrix.png')}")


if __name__ == '__main__':
    score_model()
