import flet as ft
from db_connection import get_all_products, add_lot

def lotRegister_view(page: ft.Page):
    page.title = "Medisain - Registrar Lote"

    product_map = {}  # Para mapear nombre_producto con producto_id

    def error(mensaje):
        snack_bar = ft.SnackBar(ft.Text(mensaje))
        page.snack_bar = snack_bar
        snack_bar.open = True
        page.update()

    def on_register_lot(e):
        # Validar campos obligatorios
        if not selected_product_dropdown.value:
            error("Selecciona un producto.")
            return
        
        if not lot_number_field.value:
            error("El número de lote es obligatorio.")
            return

        if not stock_field.value or not stock_field.value.isdigit():
            error("Ingresa una cantidad válida de unidades.")
            return

        # Obtener producto_id del producto seleccionado
        producto_id = product_map[selected_product_dropdown.value]

        # Datos del lote
        lot_data = {
            "numero_lote": lot_number_field.value,
            "mes_creacion": creation_month_dropdown.value,
            "year_creacion": creation_year_dropdown.value,
            "mes_vencimiento": expiration_month_dropdown.value,
            "year_vencimiento": expiration_year_dropdown.value,
            "unidades": int(stock_field.value),
            "producto_id": producto_id,  # Almacena el producto_id
        }

        # Llamar a la función para agregar el lote
        add_lot(lot_data)

        # Limpiar campos y mostrar mensaje de éxito
        for field in fields:
            field.value = None
        page.snack_bar = ft.SnackBar(ft.Text("Lote registrado con éxito."))
        page.snack_bar.open = True
        page.update()

    def load_products():
        """Carga los productos desde Firebase para el Dropdown."""
        products = get_all_products()
        product_options = [
            ft.dropdown.Option(f"{product['nombre_producto']} - {product['laboratorio']}") for product in products
        ]
        # Mapear nombre_producto con producto_id
        for product in products:
            product_map[product["nombre_producto"]] = product["id"]

        selected_product_dropdown.options = product_options
        page.update()

    def go_to_menu(e):
        page.go("/menu")

    # Campos de entrada
    fields = [
        (selected_product_dropdown := ft.Dropdown(label="Seleccionar Producto")),
        (lot_number_field := ft.TextField(label="Número de Lote")),
        # Variables para los Dropdowns de fecha
        (creation_month_dropdown := ft.Dropdown(
            label="Mes de Creación",
            options=[ft.dropdown.Option(str(month)) for month in range(1, 13)],
        )),
        (creation_year_dropdown := ft.Dropdown(
            label="Año de Creación",
            options=[ft.dropdown.Option(str(year)) for year in range(2024, 2031)],
        )),
        (expiration_month_dropdown := ft.Dropdown(
            label="Mes de Vencimiento",
            options=[ft.dropdown.Option(str(month)) for month in range(1, 13)],
        )),
        (expiration_year_dropdown := ft.Dropdown(
            label="Año de Vencimiento",
            options=[ft.dropdown.Option(str(year)) for year in range(2024, 2031)],
        )),
        (stock_field := ft.TextField(label="Cantidad de Unidades")),
    ]

    # Disposición visual de fechas en filas
    # Ajustar el ancho de los Dropdowns y la disposición de los Rows para ocupar el espacio completo
    date_rows = [
        ft.Row(
            controls=[
                ft.Container(content=creation_month_dropdown, expand=1),
                ft.Container(content=creation_year_dropdown, expand=1),
            ],
            spacing=10,
        ),
        ft.Row(
            controls=[
                ft.Container(content=expiration_month_dropdown, expand=1),
                ft.Container(content=expiration_year_dropdown, expand=1),
            ],
            spacing=10,
        ),
    ]


    button_row = ft.Row(
        controls=[
            ft.ElevatedButton(text="Registrar Lote", on_click=on_register_lot, width=250, height=50),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        on_click=go_to_menu,
        tooltip="Volver al Gestor de Lotes"
    )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(height=10),
                    ft.Row(
                        controls=[back_button, ft.Text("Registrar Lote", style=ft.TextThemeStyle.HEADLINE_SMALL)],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Divider(height=10),
                    ft.ListView(
                        controls=[*fields[:2], *date_rows, fields[-1], ft.Container(height=10), button_row],
                        expand=True,
                        spacing=20,
                        padding=ft.padding.all(50),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            expand=True,
        )
    )

    # Cargar productos al inicio
    load_products()
