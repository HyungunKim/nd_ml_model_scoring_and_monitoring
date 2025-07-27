
import pandas as pd
import numpy as np
import timeit
import os
import json
import pickle
import subprocess

##################Load config.json and get environment variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path']) 
prod_deployment_path = os.path.join(config['prod_deployment_path'])

##################Function to get model predictions
def model_predictions(data=None):
    # If no data is provided, use the test data
    if data is None:
        test_data_file = os.path.join(test_data_path, 'testdata.csv')
        data = pd.read_csv(test_data_file)

    # Load the deployed model
    model_path = os.path.join(prod_deployment_path, 'trainedmodel.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    # Prepare features (drop non-feature columns)
    X = data.drop(['corporation', 'exited'], axis=1) if 'corporation' in data.columns and 'exited' in data.columns else data

    # Make predictions
    predictions = model.predict(X)

    return predictions.tolist()  # Convert numpy array to list

##################Function to get summary statistics
def dataframe_summary():
    # Read data directly from the output folder
    data_file = os.path.join(dataset_csv_path, 'finaldata.csv')

    # Check if the file exists
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file not found: {data_file}")

    # Read data
    data = pd.read_csv(data_file)

    # Get numeric columns
    numeric_columns = data.select_dtypes(include=['number']).columns.tolist()

    # Calculate statistics for each numeric column
    summary_stats = []
    for col in numeric_columns:
        col_data = data[col]
        mean = col_data.mean()
        median = col_data.median()
        std = col_data.std()
        summary_stats.append({'column': col, 'mean': mean, 'median': median, 'std': std})

    return summary_stats

##################Function to check missing data
def missing_data():
    # Read data directly from the output folder
    data_file = os.path.join(dataset_csv_path, 'finaldata.csv')

    # Check if the file exists
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file not found: {data_file}")

    # Read data
    data = pd.read_csv(data_file)

    # Calculate percentage of NA values for each column
    na_percentages = []
    for col in data.columns:
        na_count = data[col].isna().sum()
        na_percentage = na_count / len(data) * 100
        na_percentages.append({'column': col, 'na_percentage': na_percentage})

    return na_percentages

##################Function to get timings
def execution_time():
    # Time the ingestion.py script
    start_time = timeit.default_timer()
    os.system('python ingestion.py')
    ingestion_time = timeit.default_timer() - start_time

    # Time the training.py script
    start_time = timeit.default_timer()
    os.system('python training.py')
    training_time = timeit.default_timer() - start_time

    return [ingestion_time, training_time]

##################Function to check dependencies
def outdated_packages_list():
    # Get list of installed packages and their versions
    installed_cmd = subprocess.check_output(['pip', 'freeze'])
    installed = installed_cmd.decode('utf-8').strip().split('\n')

    # Get list of outdated packages
    outdated_cmd = subprocess.check_output(['pip', 'list', '--outdated'])
    outdated_lines = outdated_cmd.decode('utf-8').strip().split('\n')[2:]  # Skip header lines

    # Parse outdated packages info
    outdated_packages = []
    for line in outdated_lines:
        if line:
            parts = line.split()
            if len(parts) >= 3:
                package_name = parts[0]
                current_version = parts[1]
                latest_version = parts[2]
                outdated_packages.append({
                    'package': package_name,
                    'current_version': current_version,
                    'latest_version': latest_version
                })

    return outdated_packages


if __name__ == '__main__':
    print("Model Predictions:")
    print(model_predictions())

    print("\nDataframe Summary:")
    print(dataframe_summary())

    print("\nMissing Data:")
    print(missing_data())

    print("\nExecution Time:")
    print(execution_time())

    print("\nOutdated Packages:")
    print(outdated_packages_list())
