# Use official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /bot

# Copy requirements if present
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .


# Command to run your app (update as needed)
CMD ["python", "main.py"]