FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir PyMySQL

# Copy application
COPY . .

# Create uploads directory
RUN mkdir -p app/static/uploads

# Expose port
EXPOSE 5000

# Run application
CMD ["python3", "run.py"]
