import flet as ft
from db_connection import delete_product

def view(page):
    def on_delete_product(e):
        product_id = product_id_field.value

        # Llamar a la función para eliminar el producto
        delete_product(product_id)
        product_id_field.value = ""
        page.snack_bar = ft.SnackBar(ft.Text("Producto eliminado con éxito."))
        page.snack_bar.open = True
        page.update()

    def cancelar(e):
        page.go("/gestion_productos")

    product_id_field = ft.TextField(label="ID del Producto a Eliminar")

    button_row = ft.Row(
        controls=[
            ft.ElevatedButton(text="Eliminar Producto", on_click=on_delete_product, width=250, height=50),
            ft.ElevatedButton("Volver", on_click=cancelar, width=250, height=50, color="red"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    return ft.View(
        "/delete_product",
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Eliminar Producto", style=ft.TextThemeStyle.HEADLINE_SMALL),
                        ft.Divider(height=20),
                        product_id_field,
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