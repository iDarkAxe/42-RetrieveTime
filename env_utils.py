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
		print("File not encrypted, cannot decrypt")

if os.path.isfile(".env") == False:
	print(".env File not found")
	sys.exit(1)

# Search if '.key' file exist, if not create it and generate a new key
if os.path.isfile(".key") == False:
	print("key File not found")
	key = Fernet.generate_key()
	f = open(".key", "wb")
	f.write(key)
	print("key File created successfuly")
	f.close()
	sys.exit(1)
else:
	f = open(".key", "rb")
	key = f.read()
	# print("key is ", key)
	decrypt(".env", key)

load_dotenv()

# Searching to load all variables in .env
if os.getenv("CLIENT_ID", "") == "":
	print("CLIENT_ID not found")
	sys.exit(1)
else:
	print("CLIENT_ID ", os.getenv("CLIENT_ID", ""))

if os.getenv("CLIENT_SECRET", "") == "":
	print("CLIENT_SECRET not found")
	sys.exit(1)
else:
	print("CLIENT_SECRET ", os.getenv("CLIENT_SECRET", ""))

if os.getenv("auth_token", "") == "":
	print("auth_token not found")
	# Make a new token HERE
	sys.exit(1)
else:
	print("auth_token ", os.getenv("auth_token", ""))

encrypt(".env", key)
