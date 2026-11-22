
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY receptor_mqtt.py .

CMD ["python", "receptor_mqtt.py"]
