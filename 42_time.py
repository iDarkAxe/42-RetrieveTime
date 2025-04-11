import sys
from datetime import datetime, timedelta
import requests
from os import getenv, path, system
from sys import argv

env_utils_path = path.dirname(argv[0])
if env_utils_path != "":
	env_utils_path += "/"
else:
	env_utils_path="./"

env_utils=env_utils_path + "env_utils.py"

def encrypt_before_close(error_level):
    system(f"python3 {env_utils} 1")
    sys.exit(error_level)

# Vérifier si le premier argument (USER_NAME) est fourni
if len(sys.argv) < 2:
    print("Erreur: Veuillez entrer un nom d'utilisateur.")
    sys.exit(1)

user_name = sys.argv[1]  # Nom d'utilisateur 42

# Configuration
from dotenv import load_dotenv

system(f"python3 {env_utils} 0")
load_dotenv()
token = getenv("auth_token", "")
if token == "":
    system(f"python3 {env_utils} 1")
    raise SystemExit('Error : Token still not recovered')
system(f"python3 {env_utils} 1")

url = f"https://api.intra.42.fr/v2/users/{user_name}/locations"
headers = {"Authorization": f"Bearer {token}"}

# Déterminer automatiquement le mois et l'année actuels
now = datetime.utcnow()

if len(sys.argv) == 3:
    try:
        length = int(sys.argv[2])  # Convertir en entier
        if (length != 0) & (length != 1):
            raise ValueError  # Lever une erreur si le mois est invalide
    except ValueError:
        print("Erreur: La longueur ne peut être que 0 ou 1")
        sys.exit(1)
else:
    length = 0  # Utiliser short par defaut

if len(sys.argv) == 4:
    try:
        target_month = int(sys.argv[3])  # Convertir en entier
        if target_month < 1 or target_month > 12:
            raise ValueError  # Lever une erreur si le mois est invalide
    except ValueError:
        print(f"Erreur: Le mois {target_month:02d} doit être un nombre entre 1 et 12.")
        sys.exit(1)
    try:
        length = int(sys.argv[2])  # Convertir en entier
        if (length != 0) & (length != 1):
            raise ValueError  # Lever une erreur si le mois est invalide
    except ValueError:
        print("Erreur: La longueur ne peut être que 0 ou 1")
        sys.exit(1)
else:
    target_month = now.month  # Utiliser le mois actuel par défaut

target_year = now.year
# print(f"\ntarget_month {target_month:02d}, : length {length}")

# Récupération des données

page_number = 1
locations = []

range_val = f"2025-{target_month}-01,2025-{target_month+1}-01"

# Fonction pour récupérer toutes les localisations
while True:
    # Effectuer la requête avec la pagination
    response = requests.get(url, headers=headers, params={
        "page[number]": page_number,
        "page[size]": 100,
        "range[begin_at]": range_val  # Exemple de plage de dates
    })
    
    if response.status_code == 200:
        data = response.json()
        locations.extend(data)
        
        # Si moins de 100 éléments sont renvoyés, nous avons atteint la dernière page
        if len(data) < 100:
            break
        
        # Sinon, passez à la page suivante
        page_number += 1
    else:
        print("Erreur:", response.json())
        break

if response.status_code != 200:
    print("Erreur requete")
    print("Erreur:", response.json())
    raise SystemExit("Erreur:", response.json())
    # sys.exit(1)

total_time = timedelta()  # Stocke le temps total passé
now = datetime.utcnow()

for loc in locations:
    start_time = datetime.fromisoformat(loc['begin_at'][:-1])  # Convertir ISO 8601 en datetime
    end_time = loc['end_at']
    if end_time:
        end_time = datetime.fromisoformat(end_time[:-1])  # Convertir si présent
    else:
        end_time = now  # Si toujours connecté, prendre l'instant présent

    # Filtrer par mois et année actuels
    if start_time.month == target_month and start_time.year == target_year:
        session_duration = end_time - start_time
        total_time += session_duration
        if length == 1:
            print(f"Début: {start_time}, Fin: {end_time}, Durée: {session_duration}")

# Affichage du temps total
hours, remainder = divmod(total_time.total_seconds(), 3600)
minutes, _ = divmod(remainder, 60)
if length == 1:
    print("")
print(f"Temps total passé en {target_month:02d}/12 : {int(hours)}h {int(minutes)}min")
