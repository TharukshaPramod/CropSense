# preprocessor/Dockerfile
FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir fastapi uvicorn pandas scikit-learn pyarrow joblib python-dotenv
COPY . /app
EXPOSE 8001
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
