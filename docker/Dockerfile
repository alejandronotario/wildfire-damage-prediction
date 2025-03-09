# docker/Dockerfile
FROM python:3.11-slim

# Instalar dependencias
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar los scripts
COPY scripts/ /app/scripts/

# Definir la entrada: puedes elegir ejecutar el script de ingesta o dejarlo parametrizado
CMD ["python", "scripts/ingest_data.py"]
