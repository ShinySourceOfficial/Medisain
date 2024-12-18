import flet as ft
from db_connection import get_user_role


def menu_view(page: ft.Page):
    #page.window.maximized = True
    page.title = "Medisain - Menú de Opciones"
    user_rut = page.session.get("user_rut")
    user_role = get_user_role(user_rut)


    def go_prodManage(e):
        page.go("/prodManage")

    def go_createUser(e):
        page.go("/createUser")

    def logout(e):
        page.session.clear()
        page.go("/login")
        page.snack_bar = ft.SnackBar(ft.Text("Sesión Cerrada Exitosamente."))
        page.snack_bar.open = True
        #page.window.maximized = False

    controls = [
        ft.Text("Bienvenido, ¿Qué desea hacer?", style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight="bold"),
        ft.Divider(height=20),
    ]

    if user_role == "admin":
        controls.append(
            ft.ElevatedButton("Crear Usuario", on_click=go_createUser, width=250, height=50)
        )
        controls.append(
            ft.ElevatedButton("Gestionar Productos", on_click=go_prodManage, width=250, height=50),
        )

    controls.append(
        ft.ElevatedButton("Cerrar Sesión", on_click=logout, width=250, height=50, color="red")
    )

    page.add(
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
    )