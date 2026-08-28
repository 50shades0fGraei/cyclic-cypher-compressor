# LUJAN TESSERACT: MARKETPLACE DEPLOYMENT IMAGE
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up the Randall environment
WORKDIR /app
COPY . /app

# Install Python requirements
# (Assuming a requirements.txt exists or just core libraries)
RUN pip install flask sqlite3

# Expose the Randall API port
EXPOSE 8080

# Launch the Lujan Tesseract SaaS API
CMD ["python", "Lujan_SaaS_API.py"]
