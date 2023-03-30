# Base image
FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ .

# Set the environment variables
ENV FLASK_APP=producer.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Expose the port
EXPOSE 5000

# Start the server
CMD [ "flask", "run" ]
