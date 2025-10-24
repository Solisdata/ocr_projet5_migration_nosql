# OCR - Projet 5 
## Projet de Migration de données en NoSQL

Projet réalisé dans le cadre de la formation **Data Engineer** d’OpenClassRoom.  
Octobre 2025 

## Contexte 
Situation fictive : Un client a transmis un dataset de données médicales de patients. Il rencontre un soucis de scalabilité avec leurs tâches quotidienne. 
Le système ne suit plus la charge (performance qui chutent, perte de données, augmentation des coûts, risque opérationnel…)
Le problème vient de l’incapacité de leur système actuel à gérer: 
 - le volume (quantités de données),
 - la variété (diversité des formats : dossier médicaux, IRM…)
 -  la vélocité des données médicales (vitesse à laquelle les données sont produites)
Le projet consiste à déployer les données médicales sur **MongoDB** pour stocker et gérer des informations variées tout en maintenant de bonnes performances même lorsque le volume de données augmente.
Les applications sont contenues dans **des conteneurs Docker** pour faciliter le déploiement, l’exécution et la reproductibilité de l’environnement. L’**infrastructure AWS** est utilisée pour stocker, traiter et distribuer les données à grande échelle, garantissant scalabilité, sécurité et accessibilité.


## Technologies utilisées
Python
MongoDB
Docker
Pymongo

## Contenu du projet

- `main.py` : script principal pour charger, nettoyer et insérer les données dans MongoDB.
- `test_main.py` : tests du script
- `data/healthcare_dataset.csv` : dataset source.  
- `docker-compose.yml` : configuration des conteneurs Docker (MongoDB + application + test).  
- `docker-entrypoint-initdb.d/init-mongo.js` : script d’initialisation de MongoDB, création des utilisateurs et rôles. 
- `.env` : variables d’environnement (non suivi par Git).
- `requirements.txt` : liste des dépendances Python nécessaires à l’exécution des scripts.

---

## Structure des données

Chaque document patient contient :

{  
  "Name": "string",  
  "Age": "int",  
  "Gender": "string",  
  "Blood Type": "string",  
  "Medical Condition": "string",  
  "Doctor": "string",  
  "Hospital": "string",  
  "Room Number": "int",  
  "Insurance Provider": "string",  
  "Admission Type": "string",  
  "Medication": "string",  
  "Test Results": "string",  
  "Billing Amount": "float/null",  
  "Date of Admission": "datetime",  
  "Discharge Date": "datetime"  
}

-- 
## Architecture

         Déployé sur AWS 
              |
        (Docker container)  
     +---------------------+
     |   Python App        |
     | healthcare_app_new  |
     | (script/main.py)    |
     +----------+----------+
                |
                v
          (Docker container) 
     +---------------------+
     |    MongoDB          |
     |   my_mongo_new      |
     +----------+----------+
                ^
                |
         (Docker container) 
     +---------------------+
     |     Tests           |
     |  healthcare_tests   |
     | (Docker container)  |
     +---------------------+

Docker Network: my_network
Volume partagé: ./data


  
---
## Système d'authentification et rôle
Les utilisateurs MongoDB sont créés dans init-mongo.js :

    admin : rôle dbAdmin - accès total sur la DB

    writer : rôle readWrite - Lecture/écriture (CRUD)

    reader : rôle read - Lecture Seul
    
**Pour se connecter utiliser la commande : docker-compose exec mongo mongosh --host mongo --port 27017 -u <username> -p <password> --authenticationDatabase <db> puis rentrer le mot de passe.**

Ou, cans le code : 
connect_mongo(user, password, host="mongo", port=27017, db_name="ma_bd") 



## Prérequis
- Installer Docker & Docker Compose
- Configuer un fichier d'environnement .env  à la racine a vec les variables suivantes : 
     #informations sur la base de données mongodb  
     DB_NAME=  
     COLLECTION_NAME=  
     #pour les users_roles  
     MONGO_ROOT_USER=admin  
     MONGO_ROOT_PASS=  
     READER_USER=reader  
     READER_PASS=  
     WRITER_USER=writer  
     WRITER_PASS=  

  
## Installation

1. Cloner le projet  
git clone <repo-url>
cd <project-folder>

2.  Activer environnement :
env\Scripts\activate
pip install -r requirements.txt

3. Lancer les conteneurs Docker
docker-compose up -d

## Usages
Charger le CSV et insérer dans MongoDB :   
docker compose run --rm app python main.py

Test : pour exécuter la suite de tests de l'application :   
docker-compose run app pytest test/main_test.py

Notes  
.env n’est pas versionné pour sécuriser les URI et infos sensibles.  
Les mots de passe MongoDB sont définis dans le .env. 






