import flet as ft
from db_connection import search_products

def view(page):
    search_results = ft.ListView(expand=True, spacing=10)

    def on_search_query_change(e):
        query = search_field.value.strip()

        # Limpiar los resultados antes de buscar
        search_results.controls.clear()

        # Si el cuadro de búsqueda está vacío, no buscamos nada
        if not query:
            page.update()
            return

        # Realizamos la búsqueda
        results = search_products(query)

        # Usamos un conjunto para evitar duplicados
        seen_products = set()

        # Agregar productos a los resultados, pero solo si no se han agregado previamente
        if results:
            for product in results:
                product_key = f"{product['nombre_producto']}-{product['categoria']}-{product['precio']}"  # Clave única para el producto
                if product_key not in seen_products:
                    seen_products.add(product_key)
                    search_results.controls.append(
                        ft.Text(f"Producto: {product['nombre_producto'].title()} - Categoría: {product['categoria']} - Precio: {product['precio']}")
                    )
        else:
            search_results.controls.append(ft.Text("No se encontraron productos."))
        
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

    def apply_filters(e):
        """Filtra los resultados por rango de precio y disponibilidad."""
        min_price = float(min_price_field.value or 0)
        max_price = float(max_price_field.value or float("inf"))
        available_only = available_switch.value

        # Limpiamos los resultados antes de aplicar los filtros
        search_results.controls.clear()

        filtered_results = [
            product for product in search_products(search_field.value)
            if min_price <= product["precio"] <= max_price and
            (not available_only or int(product["stock"]) > 0)
        ]

        # Usamos un conjunto para evitar duplicados
        seen_products = set()

        for product in filtered_results:
            product_key = f"{product['nombre_producto']}-{product['categoria']}-{product['precio']}"  # Clave única para el producto
            if product_key not in seen_products:
                seen_products.add(product_key)
                search_results.controls.append(
                    ft.ListTile(
                        title=ft.Text(f"{product['nombre_producto']} - {product['categoria']}"),
                        subtitle=ft.Text(f"Precio: ${product['precio']} | Stock: {product['stock']}"),
                        on_click=lambda e, p=product: show_product_details(p),
                    )
                )
        
        if not filtered_results:
            search_results.controls.append(ft.Text("No se encontraron productos que coincidan con los filtros."))
        
        page.update()

    def go_to_menu(e):
        """Redirige al menú principal."""
        page.go("/menu")

    # Campo de búsqueda
    search_field = ft.TextField(
        label="Buscar Producto",
        on_change=on_search_query_change,
        expand=True,
    )

    # Filtros adicionales
    min_price_field = ft.TextField(label="Precio Mínimo", width=150)
    max_price_field = ft.TextField(label="Precio Máximo", width=150)
    available_switch = ft.Switch(label="Mostrar solo disponibles")

    # Botón para aplicar filtros
    filter_button = ft.ElevatedButton("Aplicar Filtros", on_click=apply_filters)

    # Botón para volver al menú
    back_button = ft.ElevatedButton("Volver al Menú", on_click=go_to_menu)

    return ft.View(
        "/search",
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Buscar Productos", style=ft.TextThemeStyle.HEADLINE_SMALL),
                        ft.Row(
                            controls=[search_field, filter_button],
                            spacing=10,
                        ),
                        ft.Row(
                            controls=[min_price_field, max_price_field, available_switch],
                            spacing=10,
                        ),
                        ft.Divider(),
                        search_results,
                        back_button,  # Botón para volver al menú
                    ],
                    spacing=20,
                    expand=True,
                ),
                expand=True,
            )
        ],
    )
