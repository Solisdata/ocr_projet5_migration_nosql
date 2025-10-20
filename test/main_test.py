import pytest
import pandas as pd
from pymongo.collection import Collection
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from script.main import clean_dataframe, connect_mongo

# Charger l'environnement
load_dotenv()

# Construire l'URI avec user/pass
MONGO_URI = f"mongodb://{os.getenv('MONGO_ROOT_USER')}:{os.getenv('MONGO_ROOT_PASS')}@mongo:27017/"
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

def connect_mongo_for_test() -> Collection:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]


def test_clean_dataframe():
    df = pd.DataFrame({
        "Name": ["aLice"], "Age": ["30"], "Room Number": ["101"], 
        "Billing Amount": [-50], "Date of Admission": ["2025-01-01"],
        "Discharge Date": ["2025-01-05"],
        "Gender":["F"], "Blood Type":["A"], "Medical Condition":["Cold"],
        "Doctor":["Dr X"], "Hospital":["Hosp"], "Insurance Provider":["Ins"],
        "Admission Type":["Emergency"], "Medication":["Med"], "Test Results":["OK"]
    })
    
    df_clean = clean_dataframe(df)
    
    assert df_clean['Name'].iloc[0] == "Alice"
    assert pd.isna(df_clean['Billing Amount'].iloc[0])
    assert df_clean.duplicated().sum() == 0

def test_connect_mongo():
    try:
        collection = connect_mongo_for_test()
        assert isinstance(collection, Collection)
        print("Connexion MongoDB OK — Collection accessible.")
    except Exception as e:
        pytest.fail(f"Échec de la connexion MongoDB : {e}")

def test_integrity():
    df = clean_dataframe(pd.read_csv("data/healthcare_dataset.csv"))
    collection = connect_mongo_for_test()
    
    assert len(df) == collection.count_documents({}), "Le nombre de documents ne correspond pas"
    
    mongo_cols = collection.find_one().keys()
    for col in df.columns:
        assert col in mongo_cols, f"Colonne manquante dans MongoDB : {col}"


#pour lancer le test : docker-compose run app pytest test/main_test.py