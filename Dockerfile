# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set up work directory
WORKDIR /app

# Copy all files to the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
