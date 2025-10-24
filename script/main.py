import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os



# Fonctions utilitaires

def load_csv(file_path):
    "Charge le dataset CSV et renvoie un DataFrame"
    df = pd.read_csv(file_path)
    return df

def clean_dataframe(df):
    "Nettoie et typage du DataFrame"
    # Typage
    df['Age'] = df['Age'].astype(int)
    df['Room Number'] = df['Room Number'].astype(int)
    df['Billing Amount'] = df['Billing Amount'].astype(float)
    df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
    df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])
    
    for col in ['Name','Gender','Blood Type','Medical Condition','Doctor',
                'Hospital','Insurance Provider','Admission Type','Medication','Test Results']:
        df[col] = df[col].astype(str)
    
    # Capitalisation des noms
    df['Name'] = df['Name'].str.title()
    
    # Suppression doublons 
    df = df.drop_duplicates()
    
    # S'assurer que Billing Amount soit positif
    df.loc[:, 'Billing Amount'] = df['Billing Amount'].apply(lambda x: x if x >= 0 else None).astype(float)
    
    return df


# connexion mongo
# # reprends mon environnement
load_dotenv()

# Récupérer les variables
MONGO_ROOT_USER = os.getenv("MONGO_ROOT_USER")
MONGO_ROOT_PASS = os.getenv("MONGO_ROOT_PASS")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")


def connect_mongo(user=MONGO_ROOT_USER, password=MONGO_ROOT_PASS, db_name=DB_NAME, collection_name=COLLECTION_NAME):
    """Connexion à MongoDB avec authentification"""
    uri = f"mongodb://{user}:{password}@mongo:27017/{db_name}?authSource=admin"
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    except Exception as e:
        print("Erreur de connexion MongoDB :", e)
        raise e
    db = client[db_name]
    return db[collection_name]



#insertion data

def insert_data(collection, df):
    "Insère un DataFrame dans la collection"
    #collection.drop()
    data_dict = df.to_dict("records")
    collection.insert_many(data_dict)
    print(f"{len(data_dict)} documents insérés.")

def read_patient(collection, filter_query):
    """Récupère un document correspondant au filtre"""
    return collection.find_one(filter_query)

def read_many(collection, filter_query=None):
    """Récupère plusieurs documents correspondant au filtre"""
    if filter_query is None:
        filter_query = {}
    return list(collection.find(filter_query))

def update_patient(collection, filter_query, update_values):
    """Met à jour un document correspondant au filtre"""
    return collection.update_one(filter_query, {"$set": update_values}).modified_count

def delete_patient(collection, filter_query):
    """Supprime un document correspondant au filtre"""
    return collection.delete_one(filter_query).deleted_count




# Fonction principale

def main():
    print("Chargement du CSV...")
    df = load_csv("data/healthcare_dataset.csv")
    print("Nettoyage des données...")
    df = clean_dataframe(df)
    print("Connexion à MongoDB...")
    collection = connect_mongo()
    print("Insertion des données...")
    insert_data(collection, df)
    print("Script terminé !")

# Lancer le script
if __name__ == "__main__":
    main()