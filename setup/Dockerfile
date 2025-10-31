# Dockerfile pour construire l'image de l'application healthcare_dataset
# Installe Python et les dépendances nécessaires à l'exécution du script

FROM python:3.13.5

WORKDIR /appOCR

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exécuter le script directement
CMD ["python", "script/main.py"]