FROM python:latest

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV PAYMENT_API_KEY=zz-not-a-real-key-7c2e91b0a4d3f5e6

CMD ["python", "app.py"]
