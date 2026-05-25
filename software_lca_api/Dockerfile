# Use an official, lightweight Python base image
FROM python:3.10-slim

# Set environment variables to optimize Python inside Docker
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Ensures Python output is sent straight to terminal (useful for logs)
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first
# Doing this before copying the rest of the code leverages Docker layer caching.
# (If requirements haven't changed, Docker won't re-download them every time you change your code).
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port that Uvicorn will listen on
EXPOSE 8000

# The command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]