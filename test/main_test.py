

import pytest
import pandas as pd
from pymongo import MongoClient
from pymongo.collection import Collection
from dotenv import load_dotenv
import os
from script.main import clean_dataframe
from script.main import connect_mongo

# # reprends mon environnement
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

def connect_mongo() -> Collection:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]

def test_clean_dataframe():
    # Création d'un dataframe fictif pour tester le df
    df = pd.DataFrame({"Name": ["aLice"], "Age": ["30"], "Room Number": ["101"], 
                       "Billing Amount": [-50], "Date of Admission": ["2025-01-01"],
                       "Discharge Date": ["2025-01-05"],
                       "Gender":["F"], "Blood Type":["A"], "Medical Condition":["Cold"],
                       "Doctor":["Dr X"], "Hospital":["Hosp"], "Insurance Provider":["Ins"],
                       "Admission Type":["Emergency"], "Medication":["Med"], "Test Results":["OK"]})
    
    df_clean = clean_dataframe(df)
    
    assert df_clean['Name'].iloc[0] == "Alice", "Le nom n'a pas été correctement capitalisé"        # le nom a été transformé en capital
    assert pd.isna(df_clean['Billing Amount'].iloc[0]) # le montant négatif devenu NaN
    assert df_clean.duplicated().sum() == 0  # pas de doublon

def test_connect_mongo():
    """
    Teste la connexion à MongoDB et vérifie que la collection est accessible.
    """
    try:
        collection = connect_mongo()
        assert isinstance(collection, Collection)
        result = collection.find_one()
        print("Connexion MongoDB OK — Collection accessible.")
    except Exception as e:
        pytest.fail(f"Échec de la connexion MongoDB : {e}")

    except Exception as e:
        pytest.fail(f"Échec de la connexion MongoDB : {e}")


def test_integrity():
    df = clean_dataframe(pd.read_csv("data/healthcare_dataset.csv"))
    collection = connect_mongo()
    
    
    # Comparer nombre de lignes
    assert len(df) == collection.count_documents({})

    # Vérifier colonnes
    mongo_cols = collection.find_one().keys()
    for col in df.columns :
        assert col in mongo_cols,  f"Colonne manquante : {col}"



#pour lancer le test : python -m pytest test/main_test.py