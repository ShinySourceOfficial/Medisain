import flet as ft
from db_connection import get_user_role

def view(page):
    page.title = "Medisain - Menú de Opciones"
    user_rut = page.session.get("user_rut")
    user_role = get_user_role(user_rut)


    def go_create(e):
        page.go("/create_user")

    def go_gestion(e):
        page.go("/gestion_productos")
    
    def go_search(e):
        page.go("/search")

    def logout(e):
        page.session.clear()  # Limpiar la sesión
        page.go("/login")  # Redirigir a la pantalla de login

    controls = [
        ft.Text("Bienvenido, ¿Qué desea hacer?", style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight="bold"),
        ft.Divider(height=20),
    ]

    if user_role == "admin":
        controls.append(
            ft.ElevatedButton("Crear Usuario", on_click=go_create, width=250, height=50)
        )
        controls.append(
            ft.ElevatedButton("Gestionar Productos", on_click=go_gestion, width=250, height=50),
        )
    
    controls.append(
        ft.ElevatedButton("Buscar Producto", on_click=go_search, width=250, height=50)
    )

    controls.append(
        ft.ElevatedButton("Cerrar Sesión", on_click=logout, width=250, height=50, color="red")
    )

    return ft.View(
        "/menu",
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=controls,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        ],
    )