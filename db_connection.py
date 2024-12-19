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
            "nombres": nombres.lower(),
            "apellidos": apellidos.lower(),
            "mail": email.lower(),
            "rol": rol,
            "password": password_hash,
        }

        db.collection("usuarios").add(user_data)
        print(f"Usuario {rut} agregado correctamente.")

    except Exception as e:
        print(f"Error al agregar usuario: {e}")
    

def add_product(nombre, categoria, laboratorio, precio, descuento, sucursal, ubicacion):
    try:
        db = firestore.client()
        product_data = {
            "nombre_producto": nombre.lower(),
            "categoria": categoria,
            "laboratorio": laboratorio.lower(),
            "precio": precio,
            "descuento": descuento,
            "sucursal": sucursal.lower(),
            "ubicacion": ubicacion.lower(),
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
        #print(f"Producto {product_id} eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar producto: {e}")

def delete_lote(lote_id):
    try:
        db = firestore.client()
        db.collection("lotes").document(lote_id).delete()
    except Exception as e:
        print(f"Error al eliminar producto: {e}")

def search_products_for_prodManage(query):
    db = firestore.client()
    productos_ref = db.collection('productos')

    results = []

    if not query:
        # Recuperar todos los productos
        all_products_query = productos_ref.stream()
        # Usamos el ID del documento como identificador único
        results = [{"id": product.id, **product.to_dict()} for product in all_products_query]
    else:
        query = query.lower()

        # Búsqueda por nombre
        name_query = productos_ref.where("nombre_producto", ">=", query).where("nombre_producto", "<=", query + "\uf8ff").stream()
        name_results = [{"id": product.id, **product.to_dict()} for product in name_query]

        # Búsqueda por categoría
        category_query = productos_ref.where("categoria", ">=", query).where("categoria", "<=", query + "\uf8ff").stream()
        category_results = [{"id": product.id, **product.to_dict()} for product in category_query]

        results.extend(name_results)
        results.extend(category_results)

    # Eliminar duplicados basados en el ID
    unique_results = []
    seen_products = set()
    for product in results:
        product_id = product.get("id")  # Usamos el ID de Firestore como identificador único
        if product_id not in seen_products:
            seen_products.add(product_id)
            unique_results.append(product)

    return unique_results


def get_all_products():
    db = firestore.client()
    """Obtiene todos los productos desde Firebase."""
    products_ref = db.collection("productos").stream()
    products = []
    for product in products_ref:
        products.append({"id": product.id, **product.to_dict()})
    return products

def add_lot(lot_data):
    db = firestore.client()
    """Agrega un lote a la colección de 'lotes' en Firebase."""
    db.collection("lotes").add(lot_data)


def search_products_for_inventory(query):
    db = firestore.client()
    productos_ref = db.collection('productos')
    lotes_ref = db.collection('lotes')

    results = []

    if not query:
        # Recuperar todos los productos y sus lotes
        all_products_query = productos_ref.stream()
        for product in all_products_query:
            # Obtenemos los lotes asociados a cada producto
            product_lotes_query = lotes_ref.where("producto_id", "==", product.id).stream()
            lotes = [{"id": lote.id, **lote.to_dict()} for lote in product_lotes_query]
            # Combine la información de producto con los lotes
            for lote in lotes:
                combined_product = {"producto": product.to_dict(), "lote": lote}
                results.append(combined_product)
    else:
        query = query.lower()

        # Búsqueda por nombre de producto
        name_query = productos_ref.where("nombre_producto", ">=", query).where("nombre_producto", "<=", query + "\uf8ff").stream()
        name_results = [{"id": product.id, **product.to_dict()} for product in name_query]

        # Búsqueda por categoría
        category_query = productos_ref.where("categoria", ">=", query).where("categoria", "<=", query + "\uf8ff").stream()
        category_results = [{"id": product.id, **product.to_dict()} for product in category_query]

        # Unimos los resultados
        results.extend(name_results)
        results.extend(category_results)

        # Obtener los lotes asociados a los productos encontrados
        combined_results = []
        for product in results:
            product_lotes_query = lotes_ref.where("producto_id", "==", product["id"]).stream()
            lotes = [{"id": lote.id, **lote.to_dict()} for lote in product_lotes_query]
            for lote in lotes:
                combined_product = {"producto": product, "lote": lote}
                combined_results.append(combined_product)

        results = combined_results

    return results