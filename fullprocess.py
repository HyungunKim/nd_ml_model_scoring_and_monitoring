
import os
import json
import subprocess
import training
import scoring
import deployment
import diagnostics
import reporting
import ingestion
import pandas as pd

# Load config.json
with open('config.json', 'r') as f:
    config = json.load(f)

input_folder_path = os.path.join(config['input_folder_path'])
output_folder_path = os.path.join(config['output_folder_path'])
prod_deployment_path = os.path.join(config['prod_deployment_path'])
model_path = os.path.join(config['output_model_path'])

##################Check and read new data
def check_for_new_data():
    """Check if there are new data files that need to be ingested"""
    # First, read ingestedfiles.txt from the deployment directory
    ingested_files_path = os.path.join(prod_deployment_path, 'ingestedfiles.txt')

    # If the deployment directory or ingestedfiles.txt doesn't exist, assume all data is new
    if not os.path.exists(ingested_files_path):
        print("No record of ingested files found. All data will be treated as new.")
        return True

    # Read the list of previously ingested files
    with open(ingested_files_path, 'r') as f:
        ingested_files_content = f.read()

    # Extract the file names from the content
    ingested_files = []
    for line in ingested_files_content.split('\n'):
        if line.startswith('- '):
            ingested_files.append(line[2:])  # Remove the '- ' prefix

    # Get the list of files in the input folder
    current_files = [f for f in os.listdir(input_folder_path) if f.endswith('.csv')]

    # Check if there are any new files
    new_files = [f for f in current_files if f not in ingested_files]

    if new_files:
        print(f"Found {len(new_files)} new files: {new_files}")
        return True
    else:
        print("No new data files found.")
        return False

##################Deciding whether to proceed, part 1
# If new data is found, ingest it
new_data_found = check_for_new_data()

if new_data_found:
    print("Ingesting new data...")
    ingestion.merge_multiple_dataframe()
else:
    print("No new data to ingest. Exiting process.")
    exit()

##################Checking for model drift
def check_for_model_drift():
    """Check if there is model drift by comparing scores"""
    # Read the score from the latest model in production
    latest_score_path = os.path.join(prod_deployment_path, 'latestscore.txt')

    # If there's no deployed model yet, assume we need to train a new one
    if not os.path.exists(latest_score_path):
        print("No previous model score found. Will train a new model.")
        return True

    # Read the latest score
    with open(latest_score_path, 'r') as f:
        latest_score = float(f.read().strip())

    # Train and score a model on the new data
    print("Training model on new data...")
    training.train_model()

    print("Scoring model on test data...")
    new_score = scoring.score_model()

    print(f"Previous model score: {latest_score}")
    print(f"New model score: {new_score}")

    # Check for model drift (if new score is lower, drift has occurred)
    if new_score < latest_score:
        print("Model drift detected. New model performs worse than the deployed model.")
        return True
    else:
        print("No model drift detected. New model performs as well or better than the deployed model.")
        return False

##################Deciding whether to proceed, part 2
# If model drift is found, retrain and redeploy
model_drift_found = check_for_model_drift()

if not model_drift_found:
    print("No model drift detected. Exiting process.")
    exit()

##################Re-deployment
# Deploy the new model
print("Deploying new model...")
deployment.store_model_into_pickle()

##################Diagnostics and reporting
# Run diagnostics and reporting on the new model
print("Running diagnostics and reporting...")

# # Start the Flask app in the background
# flask_process = subprocess.Popen(['python', 'app.py'], stdout=subprocess.PIPE)
#
# # Wait a moment for the app to start
# import time
# time.sleep(5)

# Run API calls
print("Running API calls...")
subprocess.run(['python', 'apicalls.py'])

# Generate confusion matrix
print("Generating confusion matrix...")
reporting.score_model()

# # Terminate the Flask app
# flask_process.terminate()

print("Process completed successfully!")
