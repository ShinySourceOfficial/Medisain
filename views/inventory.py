import flet as ft
from datetime import datetime
from db_connection import search_products_for_inventory, delete_lote, update_lote_availability, update_product, update_lote

def inventory_view(page: ft.Page):
    page.title = "Medisain - Gestor de Inventario"
    search_results = ft.ListView(expand=True, spacing=10)

    def search_and_apply_filters(e):
        query = search_field.value.strip()
        
        # Obtener la categoría seleccionada del dropdown y asegurarse de que sea válida
        selected_category = category_dropdown.value
        if selected_category not in ["Todas", "Medicamentos", "Vitaminas y Suplementos", "Anticonceptivos", "Infantil y Mamá", "Cuidado de la Piel", "Higiene y Cuidado Personal"]:
            selected_category = "Todas"
        
        # Limpiar los resultados antes de buscar
        search_results.controls.clear()

        if not query:
            results = search_products_for_inventory("")  # Obtiene todos los productos (sin filtros de búsqueda)
        else:
            # Si hay algo en el cuadro de búsqueda, realizamos la búsqueda con la query
            results = search_products_for_inventory(query)

        min_price = float(min_price_field.value or 0)
        max_price = float(max_price_field.value or float("inf"))
        available_only = available_switch.value

        # Filtrar los resultados según los filtros establecidos
        # Filtrar los resultados según los filtros establecidos
        filtered_results = [
            product for product in results
            if min_price <= product["producto"]["precio"] <= max_price and
            (not available_only or (lote := product.get("lote")) is not None and int(lote["unidades"]) > 0) and
            (selected_category == "Todas" or product["producto"]["categoria"] == selected_category)
        ]


        seen_products = set()

        # Mostrar los productos con sus lotes
        if filtered_results:
            for item in filtered_results:
                product = item["producto"]
                lote = item["lote"]
                product_key = f"{product['nombre_producto']}-{product['categoria']}-{product['precio']}-{lote['numero_lote']}"
                if product_key not in seen_products:
                    seen_products.add(product_key)

                    precio_original = product['precio']
                    descuento = product['descuento']

                    if descuento == 0.0:
                        precio_final = precio_original
                    else:
                        precio_final = precio_original * (1 - descuento / 100)

                    precio_mostrado = f"${precio_final:.1f}"

                    lote_status = get_lote_status(lote)
                    results_color = ft.colors.BLACK12 if lote_status == "vencido" else (ft.colors.RED if lote_status == "proximo" else ft.colors.BACKGROUND)
                    text_color = ft.colors.RED if lote_status == "vencido" else (ft.colors.WHITE if lote_status == "proximo" else ft.colors.ON_BACKGROUND)
                
                    if lote_status == "vencido":
                        update_lote_availability(lote["id"], "no")
                    
                    # Crear los botones de "Editar" y "Borrar"
                    edit_button = ft.FloatingActionButton(
                        icon=ft.icons.SETTINGS,
                        mini=True,
                        on_click=lambda e, p=product, l=lote: edit_inventory_dialog(p,l)
                    )
                    delete_button = ft.FloatingActionButton(
                        icon=ft.icons.DELETE,
                        bgcolor=ft.colors.RED,
                        mini=True,
                        on_click=lambda e, l=lote: confirm_delete(l['id']),
                    )

                    button_container = ft.Container(
                        content=delete_button,
                        padding=ft.padding.symmetric(vertical=10, horizontal=10),
                    )

                    product_content = ft.ListTile(
                        title=ft.Text(f"{product['nombre_producto'].title()} - {product['categoria']} - Stock: {lote['unidades']}", color=text_color),
                        subtitle=ft.Text(f"Laboratorio: {product['laboratorio']} | Precio: ${precio_mostrado} | Lote: {lote['numero_lote']}", color=text_color),
                        on_click=lambda e, p=product, l=lote: show_product_details(p, l),
                    )

                    if lote_status == "vencido" or lote_status == "proximo":
                        search_results.controls.append(
                            ft.Container(
                                content=ft.Stack(
                                    controls=[
                                        product_content,
                                        ft.Row(
                                                controls=[button_container],
                                                alignment=ft.MainAxisAlignment.END,
                                                spacing=1,
                                        ),
                                    ],
                                    height=65,
                                ),
                                padding=6,
                                border=ft.border.all(1, ft.colors.BLUE_50),
                                border_radius=5,
                                bgcolor=results_color,
                            )
                        )
                    
                    else:
                        search_results.controls.append(
                            ft.Container(
                                content=ft.Stack(
                                    controls=[
                                        product_content,
                                        ft.Row(
                                                controls=[edit_button, button_container],
                                                alignment=ft.MainAxisAlignment.END,
                                                spacing=1,
                                        ),
                                    ],
                                    height=65,
                                ),
                                padding=6,
                                border=ft.border.all(1, ft.colors.BLUE_50),
                                border_radius=5,
                                bgcolor=results_color,
                            )
                        )

        else:
            search_results.controls.append(ft.Text("No se encontraron productos que coincidan con los filtros."))

        page.update()
        show_expiry_warnings(filtered_results)

    def get_lote_status(lote):
        """Determina si un lote está vencido o próximo a vencer."""
        current_date = datetime.now()
        expiry_date = datetime(lote["year_vencimiento"], lote["mes_vencimiento"], 1)
        days_to_expiry = (expiry_date - current_date).days

        if days_to_expiry < 0:
            return "vencido"
        elif days_to_expiry <= 30:
            return "proximo"
        else:
            return "vigente"


    def show_expiry_warnings(filtered_results):
        """Muestra advertencias sobre productos próximos a vencer."""
        warnings = [
            f"{item['producto']['nombre_producto']} - Lote {item['lote']['numero_lote']} vence en {item['lote']['mes_vencimiento']}/{item['lote']['year_vencimiento']}"
            for item in filtered_results
            if get_lote_status(item["lote"]) == "proximo"
        ]
        if warnings:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Productos próximos a vencer:\n" + "\n".join(warnings)),
                open=True,
            )
            page.update()

    def confirm_delete(lote_id):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text("¿Estás seguro de que deseas eliminar este producto?"),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.TextButton("Eliminar", on_click=lambda e: delete_lote_and_refresh(lote_id)),
            ],
        )
        page.dialog.open = True
        page.update()



    def delete_lote_and_refresh(lote_id):
        delete_lote(lote_id) # Llama a la función para eliminar el producto
        page.dialog.open = False
        page.snack_bar = ft.SnackBar(ft.Text("Producto Eliminado con éxito."))
        page.snack_bar.open = True
        page.update()
        search_and_apply_filters(None)  # Actualiza la lista de productos después de borrar



    def edit_inventory_dialog(product,lote):
        error_message = ft.Text("", color="red")
        stock_field = ft.TextField(label="Nuevo Stock", value=lote["unidades"])

        def save_changes(e):       

            try:
                if len(str(stock_field.value)) > 15:
                    error_message.value = "El stock no debe exceder los 15 caracteres."
                    page.dialog.update()
                    return

                stock = int(stock_field.value)
                if stock < 0:
                    error_message.value = "El stock no puede ser negativo."
                    page.dialog.update()
                    return
            except ValueError:
                error_message.value = "Ingrese un número válido en el stock."
                page.dialog.update()
                return
            
            updated_data_lote = {
                "unidades": int(stock_field.value),
            }
            update_lote(lote["id"], updated_data_lote)  # Llama a la función de Firestore
            page.dialog.open = False
            page.snack_bar = ft.SnackBar(ft.Text("Producto actualizado correctamente."))
            page.snack_bar.open = True
            page.update()
            search_and_apply_filters(None)  # Actualiza la lista de productos

        page.dialog = ft.AlertDialog(
            title=ft.Text("Editar Producto"),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        stock_field,
                        error_message
                    ],
                ),
                width=600,  # Ancho deseado del contenido
                height=400,  # Alto deseado del contenido
                padding=10,  # Opcional: agregar un padding
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.TextButton("Guardar", on_click=save_changes),
            ],
        )
        page.dialog.open = True
        page.update()


    def show_product_details(product, lote):
        """Muestra los detalles del producto seleccionado."""
        page.dialog = ft.AlertDialog(
            title=ft.Text(f"Detalles de {product['nombre_producto']}"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Categoría: {product['categoria']}"),
                    ft.Text(f"Laboratorio: {product['laboratorio']}"),
                    ft.Text(f"Precio: ${product['precio']}"),
                    ft.Text(f"Descuento: {product['descuento']}%"),
                    ft.Text(f"Stock: {lote['unidades']}"),
                    ft.Text(f"Fecha de Fabricación: {lote['mes_creacion']}/{lote['year_creacion']}"),
                    ft.Text(f"Fecha de Vencimiento: {lote['mes_vencimiento']}/{lote['year_vencimiento']}"),
                    ft.Text(f"Número de Lote: {lote['numero_lote']}"),
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


    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[back_button, ft.Text("Buscar Inventario", style=ft.TextThemeStyle.HEADLINE_SMALL)],
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
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Divider(),
                    search_results,  # Resultados de la búsqueda
                    ft.Divider(),
                ],
                spacing=10,
                expand=True,
            ),
            expand=True,
        )
    )

