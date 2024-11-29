import flet as ft
from db_connection import validate_credentials

def view(page):
    page.title = "Medisain - Inicio de Sesión"
    rut_field = ft.TextField(label="RUT", autofocus=True)
    password_field = ft.TextField(label="Contraseña", password=True)
    error_message = ft.Text("", color="red")

    def validar_usuario(e):
        rut = rut_field.value.strip()
        password = password_field.value.strip()

        if not rut or not password:
            error_message.value = "Por favor, ingrese su RUT y contraseña."
            page.update()
            return
        
        if validate_credentials(rut, password):
            page.session.set("user_rut", rut)
            page.go("/menu")
        else:
            error_message.value = "Datos incorrectos. Inténtelo nuevamente."
            page.update()

    def cerrar_aplicacion(e):
        """Cierra la aplicación."""
        page.window_close()

    return ft.View(
            "/login",
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Iniciar Sesión", size=30),
                            ft.Divider(height=20),
                            rut_field,
                            password_field,
                            ft.ElevatedButton("Iniciar Sesión", on_click=validar_usuario, width=250, height=50),
                            error_message,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=30,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                ft.ElevatedButton("Cerrar Aplicación", on_click=cerrar_aplicacion, width=170, height=50, color="red"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.END,
        )
