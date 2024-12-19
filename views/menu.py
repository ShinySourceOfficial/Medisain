import flet as ft
from db_connection import get_user_role


def menu_view(page: ft.Page):
    #page.window.maximized = True
    page.title = "Medisain - Menú de Opciones"
    user_rut = page.session.get("user_rut")
    user_role = get_user_role(user_rut)

    def go_inventory(e):
        page.go("/inventory")

    def go_prodManage(e):
        page.go("/prodManage")

    def go_lotRegister(e):
        page.go("/lotRegister")

    def go_saleRegister(e):
        page.go("/saleRegister")

    def go_createUser(e):
        page.go("/createUser")

    def logout(e):
        page.session.clear()
        page.go("/login")
        page.snack_bar = ft.SnackBar(ft.Text("Sesión Cerrada Exitosamente."))
        page.snack_bar.open = True
        #page.window.maximized = False


    if user_role == "admin":
        main_container= ft.Container(
                content= ft.Row(
                    controls=[
                        ft.Container(
                            content= ft.Column(
                                controls=[
                                    ft.Container(height=15),
                                    ft.Text("Bienvenido, ¿Qué desea hacer?", style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight="bold"),
                                    ft.Divider(height=20),
                                    ft.Container(height=35),
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton("Gestionar Inventario", on_click=go_inventory, width=300, height=70, style=ft.ButtonStyle(text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD))),
                                            ft.ElevatedButton("Gestionar Productos", on_click=go_prodManage, width=300, height=70, style=ft.ButtonStyle(text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD))),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=35,
                                    ),
                                    ft.Container(height=15),
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton("Registrar Lote", on_click=go_lotRegister, width=300, height=70, style=ft.ButtonStyle(text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD))),
                                            ft.ElevatedButton("Ver Registro de Ventas", on_click=go_saleRegister, width=300, height=70, style=ft.ButtonStyle(text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD))),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=35,
                                    ),
                                    ft.Container(height=15),
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton("Crear Usuario", on_click=go_createUser, width=300, height=70, style=ft.ButtonStyle(text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD))),
                                            ft.ElevatedButton("Cerrar Sesión", on_click=logout, width=300, height=70, color="red", style=ft.ButtonStyle(text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)))
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=35,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10,
                            ),
                            padding=1,
                            width=800,
                            height=650,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width= 900,
                height=700,
                border_radius=20,
                bgcolor= ft.colors.WHITE10 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLACK12,
            )
        
    
    elif user_role == "empleado":
        main_container= ft.Container(
                content= ft.Row(
                    controls=[
                        ft.Container(
                            content= ft.Column(
                                controls=[
                                    ft.Container(height=15),
                                    ft.Text("Bienvenido, ¿Qué desea hacer?", style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight="bold"),
                                    ft.Divider(height=20),
                                    ft.Container(height=35),
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton("Gestionar Inventario", on_click=go_inventory, width=300, height=70, style=ft.ButtonStyle(text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD))),
                                            ft.ElevatedButton("Registrar Lote", on_click=go_lotRegister, width=300, height=70, style=ft.ButtonStyle(text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD))),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=35,
                                    ),
                                    ft.Container(height=15),
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton("Ver Registro de Ventas", on_click=go_saleRegister, width=300, height=70, style=ft.ButtonStyle(text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD))),
                                            ft.ElevatedButton("Cerrar Sesión", on_click=logout, width=300, height=70, color="red", style=ft.ButtonStyle(text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)))
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=35,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10,
                            ),
                            padding=1,
                            width=800,
                            height=650,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width= 900,
                height=700,
                border_radius=20,
                bgcolor= ft.colors.WHITE10 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLACK12,
            )
    

    else:
        main_container= ft.Container(
                content= ft.Row(
                    controls=[
                        ft.Container(
                            content= ft.Column(
                                controls=[
                                    ft.Container(height=15),
                                    ft.Text("Bienvenido, ¿Qué desea hacer?", style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight="bold"),
                                    ft.Divider(height=20),
                                    ft.Container(height=35),
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton("Cerrar Sesión", on_click=logout, width=300, height=70, color="red", style=ft.ButtonStyle(text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)))
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=35,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10,
                            ),
                            padding=1,
                            width=800,
                            height=650,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width= 900,
                height=700,
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