# Use Ubuntu as the base image
FROM ubuntu:22.04

# Set environment variables to avoid interaction prompts
ENV DEBIAN_FRONTEND=noninteractive
# Set the time zone
ENV TZ=Asia/Kolkata

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    ntp \
    curl \
    wget \
    gcc \
    g++ \
    libsqlite3-dev \
    libpq-dev \
    software-properties-common && \
    rm -rf /var/lib/apt/lists/*

# Add deadsnakes PPA to install Python 3.11
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-venv python3.11-dev python3.11-distutils && \
    rm -rf /var/lib/apt/lists/*

# Set python3 to 3.11 and ensure pip is for 3.11 only (avoid system site-packages)
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Copy the requirements.txt first to leverage Docker layer caching
COPY requirements.txt /app/requirements.txt

# Install Python dependencies with 3.11 explicitly so cryptography/cffi go to 3.11 site-packages
RUN python3.11 -m pip install --no-cache-dir --upgrade pip && \
    python3.11 -m pip install --no-cache-dir -r /app/requirements.txt

# Copy the FastAPI application code to the container
COPY . /app

# Set the working directory
WORKDIR /app

# Create a temporary directory for uploads, if needed
RUN mkdir -p /app/temp

# Set permissions for the temp directory
RUN chmod -R 777 /app/temp

# Run with 3.11 so we use only pip-installed packages (avoid system /usr/lib/python3/dist-packages)
CMD ["python3.11", "src/app.py"]