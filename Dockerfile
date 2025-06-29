
# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*
# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Copy application files
COPY static ./static
COPY templates ./templates
COPY app.py dbcontext.py person.py ./

# Expose the port
EXPOSE 5000

# Set the entry point
ENTRYPOINT ["python3", "app.py"]
