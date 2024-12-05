import os
import hashlib
import firebase_admin
from firebase_admin import credentials, firestore


def initialize_firebase():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cred_path = os.path.join(current_dir, "assets", "db", "AccountKey.json")

        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        print("Conexión a Firebase exitosa.")
    except Exception as e:
        print(f"Error al conectar con Firebase: {e}")



def validate_credentials(rut, password):
    try:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        db = firestore.client() 
        user_ref = db.collection("usuarios").where("rut", "==", rut) 
        docs = user_ref.get()
        if docs:
            for doc in docs:
                user_data = doc.to_dict()
                if user_data.get("password") == password_hash:
                    return True

        return False  

    except Exception as e:
        print(f"Error al validar credenciales: {e}")
        return False
    

def get_user_role(rut):
    try:
        db = firestore.client()
        user_ref = db.collection("usuarios").where("rut", "==", rut)
        docs = user_ref.get()

        if docs:
            for doc in docs:
                user_data = doc.to_dict()
                return user_data.get("rol") 
        return None 

    except Exception as e:
        print(f"Error al obtener el rol del usuario: {e}")
        return None