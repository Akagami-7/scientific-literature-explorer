import pyrebase
import os
from dotenv import load_dotenv

load_dotenv()

class AuthManager:
    def __init__(self):
        config = {
            "apiKey": os.getenv("FIREBASE_API_KEY"),
            "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
            "projectId": os.getenv("FIREBASE_PROJECT_ID"),
            "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
            "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
            "appId": os.getenv("FIREBASE_APP_ID"),
            "databaseURL": "" # Not used but pyrebase might expect it
        }
        self.firebase = pyrebase.initialize_app(config)
        self.auth = self.firebase.auth()

    def signup(self, email, password):
        try:
            user = self.auth.create_user_with_email_and_password(email, password)
            return {"success": True, "user": user}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def login(self, email, password):
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            return {"success": True, "user": user}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def reset_password(self, email):
        try:
            self.auth.send_password_reset_email(email)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def login_with_google(self, id_token):
        try:
            # Using the ID token to sign in via Firebase Auth REST API
            # Pyrebase supports this through sign_in_with_custom_token if we get one,
            # or we can use the credential directly if we have the right payload.
            # However, pyrebase's sign_in_with_google is the direct way.
            user = self.auth.sign_in_with_google(id_token)
            return {"success": True, "user": user}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_user_info(self, id_token):
        try:
            return self.auth.get_account_info(id_token)
        except Exception as e:
            return None
