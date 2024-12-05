import flet as ft
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
        bgcolor= ft.colors.WHITE70 if page.theme_mode == ft.ThemeMode.LIGHT else "black",
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












"""import flet as ft
from db_connection import validate_credentials

def view(page: ft.Page):
    bg_path = "../assets/img/bglog.png"
    logo_path = "../assets/img/icon.png"

    page.title = "Medisain - Inicio de Sesión"
    page.window.width = 1000
    page.window.height = 700
    page.window.maximizable = False
    page.window.resizable = False
    

    rut_field = ft.TextField(label="Ingrese su RUT", hint_text="12345678-9", autofocus=False)
    password_field = ft.TextField(label="Ingrese su Contraseña", password=True, hint_text="******")
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


    app_logo = ft.Image(
        src=logo_path,  # Reemplaza con la ruta correcta de tu logo
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN,
    )

    # Contenedor principal
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
                            ft.ElevatedButton("Iniciar Sesión", on_click=validar_usuario, width=250, height=50),
                            error_message,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=20,
                    width=450,  # Ancho reducido para el lado izquierdo
                    height=350,  # Alto reducido
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=app_logo,
                    width=250,  # Ancho reducido para el lado derecho
                    height=350,  # Alto reducido
                    alignment=ft.alignment.center,
                    padding=20,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=800,
        height=470,
        border_radius=20,
        bgcolor="white" if page.theme_mode == ft.ThemeMode.LIGHT else "black",
    )

    

    controls = [
        ft.Text("Bienvenido, ¿Qué desea hacer?", style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight="bold"),
        ft.Divider(height=20),
    ]

    text = ft.Container(
        content=rut_field,
        width=300,  # Fija un ancho
        height=60,  # Fija una altura
        bgcolor="transparent",  # Fondo transparente para mantener el diseño
    )
    

    return ft.View(
    "/login",
    controls=[
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.TextField()
                ]
            ),
            alignment=ft.alignment.center,
            expand=True,
        ),
    ],
    bgcolor=ft.colors.TRANSPARENT,
    decoration=ft.BoxDecoration(
        image=ft.DecorationImage(
            src=bg_path,  
            fit=ft.ImageFit.COVER,  
            repeat=ft.ImageRepeat.NO_REPEAT,
        )
    ),
)"""

