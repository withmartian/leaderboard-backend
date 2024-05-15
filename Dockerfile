# Using debian trixie
FROM debian:trixie-slim


# Install only necessary packages
RUN apt-get update && \
    apt-get install -y python3.11 python3.11-venv python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /opt

# Set up virtual environment
RUN python3.11 -m venv venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip

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
