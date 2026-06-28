# Nutzen der schlanken Python-Standard-Runtime
FROM python:3.11-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere das Skript in den Container
COPY http_downloader_old.py .

# Definiere den Einstiegspunkt, damit Argumente direkt durchgereicht werden
ENTRYPOINT ["python", "http_downloader.py"]
