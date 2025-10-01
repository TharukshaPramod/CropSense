# Dockerfile
# predictor/Dockerfile
FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir fastapi uvicorn scikit-learn joblib pandas python-dotenv
COPY . /app
EXPOSE 8002
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8002"]
