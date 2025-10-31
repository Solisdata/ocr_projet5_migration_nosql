set -e

git clone https://github.com/Solisdata/ocr_projet5_migration_nosql.git
cd ocr_projet5_migration_nosql

# Vérifier que le fichier .env existe
if [ ! -f ".env" ]; then
  echo "⚠️  Fichier .env manquant ! Créez-le avant de continuer."
  exit 1
fi

# Activer environnement Python
python -m venv .venv
source .venv\Scripts\Activate.ps1

# Installer dépendances
pip install -r requirements.txt

# Lancer Docker
docker-compose up -d

echo "=== Installation terminée ==="
echo "Pour insérer les données : docker compose run --rm app python main.py"
echo "Pour lancer les tests : docker-compose run app pytest test/main_test.py"