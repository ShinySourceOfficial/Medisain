import flet as ft
from db_connection import add_product

def view(page):
    page.title = "Medisain - Añadir Productos"
    def on_add_product(e):
        # Obtener valores de los campos
        nombre = nombre_field.value
        categoria = categoria_field.value
        laboratorio = laboratorio_field.value
        precio = float(precio_field.value)
        stock = int(stock_field.value)
        fecha_vencimiento = fecha_vencimiento_field.value
        numero_lote = numero_lote_field.value
        descuento = float(descuento_field.value)
        sucursal = sucursal_field.value
        ubicacion = ubicacion_field.value

        # Llamar a la función para agregar producto
        add_product(
            nombre, categoria, laboratorio, precio, stock,
            fecha_vencimiento, numero_lote, descuento, sucursal, ubicacion
        )

        # Limpiar campos y mostrar mensaje de éxito
        for field in fields:
            field.value = ""
        page.snack_bar = ft.SnackBar(ft.Text("Producto agregado con éxito."))
        page.snack_bar.open = True
        page.update()

    def cancelar(e):
        page.go("/gestion_productos")

    # Campos de entrada
    fields = [
        (nombre_field := ft.TextField(label="Nombre del Producto")),
        (categoria_field := ft.TextField(label="Categoría")),
        (laboratorio_field := ft.TextField(label="Laboratorio")),
        (precio_field := ft.TextField(label="Precio")),
        (stock_field := ft.TextField(label="Stock")),
        (fecha_vencimiento_field := ft.TextField(label="Fecha de Vencimiento")),
        (numero_lote_field := ft.TextField(label="Número de Lote")),
        (descuento_field := ft.TextField(label="Descuento")),
        (sucursal_field := ft.TextField(label="Sucursal")),
        (ubicacion_field := ft.TextField(label="Ubicación")),
    ]

    button_row = ft.Row(
        controls=[
            ft.ElevatedButton(text="Agregar Producto", on_click=on_add_product, width=250, height=50),
            ft.ElevatedButton("Volver", on_click=cancelar, width=250, height=50, color="red"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    # Usar ListView para hacer desplazable el contenido
    return ft.View(
        "/add_product",
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Agregar Producto", style=ft.TextThemeStyle.HEADLINE_SMALL),
                        ft.Divider(height=20),
                        ft.ListView(
                            controls=[*fields, button_row],
                            expand=True,  # Ocupa todo el espacio disponible
                            spacing=20,   # Espacio entre los elementos
                            padding=ft.padding.all(20),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                ),
                expand=True,
            )
        ],
    )
