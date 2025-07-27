from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import json
import os
from diagnostics import model_predictions, dataframe_summary, missing_data, execution_time, outdated_packages_list
from scoring import score_model



######################Set up variables for use in our script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'

with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path'])


#######################Prediction Endpoint
@app.route("/prediction", methods=['POST','OPTIONS'])
def predict():        
    # Get file path from the request
    file_path = request.json.get('file_path', None)

    # If no file path is provided, use the test data
    if file_path is None:
        file_path = os.path.join(test_data_path, 'testdata.csv')

    # Load the data
    data = pd.read_csv(file_path)

    # Get predictions
    predictions = model_predictions(data)

    return jsonify(predictions)

#######################Scoring Endpoint
@app.route("/scoring", methods=['GET','OPTIONS'])
def scoring():        
    # Get the F1 score
    f1_score = score_model()

    return jsonify({'f1_score': f1_score})

#######################Summary Statistics Endpoint
@app.route("/summarystats", methods=['GET','OPTIONS'])
def stats():        
    # Get summary statistics
    summary_stats = dataframe_summary()

    return jsonify(summary_stats)

#######################Diagnostics Endpoint
@app.route("/diagnostics", methods=['GET','OPTIONS'])
def diagnostics():        
    # Get timing information
    timing = execution_time()

    # Get missing data information
    missing = missing_data()

    # Get outdated packages
    outdated = outdated_packages_list()

    return jsonify({
        'execution_time': timing,
        'missing_data': missing,
        'outdated_packages': outdated
    })

if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=config['api_port'], debug=True, threaded=True)
