
import boto3
from botocore.exceptions import ClientError

def create_dynamodb_tables(region_name="us-east-1"):
    dynamodb = boto3.resource('dynamodb', region_name=region_name)

    # Tabla para registros de incendios (FireDamageRecords)
    try:
        table_fire = dynamodb.create_table(
            TableName='FireDamageRecords',
            KeySchema=[
                {
                    'AttributeName': 'OBJECTID',
                    'KeyType': 'HASH'  # Clave principal
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'OBJECTID',
                    'AttributeType': 'N'  # Número
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table_fire.wait_until_exists()
        print("Tabla FireDamageRecords creada correctamente.")
    except ClientError as e:
        print("Error al crear FireDamageRecords:", e.response['Error']['Message'])

    # Tabla para resultados de predicciones (PredictionResults)
    try:
        table_pred = dynamodb.create_table(
            TableName='PredictionResults',
            KeySchema=[
                {
                    'AttributeName': 'PredictionID',
                    'KeyType': 'HASH'  # Clave principal
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'PredictionID',
                    'AttributeType': 'S'  # String
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table_pred.wait_until_exists()
        print("Tabla PredictionResults creada correctamente.")
    except ClientError as e:
        print("Error al crear PredictionResults:", e.response['Error']['Message'])

if __name__ == "__main__":
    create_dynamodb_tables()
