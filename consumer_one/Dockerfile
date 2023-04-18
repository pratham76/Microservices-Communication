# Base image
FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install flask
RUN pip install flask

# Copy the healthcheck.py file
COPY healthcheck.py .

ENV FLASK_APP=healthcheck.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production
# Set the environment variable
ENV HEALTH_CHECK_URL=http://producer:5000/health_check

# Run the healthcheck script
CMD ["python", "healthcheck.py"]


