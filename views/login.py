import flet as ft
import time
from db_connection import validate_credentials


def login_view(page: ft.Page):
    page.title = "Medisain - Inicio de Sesión"

    icon_path = "../assets/img/icon.png"


    rut_field = ft.TextField(label="Ingrese su RUT", hint_text="12345678-9", autofocus=False)
    password_field = ft.TextField(label="Ingrese su Contraseña", password=True, hint_text="******")
    error_message = ft.Text("", color="red")

    def validar_usuario(e):
        rut = rut_field.value.strip()
        password = password_field.value.strip()

        if "-" not in rut:
            rut = rut[:-1] + "-" + rut[-1]

        if not rut or not password:
            error_message.value = "Por favor, ingrese su RUT y contraseña."
            page.update()
            return
        
        if validate_credentials(rut, password):
            page.snack_bar = ft.SnackBar(ft.Text("Inicio de Sesión Exitoso."))
            page.snack_bar.open = True
            page.update()
            time.sleep(1)
            page.session.set("user_rut", rut)
            page.go("/menu")
        else:
            error_message.value = "Datos incorrectos. Inténtelo nuevamente."
            print(rut)
            page.update()
    

    icon_logo = ft.Image(
        src=icon_path,  # Reemplaza con la ruta correcta de tu logo
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN,
    )
    

    main_container = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Iniciar Sesión", size=30, weight="bold"),
                            ft.Divider(height=20),
                            ft.Text("Ingrese su RUT"),
                            rut_field,
                            ft.Text("Ingrese su Contraseña"),
                            password_field,
                            ft.Container(height=20),
                            ft.ElevatedButton("Iniciar Sesión", on_click=validar_usuario, width=250, height=50),
                            error_message,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=1,
                    width=450,  # Ancho reducido para el lado izquierdo
                    height=350,  # Alto reducido
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=icon_logo,
                    width=250,  # Ancho reducido para el lado derecho
                    height=350,  # Alto reducido
                    alignment=ft.alignment.center,
                    padding=20,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width= 800,
        height=470,
        border_radius=20,
        bgcolor= ft.colors.WHITE10 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLACK12,
    )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    main_container
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            expand=True,
        ),
    )
