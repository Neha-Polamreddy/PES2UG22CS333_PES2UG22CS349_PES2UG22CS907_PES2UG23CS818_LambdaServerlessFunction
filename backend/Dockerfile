# Dockerfile
FROM python:3.10-slim

RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Add the wait-for-postgres script
COPY wait_for_postgres.sh /wait_for_postgres.sh
RUN chmod +x /wait_for_postgres.sh

# Final command that waits for Postgres before starting the app
CMD ["/wait_for_postgres.sh", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

