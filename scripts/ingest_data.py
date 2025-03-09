# Este script descarga un archivo geojson de un bucket de S3 y lo ingesta en una tabla de DynamoDB
import boto3
import json
import os
from botocore.exceptions import ClientError

# Configuración: nombre del bucket y key del archivo
S3_BUCKET = "tu-bucket-datos"
GEOJSON_KEY = "datasets/fire_damage.geojson"

def download_geojson(bucket, key, download_path="data.geojson"):
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket, key, download_path)
        print(f"Archivo descargado: {download_path}")
    except ClientError as e:
        print("Error al descargar archivo:", e.response['Error']['Message'])
        raise

def ingest_to_dynamodb(file_path, region_name="us-east-1"):
    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    table = dynamodb.Table('FireDamageRecords')

    with open(file_path, 'r') as f:
        data = json.load(f)

    # Asumiendo que el geojson tiene una clave "features" con los registros
    records = data.get("features", [])
    for record in records:
        # Cada record es un diccionario; asumimos que las propiedades contienen las columnas
        properties = record.get("properties", {})
        # Se requiere que 'OBJECTID' esté presente y sea numérico
        try:
            object_id = int(properties.get("OBJECTID"))
        except (TypeError, ValueError):
            continue

        # Inserción en DynamoDB
        try:
            table.put_item(Item=properties)
        except ClientError as e:
            print(f"Error al insertar el record {object_id}: {e.response['Error']['Message']}")

    print("Ingesta de datos completada.")

if __name__ == "__main__":
    local_file = "data.geojson"
    download_geojson(S3_BUCKET, GEOJSON_KEY, download_path=local_file)
    ingest_to_dynamodb(local_file)
