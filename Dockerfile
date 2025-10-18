# Dockerfile pour construire l'image de l'application healthcare_dataset
# Installe Python et les dépendances nécessaires à l'exécution du script

# Utilise une image Python officielle
FROM python:3.13.5

# Définir le répertoire de travail dans le conteneur
WORKDIR /appOCR

# Copier le fichier des dépendances et installer
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout ton code dans le conteneur
COPY . .

# Commande par défaut pour lancer ton script
ENTRYPOINT ["python", "-m"]

# Commande par défaut si aucun argument n'est fourni
CMD ["scripts.main"]