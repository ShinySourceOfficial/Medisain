import flet as ft
from db_connection import update_product

def view(page):
    def on_update_product(e):
        product_id = product_id_field.value
        updated_data = {
            "nombre_producto": nombre_field.value,
            "precio": float(precio_field.value),
            "stock": int(stock_field.value),
        }

        # Llamar a la función para actualizar el producto
        update_product(product_id, updated_data)
        page.snack_bar = ft.SnackBar(ft.Text("Producto actualizado con éxito."))
        page.snack_bar.open = True
        page.update()
    
    def cancelar(e):
        page.go("/gestion_productos")

    product_id_field = ft.TextField(label="ID del Producto")
    nombre_field = ft.TextField(label="Nuevo Nombre")
    precio_field = ft.TextField(label="Nuevo Precio")
    stock_field = ft.TextField(label="Nuevo Stock")

    button_row = ft.Row(
        controls=[
            ft.ElevatedButton(text="Actualizar Producto", on_click=on_update_product, width=250, height=50),
            ft.ElevatedButton("Volver", on_click=cancelar, width=250, height=50, color="red"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    return ft.View(
        "/update_product",
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Actualizar Producto", style=ft.TextThemeStyle.HEADLINE_SMALL),
                        ft.Divider(height=20),
                        product_id_field,
                        nombre_field,
                        precio_field,
                        stock_field,
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
