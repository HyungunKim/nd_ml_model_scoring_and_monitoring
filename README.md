# ML Model Scoring and Monitoring

This project implements a system for ML model scoring, monitoring, and automated redeployment.

## Project Structure

- `ingestion.py`: Reads data files, combines them, and saves the merged dataset.
- `training.py`: Trains a logistic regression model on the ingested data.
- `scoring.py`: Calculates F1 score for the model on test data.
- `deployment.py`: Deploys the model by copying files to the production directory.
- `diagnostics.py`: Performs model and data diagnostics.
- `reporting.py`: Generates a confusion matrix plot.
- `app.py`: Sets up API endpoints for predictions, scoring, and diagnostics.
- `apicalls.py`: Calls the API endpoints and saves the responses.
- `fullprocess.py`: Automates the entire ML pipeline.
- `cronjob.txt`: Contains a cron job to run the pipeline every 10 minutes.

## Steps

1. **Data Ingestion**: Read data files, combine them, remove duplicates, and save the merged dataset.
2. **Model Training**: Train a logistic regression model on the ingested data.
3. **Model Scoring**: Calculate F1 score for the model on test data.
4. **Model Deployment**: Copy model files to the production directory.
5. **Diagnostics**: Perform model predictions, calculate statistics, check for missing data, measure execution time, and check for outdated packages.
6. **Reporting**: Generate a confusion matrix plot.
7. **API Setup**: Create endpoints for predictions, scoring, statistics, and diagnostics.
8. **Process Automation**: Check for new data, detect model drift, retrain and redeploy if needed.

## How to Run

### Local Setup
1. Update `config.json` to set the correct paths and API port (default is 8123).
2. Run `python fullprocess.py` to execute the entire pipeline.
3. Set up a cron job using the command in `cronjob.txt` to automate the process.

### Docker Setup
1. Build the Docker image:
   ```
   docker build -t ml-monitoring .
   ```

2. Run the Docker container (replace PORT with the port configured in config.json, default is 8000):
   ```
   docker run -d -p PORT:PORT --name ml-monitoring-container ml-monitoring
   ```

3. Access the API at http://localhost:PORT (where PORT is the configured port)

4. To check if the cronjob is working:
   ```
   # Connect to the container
   docker exec -it ml-monitoring-container bash

   # View the cron log
   cat /app/cron.log

   # Check if cron is running
   ps aux | grep cron

   # View the crontab
   crontab -l
   ```

## Automation

The system automatically:
- Checks for new data
- Ingests new data if found
- Checks for model drift
- Retrains and redeploys the model if drift is detected
- Runs diagnostics and reporting on the new model

## Recent Changes

- **Data Storage**: Data is now saved directly to the output folder instead of using SHA subdirectories, making it easier to find the latest data.
- **Docker Support**: Added Docker containerization for easier deployment and consistent environment.
- **Improved Cronjob**: Updated cronjob to work in both local and Docker environments with logging for better monitoring.
- **Configurable Port**: API port is now configurable through config.json instead of being hardcoded, allowing for more flexibility in deployment.
