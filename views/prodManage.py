import flet as ft
from db_connection import search_products_for_prodManage, delete_product, update_product

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
            results = search_products_for_prodManage("")  # Obtiene todos los productos (sin filtros de búsqueda)
        else:
            # Si hay algo en el cuadro de búsqueda, realizamos la búsqueda con la query
            results = search_products_for_prodManage(query)

        min_price = float(min_price_field.value or 0)
        max_price = float(max_price_field.value or float("inf"))

        # Filtrar los resultados según los filtros establecidos, incluyendo la categoría seleccionada
        filtered_results = [
            product for product in results
            if min_price <= product["precio"] <= max_price and
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

                    precio_original = product['precio']
                    descuento = product['descuento']

                    if descuento == 0.0:
                        precio_final = precio_original
                    else:
                        precio_final = precio_original * (1 - descuento / 100)

                    precio_mostrado = f"${precio_final:.1f}"
                              
                    
                    # Crear los botones de "Editar" y "Borrar"
                    edit_button = ft.FloatingActionButton(
                        icon=ft.icons.SETTINGS,
                        mini=True,  # Botón más pequeño
                        on_click=lambda e, p=product: edit_product_dialog(p)
                    )
                    delete_button = ft.FloatingActionButton(
                        icon=ft.icons.DELETE,
                        bgcolor=ft.colors.RED,
                        mini=True,
                        on_click=lambda e, p=product: confirm_delete(p['id']),  # Usamos el ID de Firestore aquí
                    )

                    button_container = ft.Container(
                        content=delete_button,
                        padding=ft.padding.symmetric(vertical=10, horizontal=10),
                    )

                    product_content = ft.ListTile(
                        title=ft.Text(f"{product['nombre_producto'].title()} - {product['categoria'].title()}"),
                        subtitle=ft.Text(f"Laboratorio: {product['laboratorio']} | Precio: ${precio_mostrado}"),
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
                                            spacing=1,
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

        
    def edit_product_dialog(product):
        error_message = ft.Text("", color="red")
        name_field = ft.TextField(label="Nuevo Nombre", value=product["nombre_producto"])
        category_dropdown = ft.Dropdown(
            label="Nueva Categoría",
            options=[
                ft.dropdown.Option("Medicamentos"),
                ft.dropdown.Option("Vitaminas y Suplementos"),
                ft.dropdown.Option("Anticonceptivos"),
                ft.dropdown.Option("Infantil y Mamá"),
                ft.dropdown.Option("Cuidado de la Piel"),
                ft.dropdown.Option("Higiene y Cuidado Personal"),
            ],
            value=product["categoria"],  # Valor inicial
        )
        lab_field = ft.TextField(label="Nuevo Laboratorio", value=product["laboratorio"])
        precio_field = ft.TextField(label="Nuevo Precio", value=(product["precio"]))
        descuento_field = ft.TextField(label="Nuevo Descuento", value=product["descuento"])
        sucursal_field = ft.TextField(label="Nueva Sucursal", value=product["sucursal"])
        ubicacion_field = ft.TextField(label="Nueva Ubicación", value=product["ubicacion"])

        def save_changes(e):

            if not name_field.value:
                error_message.value = "El nombre es obligatorio. Ingrese un nombre para el producto."
                page.dialog.update()
                return
        
            if len(name_field.value) > 20:
                error_message.value = "El número máximo de caracteres es de 20."
                page.dialog.update()
                return
            
            if not category_dropdown.value:
                error_message.value = "Selecciona una categoría."
                page.dialog.update()
                return
            
            if not lab_field.value:
                error_message.value = "El laboratorio es obligatorio. Ingrese el laboratorio que fabrico el producto."
                page.dialog.update()
                return
            
            if len(lab_field.value) > 20:
                error_message.value = "El número máximo de caracteres es de 20."
                page.dialog.update()
                return
            
            try:
                # Convertir el valor a cadena para verificar la longitud
                if len(str(precio_field.value)) > 15:
                    error_message.value = "El precio no debe exceder los 15 caracteres."
                    page.dialog.update()
                    return

                # Convertir el valor a un número para validarlo
                precio = float(precio_field.value)  # Usar float para aceptar valores decimales si es necesario
                if precio < 0:
                    error_message.value = "El precio no puede ser negativo."
                    page.dialog.update()
                    return
            except ValueError:
                # Si no se puede convertir a número, mostrar un error
                error_message.value = "Ingrese un número válido en el precio."
                page.dialog.update()
                return
            
            try:
                if len(str(descuento_field.value)) > 3:
                    error_message.value = "El descuento no debe exceder los 3 caracteres."
                    page.dialog.update()
                    return

                descuento = float(descuento_field.value)  # Usar float para aceptar valores decimales si es necesario
                if descuento < 0:
                    error_message.value = "El descuento no puede ser negativo."
                    page.dialog.update()
                    return
                if descuento > 100:
                    error_message.value = "El descuento no puede ser más del 100%."
                    page.dialog.update()
                    return
            except ValueError:
                error_message.value = "Ingrese un número válido en el descuento."
                page.dialog.update()
                return
            
            if not sucursal_field.value:
                error_message.value = "La sucursal es obligatoria."
                page.dialog.update()
                return
            
            if len(sucursal_field.value) > 20:
                error_message.value = "El número máximo de caracteres es de 20."
                page.dialog.update()
                return
            
            if not ubicacion_field.value:
                error_message.value = "La ubicación es obligatoria."
                page.dialog.update()
                return
            
            if len(ubicacion_field.value) > 20:
                error_message.value = "El número máximo de caracteres es de 20."
                page.dialog.update()
                return

            updated_data = {
                "nombre_producto": name_field.value.strip(),
                "categoria": category_dropdown.value,
                "laboratorio": lab_field.value.strip(),
                "precio": float(precio_field.value),
                "descuento": float(descuento_field.value),
                "sucursal": sucursal_field.value.strip(),
                "ubicacion": ubicacion_field.value.strip(),
            }
            update_product(product["id"], updated_data)  # Llama a la función de Firestore
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
                        name_field, 
                        category_dropdown, 
                        lab_field, 
                        precio_field, 
                        descuento_field, 
                        sucursal_field, 
                        ubicacion_field, 
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


    def show_product_details(product):
        """Muestra los detalles del producto seleccionado."""
        page.dialog = ft.AlertDialog(
            title=ft.Text(f"Detalles de {product['nombre_producto']}"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Categoría: {product['categoria']}"),
                    ft.Text(f"Laboratorio: {product['laboratorio']}"),
                    ft.Text(f"Precio: ${product['precio']}"),
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

