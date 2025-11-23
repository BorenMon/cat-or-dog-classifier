ARG ENVIRONMENT=development # default environment

FROM python:3.13.5

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

CMD mlflow ui --port 5000 --host 0.0.0.0 --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --allowed-hosts "*" --cors-allowed-origins "*" & \
    if [ "$ENVIRONMENT" = "production" ]; then \
        fastapi run main.py --host 0.0.0.0 --port 8000 --workers 4; \
    else \
        fastapi dev main.py --host 0.0.0.0 --port 8000 --reload; \
    fi

