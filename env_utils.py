# For using variables as ENV variables
from dotenv import load_dotenv
# OS and system libraries
import os
import sys
# For Encryption and Decryption
# https://emilylahren.com/2024/07/using-an-encrypted-env-file-with-your-python-script-to-secure-data/
from cryptography.fernet import Fernet, InvalidToken



def encrypt(filename, key):
    try:
        f = Fernet(key)
        with open(filename, "rb") as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open(filename, "wb") as file:
            file.write(encrypted_data)
    except InvalidToken:
        errorMessage = "Token error has occurred while trying to encrypt the file \"" + filename + "'"
        errorLine = sys.exc_info()[2].tb_lineno
        print("Exception: " + InvalidToken) # was errorType but changed to avoid undefined variable
        print("Error Message: " + errorMessage)
        print("Error line: " + str(errorLine))
    
def decrypt(filename, key):
    try:
        f = Fernet(key)
        with open(filename, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open(filename, "wb") as file:
            file.write(decrypted_data)
    except InvalidToken:
        print("Error: File not encrypted or already decrypted, cannot decrypt now")
        exit(1)


# print("File not encrypted or already decrypted, cannot decrypt now")

# Search if '.key' file exist, if not create it and generate a new key
def find_key():
    if os.path.isfile(f"{env_utils_path}.key") == False:
        print("key File not found")
        key = Fernet.generate_key()
        f = open(f"{env_utils_path}.key", "wb")
        f.write(key)
        print("key File created successfuly")
        f.close()
        return key
    else:
        f = open(f"{env_utils_path}.key", "rb")
        key = f.read()
        return key

# Search if an environment variable exist, and raise error associated
def search_env(var, error_level=0):
    if os.getenv(var, "") == "":
        print("Error : " + var + " not found")
    else:
        print(var + " ", os.getenv(var, ""))
    return error_level

from dotenv import load_dotenv
from os import path

env_utils_path = path.dirname(sys.argv[0])
if env_utils_path != "":
	env_utils_path += "/"
else:
	env_utils_path="./"
env_utils=env_utils_path + "env_utils.py"

if os.path.isfile(f"{env_utils_path}.env") == False:
    print(".env File not found")
    sys.exit(1)

key = find_key()
# print("key here is ", key)

if len(sys.argv) == 2:
    try:
        choice = int(sys.argv[1])  # Convertir en entier
    except ValueError:
        sys.exit(1)
    if choice == 0:
        decrypt(f"{env_utils_path}.env", key)
    elif choice == 1:
        encrypt(f"{env_utils_path}.env", key)
    if choice == 2:
        decrypt(f"{env_utils_path}.env", key)
        load_dotenv()
        search_env("CLIENT_ID", 1)
        search_env("CLIENT_SECRET", 1)
        search_env("auth_token", 1)
        encrypt(f"{env_utils_path}.env", key)
    sys.exit(0)

# Searching to load all variables in .env
try:
    if search_env("CLIENT_ID", 1) != 0:
        raise 1
    if search_env("CLIENT_SECRET", 1) != 0:
        raise 1
    if search_env("auth_token", 1) != 0:
        os.system(f"python3 {env_utils_path}retrieve_token.py")
except:
    print("One or more errors blocked execution here")
    sys.exit(1)

load_dotenv()
