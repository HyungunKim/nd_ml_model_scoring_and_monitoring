import requests
import json
import os

# Load config.json
with open('config.json', 'r') as f:
    config = json.load(f)

model_path = os.path.join(config['output_model_path'])
test_data_path = os.path.join(config['test_data_path'])

# Specify a URL that resolves to your workspace
URL = "http://127.0.0.1:8000"

# Call each API endpoint and store the responses
# Prediction endpoint
test_data_file = os.path.join(test_data_path, 'testdata.csv')
prediction_payload = {'file_path': test_data_file}
response1 = requests.post(f"{URL}/prediction", json=prediction_payload).json()

# Scoring endpoint
response2 = requests.get(f"{URL}/scoring").json()

# Summary statistics endpoint
response3 = requests.get(f"{URL}/summarystats").json()

# Diagnostics endpoint
response4 = requests.get(f"{URL}/diagnostics").json()

# Combine all API responses
responses = {
    'prediction': response1,
    'scoring': response2,
    'summary_stats': response3,
    'diagnostics': response4
}

# Create model directory if it doesn't exist
if not os.path.exists(model_path):
    os.makedirs(model_path)

# Write the responses to your workspace
with open(os.path.join(model_path, 'apireturns.txt'), 'w') as f:
    f.write(json.dumps(responses, indent=4))

print(f"API responses saved to {os.path.join(model_path, 'apireturns.txt')}")

if __name__ == '__main__':
    pass