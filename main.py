import flet as ft
from views import login, menu, create_user, gestion_productos, view_prod, add_prod, update_prod, delete_prod, search
from db_connection import initialize_firebase
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="Detected filter using positional arguments")


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    initialize_firebase()

    def route_change(event):
        route = event.route

        page.views.clear()

        if route == "/login":
            page.views.append(login.view(page))
        elif route == "/menu":
            page.views.append(menu.view(page))
        elif route == "/create_user":
            page.views.append(create_user.view(page))
        elif route == "/gestion_productos":
            page.views.append(gestion_productos.view(page))
        elif route == "/view_products":
            page.views.append(view_prod.view(page))
        elif route == "/add_product":
            page.views.append(add_prod.view(page))
        elif route == "/update_product":
            page.views.append(update_prod.view(page))
        elif route == "/delete_product":
            page.views.append(delete_prod.view(page))
        elif route == "/search":
            page.views.append(search.view(page))
        else:
            page.views.append(login.view(page))
        
        page.update()

    page.on_route_change = route_change

    def view_pop(view):
        page.views.pop()
        page.update()
    
    page.on_view_pop = view_pop

    page.go("/login")

ft.app(target=main)

