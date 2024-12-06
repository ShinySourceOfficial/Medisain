import flet as ft
from db_connection import add_user

def createUser_view(page: ft.Page):
    page.title = "Medisain - Creación de Usuario"

    def error(mensaje):
        snack_bar = ft.SnackBar(ft.Text(mensaje))
        page.snack_bar = snack_bar
        snack_bar.open = True
        page.update()  

    def validar_creacion(e):
        rut = rut_input.value.strip().replace(".", "")
        nombres = nombres_input.value.strip().upper()
        apellidos = apellidos_input.value.strip().upper()
        email = email_input.value.strip()
        rol = rol_dropdown.value
        password = password_input.value

        if "-" not in rut:
            rut = rut[:-1] + "-" + rut[-1]

        if len(rut) != 10 or rut.count("-") != 1:
            error("El RUT debe tener exactamente 10 caracteres con el guion.")
            return
        
        if not nombres or not apellidos:
            error("Los nombres y apellidos son obligatorios.")
            return

        if "@" not in email:
            error("El correo debe contener '@'.")
            return

        if rol not in ["empleado", "administrador"]:
            error("Debe seleccionar un rol válido.")
            return

        if not password:
            error("La contraseña es obligatoria.")
            return
        
        if rol == "administrador":
            rol = "admin"

        add_user(rut, nombres, apellidos, email, rol, password)

        page.snack_bar = ft.SnackBar(ft.Text("Usuario agregado con éxito."))
        page.snack_bar.open = True
        page.go("/menu")

    def cancelar_creacion(e):
        page.go("/menu")
    
    rut_input = ft.TextField(label="RUT (formato: 12345678-9)", keyboard_type=ft.KeyboardType.NUMBER)
    nombres_input = ft.TextField(label="Nombres (en mayúsculas)")
    apellidos_input = ft.TextField(label="Apellidos (en mayúsculas)")
    email_input = ft.TextField(label="Correo Electrónico")
    rol_dropdown = ft.Dropdown(
        label="Rol",
        options=[
            ft.dropdown.Option("empleado"),
            ft.dropdown.Option("administrador"),
        ],
    )
    password_input = ft.TextField(label="Contraseña", password=True)

    button_row = ft.Row(
        controls=[
            ft.ElevatedButton("Agregar Usuario", on_click=validar_creacion, width=250, height=50),
            ft.ElevatedButton("Cancelar", on_click=cancelar_creacion, width=250, height=50, color="red"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    controls=[
        ft.Text("Crear Usuario", style=ft.TextThemeStyle.HEADLINE_SMALL),
        rut_input,
        nombres_input,
        apellidos_input,
        email_input,
        rol_dropdown,
        password_input,
        button_row,
    ]


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

