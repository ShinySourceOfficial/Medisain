import flet as ft

def view(page):
    page.title = "Medisain - Gestor de Productos"

    def go_to_view(e):
        page.go("/view_products")

    def go_to_add(e):
        page.go("/add_product")

    def go_to_update(e):
        page.go("/update_product")
    
    def go_to_delete(e):
        page.go("/delete_product")

    def exit(e):
        page.go("/menu")

    controls = [
        ft.Text("Gestor de Productos", style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight="bold"),
        ft.Divider(height=20),
        ft.ElevatedButton("Ver Productos", on_click=go_to_view, width=250, height=50),
        ft.ElevatedButton("Añadir Productos", on_click=go_to_add, width=250, height=50),
        ft.ElevatedButton("Actualizar Productos", on_click=go_to_update, width=250, height=50),
        ft.ElevatedButton("Borrar Productos", on_click=go_to_delete, width=250, height=50),
        ft.ElevatedButton("Salir al Menú", on_click=exit, width=250, height=50, color="red"),
    ]

    return ft.View(
        "/gestion_productos",
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