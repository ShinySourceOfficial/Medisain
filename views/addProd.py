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
        nombre = nombre_field.value.strip()

        if not nombre:
            error("El nombre es obligatorio. Ingrese un nombre para el producto.")
            return
        
        if len(nombre) > 20:
            error("El número máximo de caracteres es de 20.")
            return
        
        categoria = categoria_dropdown.value

        if not categoria:
            error("Selecciona una categoría.")
            return

        laboratorio = laboratorio_field.value.strip()

        if not laboratorio:
            error("El laboratorio es obligatorio. Ingrese el laboratorio que fabrico el producto.")
            return
        
        if len(laboratorio) > 20:
            error("El número máximo de caracteres es de 20.")
            return
        
        try:
            if len(str(precio_field.value)) > 15:
                error("El precio no debe exceder los 15 caracteres.")
                return

            precio = float(precio_field.value) 
            if precio < 0:
                error("El precio no puede ser negativo.")
                return
        except ValueError:
            error("Ingrese un número válido en el precio.")
            return

        precio = float(precio_field.value)

        
        try:
            if len(str(descuento_field.value)) > 3:
                error("El descuento no debe exceder los 3 caracteres.")
                return

            descuento = float(descuento_field.value)
            if descuento < 0:
                error("El descuento no puede ser negativo.")
                return
            if descuento > 100:
                error("El descuento no puede ser más del 100%.")
                return
        except ValueError:
            error("Ingrese un número válido en el descuento.")
            return

        descuento = float(descuento_field.value)

        sucursal = sucursal_field.value.strip()

        if not sucursal:
            error("La sucursal es obligatoria.")
            return
        
        if len(sucursal) > 20:
            error("El número máximo de caracteres es de 20.")
            return

        ubicacion = ubicacion_field.value.strip()

        if not ubicacion:
            error("La ubicación es obligatoria.")
            return
        
        if len(ubicacion) > 20:
            error("El número máximo de caracteres es de 20.")
            return


        # Llamar a la función para agregar producto
        add_product(
            nombre, categoria, laboratorio, precio,
            descuento, sucursal, ubicacion
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
        tooltip="Volver al Gestor de Productos"
    )


    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(height=10),
                    ft.Row(
                        controls=[back_button, ft.Text("Agregar Producto", style=ft.TextThemeStyle.HEADLINE_SMALL),],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Divider(height=10),
                    ft.ListView(
                        controls=[*fields,
                                  ft.Container(height=10),
                                  button_row],
                        expand=True,  # Ocupa todo el espacio disponible
                        spacing=20,   # Espacio entre los elementos
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
