FROM python:3.10.4-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "asgi:api", "--host", "0.0.0.0", "--port", "8080"]
