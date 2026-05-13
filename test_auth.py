import os
from auth import AuthManager
from dotenv import load_dotenv

load_dotenv()

def test_auth_methods():
    try:
        manager = AuthManager()
        print("Auth object:", manager.auth)
        print("Methods in Auth object:", dir(manager.auth))
        
        if hasattr(manager.auth, 'sign_in_with_google'):
            print("sign_in_with_google exists!")
        else:
            print("sign_in_with_google DOES NOT exist.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_auth_methods()
