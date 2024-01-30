# Use a specific Python version
FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Install system-level dependencies
RUN apt-get update && \
    apt-get install -y build-essential default-libmysqlclient-dev pkg-config

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install pkg-config
RUN apt-get install -y pkg-config

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup
CMD python3 main.py

