# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11.6-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Inform Docker that the container is listening on the specified port at runtime.
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
