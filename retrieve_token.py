import requests
from time import time

REDIRECT_URI = "http://localhost:8000/callback"
TOKEN_FILE = "token.json"  # Fichier pour stocker le token d'accès et le token de rafraîchissement

from dotenv import load_dotenv
from os import getenv, system, path
from sys import exit, argv

env_utils_path = path.dirname(argv[0])
if env_utils_path != "":
	env_utils_path += "/"
else:
	env_utils_path="./"
env_utils=env_utils_path + "env_utils.py"

system(f"python3 {env_utils} 0")

load_dotenv()
CLIENT_ID = getenv("CLIENT_ID", "")
CLIENT_SECRET = getenv("CLIENT_SECRET", "")
if CLIENT_ID == "" or CLIENT_SECRET == "":
    print("Error : Tokens not recovered")
    system(f"python3 {env_utils} 1")
    exit(1)
system(f"python3 {env_utils} 1")

def get_auth_code():
    # URL d'autorisation
    auth_code_url = f"https://api.intra.42.fr/oauth/authorize?client_id={CLIENT_ID}&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fcallback&response_type=code"
    print(f"Allez à cette URL pour obtenir le code d'autorisation : {auth_code_url}")
    auth_code = input("Entrez le code d'autorisation obtenu depuis l'URL : ")
    return auth_code

def get_tokens(auth_code):
    # Échanger le code d'autorisation contre un token d'accès et un token de rafraîchissement
    token_url = "https://api.intra.42.fr/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        tokens = response.json()
        print("Token d'accès et token de rafraîchissement obtenus.")
        # Sauvegarder les tokens dans un fichier
        with open(TOKEN_FILE, "w") as f:
            f.write(str(tokens))
        return tokens
    else:
        print("Erreur lors de l'obtention des tokens:", response.json())
        return None

def refresh_access_token(refresh_token):
    # Utiliser le refresh_token pour obtenir un nouveau token d'accès
    token_url = "https://api.intra.42.fr/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        tokens = response.json()
        print("Token d'accès renouvelé.")
        # Sauvegarder les nouveaux tokens
        with open(TOKEN_FILE, "w") as f:
            f.write(str(tokens))
        return tokens
    else:
        print("Erreur lors du renouvellement du token:", response.json())
        return None

def load_tokens():
    # Charger les tokens à partir du fichier
    try:
        with open(TOKEN_FILE, "r") as f:
            tokens = eval(f.read())  # Utilisez eval pour obtenir le dictionnaire
        return tokens
    except FileNotFoundError:
        return None

def get_access_token():
    # Charger les tokens enregistrés
    tokens = load_tokens()

    if tokens:
        # Vérifier si le token d'accès est expiré (c'est-à-dire si le token a expiré depuis plus de 60 secondes)
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")
        expires_at = tokens.get("expires_at")

        # Si le token d'accès est expiré, utiliser le refresh_token
        if expires_at and time() > expires_at:
            print("Token d'accès expiré, renouvellement...")
            tokens = refresh_access_token(refresh_token)
            if tokens:
                return tokens["access_token"]
        else:
            return access_token
    else:
        # Si aucun token n'est trouvé, obtenir un nouveau code d'autorisation
        auth_code = get_auth_code()
        tokens = get_tokens(auth_code)
        return tokens["access_token"]

# Utilisation du token d'accès
access_token = get_access_token()
# print(f"Access Token: {access_token}")

system(f"python3 {env_utils} 0")
system(f"dotenv -f {env_utils_path}.env set auth_token {access_token}")
system(f"python3 {env_utils} 1")
