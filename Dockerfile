# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install git & docker
RUN apt-get update && apt-get install -y git
RUN apt-get update && apt-get install -y docker.io

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install docker package to interact with Docker from Python
RUN pip install docker

# Run app.py when the container launches
CMD ["python", "main.py"]