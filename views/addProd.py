import flet as ft
from db_connection import add_product

def addProd_view(page: ft.Page):
    page.title = "Medisain - Añadir Productos"

    def error(mensaje):
        snack_bar = ft.SnackBar(ft.Text(mensaje))
        page.snack_bar = snack_bar
        snack_bar.open = True
        page.update()  

    def on_add_product(e):
        # Obtener valores de los campos
        nombre = nombre_field.value

        if not nombre:
            error("El nombre es obligatorio. Ingrese un nombre para el producto.")
            return
        
        categoria = categoria_dropdown.value

        if not categoria:
            error("Selecciona una categoría.")
            return

        laboratorio = laboratorio_field.value

        if not laboratorio:
            error("El laboratorio es obligatorio. Ingrese el laboratorio que fabrico el producto.")
            return
        
        if not precio_field.value or not precio_field.value.isdigit():
            error("Ingrese una cifra correcta en el precio.")
            return

        precio = float(precio_field.value)

        if not stock_field.value or not stock_field.value.isdigit():
            error("Ingrese una cifra correcta en el stock.")
            return

        stock = int(stock_field.value)
        fecha_vencimiento = fecha_vencimiento_field.value

        if not fecha_vencimiento:
            error("La fecha de vencimiento es obligatoria.")
            return

        numero_lote = numero_lote_field.value

        if not numero_lote:
            error("El número de lote es obligatorio.")
            return
        
        if not descuento_field.value or not descuento_field.value.isdigit():
            error("Ingrese una cifra correcta en el descuento.")
            return

        descuento = float(descuento_field.value)
        sucursal = sucursal_field.value

        if not sucursal:
            error("La sucursal es obligatoria.")
            return

        ubicacion = ubicacion_field.value

        if not ubicacion:
            error("La ubicación es obligatoria.")
            return


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

    def go_to_prodManage(e):
        page.go("/prodManage")

    # Campos de entrada
    fields = [
        (nombre_field := ft.TextField(label="Nombre del Producto")),
        (categoria_dropdown := ft.Dropdown(
            label="Categoría",
            options=[
                ft.dropdown.Option("Medicamentos"),
                ft.dropdown.Option("Vitaminas y Suplementos"),
                ft.dropdown.Option("Anticonceptivos"),
                ft.dropdown.Option("Infantil y Mamá"),
                ft.dropdown.Option("Cuidado de la Piel"),
                ft.dropdown.Option("Higiene y Cuidado Personal"),
            ])),
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
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        on_click=go_to_prodManage,
        tooltip="Volver al Menú"
    )


    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[back_button, ft.Text("Agregar Producto", style=ft.TextThemeStyle.HEADLINE_SMALL),],
                        alignment=ft.MainAxisAlignment.START,
                    ),
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
    )
