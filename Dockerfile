# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Prevent Python from buffering stdout/stderr (useful for Docker logs)
ENV PYTHONUNBUFFERED=1

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source code
COPY . .

# Expose Flask port
EXPOSE 5000

# Environment variable for Alpha Vantage API key (can be passed at runtime)
ENV ALPHA_VANTAGE_API_KEY=""

# Run the app
CMD ["python", "app.py"]
