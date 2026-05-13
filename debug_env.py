import os
from dotenv import load_dotenv, find_dotenv

print(f"Current working directory: {os.getcwd()}")
env_path = find_dotenv()
print(f"Found .env at: {env_path}")

load_dotenv()
api_key = os.getenv("FIREBASE_API_KEY")
print(f"FIREBASE_API_KEY: {api_key}")

if api_key is None:
    print("FAILED to load FIREBASE_API_KEY")
else:
    print("SUCCESSFULLY loaded FIREBASE_API_KEY")
