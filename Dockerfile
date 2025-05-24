# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for mysqlclient and netcat
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev build-essential netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code into the container at /app
COPY ./src /app/src

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables (can be overridden by docker-compose)
ENV FLASK_APP=src.main:app
ENV FLASK_RUN_HOST=0.0.0.0
ENV DB_HOST=db
ENV DB_PORT=3306
ENV DB_NAME=mydb
ENV DB_USERNAME=root
ENV DB_PASSWORD=password
ENV SECRET_KEY=default_secret_key_change_me

# Run the application using the entrypoint script
CMD ["/app/entrypoint.sh"]