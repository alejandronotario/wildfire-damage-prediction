# tests/test_data_contract.py
import pandas as pd
import json
import pytest

# Definición del esquema esperado
EXPECTED_COLUMNS = [
    "OBJECTID", "DAMAGE", "STREETNUMBER", "STREETNAME", "STREETTYPE", "STREETSUFFIX",
    "CITY", "STATE", "ZIPCODE", "CALFIREUNIT", "COUNTY", "COMMUNITY", "INCIDENTNAME",
    "APN", "ASSESSEDIMPROVEDVALUE", "YEARBUILT", "SITEADDRESS", "GLOBALID",
    "Latitude", "Longitude", "UTILITYMISCSTRUCTUREDISTANCE", "FIRENAME", "geometry"
]

def load_geojson(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    # Asumimos que cada registro se encuentra en data["features"] y las propiedades contienen los datos
    records = [feature["properties"] for feature in data.get("features", [])]
    return pd.DataFrame(records)

def test_columns_exist(tmp_path):
    # Para pruebas, usamos un archivo geojson de ejemplo ubicado en tests/data/
    test_file = tmp_path / "sample.geojson"
    # Aquí se crearía un archivo de ejemplo; para el ejemplo, simulamos el contenido
    sample_data = {
        "features": [
            {
                "properties": {col: None for col in EXPECTED_COLUMNS}
            }
        ]
    }
    test_file.write_text(json.dumps(sample_data))
    
    df = load_geojson(str(test_file))
    missing = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    assert not missing, f"Faltan las siguientes columnas: {missing}"

def test_no_null_in_key_columns(tmp_path):
    # Simula un geojson con datos, asegurando que 'OBJECTID' y 'GLOBALID' no sean nulos
    sample_data = {
        "features": [
            {
                "properties": {
                    **{col: "dummy" for col in EXPECTED_COLUMNS},
                    "OBJECTID": 1,
                    "GLOBALID": "GUID-12345"
                }
            }
        ]
    }
    test_file = tmp_path / "sample.geojson"
    test_file.write_text(json.dumps(sample_data))
    
    df = load_geojson(str(test_file))
    assert df["OBJECTID"].notnull().all(), "Existen valores nulos en OBJECTID"
    assert df["GLOBALID"].notnull().all(), "Existen valores nulos en GLOBALID"
