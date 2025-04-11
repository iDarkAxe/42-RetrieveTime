import requests

CLIENT_ID = "s"
CLIENT_SECRET = "e"
REDIRECT_URI = "http://localhost:8000/callback"  # Doit être identique à celui utilisé pour obtenir le code
# AUTH_CODE = "q"  # Vérifie qu'il est récent et non utilisé

# ACCEDER ICI POUR LE TOKEN AUTH_CODE

auth_code_url = f"https://api.intra.42.fr/oauth/authorize?client_id={CLIENT_ID}&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fcallback&response_type=code"
response = requests.get(auth_code_url)

if response.status_code == 200:
    print("json la : ", response.content)
    # print("Auth code token:", response.json()["code"])
else:
    print("Erreur:", response.json())

# AUTH_CODE = response.json()["code"]

# token_url = "https://api.intra.42.fr/oauth/token"
# data = {
#     "grant_type": "authorization_code",
#     "client_id": CLIENT_ID,
#     "client_secret": CLIENT_SECRET,
#     "code": AUTH_CODE,
#     "redirect_uri": REDIRECT_URI
# }

# response = requests.post(token_url, data=data)

# if response.status_code == 200:
#     print("Access Token:", response.json()["access_token"])
# else:
#     print("Erreur:", response.json())
