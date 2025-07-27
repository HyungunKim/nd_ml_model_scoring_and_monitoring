FROM python:3.8-slim

WORKDIR /app

# Install cron
RUN apt-get update && apt-get -y install cron

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p ingesteddata models production_deployment

# Set up cron job
COPY cronjob.txt /etc/cron.d/app-cron
RUN chmod 0644 /etc/cron.d/app-cron
RUN crontab /etc/cron.d/app-cron

# Expose port for API
EXPOSE 8000

# Start command
CMD ["bash", "-c", "service cron start && python app.py"]