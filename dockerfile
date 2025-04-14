FROM python:3.11-slim

WORKDIR /app
COPY . /app

# Installiere Git
RUN apt-get update && apt-get install -y git

# Installiere die benötigten Python-Pakete
RUN pip install --no-cache-dir -r requirements.txt

# Installiere flask-migrate (neu hinzugefügt)
RUN pip install flask-migrate

EXPOSE 5000

CMD ["python", "app.py"]
