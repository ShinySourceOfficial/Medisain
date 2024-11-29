import flet as ft
from db_connection import get_all_products

def view(page):
    page.title = "Medisain - Visualizador de Productos"
    def load_products():
        products = get_all_products()
        product_list.controls.clear()
        if products:
            for product in products:
                product_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(product["nombre_producto"]),
                        subtitle=ft.Text(f"Stock: {product['stock']} | Precio: ${product['precio']}"),
                    )
                )
                product_list.controls.append(
                    ft.Divider(height=20)
                )
        else:
            product_list.controls.append(ft.Text("No hay productos disponibles."))
        page.update()
    
    def cancelar(e):
        page.go("/gestion_productos")

    product_list = ft.Column()
    load_products()

    button_row = ft.Row(
        controls=[
            ft.ElevatedButton(text="Actualizar Lista", on_click=lambda e: load_products(), width=250, height=50),
            ft.ElevatedButton("Volver", on_click=cancelar, width=250, height=50, color="red"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    return ft.View(
        "/view_products",
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Lista de Productos", style=ft.TextThemeStyle.HEADLINE_SMALL),
                        ft.Divider(height=20),
                        product_list,
                        button_row,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        ],
    )

