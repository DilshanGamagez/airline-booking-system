# Start from a lightweight Python environment
FROM python:3.12-slim

# Set the working folder inside the container
WORKDIR /app

# Copy just the requirements file first (for efficient caching)
COPY requirements.txt .

# Install the Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app's code into the container
COPY . .

# Tell Docker this app listens on port 5000
EXPOSE 5000

# The command to run when the container starts
CMD ["python3", "app.py"]