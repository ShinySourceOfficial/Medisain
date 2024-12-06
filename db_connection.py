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


def add_user(rut, nombres, apellidos, email, rol, password):
    try:
        db = firestore.client()

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        user_data = {
            "rut": rut,
            "nombres": nombres.upper(),
            "apellidos": apellidos.upper(),
            "mail": email,
            "rol": rol,
            "password": password_hash,
        }

        db.collection("usuarios").add(user_data)
        print(f"Usuario {rut} agregado correctamente.")

    except Exception as e:
        print(f"Error al agregar usuario: {e}")
    

def get_all_products():
    try:
        db = firestore.client()
        products = db.collection("productos").get()
        return [product.to_dict() for product in products]
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return []


def add_product(nombre, categoria, laboratorio, precio, stock, fecha_vencimiento, numero_lote, descuento, sucursal, ubicacion):
    try:
        db = firestore.client()
        product_data = {
            "nombre_producto": nombre,
            "categoria": categoria,
            "laboratorio": laboratorio,
            "precio": precio,
            "stock": stock,
            "fecha_vencimiento": fecha_vencimiento,
            "numero_lote": numero_lote,
            "descuento": descuento,
            "sucursal": sucursal,
            "ubicacion": ubicacion,
        }
        db.collection("productos").add(product_data)
        print(f"Producto {nombre} agregado correctamente.")
    except Exception as e:
        print(f"Error al agregar producto: {e}")


def update_product(product_id, updated_data):
    try:
        db = firestore.client()
        db.collection("productos").document(product_id).update(updated_data)
        print(f"Producto {product_id} actualizado correctamente.")
    except Exception as e:
        print(f"Error al actualizar producto: {e}")


def delete_product(product_id):
    try:
        db = firestore.client()
        db.collection("productos").document(product_id).delete()
        print(f"Producto {product_id} eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar producto: {e}")

def search_products(query):
    db = firestore.client()  # Asegúrate de que firestore.client() esté correctamente configurado
    productos_ref = db.collection('productos')  # Cambia esto al nombre de tu colección

    # Inicializar los resultados de búsqueda
    results = []

    # Verificar si la consulta está vacía
    if not query:
        # Si no hay consulta, devolver todos los productos
        all_products_query = productos_ref.stream()
        results = [product.to_dict() for product in all_products_query]
    else:
        query = query.lower()

        # Buscar productos por nombre
        name_query = productos_ref.where("nombre_producto", ">=", query).where("nombre_producto", "<=", query + "\uf8ff").stream()
        name_results = [product.to_dict() for product in name_query]

        # Buscar productos por categoría
        category_query = productos_ref.where("categoria", ">=", query).where("categoria", "<=", query + "\uf8ff").stream()
        category_results = [product.to_dict() for product in category_query]

        # Combinar ambos resultados
        results.extend(name_results)
        results.extend(category_results)

    # Eliminar duplicados, si hay productos con el mismo nombre en ambas búsquedas
    unique_results = []
    seen_products = set()
    for product in results:
        # Usamos un identificador único, por ejemplo, el nombre del producto o el ID
        product_id = product.get("nombre_producto")
        if product_id not in seen_products:
            seen_products.add(product_id)
            unique_results.append(product)

    # Debug: Ver los resultados que estamos obteniendo
    print(f"Productos encontrados: {unique_results}")  # Esto te ayudará a ver si se encuentran productos

    return unique_results
