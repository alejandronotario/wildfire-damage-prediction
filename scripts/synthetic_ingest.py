# scripts/synthetic_ingest.py
import time
import boto3
import json
import random

def simulate_realtime_ingestion(region_name="us-east-1", interval=10):
    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    table = dynamodb.Table('FireDamageRecords')

    # Simulación: genera un registro sintético basado en un modelo simple.
    sample_record = {
        "OBJECTID": random.randint(100000, 999999),
        "DAMAGE": random.choice(["No Damage", "Affected (1-9%)", "Affected (10-50%)", "Destroyed"]),
        "STREETNUMBER": str(random.randint(1, 9999)),
        "STREETNAME": "Sample Street",
        "STREETTYPE": "Road",
        "STREETSUFFIX": "",
        "CITY": "Sample City",
        "STATE": "CA",
        "ZIPCODE": str(random.randint(90000, 99999)),
        "CALFIREUNIT": "Unit X",
        "COUNTY": "Sample County",
        "COMMUNITY": "Sample Community",
        "INCIDENTNAME": "Sample Fire",
        "APN": "APN" + str(random.randint(10000, 99999)),
        "ASSESSEDIMPROVEDVALUE": random.uniform(100000, 500000),
        "YEARBUILT": random.randint(1900, 2020),
        "SITEADDRESS": "123 Sample St, Sample City, CA",
        "GLOBALID": "GUID-" + str(random.randint(100000, 999999)),
        "Latitude": random.uniform(32.0, 42.0),
        "Longitude": random.uniform(-124.0, -114.0),
        "UTILITYMISCSTRUCTUREDISTANCE": random.uniform(0, 100),
        "FIRENAME": "Alt Sample Fire",
        "geometry": "POINT(-120.0 35.0)"
    }

    while True:
        try:
            table.put_item(Item=sample_record)
            print("Registro sintético insertado:", sample_record["OBJECTID"])
        except Exception as e:
            print("Error en inserción sintética:", str(e))
        time.sleep(interval)  # Espera 'interval' segundos antes del siguiente registro

if __name__ == "__main__":
    simulate_realtime_ingestion()
