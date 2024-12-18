import flet as ft
from db_connection import search_products, delete_product

def prodManage_view(page: ft.Page):
    page.title = "Medisain - Gestor de Productos"
    search_results = ft.ListView(expand=True, spacing=10)

    def search_and_apply_filters(e):
        query = search_field.value.strip()
        
        # Obtener la categoría seleccionada del dropdown y asegurarse de que sea válida
        selected_category = category_dropdown.value
        if selected_category not in ["Todas", "Medicamentos", "Vitaminas y Suplementos", "Anticonceptivos", "Infantil y Mamá", "Cuidado de la Piel", "Higiene y Cuidado Personal"]:
            selected_category = "Todas"  # Si el valor no es válido, se establece en "Todas"
        
        # Limpiar los resultados antes de buscar
        search_results.controls.clear()

        # Si el cuadro de búsqueda está vacío, mostramos todos los productos
        if not query:
            results = search_products("")  # Obtiene todos los productos (sin filtros de búsqueda)
        else:
            # Si hay algo en el cuadro de búsqueda, realizamos la búsqueda con la query
            results = search_products(query)

        min_price = float(min_price_field.value or 0)
        max_price = float(max_price_field.value or float("inf"))
        available_only = available_switch.value

        # Filtrar los resultados según los filtros establecidos, incluyendo la categoría seleccionada
        filtered_results = [
            product for product in results
            if min_price <= product["precio"] <= max_price and
            (not available_only or int(product["stock"]) > 0) and
            (selected_category == "Todas" or product["categoria"] == selected_category)
        ]

        # Usamos un conjunto para evitar duplicados
        seen_products = set()

        # Mostrar los productos filtrados
        if filtered_results:
            for product in filtered_results:
                product_key = f"{product['nombre_producto']}-{product['categoria']}-{product['precio']}"  # Clave única para el producto
                if product_key not in seen_products:
                    seen_products.add(product_key)
                    
                    # Crear los botones de "Editar" y "Borrar"
                    edit_button = ft.FloatingActionButton(
                        icon=ft.icons.SETTINGS,
                        mini=True,  # Botón más pequeño
                        on_click=lambda e, p=product: print(f"Editar {p['nombre_producto']}")
                    )
                    delete_button = ft.FloatingActionButton(
                        icon=ft.icons.DELETE,
                        bgcolor=ft.colors.RED,
                        mini=True,
                        on_click=lambda e, p=product: confirm_delete(p['id']),  # Usamos el ID de Firestore aquí
                    )

                    button_container = ft.Container(
                        content=delete_button,
                        padding=ft.padding.symmetric(vertical=10),
                    )

                    product_content = ft.ListTile(
                        title=ft.Text(f"{product['nombre_producto'].title()} - {product['categoria'].title()}"),
                        subtitle=ft.Text(f"Precio: ${product['precio']} | Stock: {product['stock']}"),
                        on_click=lambda e, p=product: show_product_details(p),
                    )
                    
                    # Agregar todo a un Stack para superponer
                    search_results.controls.append(
                        ft.Container(
                            content=ft.Stack(
                                controls=[
                                    product_content,  # Producto como fondo
                                    ft.Row(
                                            controls=[edit_button, button_container],
                                            alignment=ft.MainAxisAlignment.END,
                                            spacing=10,
                                    ),
                                ],
                                height=65,  # Altura del Stack
                            ),
                            padding=6,
                            border=ft.border.all(1, ft.colors.BLUE_50),  # Borde opcional
                            border_radius=5,
                        )
                    )

        else:
            search_results.controls.append(ft.Text("No se encontraron productos que coincidan con los filtros."))

        page.update()

    def confirm_delete(product_id):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text("¿Estás seguro de que deseas eliminar este producto?"),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.TextButton("Eliminar", on_click=lambda e: delete_product_and_refresh(product_id)),
            ],
        )
        page.dialog.open = True
        page.update()



    def delete_product_and_refresh(product_id):
        delete_product(product_id) # Llama a la función para eliminar el producto
        page.dialog.open = False
        page.snack_bar = ft.SnackBar(ft.Text("Producto Eliminado con éxito."))
        page.snack_bar.open = True
        page.update()
        search_and_apply_filters(None)  # Actualiza la lista de productos después de borrar


    def show_product_details(product):
        """Muestra los detalles del producto seleccionado."""
        page.dialog = ft.AlertDialog(
            title=ft.Text(f"Detalles de {product['nombre_producto']}"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Categoría: {product['categoria']}"),
                    ft.Text(f"Laboratorio: {product['laboratorio']}"),
                    ft.Text(f"Precio: ${product['precio']}"),
                    ft.Text(f"Stock: {product['stock']}"),
                    ft.Text(f"Fecha de Vencimiento: {product['fecha_vencimiento']}"),
                    ft.Text(f"Número de Lote: {product['numero_lote']}"),
                    ft.Text(f"Descuento: {product['descuento']}%"),
                    ft.Text(f"Sucursal: {product['sucursal']}"),
                    ft.Text(f"Ubicación: {product['ubicacion']}"),
                ]
            ),
            actions=[ft.TextButton("Cerrar", on_click=close_dialog)],
        )
        page.dialog.open = True
        page.update()

    def close_dialog(e=None):
        """Cierra el cuadro de diálogo."""
        page.dialog.open = False
        page.update()

    def go_to_menu(e):
        """Redirige al menú principal."""
        page.go("/menu")

    def go_to_add(e):
        page.go("/addProd")

    # Campo de búsqueda
    search_field = ft.TextField(
        label="Buscar Producto",
        expand=True,
    )

    # Filtros adicionales
    min_price_field = ft.TextField(label="Precio Mínimo", width=150)
    max_price_field = ft.TextField(label="Precio Máximo", width=150)
    available_switch = ft.Switch(label="Mostrar solo disponibles")
    category_dropdown = ft.Dropdown(
        label="Categoría", 
        options=[
            ft.dropdown.Option("Todas"),
            ft.dropdown.Option("Medicamentos"),
            ft.dropdown.Option("Vitaminas y Suplementos"),
            ft.dropdown.Option("Anticonceptivos"),
            ft.dropdown.Option("Infantil y Mamá"),
            ft.dropdown.Option("Cuidado de la Piel"),
            ft.dropdown.Option("Higiene y Cuidado Personal"),
        ],
        width=270  # Puedes ajustar el tamaño si lo deseas
    )

    # Botón para buscar y aplicar filtros
    search_button = ft.IconButton(
        icon=ft.icons.SEARCH,  # Establecer el icono de búsqueda
        on_click=search_and_apply_filters,
        width=50,  # Ajusta el tamaño del botón si es necesario
        height=50,
        icon_size=40,  # Ajusta el tamaño del icono
        tooltip="Buscar"  # Tooltip para mostrar el texto al pasar el mouse por encima
    )


    # Botón de "Volver al Menú" con flecha hacia la izquierda
    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        on_click=go_to_menu,
        tooltip="Volver al Menú"
    )

    # Al iniciar, cargamos todos los productos sin ningún filtro
    search_and_apply_filters(None)

    # Botón de Añadir Producto (+) en la esquina inferior derecha
    add_product_button = ft.IconButton(
        icon=ft.icons.ADD,
        on_click=go_to_add,  # No tiene funcionalidad por ahora
        tooltip="Añadir Producto",
        icon_size=35,  # Ajusta el tamaño del icono
        bgcolor=ft.colors.BLUE_500,  # Color de fondo del botón
        icon_color=ft.colors.WHITE,  # Color del icono
        width=70,  # Tamaño del botón
        height=70  # Botón redondo
    )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[back_button, ft.Text("Buscar Productos", style=ft.TextThemeStyle.HEADLINE_SMALL)],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Row(
                        controls=[search_field, search_button],
                        spacing=1,
                    ),
                    ft.Row(
                        controls=[
                            category_dropdown,
                            min_price_field,
                            max_price_field,
                            available_switch,
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.START,  # Alineación de los filtros a la izquierda
                    ),
                    ft.Divider(),
                    search_results,  # Resultados de la búsqueda
                    ft.Divider(),
                    ft.Container(
                        content=ft.Row(
                            controls=[add_product_button],  # Botón de añadir producto
                            alignment=ft.MainAxisAlignment.END,  # Alineación a la derecha
                        ),
                        padding=ft.padding.only(right=5),  # Espaciado superior para separar del resto
                    ),
                ],
                spacing=10,
                expand=True,
            ),
            expand=True,
        )
    )

